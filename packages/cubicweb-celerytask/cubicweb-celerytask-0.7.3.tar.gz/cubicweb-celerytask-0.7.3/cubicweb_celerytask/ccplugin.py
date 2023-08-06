# -*- coding: utf-8 -*-
# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import datetime
import json
import logging
import os
import time

import celery
import redis.exceptions

from cubicweb.toolsutils import Command
from cubicweb.server.serverconfig import ServerConfiguration
from cubicweb.cwctl import CWCTL
from cubicweb_celerytask.entities import sync_task_state

from cw_celerytask_helpers.monitor import MONITOR_KEY
from cw_celerytask_helpers.utils import get_redis_client

logger = logging.getLogger(__name__)

REQUEUE_TIMEOUT = 600


class CeleryMonitorCommand(Command):
    """Synchronize celery task statuses"""

    name = 'celery-monitor'
    arguments = '<instance>'
    min_args = max_args = 1
    options = (
        ('loglevel',
         {'short': 'l', 'type': 'choice', 'metavar': '<log level>',
          'default': 'info', 'choices': ('debug', 'info', 'warning', 'error')},
         ),
    )

    def run(self, args):
        from cubicweb import repoapi
        from cubicweb.cwctl import init_cmdline_log_threshold
        config = ServerConfiguration.config_for(args[0])
        config.global_set_option('log-file', None)
        config.log_format = '%(levelname)s %(name)s: %(message)s'
        init_cmdline_log_threshold(config, self['loglevel'])
        # use only one database connection by default (require cubicweb>=3.24)
        os.environ.setdefault('CW_CONNECTIONS_POOL_SIZE', '1')
        repo = repoapi.get_repository(config=config)
        repo.hm.call_hooks('server_maintenance', repo=repo)
        source = repo.system_source
        while True:
            try:
                with repo.internal_cnx() as cnx:
                    while True:
                        try:
                            self.loop(cnx)
                        except redis.exceptions.ConnectionError:
                            logger.error('redis ConnectionError, retry in 5s')
                            time.sleep(5)
            except (source.OperationalError, source.InterfaceError):
                while True:
                    source.exception('connection lost, retry in 5s')
                    time.sleep(5)
                    try:
                        for cnxset in repo.cnxsets:
                            cnxset.reconnect()
                    except (source.OperationalError, source.InterfaceError):
                        continue
                    else:
                        break

    @staticmethod
    def requeue(cnx, client):
        """Requeue pending tasks in case we have missed some events.

        For instance, in case of "worker lost", we don't have task events.
        Only requeue tasks within the "visibility_timeout" (default 1h), since
        tasks status is lost after this period.
        """
        try:
            timeout = celery.current_app.conf[
                'BROKER_TRANSPORT_OPTIONS']['visibility_timeout']
        except KeyError:
            timeout = 3600
        date = datetime.datetime.utcnow() - datetime.timedelta(seconds=timeout)
        for task_id, in cnx.execute(
            'Any T ORDERBY C WHERE X is CeleryTask, X task_id T, '
            'X in_state ST, ST name IN ("waiting", "queued", "running"), '
            'X creation_date C, X creation_date > %(d)s', {'d': date},
            build_descr=False
        ):
            client.lpush(
                MONITOR_KEY,
                json.dumps({'task_id': task_id, 'task_name': None}))

    @staticmethod
    def loop(cnx, timeout=None):
        client = get_redis_client()
        client.ping()
        logger.info('Connected to redis')
        test = (cnx.repo.config.mode == "test")
        requeue_timer = timer = time.time()
        while True:
            # pop item from MONITOR_KEY
            data = client.brpop(MONITOR_KEY, timeout=1)
            if data is None:
                now = time.time()
                if timeout is not None and abs(timer - now) > timeout:
                    break
                if abs(requeue_timer - time.time()) > REQUEUE_TIMEOUT:
                    # no items left in MONITOR_KEY and we reached the
                    # REQUEUE_TIMEOUT, requeue tasks in MONITOR_KEY
                    CeleryMonitorCommand.requeue(cnx, client)
                    requeue_timer = time.time()
                continue
            payload = json.loads(data[1].decode())
            task_id, task_name = payload['task_id'], payload['task_name']
            try:
                sync_task_state(cnx, task_id, task_name)
            except Exception:
                logger.exception('Unhandled exception while syncing '
                                 'task <Task %s (%s)>', task_id,
                                 task_name)
                cnx.rollback()
                if test:
                    # we should not hide exceptions in tests
                    raise


CWCTL.register(CeleryMonitorCommand)
