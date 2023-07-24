# coding=utf-8

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import create_engine, Column
from sqlalchemy import Integer, String, Float, Boolean, DECIMAL, Enum, Date, DateTime, Time, Text
from datetime import datetime,date

from sqlalchemy.orm import registry

mapper_registry = registry()

@mapper_registry.mapped
class BarData:
    __tablename__ = 'llbardata'

    id = Column(Integer,primary_key=True)
    symbol = Column(String(50))
    interval = Column(String(50))
    datetime: Mapped[datetime]
    open = Column(DECIMAL(10,3))
    close = Column(DECIMAL(10,3))
    high = Column(DECIMAL(10,3))
    low = Column(DECIMAL(10,3))
    vol = Column(DECIMAL(10,3))
    turnover = Column(DECIMAL(10,3))
    asset = Column(String(50))
    adjust = Column(String(50))

    # 结果集返回为 字典类型
    def to_dict(self):
        dict_ = self.__dict__
        if "_sa_instance_state" in dict_:
            del dict_["_sa_instance_state"]
        return dict_

@mapper_registry.mapped
class BarDataOverview:
    __tablename__ = 'llbaroverview'

    id = Column(Integer,primary_key=True)
    symbol = Column(String(50))
    exchange = Column(String(50))
    interval = Column(String(50))
    count = Column(Integer)
    start = Column(DateTime)
    end = Column(DateTime)
    adjust = Column(String(50))
    asset = Column(String(50))

    # 结果集返回为 字典类型
    def to_dict(self):
        dict_ = self.__dict__
        if "_sa_instance_state" in dict_:
            del dict_["_sa_instance_state"]
        return dict_
    
@mapper_registry.mapped
class TradeData:
    __tablename__ = 'lltrade'

    id = Column(Integer,primary_key=True)
    date = Column(Date)
    symbol = Column(String(50))
    name = Column(String(50))
    asset = Column(String(50)) #E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 ETF ，默认E 
    bs = Column(String(50))
    num = Column(Integer)
    price = Column(DECIMAL(10,3))
    fee = Column(DECIMAL(10,3))
    otherfee = Column(DECIMAL(10,3))

    # 结果集返回为 字典类型
    def to_dict(self):
        dict_ = self.__dict__
        if "_sa_instance_state" in dict_:
            del dict_["_sa_instance_state"]
        return dict_

#@mapper_registry.mapped
class AccountData:
    pass