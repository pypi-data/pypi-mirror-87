from ..connection.connect import *
from datetime import datetime
from pymodm import fields, MongoModel


class Position(MongoModel):
    """仓位基础"""
    # 交易所
    exchange_name = fields.CharField(min_length=3)
    # 币对
    coin_pair = fields.CharField(min_length=3)
    # 当前基础币总花费
    cost = fields.FloatField()
    # 持有目标币数量
    hold = fields.FloatField()

    class Meta:
        connection_alias = DB_POSITION

    @classmethod
    def position_with(cls, exchange_name, coin_pair_str):
        """获取仓位信息、无则创建

        Parameters
        ----------
        exchange_name : str
        coin_pair_str : str
        """
        try:
            return cls.objects.raw({'exchange_name': exchange_name, 'coin_pair': coin_pair_str}).first()
        except Exception:
            return cls(exchange_name=exchange_name, coin_pair=coin_pair_str, cost=0, hold=0)

    def update(self, increase_cost, increase_hold):
        """更新仓位

        Parameters
        ----------
        increase_cost : float
            0.00000123
        increase_hold : float
            0.00000123
        """
        self.cost += increase_cost
        self.hold += increase_hold
        self.save()

    def reset(self):
        """重置仓位(全部卖出了)"""
        self.cost = 0
        self.hold = 0
        self.save()


class AIMSPosition(Position):
    """ AIMS 策略仓位 """
    # 仓位更新日期
    update_date = fields.DateTimeField()

    def update(self, increase_cost, increase_hold):
        self.update_date = datetime.now()
        super().update(increase_cost, increase_hold)

    class Meta:
        connection_alias = DB_POSITION
        collection_name = CN_AIMS_POS


class AIMSPositionSelling(AIMSPosition):
    """ AIMS 卖出记录 """
    # 卖出价格
    close_price = fields.FloatField()
    # 盈利
    profit_amount = fields.FloatField()
    # 日期
    date = fields.DateTimeField()

    class Meta:
        connection_alias = DB_POSITION
        collection_name = CN_AIMS_POS_CLOSE

    @classmethod
    def with_aims_position(cls, position: AIMSPosition):
        pos = AIMSPositionSelling()
        pos.hold = position.hold
        pos.cost = position.cost
        pos.exchange_name = position.exchange_name
        pos.coin_pair = position.coin_pair
        return pos


class AIPRecord(MongoModel):
    """ 定投记录 """
    exchange = fields.CharField()
    coin_pair = fields.CharField()
    date = fields.DateTimeField()
    cost = fields.FloatField()
    amount = fields.FloatField()

    class Meta:
        connection_alias = DB_POSITION
        connection_name = CN_AIP_RECORDS
