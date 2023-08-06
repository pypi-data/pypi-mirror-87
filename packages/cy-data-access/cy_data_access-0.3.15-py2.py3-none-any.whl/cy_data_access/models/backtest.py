from pymodm import MongoModel, fields
from bson.codec_options import CodecOptions
from ..connection.connect import DB_BACKTEST


class BacktestSummary(MongoModel):

    parameter = fields.CharField()
    equity_curve = fields.Decimal128Field()
    start_date = fields.DateTimeField()
    end_date = fields.DateTimeField()

    class Meta:
        connection_alias = DB_BACKTEST
        codec_options = CodecOptions(tz_aware=True)


def backtest_summary_class(collection_name) -> BacktestSummary:
    """Define a record class with a specify collection name"""
    assert collection_name is not None and isinstance(collection_name, str)
    class_name = collection_name + "_bt_summary"
    _cls = type(class_name, BacktestSummary.__bases__, dict(BacktestSummary.__dict__))
    _cls._mongometa.collection_name = collection_name
    return _cls
