# coding=utf-8

import numpy as np
import pandas as pd
import akshare as ak
from sqlalchemy import create_engine

# 从AKshare中获取数据
class AKShare_Data:
    # 指数行情数据
    def download_zh_gz_bardata(
            symbols,
            interval,
            start_d,
            end_d
    ) -> pd.DataFrame:
        
        result_df = pd.DataFrame()

        for vSymbol in symbols:
            try:
                tmp_df = ak.stock_zh_index_daily_em(
                    symbol=vSymbol,
                    start_date=start_d, 
                    end_date=end_d)

                if not tmp_df.columns.empty:
                    tmp_df['symbol'] = vSymbol
                    tmp_df['interval'] = interval
                    tmp_df['asset'] = 'I'  #E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 ETF ，默认E
                    tmp_df['adjust'] = ''

            except KeyError:
                tmp_df =pd.DataFrame(
                    columns=['symbol','interval','datetime','open','close','high','low','vol','turnover','asset','adjust'])
            
            result_df = pd.concat([result_df,tmp_df],ignore_index=True)

        if result_df.columns.empty:
            return pd.DataFrame(
                columns=['symbol','interval','datetime','open','close','high','low','vol','turnover','asset','adjust']
            )
        
        result_df = result_df.rename(
            columns={
                "date":"datetime",
                "open":"open",
                "close":"close",
                "high":"high",
                "low":"low",
                "volume":"vol",
                "amount":"turnover"}
        )
        
        result_df['datetime'] = pd.to_datetime(result_df['datetime'])
        result_df['vol'] = pd.to_numeric(result_df['vol'])
        result_df['turnover'] = pd.to_numeric(result_df['turnover'])
        result_df = result_df[['symbol','interval','datetime','open','close','high','low','vol','turnover','asset','adjust']]
        #result_df = result_df.set_index(['symbol','datetime'])
        
        return result_df

    # 股票行情数据
    def download_zh_a_bardata(
            symbols,
            interval,
            start_d,
            end_d
    ) -> pd.DataFrame:
        
        result_df = pd.DataFrame()
        if len(symbols) == 0:
            tmp_df = pd.DataFrame(
                    [],
                    columns=['symbol','interval','datetime','open','close','high','low','vol','turnover','asset','adjust']
                )
            tmp_df.set_index(['symbol','datetime'])
            return tmp_df
        
        for vSymbol in symbols:
            try:
                tmp_df = ak.stock_zh_a_hist(
                    symbol=vSymbol, 
                    period=interval, 
                    start_date=start_d, 
                    end_date=end_d, 
                    adjust="")
                
                if not tmp_df.columns.empty:
                    tmp_df['symbol'] = vSymbol
                    tmp_df['interval'] = interval
                    tmp_df['asset'] = 'E' #E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 ETF ，默认E 
                    tmp_df['adjust'] = ''
                
            except KeyError:
                tmp_df = pd.DataFrame(
                    columns=['symbol','interval','datetime','open','close','high','low','vol','turnover','asset','adjust']
                )
            result_df = pd.concat([result_df,tmp_df],ignore_index=True)

        result_df = result_df.rename(columns={"日期":"datetime",
                                "开盘":"open",
                                "收盘":"close",
                                "最高":"high",
                                "最低":"low",
                                "成交量":"vol",
                                "成交额":"turnover"})
        
        result_df['datetime'] = pd.to_datetime(result_df['datetime'])
        result_df['vol'] = pd.to_numeric(result_df['vol'])
        result_df['turnover'] = pd.to_numeric(result_df['turnover'])

        result_df = result_df[['symbol','interval','datetime','open','close','high','low','vol','turnover','asset','adjust']]
        #result_df = result_df.set_index(['symbol','datetime'])

        return result_df

    ## 基金ETF行情数据
    def download_zh_funt_bardata(
            symbols,
            interval,
            start_d,
            end_d) -> pd.DataFrame:
        
        result_df = pd.DataFrame()

        if len(symbols) == 0:
            tmp_df = pd.DataFrame(
                    [],
                    columns=['symbol','interval','datetime','open','close','high','low','vol','turnover','asset','adjust']
                )
            tmp_df.set_index(['symbol','datetime'])

            return tmp_df
        
        for vSymbol in symbols:
            try:
                tmp_df = ak.fund_etf_hist_em(
                    symbol=vSymbol, 
                    period=interval, 
                    start_date=start_d, 
                    end_date=end_d, 
                    adjust="")
                
                if not tmp_df.columns.empty:
                    tmp_df['symbol'] = vSymbol
                    tmp_df['interval'] = interval
                    tmp_df['asset'] = 'ETF' #E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权  ETF ，默认E
                    tmp_df['adjust'] = ''

            except KeyError:
                tmp_df = pd.DataFrame(
                    [],
                    columns=['symbol','interval','datetime','open','close','high','low','vol','turnover','asset','adjust']
                )

            result_df = pd.concat([result_df,tmp_df],ignore_index=True)

        result_df = result_df.rename(columns={"日期":"datetime",
                                "开盘":"open",
                                "收盘":"close",
                                "最高":"high",
                                "最低":"low",
                                "成交量":"vol",
                                "成交额":"turnover"})
        
        result_df['datetime'] = pd.to_datetime(result_df['datetime'])
        result_df['vol'] = pd.to_numeric(result_df['vol'])
        result_df['turnover'] = pd.to_numeric(result_df['turnover'])
        result_df = result_df[['symbol','interval','datetime','open','close','high','low','vol','turnover','asset','adjust']]
        #result_df = result_df.set_index(['symbol','datetime'])

        return result_df