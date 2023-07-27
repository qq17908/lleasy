# coding=utf-8

import numpy as np
import pandas as pd

class Strategy():
    def __init__():
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
        trades_df -> pd.DataFrame 
            包含每个交易日的交易数据,主要包括内容：
            0. datetime     交易日期
            1. symbol       标的编号
            2. price        买入卖出价格（元）
            3. num          买入卖出数量（手数）
            4. serviceMoney 交易服务费
            5. totalNum     持仓数量
            6. cash         持有现金
            7. value        资产总价值 = 持有现金 + 持有标的的价值
        benchmarks_df ->pd.DataFrame
            包含基准标的的‘close’行情数据，主要包括内容：
            0.datetime
            1.benchmark_close : 基准标的close行情数据
        start_date -> datetime  回测开始日期
        end_date -> datetime    回测结束日期
        investCash -> float     起始资金

    返回值：
        trades_df -> pd.DataFrame
            1. rtn -> 每日收益率
    """
    def cal_Statistics(self,trades_df,benchmarks_df,start_date,end_date) -> pd.DataFrame:
        # 总交易天数、总交易月数、总交易年数
        bt_start_date = start_date
        bt_end_date = end_date

        # 总交易天数
        self.total_days = (end_date - start_date).days
        # 总交易月数
        self.total_months = int(np.round(self.total_days/30))
        # 总交易年数
        self.total_years = self.total_days / 365
        # 起始资金
        self.total_invest = trades_df.iloc[0].cash
        # 最后总资产
        self.final_value = trades_df.iloc[-1].value

        self.trades_df = trades_df

    # 基准年化收益率、基准每日收益
    def _cal_Reference_Returns(benchmarks:pd.DataFrame):
        pass

    # 每日收益率 = T日总资产 / T-1日总资产
    def _cal_Rtn(self) -> float:
        rtn = (self.trades_df['value'] / self.trades_df['value'].shift(1)) - 1
        self.trades_df['rtn'] = rtn

    # 策略每日收益率
    def _cal_Total_Returns(self) -> float:
        self.trades_df['caption'] = self.trades_df.iloc[0].cash
        self.trades_df['total_rtn'] = self.trades_df['value'] / self.trades_df['caption'] - 1

        total_rtn = self.trades_df['total_rtn'].iloc[-1]
        return total_rtn

    # 策略年化收益率 Total Annualized Returns
    def _cal_Total_Annualized_Returns(self) -> float:
        ys_ = self.total_days / 250
        self.trades_df['annual_rtn'] = (self.trades_df['total_rtn'] + 1 ) * (1/ys_) - 1
        annual_rtn = self.trades_df['annual_rtn'].iloc[-1]
        return annual_rtn

    # 年化波动率
    def _cal_Algorithm_volatility(self):
        ret = self.trades_df['total_rtn']
        volatility = ret.std().np.sqrt(250)
        self.trades_df['volatility'] = volatility
        avg_volatility = self.trades_df['volatility'].mean()

        return  avg_volatility

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

    # 夏普比率 sharpe ratio
    def _cal_SharpeRatio(self):
        total_ret = self.trades_df['total_rtn']
        roll_yearly_return = total_ret.mean() * 250
        self.trades_df['sharp'] = (roll_yearly_return - 0.04) / self.trades_df['volatility']

        avg_sharp = self.trades_df['sharp'].mean()

        return avg_sharp

    # 卡尔玛比率 calmar ratio
    def _cal_CalmarRatio(self):
        pass

    # 阿尔法 alpha
    def _cal_Alpha(self):
        pass
    
    # 贝塔 beta
    def _cal_Beta(self):
        pass


class Reports():
    def __init__(self) -> None:
        pass

    def report():
        pass


