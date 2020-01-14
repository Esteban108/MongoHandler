import logging
import sys

from .mongo_handler import MongoHandler
from config.settings import mongo_logs_db, LOG_LEVEL
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(MongoHandler(**mongo_logs_db))
if LOG_LEVEL == logging.DEBUG:
    logger.addHandler(logging.StreamHandler(sys.stderr))
    logger.debug(f' Start log in debug mode')
