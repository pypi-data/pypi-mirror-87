import empyrical as ep
import numpy as np
import pandas as pd
from addict import Dict


class Stats:
    """配套结果生成的对应输出
    """
    def __init__(self, sret, bret):
        """策略收益及基准收益
            pct_change
        """
        self.sret = sret.copy()
        self.bret = bret.copy()
        self.sret.index = pd.to_datetime(self.sret.index)
        self.bret.index = pd.to_datetime(self.bret.index)
        self.stats = Dict()

    @staticmethod
    def _mdd(cum_val):
        """
        cum_val datetimeindex: cumval
        返回净值中最大回撤开始及结束日期
        """
        backmax = cum_val.cummax()
        drawdown = cum_val / backmax - 1.0
        end = drawdown.idxmin()
        begin = cum_val.tolist().index(backmax[end])
        return int(cum_val.index[begin].strftime('%Y%m%d') +
                   end.strftime('%Y%m%d'))

    @classmethod
    # 只显示大与2%的回撤
    def _get_max_drawdown_list(cls, cum_val, threshold=2e-2):
        """
        cum_val datetimeindex: cumval
        return
        begin_dt end_dt ratio
        """
        df = pd.Series(index=cum_val.index)
        for ind in df.index:
            df.loc[ind] = cls._mdd(cum_val.loc[:ind])

        change_dt = df[df.diff().shift(-1) >= 100000000].index

        max_drowlist = [int(df.loc[m]) for m in change_dt] + [int(df.iloc[-1])]
        max_drowlist = [(str(x)[:8], str(x)[8:],
                         cum_val.loc[str(x)[8:]] / cum_val.loc[str(x)[:8]] - 1)
                        for x in max_drowlist]
        max_drowlist = pd.DataFrame(max_drowlist,
                                    columns=['begin_dt', 'end_dt', 'ratio'])
        max_drowlist = max_drowlist[max_drowlist['ratio'] < -threshold]
        max_drowlist['datelen'] = (pd.to_datetime(max_drowlist['end_dt']) -
                                   pd.to_datetime(max_drowlist['begin_dt'])).dt.days
        return max_drowlist

    def run(self):
        self.stats.annual_return = ep.annual_return(self.sret)
        self.stats.annual_volatility = ep.annual_volatility(self.sret)
        self.stats.excess_return = ep.alpha(self.sret, self.bret)
        self.stats.excess_volatility = ep.annual_volatility(self.sret -
                                                            self.bret)
        self.stats.max_drawdown = ep.max_drawdown(self.sret)
        self.stats.information_ratio = ep.excess_sharpe(
            self.sret, self.bret) * np.sqrt(252)
        self.stats.max_drawdown_list = self._get_max_drawdown_list(
            (self.sret.fillna(0) + 1).cumprod())
        return
