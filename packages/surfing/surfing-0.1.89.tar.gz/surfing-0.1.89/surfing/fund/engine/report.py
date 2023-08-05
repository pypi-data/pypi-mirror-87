import pandas as pd
import numpy as np
import datetime
import copy
from pprint import pprint 
import platform
import matplotlib as mpl
import json
from collections import Counter
from .painter.asset_painter import AssetPainter
from .painter.fund_painter import FundPainter
from .painter.hybrid_painter import HybridPainter
from ...data.struct import AssetWeight, AssetPosition, AssetPrice, AssetValue
from .asset_helper import TAAHelper
from ...data.manager.manager_fund import FundDataManager
from ...data.struct import FundTrade, TaaTunerParam, FundPosition, TAAParam
from .asset_helper import SAAHelper, TAAHelper, FAHelper, TAAStatusMode
from ...util.calculator import Calculator

CURRENT_PLATFORM = platform.system()
if CURRENT_PLATFORM == 'Darwin':
    mpl.rcParams['font.family'] = ['Heiti TC']
else:
    mpl.rcParams['font.family'] = ['STKaiti']

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)

class ReportHelper:
    
    '''
    save backtest history
    '''

    def __init__(self):
        pass

    def init(self): 
        pass

    def plot_init(self, dm, taa_helper=None, score_select=None):
        self.index_price = dm.get_index_price()
        self.fund_info = dm.get_fund_info()
        self.fund_nav = dm.dts.fund_nav
        self.fund_indicator = dm.dts.fund_indicator
        self.taa_params = taa_helper.params if isinstance(taa_helper, TAAHelper) else None
        self.index_pct = dm.dts.index_pct
        self.dts = dm.dts.trading_days.datetime
        self.fund_manager_info = dm.dts.fund_manager_info
        self.fund_score_dm = dm._score_manager.score_cache
        trade_list = []
        for d, trade_d in self.trade_history.items():
            trade_d = [_.__dict__ for _ in trade_d]
            trade_list.extend(trade_d)
        self.trade_df = pd.DataFrame(trade_list)
        if not self.trade_df.empty:
            self.trade_df['year'] = [_.year for _ in self.trade_df.trade_date]
        self.pct_df = dm.dts._index_pct_df
        self.score_select = score_select
        self.active_fund_info = dm.dts.active_fund_info
        self.fund_info = self.fund_info.set_index('fund_id')
        for r in self.active_fund_info.itertuples():
            self.fund_info.loc[r.fund_id,'index_id'] = r.index_id
        self.fund_info = self.fund_info.reset_index()

    def setup(self, saa:AssetWeight=None):
        self.saa_weight = saa.__dict__ if saa else None
        self.asset_cash_history = {}
        self.asset_position_history = {}
        self.asset_market_price_history = {}
        self.pending_trade_history = {}
        self.asset_weights_history = {}
        self.tactic_history = {}
        self.fund_position_history = {}
        self.trade_history = {}
        self.rebalance_date = []
        self.fund_cash_history = {}
        self.fund_marktet_price_history = {}
        self.fund_weights_history = {}
        self.fund_score = {}
        self.fund_score_raw = {}
        self.target_allocation = {}
        self._rebalance_details = []
        self._rebalance_history = []

    def update(self,dt:datetime, asset_cur_position:AssetPosition, asset_cur_price:AssetPrice, pend_trades:list, fund_cur_position:FundPosition, fund_nav:dict, traded_list:list, fund_score:dict, fund_score_raw:dict, target_allocation):   
        # 检查回测时使用
        self.asset_cash_history[dt] = asset_cur_position.cash##
        self.asset_position_history[dt] = asset_cur_position.__dict__##
        self.pending_trade_history[dt] = pend_trades##
        if fund_cur_position is not None:
            dic = {f : f_info.__dict__  for f, f_info in fund_cur_position.copy().funds.items()}
            for f, f_info in dic.items():
                f_info['price'] =  fund_nav[f]
            self.fund_position_history[dt] = dic     
            self.fund_cash_history[dt] = fund_cur_position.cash
            mv, fund_w = fund_cur_position.calc_mv_n_w(fund_navs=fund_nav)
            self.fund_marktet_price_history[dt] = mv
            self.fund_weights_history[dt] = { fund_id : w_i for fund_id, w_i in fund_w.items() if w_i > 0}
            self.fund_score[dt] = fund_score
            self.fund_score_raw[dt] = fund_score_raw

        self.asset_market_price_history[dt] = AssetValue(prices=asset_cur_price, positions=asset_cur_position).sum() 
        asset_w = AssetValue(prices=asset_cur_price, positions=asset_cur_position).get_weight().__dict__
        self.asset_weights_history[dt] = { index_id : w_i for index_id, w_i in asset_w.items() if w_i > 0}
        if traded_list is not None:
            if len(traded_list) > 0:
                self.rebalance_date.append(dt)
                self.trade_history[dt] = traded_list
        self.target_allocation[dt] = target_allocation
        
    def _calc_stat_yearly(self, mv_df):
        if not self.trade_df.empty:
            trade_df = self.trade_df.set_index(['year','trade_date'])
            trade_df = trade_df[trade_df['is_buy'] == True]
            trade_amount_year = trade_df.groupby('year').sum()
            mv_df = mv_df.reset_index()
            dates = mv_df['date'].values
            mv_df['year'] = [_.year for _ in mv_df.date]
            mv_df = mv_df.set_index(['year','date'])
            res = []
            for year in trade_amount_year.index:
                mv_year = mv_df.loc[year]
                dic = {
                    'year': year,
                    'yearly_amount': trade_amount_year.loc[year, 'amount'],
                    'year_begin_mv': mv_df.loc[year].iloc[0].mv,
                    'year_end_mv':mv_year.iloc[-1].mv,
                    'year_mdd':1 - (mv_year.mv / mv_year.mv.cummax()).min()
                    }
                res.append(dic)
            self.turnover_df = pd.DataFrame(res)
            self.turnover_df['turnover_rate_yearly'] = 100 * self.turnover_df['yearly_amount'] / self.turnover_df['year_begin_mv']
            self.turnover_df['year_ret'] = self.turnover_df.year_end_mv / self.turnover_df.year_begin_mv - 1
            self.turnover_rate_yearly_avg = self.turnover_df['turnover_rate_yearly'].sum() / (mv_df.index[-1][0] - mv_df.index[0][0] + 1)
            total_amount = self.trade_df[self.trade_df['is_buy'] == True].amount.sum()
            self.turnover_rate_amt_mv_gmean = Calculator.get_turnover_rate(dates=dates, values=mv_df.mv.values, total_amount=total_amount)
        else:
            self.turnover_df = pd.DataFrame()
            self.turnover_rate_yearly_avg = 0
            self.turnover_rate_amt_mv_gmean = 0

    def _calc_stat(self, df):
        res = Calculator.get_stat_result_from_df(df=df.reset_index(), date_column='date', value_column='mv')
        w = copy.deepcopy(self.saa_weight) if self.saa_weight else AssetWeight().__dict__ # asset weight float
        self._calc_stat_yearly(df)
        w['mdd'] = res.mdd #float
        w['annual_ret'] = res.annualized_ret #float
        w['ret_over_mdd'] = res.ret_over_mdd #float
        w['sharpe'] = res.sharpe #float 
        w['recent_1m_ret'] = res.recent_1m_ret #float
        w['recent_3m_ret'] = res.recent_3m_ret #float
        w['recent_6m_ret'] = res.recent_6m_ret #float
        w['recent_1y_ret'] = res.recent_y1_ret #float
        w['5_year_ret'] = res.recent_y5_ret #float
        w['3_year_ret'] = res.recent_y3_ret #float
        w['1_year_ret'] = res.recent_y1_ret #float
        w['annual_vol'] = res.annualized_vol #float
        w['mdd_d1'] = res.mdd_date1 #datetime
        w['mdd_d2'] = res.mdd_date2 #datetime
        w['turnover_rate_yearly_avg'] = self.turnover_rate_yearly_avg #float 两种算法的换手率结果很接近
        w['turnover_rate_amt_mv_gmean'] = self.turnover_rate_amt_mv_gmean #float
        w['start_date'] = res.start_date #datetime
        w['end_date'] = res.end_date #datetime
        if not self.trade_df.empty:
            w['total_fee_over_begin_mv'] = self.trade_df.commission.sum() / df.mv[0] #float
            w['total_commission'] = self.trade_df.commission.sum()
        else:
             w['total_fee_over_begin_mv'] = 0
             w['total_commission'] = 0
        w['rebalance_date'] = self.rebalance_date #list
        w['last_unit_nav'] = res.last_unit_nav
        w['last_mv_diff'] = res.last_mv_diff
        w['last_increase_rate'] = res.last_increase_rate
        w['market_value'] = df #dataframe
        w['rebalance_times'] = len(self.rebalance_date)
        w['recent_drawdown'] = res.recent_drawdown
        w['recent_mdd_date1'] = str(res.recent_mdd_date1) # str
        w['worst_3m_ret'] = res.worst_3m_ret
        w['worst_6m_ret'] = res.worst_6m_ret
        hold_days = self.rebalance_date + [df.index.values[-1]]
        index_list = df.index.tolist()
        result = {}
        for d in hold_days[:-1]:
            d1 = hold_days[hold_days.index(d) + 1]
            idx0 = index_list.index(d)
            idx1 = index_list.index(d1)
            result[d.strftime('%Y-%m-%d')] = (idx1 - idx0) / 242
        w['hold_years'] = result # dic
        return w

    def get_asset_stat(self):
        self.asset_mv = pd.DataFrame([ {'date':k, 'mv':v} for k,v in self.asset_market_price_history.items()]).set_index('date')
        w = self._calc_stat(self.asset_mv.copy())
        return w
    
    def save_asset_bk(self, json_name):
        dic = self.get_asset_stat()
        dic['market_value'] =  dic['market_value'].reset_index().to_dict('records')
        with open(f'{json_name}.json','w') as f:
            f.write(json.dumps(dic, cls=DatetimeEncoder))

    def get_fund_stat(self):
        if not self.fund_marktet_price_history:
            return None
            
        self.fund_mv = pd.DataFrame([ {'date':k, 'mv':v} for k,v in self.fund_marktet_price_history.items()]).set_index('date')
        w = self._calc_stat(self.fund_mv.copy())
        return w

    def get_last_position(self):
        last_date = list(self.fund_position_history.keys())[-1]
        dic = self.fund_position_history[last_date]
        weight_dict = self.fund_weights_history[last_date]
        name_dict =  self.fund_info[['fund_id','desc_name']].set_index('fund_id').to_dict()['desc_name']
        dic_list = [v for k,v in dic.items() if v['volume'] > 0]
        pos_df = pd.DataFrame(dic_list).sort_values('index_id')[['fund_id','index_id']].set_index('fund_id')
        pos_df['weight'] = pos_df.index.map(lambda x : weight_dict[x])
        pos_df['desc_name'] = pos_df.index.map(lambda x : name_dict[x])
        pos_df.index.name = last_date
        pos_df = pos_df.sort_values('weight', ascending = False)
        dt = sorted(list(self.fund_score_dm.keys()))[-1]
        fund_rank = []
        for i in pos_df.itertuples():
            _score_dict = self.fund_score_dm[dt][i.index_id][self.score_select[i.index_id]]
            _score_list = sorted(_score_dict.items(), key=lambda x:x[1], reverse=True)
            _fund_list = [i[0] for i in _score_list]
            rank_i = _fund_list.index(i.Index) + 1 if i.Index in _fund_list else 10000
            fund_rank.append(rank_i)
        pos_df = pos_df.join(self.fund_info.set_index('fund_id')[['fund_manager']])
        pos_df.loc[:,'fund_rank'] = fund_rank
        return pos_df

    def get_last_target_fund_allocation(self, target_fund):
        res = []
        fund_info_dic = self.fund_info[['fund_id','desc_name']].set_index('fund_id').to_dict()['desc_name']
        for fund_id, fund_w in target_fund.items():
            dic = {'fund_id':fund_w.fund_id,
                'index_id':fund_w.index_id, 
                'weight':round(fund_w.fund_wgt,3),
                'desc_name':fund_info_dic[fund_w.fund_id]}
            res.append(dic)
        target_fund = pd.DataFrame(res).set_index('fund_id')
        target_fund = target_fund.join(self.fund_info.set_index('fund_id')[['fund_manager']])
        target_fund.index.name = list(self.fund_position_history.keys())[-1]
        return target_fund.sort_values('weight', ascending = False)[['index_id','weight','desc_name','fund_manager']]

    def get_fund_trade(self):
        fsdf = self.fund_score.copy()
        fund_info_df = self.fund_info.copy().set_index('fund_id')
        fund_trade = []
        for d in self.trade_history:
            f_t = [ i.__dict__  for i in self.trade_history[d] if isinstance(i, FundTrade)]
            fund_trade.extend(f_t)
        if len(fund_trade) < 1:
            return pd.DataFrame()
        ft_res = []
        for ft in fund_trade:
            ft['desc_name'] = fund_info_df.loc[ft['fund_id'], 'desc_name']
            index_id = fund_info_df.loc[ft['fund_id'], 'index_id']
            try:
                s = fsdf[ft['submit_date']][index_id][ft['fund_id']]
            except:
                s = np.nan
            ft['submit_d_score'] = s
            fund_id = ft['fund_id']
            submit_d = ft['submit_date']
            traded_d = ft['trade_date']
            ft['before_w']  = self.fund_weights_history[submit_d].get(fund_id,0)
            ft['after_w'] = self.fund_weights_history[traded_d].get(fund_id,0)
            ft_res.append(ft)
        df = pd.DataFrame(ft_res)
        df['before_w'] = df['before_w'].round(4)
        df['after_w'] = df['after_w'].round(4)
        dts = df.submit_date.unique().tolist()
        for dt in dts:
            _df = df[df['submit_date'] == dt]
            fund_id = _df.iloc[-1].fund_id
            df.loc[(df['submit_date'] == dt) & (df['fund_id'] == fund_id),'after_w'] = 1 - _df.iloc[:-1].after_w.sum()
            df.loc[(df['submit_date'] == dt) & (df['fund_id'] == fund_id),'before_w'] = 1 - _df.iloc[:-1].before_w.sum()
        return df

    @staticmethod
    def fund_rank_recent_analysis(dm, fund_id, score_select):
        score_dict = dm._score_manager.score_cache
        fund_info = dm.dts.fund_info
        fund_indicator = dm.dts.fund_indicator
        fund_nav = dm.dts.fund_nav
        index_price = dm.dts.index_price
        index_id = fund_info[fund_info['fund_id'] == fund_id].index_id.values[0]
        score_func = dm._score_manager.funcs[index_id][score_select[index_id]]
        return HybridPainter.fund_rank_recent_analysis(fund_id,index_id,score_dict,fund_info,fund_indicator,fund_nav,index_price,score_func,score_select)

    def get_asset_trade(self):
        asset_trade = []
        for d in self.trade_history:
            a_t = [ i.__dict__  for i in self.trade_history[d] if not isinstance(i, FundTrade)]
            asset_trade.extend(a_t) 
        res = []
        for dic in asset_trade: 
            index_id = dic['index_id']
            submit_d = dic['submit_date']
            traded_d = dic['trade_date']
            dic['before_w'] = self.asset_weights_history[submit_d].get(index_id, 0)
            dic['after_w'] = self.asset_weights_history[traded_d].get(index_id, 0)
            res.append(dic)
        df = pd.DataFrame(res)
        df['before_w'] = df['before_w'].round(4)
        df['after_w'] = df['after_w'].round(4)
        dts = df.submit_date.unique().tolist()
        for dt in dts:
            _df = df[df['submit_date'] == dt]
            index_id = _df.iloc[-1].index_id
            df.loc[(df['submit_date'] == dt) & (df['index_id'] == index_id),'after_w'] = 1 - _df.iloc[:-1].after_w.sum()
            df.loc[(df['submit_date'] == dt) & (df['index_id'] == index_id),'before_w'] = 1 - _df.iloc[:-1].before_w.sum()
        return df

    def get_fund_position(self):
        fund_pos = []
        for d in self.fund_position_history:
            for i in self.fund_position_history[d].values():
                if i['volume'] > 0:
                    i['datetime'] = d
                    fund_pos.append(i)
        return pd.DataFrame(fund_pos).sort_values('datetime')

    def get_index_fee_avg(self):
        self.index_fee = self.trade_df.copy()
        if self.index_fee.empty:
            self.index_fee_buy = pd.DataFrame()
            self.index_fee_sel = pd.DataFrame()
            self.index_fee_buy['fee_ratio_avg'] = 0
            self.index_fee_sel['fee_ratio_avg'] = 0
            self.index_fee['fee_ratio_avg'] = 0
        else:
            self.index_fee_buy = self.index_fee[self.index_fee.is_buy].groupby('index_id').sum()
            self.index_fee_sel = self.index_fee[np.logical_not(self.index_fee.is_buy)].groupby('index_id').sum()
            self.index_fee_buy['fee_ratio_avg'] = self.index_fee_buy.commission / self.index_fee_buy.amount
            self.index_fee_sel['fee_ratio_avg'] = self.index_fee_sel.commission / self.index_fee_sel.amount
            self.index_fee = self.index_fee.groupby('index_id').sum()
            self.index_fee['fee_ratio_avg'] = self.index_fee.commission / self.index_fee.amount

    def get_rebalance_detail(self):
        #rebalance_details = [i['rebalance_reason'][0]['rebalanace_reason'] for i in self._rebalance_details]
        #rebalance_details = dict(Counter(rebalance_details))
        trade_df = self.trade_df.copy()
        fund_mv = self.fund_mv.copy()
        result = self._calc_stat(fund_mv).copy()
        _rb_df = pd.DataFrame(self._rebalance_details)
        submit_date_to_trade_day = trade_df[['submit_date','trade_date']].set_index('submit_date').to_dict()['trade_date']
        turnover_df = trade_df[trade_df['is_buy'] == True].groupby('submit_date').sum()[['amount']].join(fund_mv).copy().reset_index()
        turnover_df['trade_date'] = turnover_df['submit_date'].map(lambda x : submit_date_to_trade_day[x])
        turnover_df = turnover_df[['amount','mv','trade_date']].set_index('trade_date')
        _rb_df['trade_date'] = _rb_df['datetime'].map(lambda x : submit_date_to_trade_day[x])
        _rb_df['rebalance reason'] = _rb_df['rebalance_reason'].map(lambda x : x[0]['rebalanace_reason'])
        _res = []
        for dic in _rb_df['rebalance_reason']:
            dic = dic[0]
            strs = [ f'{v} ' for k , v in dic.items() if k is not 'rebalanace_reason']
            strs = ''.join(strs)
            _res.append(strs)
        _rb_df['rebalance_detail'] = _res
        _rb_df = _rb_df[['trade_date','rebalance reason','rebalance_detail']].set_index('trade_date').copy()
        turnover_df['turnover'] = turnover_df['amount'] / turnover_df['mv']
        _df = pd.DataFrame([{'trade_date':d,'hold_year':l} for d,l in result['hold_years'].items()]).set_index('trade_date')
        _df.index = pd.to_datetime(_df.index)
        turnover_df = turnover_df.join(_df).join(_rb_df).copy()
        return turnover_df[['turnover','hold_year','rebalance reason','rebalance_detail']]

    def backtest_asset_plot(self):
        bt_type = 'asset'
        print(f'{bt_type} report')
        w = self.get_asset_stat()
        del w['market_value']
        pprint(w)
        AssetPainter.plot_asset_weights(self.asset_weights_history, self.saa_weight)
        HybridPainter.plot_market_value(self.asset_mv, bt_type, self.index_price, self.saa_weight, w)
        AssetPainter.plot_asset_mdd_period(self.asset_mv, self.saa_weight, self.index_price, self.asset_weights_history)
        AssetPainter.plot_asset_mdd_amount(self.asset_mv, self.index_price, self.asset_position_history)

    def backtest_fund_plot(self):
        bt_type = 'fund'
        print(f'{bt_type} report')
        w = self.get_fund_stat()
        mv = w['market_value'].copy()
        del w['market_value']
        pprint(w)
        w['market_value'] = mv
        self.get_index_fee_avg()
        #FundPainter.plot_fund_weights(self.fund_weights_history, self.fund_cash_history, self.fund_marktet_price_history, self.saa_weight)
        HybridPainter.plot_market_value_with_mdd_analysis(self.fund_mv, bt_type, self.index_price, self.saa_weight, w)
        FundPainter.plot_fund_mdd_periods(self.fund_mv, self.fund_weights_history, self.fund_nav, self.fund_info)
        FundPainter.plot_fund_mdd_amounts(self.fund_mv, self.fund_nav, self.fund_info, self.fund_position_history.copy())
        FundPainter.plot_fund_alpha(self.fund_nav, self.fund_info, self.index_price, self.fund_position_history.copy(), w)
        #FundPainter.plot_mv_on_each_asset(self.fund_nav, self.fund_info, self.index_price, self.fund_position_history.copy(), w)
        #HybridPainter.plot_asset_fund_mv_diff(self.asset_mv, self.fund_mv)
        # if not self.index_fee.empty:
        #     FundPainter.plot_index_fund_fee(self.index_fee)
        # if not self.turnover_df.empty:
        #     FundPainter.plot_fund_ret_each_year(self.turnover_df, w['mdd'], w['annual_ret'] )
        #     FundPainter.plot_turnover_rate_each_year(self.turnover_df, self.turnover_rate_yearly_avg)

    def singel_index_plot(self):
        w = self.get_fund_stat()
        HybridPainter.plot_market_value_with_mdd_analysis(self.fund_mv, 'fund', self.index_price, self.saa_weight, w)
        FundPainter.plot_fund_mdd_periods(self.fund_mv, self.fund_weights_history, self.fund_nav, self.fund_info)
        FundPainter.plot_fund_alpha(self.fund_nav, self.fund_info, self.index_price, self.fund_position_history.copy(), w)

    def asset_price_ratio(self):    
        fund_trade = self.get_fund_trade()
        return HybridPainter.plot_asset_price_ratio(self.fund_nav, self.fund_info, self.index_price, self.fund_score_dm, self.get_fund_stat(), self.dts, self.saa_weight, fund_trade, self.score_select)
        
    def plot_whole(self):
        self.backtest_fund_plot()
        self.backtest_asset_plot()
        
    def _plot_fund_score(self, asset, is_tuning):
        FundPainter.plot_fund_score(self.fund_mv, 
                                    self.fund_weights_history, 
                                    self.trade_history,
                                    self.index_price, 
                                    self.asset_weights_history,
                                    self.fund_info,
                                    self.fund_nav,
                                    self.fund_score,
                                    self.fund_score_raw,
                                    self.fund_indicator,
                                    asset,
                                    is_tuning,
                                    self.score_select,
                                    )
   
    def _index_pct_plot(self, index_id:str, saa_mv:pd.DataFrame, taa_mv:pd.DataFrame):
        pct = TaaTunerParam.POOL[index_id]
        index_pct = self.index_pct.xs(index_id, level=1, drop_level=True)[[pct]].rename(columns={pct:index_id})
        AssetPainter.plot_taa_analysis(saa_mv, taa_mv, index_id, index_pct, self.taa_params, self.index_price)
        
    def _plot_taa_saa(self, saa_mv, taa_mv, index_id):
        pct = TaaTunerParam.POOL[index_id]
        index_pct = self.index_pct.xs(index_id, level=1, drop_level=True)[[pct]].rename(columns={pct:index_id})
        AssetPainter.plot_asset_taa_saa(saa_mv, taa_mv, index_id, index_pct)
       
    def save_fund_bk_data(self, csv_title:str='check'):
        self.fund_mv.to_csv(csv_title + '_fund_mv.csv')
        self.get_fund_trade().to_csv(csv_title + '_fund_trade.csv')
        self.get_fund_position().to_csv(csv_title + '_fund_pos.csv')
        pd.DataFrame(self.asset_position_history).T.to_csv(csv_title + '_asset_pos.csv')
        if hasattr(self, 'asset_mv'):
            self.asset_mv.to_csv(csv_title + '_asset_mv.csv')
        self.get_asset_trade().to_csv(csv_title + '_asset_trade.csv')
    
    def update_rebalance_detail(self, dt, rebalance_reason, trigger_detail):
        if bool(rebalance_reason):
            self._rebalance_details.append({'datetime':dt,'rebalance_reason':rebalance_reason})
        self._rebalance_history.append({'datetime':dt,'rebalance_reason':trigger_detail})

    def plot_taa_pct_df(self, dt):
        res = []
        for index_id, pct_data in TaaTunerParam.POOL.items():
            res.append( self.pct_df.loc[index_id][['datetime',pct_data]].reset_index().pivot_table(index='datetime', columns='index_id')[pct_data])
        pct_df = pd.concat(res, axis=1, sort=True)
        df = pct_df.loc[dt:]
        HybridPainter.plot_taa_detail(df)

    @staticmethod
    def get_taa_result(index_id:str, start_date:datetime.date, end_date:datetime.date, taaParam:TAAParam, dm:FundDataManager):
        taa_helper = TAAHelper(taa_params=taaParam)
        _dts = dm.get_trading_days()
        dts = _dts[(_dts.datetime >= start_date) & (_dts.datetime <= end_date)].datetime 
        fake_weight = AssetWeight(**{index_id:1})
        for dt in dts:
            asset_pct = dm.get_index_pcts_df(dt)
            taa_helper.on_price(dt=dt, asset_price=None, cur_saa=fake_weight, asset_pct=asset_pct, select_val={},score_dict={})
        df = pd.DataFrame(taa_helper.tactic_history).T.dropna()
        df['last_date'] = df.index.to_series().shift(1)
        con = df[index_id] != df[index_id].shift(1)
        df_diff_part = df[con].copy()
        df_diff_part = df_diff_part.reset_index().rename(columns={'index':'begin_date'})
        next_date = df_diff_part['last_date'].shift(-1).tolist()
        next_date[-1] = df.index.values[-1]
        df_diff_part['end_date'] = next_date
        df_result = df_diff_part[df_diff_part[index_id] != TAAStatusMode.NORMAL][['begin_date','end_date',index_id]]
        df_result = df_result.rename(columns = {index_id:'status'})
        return df_result.to_dict('records') 

    def get_date_score(self, datetime:datetime.date):
        fund_score = self.fund_score[datetime]
        fund_score_raw = self.fund_score_raw[datetime]
        desc_name_dic = self.fund_info[['fund_id','desc_name']].set_index('fund_id').to_dict()['desc_name']
        res = []
        for index_id, score_dic in fund_score.items():
            for fund_id, fund_s in score_dic.items():
                dic = {
                    'index_id' : index_id,
                    'fund_id': fund_id,
                    'desc_name':desc_name_dic[fund_id],
                    'score':fund_s,
                    'raw_score':fund_score_raw[index_id][fund_id],
                }
                res.append(dic)
        return pd.DataFrame(res).sort_values(['index_id','score'],ascending=[True,False]).set_index('index_id')

    def get_mdd_recover_stats(self):
        fund_mv = pd.DataFrame([ {'date':k, 'mv':v} for k,v in self.fund_marktet_price_history.items()]).set_index('date')
        res = Calculator.get_mdd_recover_result(fund_mv)
        return res

    def get_mdd_stats(self):
        fund_mv = pd.DataFrame([ {'date':k, 'mv':v} for k,v in self.fund_marktet_price_history.items()]).set_index('date')
        res = Calculator.get_mdd_result(fund_mv)
        return res

    @staticmethod
    def plot_fund_score(fund_id:str='200002!0',begin_date:datetime.date=datetime.date(2015,1,1),dm:FundDataManager=None):
        FundPainter.plot_fund_rank(score_dic=dm._score_manager.score_cache,
                                   fund_info=dm.dts.fund_info,
                                   fund_id=fund_id,
                                   begin_date=begin_date,
                                   fund_index_map=dm.dts.fund_index_map)

    @staticmethod
    def indicator_score_d(begin_d:datetime.date, fund_list:list, direction:str, m:FundDataManager):
        indicator_1 = m.dts.fund_indicator[(m.dts.fund_indicator.fund_id.isin(fund_list)) &
                            (m.dts.fund_indicator.datetime == begin_d)]
        indicator_1 = indicator_1[['fund_id','alpha','beta','track_err','fee_rate','index_id']].rename(columns={'alpha':f'{direction}_alpha',
                                                                                                            'beta':f'{direction}_beta',
                                                                                                            'track_err':f'{direction}_track_err'})
        indicator_1 = indicator_1.set_index('fund_id')
        score_day_dic = m._score_manager.score_cache[begin_d]
        fund_ranks = {}
        for index_id, score_dic in score_day_dic.items():
            _rank = sorted(score_dic.items(), key=lambda x:x[1], reverse=True)
            fund_rank = [i[0] for i in _rank]
            fund_ranks[index_id] = fund_rank
        rank_result = []
        for r in indicator_1.itertuples():
            try:
                rank_result.append(fund_ranks[r.index_id].index(r.Index) + 1)   
            except:
                rank_result.append(10000)
        indicator_1.loc[:,f'{direction}_rank'] = rank_result
        return indicator_1
     
    @staticmethod
    def fund_trade_result(_bk_class,_bk_result,m):
        _dts = m.dts.trading_days.datetime.tolist()
        rebalance_date = _bk_result['rebalance_date']
        begin_date = rebalance_date[0]
        mv_df = _bk_result['market_value']
        rebalance_list = [begin_date] + [i for i in rebalance_date if i > begin_date] + [mv_df.index[-1]]
        fund_info_dic = m.dts.fund_info[['fund_id','desc_name']].set_index('fund_id').to_dict()['desc_name']
        df_list = []
        for i in range(len(rebalance_list)-1):
            begin_d = rebalance_list[i]
            end_d = rebalance_list[i+1]
            score_day_1 = _dts[_dts.index(begin_d) -1]
            score_day_2 = _dts[_dts.index(end_d) -1]
            pos_dic = _bk_class._report_helper.fund_position_history[begin_d]
            res = []
            for fund_id, fund_pos_i in pos_dic.items():
                if fund_pos_i['volume'] > 1:
                    res.append({
                        'fund_id':fund_pos_i['fund_id'],
                        'volume':fund_pos_i['volume'],
                        'price1':fund_pos_i['price'],
                        'index_id':fund_pos_i['index_id'],
                    })
            pos_i_df = pd.DataFrame(res)
            pos_i_df.loc[:,'price2'] = pos_i_df['fund_id'].map(lambda x : m.dts.fund_nav.loc[end_d,x])
            pos_i_df['amount'] = pos_i_df['volume'] * pos_i_df['price1']
            pos_i_df['weight'] = pos_i_df['amount'] / pos_i_df['amount'].sum()
            pos_i_df.loc[:,'desc_name'] = pos_i_df['fund_id'].map(lambda x: fund_info_dic[x])
            pos_i_df['fund_ret_rate'] = (pos_i_df['price2'] / pos_i_df['price1']) - 1
            pos_i_df['fund_return'] = pos_i_df['fund_ret_rate'] * pos_i_df['weight'] 
            pos_i_df_show = pos_i_df[['fund_id','desc_name','index_id','weight','fund_ret_rate','fund_return']]
            pos_i_df_show = pos_i_df_show.sort_values('fund_return', ascending=False)
            fund_list = pos_i_df_show.fund_id.tolist()
            pos_i_df_show = pos_i_df_show.set_index('fund_id')
            indicator_1 = ReportHelper.indicator_score_d(score_day_1, fund_list, 'buy', m)
            indicator_2 = ReportHelper.indicator_score_d(score_day_2, fund_list, 'sell', m)
            pos_i_df_show = pos_i_df_show.join(indicator_1[['buy_alpha','buy_beta','buy_track_err','fee_rate','buy_rank']]).join(indicator_2[['sell_alpha','sell_beta','sell_track_err','sell_rank']])
            pos_i_df_show = pos_i_df_show.reset_index()
            pos_i_df_show.index.name = f'{begin_d}~{end_d}'
            pos_i_df_show.loc[:,'buy_signal_date'] = begin_d
            pos_i_df_show.loc[:,'sell_signal_date'] = end_d
            df_list.append(pos_i_df_show)
        return pd.concat(df_list)

    @staticmethod
    def recent_week_return(pos_df,fund_result,weight_df,saa,mv_df,m,benchmark,end_date=None,begin_date=None,port_id='',fund_info=None):
        # 把买卖交易费平滑打入净值中
        def _index_price_ratio_item(index_ratio_res, d1, d2, is_buy_fee, is_sell_fee):
            _index_ratio_res = []
            for index_id, fund_list in index_ratio_res.items():
                _nav = m.dts.fund_nav[fund_list].loc[d1:d2]
                if is_buy_fee:
                    for fund_id in _nav:
                        fund_i_fee = buy_dic.get(fund_id,0)
                        fee_discount_l = np.linspace(1,1-fund_i_fee,_nav.shape[0])
                        _nav[fund_id] = _nav[fund_id] * fee_discount_l
                if is_sell_fee:
                    for fund_id in _nav:
                        fund_i_fee = sell_dic.get(fund_id,0)
                        fee_discount_l = np.linspace(1,1-fund_i_fee,_nav.shape[0])
                        _nav[fund_id] = _nav[fund_id] * fee_discount_l
                _nav['index_price'] = m.dts.index_price.loc[d1:d2,index_id]
                _nav = _nav/_nav.iloc[0]
                _nav['mean'] = _nav.mean(axis=1)
                _nav.loc[:,index_id] = _nav['mean'] / _nav['index_price']
                _index_ratio_res.append(_nav[[index_id]].copy())   
            res_df = pd.concat(_index_ratio_res, sort=True, axis=1)
            return res_df

        def _ret_item(begin_date, today, is_buy_fee, is_sell_fee):
            _fund_list = list(weight_df[begin_date].keys())
            _nav = m.dts.fund_nav[_fund_list].loc[begin_date:today]
            fund_ret = _nav.iloc[-1] / _nav.iloc[0] - 1
            ret_df = pd.DataFrame(fund_ret).rename(columns={0:'ret'})
            res = []
            for k,w in weight_df[begin_date].items():
                res.append({'fund_id':k,'weight':w})
            _weight_df = pd.DataFrame(res).set_index('fund_id')
            res_df = ret_df.join(_weight_df)
            res_df.loc[:,'rets'] = res_df['ret'] * res_df['weight']
            res_df.loc[:,'begin_date'] = begin_date
            res_df.loc[:,'end_date'] = today
            return res_df

        buy_dic = (fund_info[['fund_id','purchase_fee']].set_index('fund_id') * 0.15).to_dict()['purchase_fee']
        sell_dic = fund_info[['fund_id','redeem_fee']].set_index('fund_id').to_dict()['redeem_fee']
        index_price = m.dts.index_price
        if end_date is None:
            today = datetime.date.today()
        else:
            today = end_date
        if begin_date is None:
            begin_date =  today - datetime.timedelta(days=today.weekday())
        trading_days = sorted(list(set(m.dts.trading_days.datetime) & set(mv_df.index)))
        mv_df = mv_df.loc[begin_date:].reindex(trading_days)
        stats = Calculator.get_stat_result_from_df(df=mv_df.dropna().reset_index(), date_column='date', value_column='mv')
        annual_ret= round(stats.annualized_ret,3)
        mdd = round(stats.mdd,4)
        df_plot_i = mv_df.join(m.dts.index_price[[benchmark]]).loc[begin_date:today]
        df_plot_i = df_plot_i / df_plot_i.iloc[0]
        total_ret = int((stats.last_unit_nav - 1) * 10000)
        st = f'check period annual ret : {annual_ret} mdd : {mdd} total_ret {total_ret} bp'
        FundPainter.plot_recent_ret(df_plot_i,begin_date,today,st,port_id)
        _index_list = []
        for asset, w in saa.__dict__.items():
            if w > 0 and asset != 'cash':
                _index_list.append(asset)
        _index_price = index_price.loc[begin_date:today]
        _index_price = _index_price / _index_price.iloc[0]
        AssetPainter.plot_index_price_ratio(_index_price,'index_price')
        
        if begin_date >= fund_result['rebalance_date'][-1]:
            res_df = _ret_item(begin_date,today, False, False)
        else:
            date_list = [[begin_date,fund_result['rebalance_date'][-1]],[fund_result['rebalance_date'][-1],today]]
            _res_dt_df = []
            for idx,dl in enumerate(date_list):
                b1 = dl[0]
                b2 = dl[1]
                _res_dt_df.append(_ret_item(b1, b2, False, False))
            res_df = pd.concat(_res_dt_df, axis=0, sort=True)
        #res_df.loc[:,'rets'] = res_df['ret'] * res_df['weight']
        res_df = res_df.sort_values('rets',ascending=False)
        res_df.loc[:,'rets'] = [str(int(i*10000))+'BP' for i in res_df.loc[:,'rets']]
        desc_dic = fund_info[['fund_id','desc_name']].set_index('fund_id').to_dict()['desc_name']
        index_dic = fund_info[['fund_id','index_id']].set_index('fund_id').to_dict()['index_id']
        res_df['desc_name'] = res_df.index.map(lambda x : desc_dic[x])
        res_df['index_id'] = res_df.index.map(lambda x : index_dic[x])        
        if begin_date > fund_result['rebalance_date'][-1]:
            d1 = begin_date
            d2 = today
            index_ratio_res = {}
            _fund_list = list(weight_df[begin_date].keys())
            for fund_id in _fund_list:
                _index_id = index_dic[fund_id]
                if _index_id not in index_ratio_res:
                    index_ratio_res[_index_id] = [fund_id]
                else:
                    index_ratio_res[_index_id].append(fund_id)
            res_index_df = _index_price_ratio_item(index_ratio_res, d1, d2, False, False)
        else:
            date_list = [[begin_date,fund_result['rebalance_date'][-1]],[fund_result['rebalance_date'][-1],today]]
            _res_df = []
            for idx,dl in enumerate(date_list):
                b1 = dl[0]
                b2 = dl[1]
                _res = {}
                for fund_id, fund_pos_i in pos_df[b1].items():
                    if fund_pos_i['volume'] > 1:
                        if fund_pos_i['index_id'] not in _res:
                            _res[fund_pos_i['index_id']] = [fund_pos_i['fund_id']]
                        else:
                            _res[fund_pos_i['index_id']].append(fund_pos_i['fund_id'])
                if idx == 0:
                    _df = _index_price_ratio_item(_res, b1, b2, False, True)
                elif idx == 1:
                    _df = _index_price_ratio_item(_res, b1, b2, True, False)
                _res_df.append(_df)
            df_1 = _res_df[0]
            df_2 = _res_df[1]
            df_2 = df_1.iloc[-1] * df_2
            res_index_df = df_1.iloc[:-1].append(df_2, sort=True)
        AssetPainter.plot_index_price_ratio(res_index_df.dropna(),'price_ratio')
        res_df = res_df.rename(columns={'ret':'fund_ret'})
        res_df['fund_ret'] = res_df.fund_ret.map(lambda x: str(round(x*100,2)) +'%')
        res_df['weight'] = res_df.weight.map(lambda x: str(round(x*100,2)) +'%')
        return res_df[['begin_date','end_date','desc_name','index_id','fund_ret','weight','rets']]

    @staticmethod
    def rolling_analysis(rolling_year, index_id, m, mv_df, fund_annual_ret, ret_list=[]):
        if '沪深300' in mv_df:
            mv_df = mv_df.drop('沪深300', axis=1)
        mv_df = mv_df.join(m.dts.index_price[[index_id]])
        mv_df = mv_df / mv_df.shift(1)
        annual_ret = (mv_df.rolling(window=242*rolling_year).agg(lambda x : x.prod() - 1))/rolling_year
        FundPainter.plot_rolling_analysis(annual_ret,fund_annual_ret,rolling_year,index_id,ret_list)
     
    @staticmethod
    def regular_rebalance_in_index_strategy(m, begin_date,end_date,index_id,rebalance_year,top_funds):
        dts = m.dts.trading_days.datetime
        fund_score_dic = m._score_manager.score_cache
        fund_info = m.dts.fund_info
        index_price = m.dts.index_price
        fund_nav = m.dts.fund_nav
        result_df, pos_df = HybridPainter.regular_rebalance_in_index_strategy(begin_date,end_date,index_id,rebalance_year,top_funds,dts,fund_score_dic,fund_info,index_price,fund_nav)
        return result_df, pos_df

    @staticmethod
    def mining_fac_importances(m,start_date,end_date,index_id,top_num,wind_class_2):
        '''
        index_id = 'csi500'
        start_date = datetime.date(2020,1,1)
        end_date = datetime.date(2020,8,10)
        top_num = 5
        wind_class_2 = ['被动指数型基金']
        ReportHelper.mining_fac_importances(m,start_date,end_date,index_id,top_num,wind_class_2)
        '''
        _dts = m.dts.trading_days.datetime
        _dts = _dts[(_dts >= start_date) & (_dts <= end_date)]
        _start_date = _dts.iloc[0]
        _end_date = _dts.iloc[-1]
        fund_info = m.dts.fund_info
        _fund_list = fund_info[(fund_info['index_id'] == index_id) & fund_info['wind_class_2'].isin(wind_class_2)].fund_id.tolist()
        _index_fund_pack = m.dts.index_fund_indicator_pack.loc[index_id].loc[_start_date:_end_date]
        _dts = _index_fund_pack.index.get_level_values(0).tolist()
        _col1 = m.dts.fund_nav.columns.tolist()
        fl = [i for i in _fund_list if i in _col1]
        _fund_nav = m.dts.fund_nav[fl].loc[_start_date:_end_date].dropna(axis=1)
        top_funds = (_fund_nav.iloc[-1] / _fund_nav.iloc[0]).sort_values(ascending=False).index.tolist()
        indicator_existed_fund = _index_fund_pack.loc[_start_date].index.tolist()
        top_funds = [i for i in top_funds if i in indicator_existed_fund][:top_num]
        cur_d = _index_fund_pack.loc[_start_date]
        cur_d_sta = cur_d.apply(lambda x: (x - x.mean() + 1e-6)/ (x.std() + 1e-6), axis=0)
        cur_d_sta['beta'] = cur_d['beta']
        cur_d_sta['year_length'] = cur_d['year_length']
        cur_d = cur_d_sta
        return pd.DataFrame(cur_d.rank(pct=True).loc[top_funds].mean(axis=0)).rename(columns={0:'rank'}).sort_values('rank',ascending=False)