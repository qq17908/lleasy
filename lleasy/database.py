# coding=utf-8
import os
from lleasy.config import Config
from sqlalchemy import create_engine,select,insert
from sqlalchemy.orm import Session
from lleasy.object import TradeData,BarData,BarDataOverview
import pandas as pd

ROOT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__),os.pardir))
CONFIG_FILE_PATH = os.path.join(ROOT_PATH,'config.cfg')

# 数据源管理
class SqliteDatabase():
    def __init__(self) -> None:
        config = Config()
        config_dict = config.get_config('datasource_file')
        local_db_type = config_dict['local_db_type']
        local_db_path = config_dict['local_db_path']

        local_db_path = ROOT_PATH + local_db_path

        self.engine = create_engine("sqlite:///" + local_db_path, echo=True, echo_pool="debug", hide_parameters=True)
        self.session = Session(self.engine)
    
    def getDBSession(self) -> Session:
        return self.session

    def load_bar_data(self) -> list:
        result = self.session.query(BarData).all()
        return result

    # 查询单个标的行情数据
    def get_symbol_bars_bySEDate(self, symbol, start_date, end_date) -> pd.DataFrame:
        bars = self.session.query(BarData)\
                .where(BarData.symbol==symbol)\
                .where(BarData.datetime >= start_date)\
                .where(BarData.datetime <= end_date)\
                .all()

        symbol_bars = [bar.to_dict() for bar in bars]

        symbol_bars=pd.DataFrame(
                                symbol_bars,
                                columns=['datetime','symbol','open','close','high','low']
                                )
        return symbol_bars

    # 同时查询多个标的行情数据
    def get_symbols_bars(self, symbols:list, start_date, end_date) -> pd.DataFrame:
        stmt = select(BarData)\
            .where(BarData.symbol.in_(symbols))\
            .where(BarData.datetime >= start_date)\
            .where(BarData.datetime <= end_date)
        
        bars = self.session.scalars(stmt).all()

        symbol_bars = [bar.to_dict() for bar in bars]

        symbol_bars=pd.DataFrame(
                                symbol_bars,
                                columns=['datetime','symbol','open','close','high','low']
                                )

        return symbol_bars

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

    #更新llbaroverview表示数据
    def update_bar_overview(self) -> None:
        # 删除baroverview表数据
        llbar = self.session.query(BarData)
        # 查询llbardata数据，将查询结果插入baroverview表

        pass

    #返回llbaroverview所有数据
    def get_bar_overview(self)  -> list:
        llbaroverview = self.session.query(BarDataOverview).all()
        llbaroverview_dict = [baroverview.to_dict() for baroverview in llbaroverview]
        return llbaroverview_dict