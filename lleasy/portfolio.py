# coding=utf-8

import numpy as np
import pandas as pd

class Portfolio():
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
            7. value        资产总价值
        start_date -> datetime  回测开始日期
        end_date -> datetime    回测结束日期
        investCash -> float     起始资金

    返回值：

    """
    def cal_Portfolio(trades_df,start_date,end_date) -> pd.DataFrame:
        # 总交易天数、总交易月数、总交易年数
        bt_start_date = start_date
        bt_end_date = end_date

        # 总交易天数
        total_days = (end_date - start_date).days
        # 总交易月数
        total_months = int(np.round(total_days/30))
        # 总交易年数
        total_years = total_days / 365

        # 起始资金
        total_invest = trades_df.iloc[0].cash
        # 最后总资产
        final_value = trades_df.iloc[-1].value

    # 基准年化收益率
    def get_Cal_Reference_Returns(benchmarks:pd.DataFrame):
        pass
    
    # 收益率
    def _cal_Returns():
        pass

    # 年化收益率 Total Annualized Returns
    def _cal_Total_Annualized_Returns():
        pass



    # 年化波动率
    def _cal_Algorithm_volatility():
        pass

    # 月度历史收益率
    def _cal_Month_Returns():
        pass

    # 最大回撤 max drawdown
    def _cal_Max_Drawdown():
        pass

    # 夏普比率 sharpe ratio
    def _cal_SharpeRatio():
        pass

    # 卡尔玛比率 calmar ratio
    def _cal_CalmarRatio():
        pass

    # 阿尔法 alpha
    def _cal_Alpha():
        pass
    
    # 贝塔 beta
    def _cal_beta():
        pass


class Reports():
    def __init__(self) -> None:
        pass

    def report():
        pass


