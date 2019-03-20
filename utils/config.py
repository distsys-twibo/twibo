import json
import logging


conf = {}

logger = logging.getLogger(__name__)


def init():
    global conf
    with open('twibo.json') as f:
        conf = json.load(f)
    logger.debug('loaded config: {}'.format(str(conf)))
