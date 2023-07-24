# coding=utf-8

from sqlalchemy import create_engine,select,insert
from sqlalchemy.orm import Session
from lleasy.object import TradeData,BarData

# 数据源管理
class SqliteDatabase():
    def __init__(self,path) -> None:
        self.engine = create_engine("sqlite:///" + path, echo=True)
        self.session = Session(self.engine)
    
    def getDBSession(self) -> Session:
        return self.session

    def load_bar_data(self) -> list:
        result = self.session.query(BarData).all()
        return result

    def save_bar_data(self, bars) -> bool:
        try:
            self.session.execute(
                insert(BarData),
                bars
            )
            self.session.commit()
            return True
        except:
            self.session.rollback()
            raise

    def load_trade_data(self) -> list:
        #查询交易记录
        result = self.session.query(TradeData)
        return result.all()

    def save_trade_data(self,trades) -> bool:
        try:
            self.session.add_all(trades)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            raise

    def init_bar_overview(self) -> None:
        pass

    def get_bar_overview()  -> list:
        pass