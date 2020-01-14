import traceback
from datetime import datetime
from logging import StreamHandler

import pymongo
from pymongo import MongoClient, IndexModel


class MongoHandler(StreamHandler):
    already_checked = []

    def __init__(self, mg_db_host: str, mg_db_port: int, mg_db_usr: str, mg_db_pass: str,
                 mg_db_auth: str):
        super().__init__()
        self.client = MongoClient(mg_db_host,
                                  username=mg_db_usr,
                                  password=mg_db_pass,
                                  authSource=mg_db_auth,
                                  port=mg_db_port
                                  )

    def __create_index(self, mongo_db_name, col_name):
        self.client[mongo_db_name][col_name].create_indexes([
            IndexModel([("insertion_timestamp", pymongo.ASCENDING)]),
            IndexModel([("level", pymongo.ASCENDING)]),
            IndexModel([("caller", pymongo.ASCENDING)]),
            IndexModel([("pid", pymongo.ASCENDING)])
        ])

    def get_exc_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {'exc_info': exc_info}

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    def parse_record(self, record):
        json_log_object = {"insertion_timestamp": datetime.utcnow(),
                           "level": record.levelname,
                           'pid': record.process,
                           "message": record.getMessage(),
                           "caller": record.filename + '::' + record.funcName,
                           "module": record.module,
                           'data': {'logger_name': record.name,
                                    'funcName': record.funcName,
                                    'filename': record.filename,
                                    'lineno': record.lineno,
                                    'thread': f'{record.threadName}[{record.thread}]'
                                    }}

        if hasattr(record, 'extra_data'):
            json_log_object['data'].update(record.extra_data)

        if hasattr(record, 'first_level'):
            json_log_object.update(record.first_level)

        if record.exc_info or record.exc_text:
            json_log_object['data'].update(self.get_exc_fields(record))

        return json_log_object

    def emit(self, record):
        record = self.parse_record(record)

        mongo_db_name = record.get("mongo_db_name", "logs_db")
        col_db_name = record.get("mongo_col_name", record["module"])

        if f"{mongo_db_name}_{col_db_name}" not in self.already_checked:
            if mongo_db_name not in self.client.list_databases() or \
                    col_db_name not in self.client[mongo_db_name].collection_names():
                self.__create_index(mongo_db_name, col_db_name)
                self.already_checked.append(f"{mongo_db_name}_{col_db_name}")

        col = self.client[mongo_db_name][col_db_name]
        col.insert_one(record)
