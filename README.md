# MongoHandler

save your logs in mongo with MongoHandler.

###Easy config
```python

import logging
from mongo_handler import MongoHandler
mongo_credentials = {
    "mg_db_host": "172.17.0.2",
    "mg_db_port": 27017,
    "mg_db_usr": "admin",
    "mg_db_pass": "admin",
    "mg_db_auth": "admin"
}


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(MongoHandler(**mongo_credentials))

# mongo_db_name : logs save in this database  -- default logs_db
# mongo_col_name : logs save in this collection -- default module name
logger.info('Starting', extra={"first_level": {"mongo_db_name": "db_name", "mongo_col_name": "col_name"}})

# add extra info
logger.info('Starting', extra={"first_level": {"key":"value"}, "extra_data": {"more_data": "data"}})
```
###Example json save
```json
{
    "_id" : ObjectId("5e1dc78bf0812006525753b9"),
    "insertion_timestamp" : ISODate("2020-01-14T13:52:11.322Z"),
    "level" : "INFO",
    "pid" : 17936,
    "message" : "Starting",
    "caller" : "test_log.py::<module>",
    "module" : "test_log",
    "key": "value",
    "data" : {
        "logger_name" : "__main__",
        "funcName" : "<module>",
        "filename" : "test_log.py",
        "lineno" : 20,
        "thread" : "MainThread[140705424271168]",
        "more_data": "data"
    }
}
```