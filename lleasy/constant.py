# coding=utf-8

from enum import Enum

class Interval(Enum):
    """
    Interval of bar data.
    """
    MINUTE = "1m"
    HOUR = "1h"
    DAILY = "d"
    WEEKLY = "w"
    TICK = "tick"

class Product(Enum):
    """
    Product class.
    """
    EQUITY = "股票"
    INDEX = "指数"
    ETF = "ETF"
    BOND = "债券"
    FUND = "基金"

class Exchange(Enum):
    """
    Exchange.
    """
    # Chinese
    SSE = "SSE"             # Shanghai Stock Exchange
    SZSE = "SZSE"           # Shenzhen Stock Exchange

    CFFEX = "CFFEX"         # China Financial Futures Exchange
    SHFE = "SHFE"           # Shanghai Futures Exchange
    CZCE = "CZCE"           # Zhengzhou Commodity Exchange
    DCE = "DCE"             # Dalian Commodity Exchange
    INE = "INE"             # Shanghai International Energy Exchange
    BSE = "BSE"             # Beijing Stock Exchange
    SGE = "SGE"             # Shanghai Gold Exchange


    # Special Function
    LOCAL = "LOCAL"         # For local generated data