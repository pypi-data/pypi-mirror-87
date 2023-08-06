import dataclasses
import datetime
import pandas as pd
import numpy as np
import math
import statsmodels.api as sm
from statsmodels import regression
from scipy.stats import gmean
from functools import partial
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
from scipy.stats import kurtosis, skew

class CalculatorBase:

    TRADING_DAYS_PER_YEAR = 242
    TOTAL_DAYS_PER_YEAR = 365
    TOTAL_WEEKS_PER_YEAR = 52
    TOTAL_MONTHS_PER_YEAR = 12

    @staticmethod
    def calc_cl_alpha_beta(total: np.ndarray):
        if total.shape[0] <= 1:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    }
        X = np.array([total[:, 1], total[:, 1]]).T
        X[:, 0][X[:, 0] < 0] = 0
        X[:, 1][X[:, 1] > 0] = 0
        if np.count_nonzero(X[:, 1]) == 0:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    }
        est2 = sm.OLS(total[:, 0], sm.add_constant(X, prepend=False)).fit()
        return {'beta':est2.params[0] - est2.params[1],
                'alpha':est2.params[-1]}
    
    @staticmethod
    def calc_hm_alpha_beta(total: np.ndarray):
        if total.shape[0] <= 1:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    }
        X = np.array([total[:, 1], total[:, 1]]).T
        X[:, 1][X[:, 1] < 0] = 0
        est2 = sm.OLS(total[:, 0], sm.add_constant(X, prepend=False)).fit()
        return {'beta':est2.params[1],
                'alpha':est2.params[-1],
                }

    @staticmethod
    def calc_continue_regress_v(monthly_ret, risk_free_rate):
        # 半年周期
        window = 6
        yearly_multiplier = 2
        period_num = 12
        annual_ret = monthly_ret.rolling(window=window).apply(lambda x : x.sum() * yearly_multiplier - risk_free_rate)
        annual_vol = monthly_ret.rolling(window=window).apply(lambda x : x.std(ddof=1) * np.sqrt(period_num))
        sharpe = (annual_ret / annual_vol)
        sharpe = sharpe.replace(np.Inf, np.nan).replace(-np.Inf, sharpe).dropna() # 空值sharpe赋值np.nan
        if sharpe.shape[0] < 6:
            return np.nan
        mod = AutoReg(endog=sharpe.values, lags=1)
        res = mod.fit()
        continue_regress_v = res.params[0]
        return continue_regress_v

    @staticmethod
    def get_stat_result(dates:             pd.core.series.Series,
                        values:            pd.core.series.Series,
                        benchmark_values:  pd.core.series.Series=None,
                        risk_free_rate:    float=0.025,
                        frequency:         str='1D'):# '1W' '1M'
        assert frequency in ['1D','1W','2W','1M'], 'frequency provided is not included, must in 1D 1W 2W 1M'
        risk_free_per_day = risk_free_rate / CalculatorBase.TRADING_DAYS_PER_YEAR
        dates = pd.to_datetime(dates)
        dates = [i.date() for i in dates]
        assert len(dates) == len(values), 'date and port_values has different numbers'
        if len(dates) > 2:
            sr = pd.Series(values, index=dates).sort_index().dropna()
            sr = sr.set_axis(pd.to_datetime(sr.index), inplace=False).resample(frequency).last().dropna()
            sr.index = [i.date() for i in sr.index]
            if frequency == '1D':            
                period_1m = 20
                period_3m = period_1m * 3
                period_6m = period_1m * 6
                period_1y = CalculatorBase.TRADING_DAYS_PER_YEAR
                period_3y = period_1y * 3
                period_5y = period_1y * 5
            elif frequency == '1W':
                period_1m = 4
                period_3m = period_1m * 3
                period_6m = period_1m * 6
                period_1y = CalculatorBase.TOTAL_WEEKS_PER_YEAR
                period_3y = period_1y * 3
                period_5y = period_1y * 5
            elif frequency == '2W':
                period_1m = 2
                period_3m = period_1m * 3
                period_6m = period_1m * 6
                period_1y = CalculatorBase.TOTAL_WEEKS_PER_YEAR / 2
                period_3y = period_1y * 3
                period_5y = period_1y * 5
            elif frequency == '1M':
                period_1m = 1
                period_3m = period_1m * 3
                period_6m = period_1m * 6
                period_1y = CalculatorBase.TOTAL_MONTHS_PER_YEAR
                period_3y = period_1y * 3
                period_5y = period_1y * 5
            sr_ret = np.log(sr).diff(1).iloc[1:]
            start_date = sr.index[0] 
            end_date = sr.index[-1]
            days = (dates[-1] - dates[0]).days
            last_unit_nav = sr[-1] / sr[0]
            cumu_ret = last_unit_nav - 1
            trade_year = days / CalculatorBase.TOTAL_DAYS_PER_YEAR
            annual_ret = math.pow(last_unit_nav, CalculatorBase.TOTAL_DAYS_PER_YEAR/days) - 1
            annual_vol = sr_ret.std(ddof=1) * np.sqrt(period_1y)
            recent_1m_ret = sr[-1] / sr[-(period_1m + 1)] - 1 if len(sr) > (period_1m + 1) else sr[-1] / sr[0] - 1
            recent_3m_ret = sr[-1] / sr[-(period_3m + 1)] - 1 if len(sr) > (period_3m + 1) else sr[-1] / sr[0] - 1
            recent_6m_ret = sr[-1] / sr[-(period_6m + 1)] - 1 if len(sr) > (period_6m + 1) else sr[-1] / sr[0] - 1
            recent_1y_ret = sr[-1] / sr[-(period_1y + 1)] - 1 if len(sr) > (period_1y + 1) else sr[-1] / sr[0] - 1
            recent_3y_ret = sr[-1] / sr[-(period_3y + 1)] - 1 if len(sr) > (period_3y + 1) else sr[-1] / sr[0] - 1
            recent_5y_ret = sr[-1] / sr[-(period_5y + 1)] - 1 if len(sr) > (period_5y + 1) else sr[-1] / sr[0] - 1
            worst_3m_ret = sr.pct_change(period_3m).min()
            worst_6m_ret = sr.pct_change(period_6m).min()
            last_mv_diff = sr[-1] - sr[-2]
            last_increase_rate = (sr[-1] - sr[-2])/ sr[-2]
            sharpe = (annual_ret - risk_free_rate) / annual_vol
            recent_drawdown = 1 - (sr[-1] / sr.max())
            if np.isnan(recent_drawdown):
                recent_mdd_date1 = None
                recent_mdd_lens = None
            else:
                recent_mdd_date1 = sr.idxmax()
                recent_mdd_lens = (end_date - recent_mdd_date1).days
            mdd_part =  sr / sr.rolling(window=sr.shape[0], min_periods=1).max()
            mdd = 1 - mdd_part.min()
            if np.isnan(mdd):
                mdd_date2 = None
                mdd_date1 = None
                mdd_lens = None
            else:
                mdd_date2 = mdd_part.idxmin()
                mdd_date1 = sr[:mdd_date2].idxmax()
                mdd_lens = (mdd_date2-mdd_date1).days
            calmar = (annual_ret - risk_free_rate) / mdd
            sr_ret_no_risk_free = sr_ret - risk_free_rate / period_1y
            downside_risk = np.minimum(sr_ret_no_risk_free,0).std(ddof=1) * np.sqrt(period_1y)
            sortino = (annual_ret - risk_free_rate) / downside_risk
            var =  np.quantile(sr_ret, 0.05) # 按照最大回撤处理， 损失非负， 计算ervar用
            cvar = max(0, -sr_ret[sr_ret < var].mean())
            var = - var
            ervar = (annual_ret - risk_free_rate) / var
            skew_value = skew(sr_ret)
            kurtosis_value = kurtosis(sr_ret)        
            
            if benchmark_values is not None:
                assert len(dates) == len(benchmark_values), 'date and bench_values has different numbers'
                sr_benchmark = pd.Series(benchmark_values, index=dates).sort_index().dropna()
                sr_benchmark = sr_benchmark.set_axis(pd.to_datetime(sr_benchmark.index), inplace=False).resample(frequency).last().dropna()
                sr_benchmark.index = [i.date() for i in sr_benchmark.index]
                sr_benchmark_ret = np.log(sr_benchmark).diff(1).iloc[1:]
                last_unit_benchmark = sr_benchmark[-1] / sr_benchmark[0]
                annual_ret_benchmark = math.pow(last_unit_benchmark, CalculatorBase.TOTAL_DAYS_PER_YEAR / days) - 1
                df = pd.concat([sr, sr_benchmark],axis=1)
                df.columns= ['fund_ret','index_ret']
                df_monthly = df.set_axis(pd.to_datetime(df.index), inplace=False).resample(rule='1M').last()
                df_monthly.index = df_monthly.index.date
                monthly_ret = df_monthly.pct_change(1).dropna()
                continue_value_m = CalculatorBase.calc_continue_regress_v(monthly_ret.fund_ret,risk_free_rate)
                df_ret_risk_free = (df.pct_change(1) - risk_free_per_day).dropna()
                cl_res = CalculatorBase.calc_cl_alpha_beta(df_ret_risk_free.to_numpy())
                alpha_cl = cl_res['alpha'] * period_1y
                beta_cl = cl_res['beta']
                hm_res = CalculatorBase.calc_hm_alpha_beta(df_ret_risk_free.to_numpy())
                alpha_hm = hm_res['alpha'] * period_1y
                beta_hm = hm_res['beta']
                excess_ret = annual_ret - annual_ret_benchmark
                _index = sorted(sr_ret.index.intersection(sr_benchmark_ret.index))
                sr_ret = sr_ret.reindex(_index)
                sr_benchmark_ret = sr_benchmark_ret.reindex(_index)
                win_rate = np.mean((sr_ret > sr_benchmark_ret) * 1)
                corr = sr_ret.corr(sr_benchmark_ret)    
                track_err = (sr_ret - sr_benchmark_ret).std(ddof=1) * np.sqrt(period_1y)
                info = excess_ret / track_err
                x = sr_benchmark_ret.dropna().values
                y = sr_ret.dropna().values
                x = sm.add_constant(x)
                model = regression.linear_model.OLS(y,x).fit()
                alpha = model.params[0]
                beta = model.params[1]
                treynor = (annual_ret - risk_free_rate) / beta
                not_system_risk = sum((sr_ret - risk_free_per_day)**2) \
                                - alpha * sum(sr_ret - risk_free_per_day) \
                                - beta * sum((sr_ret - risk_free_per_day) * (sr_benchmark_ret - risk_free_per_day))
                not_system_risk = np.sqrt(not_system_risk / (len(sr_ret) - 2))
                alpha = alpha * period_1y
                df_ret = np.log(df).diff(1).iloc[1:]
                df_ret_up = df_ret[df_ret.index_ret > 0] + 1 
                up_cap_top = df_ret_up.fund_ret.product() ** (period_1y/len(df_ret_up)) - 1
                up_cap_bot = df_ret_up.index_ret.product() ** (period_1y/len(df_ret_up)) - 1
                up_capture = up_cap_top / up_cap_bot

                df_ret_down = df_ret[df_ret.index_ret < 0] + 1
                down_cap_top = df_ret_down.fund_ret.product() ** (period_1y/len(df_ret_down)) - 1
                down_cap_bot = df_ret_down.index_ret.product() ** (period_1y/len(df_ret_down)) - 1
                down_capture = down_cap_top / down_cap_bot

                df_ret['excess_ret'] = df_ret.fund_ret - df_ret.index_ret
                df_ret = df_ret.replace(np.Inf,np.nan).replace(-np.Inf,np.nan).dropna()
                mod = AutoReg(endog=df_ret.excess_ret.values, lags=1)
                res = mod.fit()
                excess_ret_cotinue = res.params[0]
                return {
                    'start_date':start_date,
                    'end_date':end_date,
                    'trade_year':trade_year,
                    'last_unit_nav':last_unit_nav,
                    'cumu_ret':cumu_ret,
                    'annual_ret':annual_ret,
                    'annual_vol':annual_vol,
                    'sharpe':sharpe,
                    'recent_1m_ret':recent_1m_ret,
                    'recent_3m_ret':recent_3m_ret,
                    'recent_6m_ret':recent_6m_ret,
                    'recent_1y_ret':recent_1y_ret,
                    'recent_3y_ret': recent_3y_ret,
                    'recent_5y_ret':recent_5y_ret,
                    'worst_3m_ret':worst_3m_ret,
                    'worst_6m_ret':worst_6m_ret,
                    'last_mv_diff':last_mv_diff,
                    'last_increase_rate':last_increase_rate,
                    'recent_drawdown':recent_drawdown,
                    'recent_mdd_date1':recent_mdd_date1,
                    'recent_mdd_lens':recent_mdd_lens,
                    'mdd':mdd,
                    'mdd_date1':mdd_date1,
                    'mdd_date2':mdd_date2,
                    'mdd_lens':mdd_lens,
                    'calmar':calmar,
                    'downside_risk':downside_risk,
                    'sortino':sortino,
                    'var':var,
                    'ervar':ervar,
                    'skew':skew_value,
                    'kurtosis':kurtosis_value,
                    'alpha_cl':alpha_cl,
                    'beta_cl':beta_cl,
                    'alpha_hm':alpha_hm,
                    'beta_hm':beta_hm,
                    'excess_ret':excess_ret,
                    'win_rate':win_rate,
                    'corr':corr,
                    'track_err':track_err,
                    'info':info,
                    'alpha':alpha,
                    'beta':beta,
                    'treynor':treynor,
                    'not_system_risk':not_system_risk,
                    'cvar':cvar,
                    'up_capture':up_capture,
                    'down_capture':down_capture,
                    'excess_ret_cotinue':excess_ret_cotinue,
                    'continue_value_m':continue_value_m,
                }
            else:
                return {
                    'start_date':start_date,
                    'end_date':end_date,
                    'trade_year':trade_year,
                    'last_unit_nav':last_unit_nav,
                    'cumu_ret':cumu_ret,
                    'annual_ret':annual_ret,
                    'annual_vol':annual_vol,
                    'sharpe':sharpe,
                    'recent_1m_ret':recent_1m_ret,
                    'recent_3m_ret':recent_3m_ret,
                    'recent_6m_ret':recent_6m_ret,
                    'recent_1y_ret':recent_1y_ret,
                    'recent_3y_ret': recent_3y_ret,
                    'recent_5y_ret':recent_5y_ret,
                    'worst_3m_ret':worst_3m_ret,
                    'worst_6m_ret':worst_6m_ret,
                    'last_mv_diff':last_mv_diff,
                    'last_increase_rate':last_increase_rate,
                    'recent_drawdown':recent_drawdown,
                    'recent_mdd_date1':recent_mdd_date1,
                    'recent_mdd_lens':recent_mdd_lens,
                    'mdd':mdd,
                    'mdd_date1':mdd_date1,
                    'mdd_date2':mdd_date2,
                    'mdd_lens':mdd_lens,
                    'calmar':calmar,
                    'downside_risk':downside_risk,
                    'sortino':sortino,
                    'var':var,
                    'cvar':cvar,
                    'ervar':ervar,
                    'skew':skew_value,
                    'kurtosis':kurtosis_value,
                }
        else:
            return {
                    'start_date':dates[0] if len(dates) > 0 else None,
                    'end_date':dates[-1] if len(dates) > 0 else None,
                    'trade_year':0,
                    'last_unit_nav':0,
                    'cumu_ret':0,
                    'annual_ret':0,
                    'annual_vol':0,
                    'sharpe':0,
                    'recent_1m_ret':0,
                    'recent_3m_ret':0,
                    'recent_6m_ret':0,
                    'recent_1y_ret':0,
                    'recent_3y_ret': 0,
                    'recent_5y_ret':0,
                    'worst_3m_ret':0,
                    'worst_6m_ret':0,
                    'last_mv_diff':0,
                    'last_increase_rate':0,
                    'recent_drawdown':0,
                    'recent_mdd_date1':dates[0] if len(dates) > 0 else None,
                    'recent_mdd_lens':0,
                    'mdd':0,
                    'mdd_date1':dates[0] if len(dates) > 0 else None,
                    'mdd_date2':dates[0] if len(dates) > 0 else None,
                    'mdd_lens':0,
                    'calmar':0,
                    'downside_risk':0,
                    'sortino':0,
                    'var':0,
                    'cvar':0,
                    'ervar':0,
                    'skew':0,
                    'kurtosis':0,
                    'alpha_cl':0,
                    'beta_cl':0,
                    'alpha_hm':0,
                    'beta_hm':0,
                    'excess_ret':0,
                    'win_rate':0,
                    'corr':0,
                    'track_err':0,
                    'info':0,
                    'alpha':0,
                    'beta':0,
                    'treynor':0,
                    'not_system_risk':0,
                    'cvar':0,
                    'up_capture':0,
                    'down_capture':0,
                    'excess_ret_cotinue':0,
                    'continue_value_m':0,
                }
