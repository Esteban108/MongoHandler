import logging
from time import time, sleep
from config import mongo_credentials
from mongo_handler import MongoHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(MongoHandler(**mongo_credentials))

logger.info('Starting', extra={"first_level": {"mongo_db_name": "LOGSSSS"}})

for e in range(0, 10):
    try:
        g = (10 / 0)
    except:
        start_time = time()
        print("start send error")
        logger.exception("no se puede dividir")
        print(f"error save in {(time() - start_time)} sec")
        continue
    sleep(1)
