import logging


logger = logging.getLogger(__name__)
background_tasks = []

async def add_tasks(app):
    for n, c in background_tasks:
        logger.info('launching background task {}'.format(n))
        app[n] = app.loop.create_task(c())
