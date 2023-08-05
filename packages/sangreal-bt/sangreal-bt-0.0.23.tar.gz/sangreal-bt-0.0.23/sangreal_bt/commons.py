from pandas.tseries.offsets import Hour, Second

class Commons:
    # 300 50 300 期货
    INDEX_FUTURE = 'IF|IH|IC'

    # 时间偏移常数
    SHIFT_TIME = Second(1)