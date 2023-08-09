# coding=utf-8

import numpy as np
import pandas as pd
from pandas import DataFrame
from lleasy.log import Log,log_decorator
log = Log("strategy_log")

class Strategy:
    def __init__(self):
        pass

    """
    说明：根据策略交易记录，对本次策略进行回归分析，分析内容包括：
        1. 收益率       returns
        2. 年化收益率   total_annualized_returns
        3. 基准年化收益率
        4. 年化波动率
        5. 月度历史收益率
        6. 最大回撤
        7. 夏普比率
        8. 卡尔玛比率
        9. 阿尔法
        10. 贝塔

    参数：
        symbol_asset_basic -> dict
            包含每个交易日的交易数据,主要包括内容：
            0. date         交易日期
            1. symbol       标的编号
            2. price        买入卖出价格（元）
            3. num          买入卖出数量（手数）
            4. serviceMoney 交易服务费（元）
            5. totalNum     持仓数量（手）
            6. cash         持有现金（元）
            7. value        资产总价值 = 持有现金 + 持有标的的价值

        bars_data_df -> DataFrame
            包含基准标的的‘close’行情数据，主要包括内容：
            1. date   - 日期
            2. symbol - 标的编号
            3. close  - 当日收盘价
            4. benchmark - 基准标的
            5. bmk_close - 基准当日收盘价

    返回值：
        result_df -> Dict
            symbol、
            today_date、today_close、today_value、hold_days、profite、profite_ratio、rtn%、annual_rtn%、avg_volatility、max_drawdown、sharpe
            benchmark、bmk_rtn、bmk_annual_rtn、alpha、beta
    """
    @log_decorator(log)
    def cal_Statistics(
            self,
            symbol_asset_basic: dict = None,
            bars_data_df: DataFrame = None,
        ) -> dict:

        symbol_bar_df = bars_data_df[['datetime','symbol','close']]
        symbol_bar_df['close'] = symbol_bar_df['close'].astype(float)
        symbol_bar_df = symbol_bar_df.set_index(['datetime'])

        symbol_bar_df['num'] = symbol_asset_basic['num']
        benchmark_bar_df = bars_data_df[['datetime','close']]
        benchmark_bar_df['close'] = benchmark_bar_df['close'].astype(float)
        benchmark_bar_df = benchmark_bar_df.set_index(['datetime'])

        symbol = symbol_asset_basic['symbol']
        today_date = symbol_bar_df.index[-1]
        today_close = symbol_bar_df['close'].iloc[-1]
        today_value = today_close * symbol_asset_basic['num']

        hold_days = symbol_bar_df.index[-1] - symbol_bar_df.index[0]
        profite = today_value - symbol_asset_basic['value']
        profite_ratio = (today_value - symbol_asset_basic['value']) / symbol_asset_basic['value']

        # 标的
        ## 每日收益率
        symbol_bar_df['rtn'] = symbol_bar_df['close'] / symbol_bar_df['close'].shift(1) - 1
        symbol_bar_df['rtn'] = pd.to_numeric(symbol_bar_df['rtn'],downcast='float')
        rtn = symbol_bar_df['rtn'].iloc[-1]

        ## 年化收益率
        year_par = (symbol_bar_df.index - symbol_bar_df.index[0]).days / 250
        symbol_bar_df['annual_rtn'] = (1 + symbol_bar_df['rtn']) ** (1 / year_par) - 1
        symbol_bar_df['annual_rtn'] = pd.to_numeric(symbol_bar_df['annual_rtn'],downcast='float')
        annual_rtn = symbol_bar_df['annual_rtn'].iloc[-1]

        ## 年化波动率
        symbol_bar_df['value'] = symbol_asset_basic['num'] * symbol_bar_df['close']
        symbol_bar_df['value'].iloc[0] = symbol_asset_basic['value']
        symbol_bar_df['value'] = pd.to_numeric(symbol_bar_df['value'], downcast='float')
        
        ret = (symbol_bar_df['value'] / symbol_bar_df['value'].shift(1)) - 1
        volatility = ret.std() * np.sqrt(250)
        symbol_bar_df['volatility'] = volatility
        avg_volatility = symbol_bar_df['volatility'].mean()

        ## 夏普比率
        symbol_bar_df['sharp'] = (symbol_bar_df['annual_rtn'] - 0.04) / symbol_bar_df['volatility']
        sharp = symbol_bar_df['sharp'].mean()

        ## 最大回撤

        # 基准(股票：000300、ETF：对应的指数)
        ## 每日收益率
        benchmark_bar_df['rtn'] = benchmark_bar_df['close'] / benchmark_bar_df['close'].shift(1)  - 1
        benchmark_bar_df['rtn'] = pd.to_numeric(benchmark_bar_df['rtn'],downcast='float')
        bmk_rtn = benchmark_bar_df['rtn'].iloc[-1]

        ## 年化收益率
        bmk_year_par = (benchmark_bar_df.index - benchmark_bar_df.index[0]).days / 250
        benchmark_bar_df['annual_rtn'] = (1 + benchmark_bar_df['rtn']) ** (1 / bmk_year_par) - 1
        bmk_annual_rtn = benchmark_bar_df['annual_rtn'].iloc[-1]

        ## 贝塔
        beta_cov = symbol_bar_df['rtn'].cov(benchmark_bar_df['rtn'])
        beta_var = symbol_bar_df['rtn'].var()
        symbol_bar_df['beta'] = beta_cov / beta_var
        beta = symbol_bar_df['beta'].mean()

        ## 阿尔法
        symbol_bar_df['alpha'] = (symbol_bar_df['annual_rtn'] - 0.04) \
                                - symbol_bar_df['beta'] * (benchmark_bar_df['annual_rtn'] - 0.04)
        alpha = symbol_bar_df['alpha'].mean()

        #返回值
        statistics = {
            'symbol':symbol,
            'today_date':today_date,
            'today_close':today_close,
            'today_value':today_value,
            'hold_days':hold_days,
            'profite':profite,
            'profite_ratio':'{:0.3%}'.format(profite_ratio),
            'rtn':'{:0.5%}'.format(rtn),
            'annual_rtn':'{:0.5%}'.format(annual_rtn),
            'avg_volatility':'{:0.5%}'.format(avg_volatility),
            'sharp':'{:0.5%}'.format(sharp),
            'bmk_rtn':'{:0.5%}'.format(bmk_rtn),
            'bmk_annual_rtn':'{:0.5%}'.format(bmk_annual_rtn),
            'alpha':'{:0.5%}'.format(alpha),
            'beta':'{:0.5%}'.format(beta)
        }

        return statistics

    # 月度历史收益率
    def _cal_Month_Returns():
        pass

    # 最大回撤 max drawdown
    def _cal_Max_Drawdown(self):
        #np.argmax作用：取出数组中最大值对应的索引
        max_dd_end = np.argmax(
            np.maximum.accumulate(self.trades_df['value']) - self.trades_df['value']
        )

        if max_dd_end == 0:
            max_dd_start = 0
        else:
            max_dd_start = np.argmax(self.trades_df['value'][:max_dd_end])
        
        mdd = self.trades_df['value'][max_dd_start] - self.trades_df['value'][max_dd_end]
        mdd_rate = mdd / self.trades_df['value'][max_dd_start]
        mdd_during = max_dd_end - max_dd_start

        return mdd_rate