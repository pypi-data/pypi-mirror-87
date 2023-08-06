Summary
-------

Run, monitor and log celery tasks.


Installation and setup
----------------------

Declare tasks using celery task or cubicweb-celery cwtasks.

On worker side, install cw-celerytask-helpers_.

celeryconfig.py example::

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = BROKER_URL
    CUBICWEB_CELERYTASK_REDIS_URL = CELERY_BROKER_URL
    CELERY_IMPORTS = ('cw_celerytask_helpers.helpers', 'module.containing.tasks')


In this configuration example, the ``cw_celerytask_helpers`` in
``CELERY_IMPORTS`` is required to have logging data (in the task) sent
back to the Cubicweb instance via Redis. The
``CUBICWEB_CELERYTASK_REDIS_URL`` is the Redis endpoint used for this
logging handling mechanism.

    
Start a worker::

    # running cubicweb tasks (celeryconfig.py will be imported from your instance config directory)
    celery -A cubicweb_celery -i <CW_INSTANCE_NAME> worker -l info

    # running pure celery tasks
    celery worker -l info


Task state synchronization requires to run the `celery-monitor` command::

    cubicweb-ctl celery-monitor <instance-name>


Ensure to have the celeryconfig.py loaded for both cubicweb instance and
celery worker, enforce by settings with CELERY_CONFIG_MODULE environment
variable (it must be an importable python module).

.. _cw-celerytask-helpers: https://www.cubicweb.org/project/cw-celerytask-helpers

Running tasks
-------------

Create a task:

.. code-block:: python

    from celery import current_app as app
    from celery.utils.log import get_task_logger

    logger = get_task_logger(__name__)

    @app.task(name='hi_there')
    def my_task(arg, kw=0):
        logger.info('HI %s %s!', arg, kw)
        return 42


Run a task:

.. code-block:: python

    from cubicweb_celerytask.entities import start_async_task

    cwtask = start_async_task(cnx, 'hi_there', 'THERE', kw=42)
    cnx.commit()


start_async_task() accept task names, task objects or task signatures:
http://docs.celeryproject.org/en/latest/userguide/canvas.html#signatures

For instance, to start the above task in a dedicated queue named `myqueue`:

.. code-block:: python

    import celery

    start_async_task(cnx, celery.signature('hi_there', args=('THERE',),
                                           kwargs={'kw': 42}, queue='myqueue'))


Testing task based application
------------------------------

In CubicWeb test mode, tasks don't run automatically, use
`cubicweb_celerytask.entities.get_tasks()` to introspect them and
`cubicweb_celerytask.entities.run_all_tasks()` to run them.

Also, CELERY_ALWAYS_EAGER and CELERY_EAGER_PROPAGATES_EXCEPTIONS are set to
True by default.
