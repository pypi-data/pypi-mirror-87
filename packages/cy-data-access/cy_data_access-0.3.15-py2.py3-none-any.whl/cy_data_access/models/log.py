from ..connection.connect import *
from pymodm import fields, MongoModel
from enum import IntEnum


class LogType(IntEnum):
    AIM = 0
    AIP = 1


class LogInfo(MongoModel):
    """日志记录"""
    log = fields.CharField()
    create = fields.DateTimeField()
    fetched = fields.BooleanField(default=False)
    log_type = fields.IntegerField(mongo_name='type')

    class Meta:
        connection_alias = DB_LOG
        collection_name = CN_COMMON_LOG

    @classmethod
    def grouped_unfetched_logs(cls):
        try:
            all_unfetcheds = list(cls.objects.raw({'fetched': False}).order_by([('create', 1)]))
            if not all_unfetcheds:
                return []
            else:
                grouped = dict()
                for log in all_unfetcheds:
                    l_type = log.log_type
                    grouped[l_type] = grouped[l_type] + [log] if grouped.get(l_type) else [log]
                return list(grouped.values())
        except Exception as e:
            print("Get logs failed, " + str(e))
            return []
