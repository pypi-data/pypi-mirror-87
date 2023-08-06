from pymodm import MongoModel, fields
from bson.codec_options import CodecOptions
from ..connection.connect import DB_MARKET


class CandleRecord(MongoModel):
    """OHLCV"""

    candle_begin_time = fields.DateTimeField(primary_key=True)
    open_price = fields.Decimal128Field(mongo_name='open')
    high_price = fields.Decimal128Field(mongo_name='high')
    low_price = fields.Decimal128Field(mongo_name='low')
    close_price = fields.Decimal128Field(mongo_name='close')
    volume = fields.Decimal128Field()

    class Meta:
        connection_alias = DB_MARKET
        codec_options = CodecOptions(tz_aware=True)

    @classmethod
    def bulk_upsert_records(cls, json_list, key_name='_id'):
        """Bulk upsert candle records"""
        coll = cls._mongometa.collection
        bulkOp = coll.initialize_unordered_bulk_op()
        for doc in json_list:
            if isinstance(key_name, list):
                filter_dict = dict(map(lambda k: (k, doc[k]), key_name))
            else:
                filter_dict = {key_name: doc[key_name]}
            doc['_cls'] = cls.__module__ + '.' + cls.__name__
            bulkOp.find(filter_dict).upsert().update({'$set': doc})
        results = bulkOp.execute()
        return results


def candle_record_class_with_components(exchange_name, coin_pair, time_frame) -> CandleRecord:
    """Convenience"""
    return candle_record_class('{}_{}_{}'.format(exchange_name.lower(), coin_pair.formatted('_').lower(), time_frame.value.lower()))


def candle_record_class(collection_name) -> CandleRecord:
    """Define a record class with a specify collection name"""
    assert collection_name is not None and isinstance(collection_name, str)
    class_name = collection_name + "_candle"
    _cls = type(class_name, CandleRecord.__bases__, dict(CandleRecord.__dict__))
    _cls._mongometa.collection_name = collection_name
    return _cls
