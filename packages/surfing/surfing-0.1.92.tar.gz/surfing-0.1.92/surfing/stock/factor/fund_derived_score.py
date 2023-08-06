from .fund_derived_factors import *
from ..fund.derived.derived_data_helper import normalize, score_rescale

class ScoreDataPrepare():

    def fund_score_data_prepare(self):
        dt = datetime.date(2012,1,1)
        self.fund_manager_info = FundManagerInfo().get()
        self.factor_alive = FundAlive().get().loc[dt:]
        self.fund_pool = FilteredFundInfoWhole().get().fund_id.tolist()
        self.factor_list = [    'AnnualRetDailyHistory', 
                                'TotalRetDailyHistory',
                                'MddDailyHistory',
                                'AnnualVolDailyHistory',
                                'DownsideStdDailyHistory',
                                'TradeYear',
                                'ContinueRegValue',
                                'FundSizeCombine',
                                'FundClAlphaHistoryWeekly',
                                'FundClBetaHistoryWeekly',
                                'FundPersonalHold',
                                'RecentMonthRet',
                            ]
        result = []
        for fac_name in self.factor_list:
            fac = eval(fac_name)().get()
            fac = fac[fac.index > dt]
            fac = fac[fac.columns.intersection(self.fund_pool)]
            columns = fac.columns.tolist()
            fac = pd.DataFrame(fac[columns].values * self.factor_alive[columns].values, columns=columns, index=self.factor_alive.index)
            fac.columns = pd.MultiIndex.from_product([[fac_name], fac.columns])
            result.append(fac)
            del fac
            del eval(fac_name)._instances[eval(fac_name)]
        self._factor = pd.concat(result, axis=1).stack()
        self._factor = self._factor.reset_index().dropna(subset=self.factor_list, how='all')
    
    def fund_score_data_prepare_2(self): 
        #self.fund_score = None
        self.fund_score = pd.read_csv('score_df.csv',index_col=0)
        self.fund_score = self.fund_score.drop(columns=['index'], errors='ignore').rename(columns={'level_1':'fund_id'})
        self.fund_score = self.fund_score.set_index('datetime')
        
        self.fund_info = FundInfo().get()
        self.manager_info = FundManagerInfo().get().set_index('mng_id')
        self.mng_score = MngScoreV1().get()
        self.mng_score['mng_id'] = self.mng_score.mng_id.map(lambda x : x[x.find('_', 0) + 1 :])
        self.mng_score = self.mng_score.set_index(['datetime','fund_type'])
        self.mng_score = self.mng_score.sort_index()
        self.mng_score = self.mng_score.rename(columns={'total_score':'mng_score'})
        self.fund_type = ['stock','bond','index','QDII','mmf']
        self.wind_class_type = self.fund_info.set_index('fund_id')['wind_class_2']

    def fund_score_data_append(self):
        self.fund_score.loc[:,'fund_type'] = self.fund_score.fund_id.map(lambda x : self.WIND_TYPE_DICT[self.wind_class_type[x]])
        date_list = sorted(self.fund_score.index.unique().tolist())
        res = []
        lens_dt = len(date_list)
        _t0 = time.time()
        for dt in date_list:
            df_dt = self.fund_score.loc[dt].set_index('fund_type').copy()
            mng_dic = self.manager_info[(self.manager_info.end_date >= dt)
                                      & (self.manager_info.start_date <= dt)]['fund_id']
            for fund_type in self.fund_type:
                df_dt_fund_type = df_dt.loc[fund_type]
                _mng_score = self.mng_score.loc[dt,fund_type][['mng_id','mng_score']]
                _mng_score = _mng_score.join(mng_dic,on='mng_id')
                _mng_score = _mng_score.groupby('fund_id').max()
                df_dt_fund_type = df_dt_fund_type.join(_mng_score[['mng_score']], on='fund_id')
                res.append(df_dt_fund_type)
            dt_idx = date_list.index(dt)
            if dt_idx % 100 == 0:
                _t1 = time.time()
                print(f' dt {dt} idx {dt_idx} total {lens_dt} cost {round(_t1 - _t0)}')
                _t0 = time.time()
        self._factor = pd.concat(res, axis=0)

    def fund_score_data_prepare_v2(self):
        dt = datetime.date(2012,1,1)
        self.fund_manager_info = FundManagerInfo().get()
        self.factor_alive = FundAlive().get().loc[dt:]
        self.fund_pool = FilteredFundInfoWhole().get().fund_id.tolist()
        self.factor_list = ['AlphaDaily1yI',
                            'AlphaDaily3yI',
                            'TradeYear',
                            'FundSizeCombine',
                            'FundClAlpha1YWeekly',
                            'FundClBeta1YWeekly']
        result = []
        for fac_name in self.factor_list:
            fac = eval(fac_name)().get()
            fac = fac[fac.index > dt]
            fac = fac[fac.columns.intersection(self.fund_pool)]
            columns = fac.columns.tolist()
            fac = pd.DataFrame(fac[columns].values * self.factor_alive[columns].values, columns=columns, index=self.factor_alive.index)
            fac.columns = pd.MultiIndex.from_product([[fac_name], fac.columns])
            result.append(fac)
            del fac
            del eval(fac_name)._instances[eval(fac_name)]
        self.fund_score = pd.concat(result, axis=1).stack()
        self.fund_score = self.fund_score.reset_index().dropna(subset=self.factor_list, how='all')
    
    def fund_score_data_prepare_2_v2(self): 
        self.fund_score = self.fund_score.drop(columns=['index'], errors='ignore').rename(columns={'level_1':'fund_id'})
        self.fund_score = self.fund_score.set_index('datetime')
        self.fund_info = FundInfo().get()
        self.manager_info = FundManagerInfo().get().set_index('mng_id')
        self.mng_score = MngScoreV2().get()
        self.mng_score['mng_id'] = self.mng_score.mng_id.map(lambda x : x[x.find('_', 0) + 1 :])
        self.mng_score = self.mng_score.set_index(['datetime','fund_type'])
        self.mng_score = self.mng_score.rename(columns={'total_score':'mng_score'})
        self.mng_score = self.mng_score.sort_index()
        self.fund_type = ['stock','bond','index','QDII']
        self.wind_class_type = self.fund_info.set_index('fund_id')['wind_class_2']

    def manager_score_data_prepare(self):
        dt = datetime.date(2012,1,1)
        self.factor_list = [    'MngAnnualRetDailyHistory', 
                                'MngTotalRetDailyHistory',
                                'MngMddDailyHistory',
                                'MngAnnualVolDailyHistory',
                                'MngDownsideStdDailyHistory',
                                'MngFundTypeTradingDays',
                                'MngFundSize',
                                'MngClAlphaWeeklyHistory',
                                'MngClBetaWeeklyHistory',
                            ]
        result = []
        for fac_name in self.factor_list:
            fac = eval(fac_name)().get()
            fac = fac[fac.index > dt]
            fac.columns = pd.MultiIndex.from_product([[fac_name], fac.columns])
            result.append(fac)
            del fac
            del eval(fac_name)._instances[eval(fac_name)]
        self._factor = pd.concat(result, axis=1).stack()
        self._factor = self._factor.reset_index().dropna(subset=self.factor_list, how='all')
        self._factor.loc[:,'fund_type'] = self._factor.mng_id.map(lambda x: x.split('_')[0])
        self._factor = self._factor.set_index(['datetime','fund_type'])
        self.fund_type = ['stock','bond','index','QDII','mmf']
        
    def manager_score_data_prepare_v2(self):
        dt = datetime.date(2012,1,1)
        self.factor_list = ['MngAnnualRetDaily1Y',
                            'MngAnnualRetDaily3Y',
                            'MngFundTypeTradingDays',
                            'MngClAlphaWeekly1Y',
                            'MngClBetaWeekly1Y',
                            'MngFundSize']
        result = []
        for fac_name in self.factor_list:
            fac = eval(fac_name)().get()
            fac = fac[fac.index > dt]
            fac.columns = pd.MultiIndex.from_product([[fac_name], fac.columns])
            result.append(fac)
            del fac
            del eval(fac_name)._instances[eval(fac_name)]
        self._factor = pd.concat(result, axis=1).stack()
        self._factor = self._factor.reset_index().dropna(subset=self.factor_list, how='all').rename(columns={'level_1':'mng_id'})
        self._factor.loc[:,'fund_type'] = self._factor.mng_id.map(lambda x: x.split('_')[0])
        self._factor = self._factor.set_index(['datetime','fund_type'])
        self.fund_type = ['stock','bond','index','QDII','mmf']

class MngScoreV1(Factor, ScoreDataPrepare):
    # 雷达图基金评价 历史业绩为重

    def __init__(self):
        super().__init__(f_name='MngScoreV1', f_type=FundFactorType.DERIVED, f_level='score')

    def calc_mng(self, df, fund_type):
        if fund_type == 'stock':
            return self.score_mng_stock(df)
        if fund_type == 'bond':
            return self.score_mng_bond(df)
        if fund_type == 'index':
            return self.score_mng_index(df)
        if fund_type == 'QDII':
            return self.score_mng_qdii(df)
        if fund_type == 'mmf':
            return self.score_mng_mmf(df)
        
    def score_mng_stock(self, df):
        df.loc[:,'mng_ret_ability'] = score_rescale(0.4*score_rescale(df['MngAnnualRetDailyHistory']) +0.6*score_rescale(df['MngTotalRetDailyHistory']))
        df.loc[:,'mng_risk_ability'] = score_rescale(0.3 * score_rescale(-df['MngMddDailyHistory']) + 0.4 * score_rescale(-df['MngAnnualVolDailyHistory']) + 0.3 * score_rescale(-df['MngDownsideStdDailyHistory']))
        df.loc[:,'mng_select_time'] =  score_rescale(normalize(df['MngClAlphaWeeklyHistory']))
        df.loc[:,'mng_select_stock'] = score_rescale(normalize(df['MngClBetaWeeklyHistory']) )
        df.loc[:,'mng_experience'] = score_rescale( 0.8 *  score_rescale(df['MngFundTypeTradingDays']) + 0.2 * score_rescale(df['MngFundSize']))
        df.loc[:,'mng_score'] = score_rescale(df.loc[:,'mng_ret_ability'] + df.loc[:,'mng_risk_ability'] + df.loc[:,'mng_select_time'] + df.loc[:,'mng_select_stock'] + 1.5 * df.loc[:,'mng_experience'])
        return df[['mng_id','mng_ret_ability','mng_risk_ability','mng_select_time','mng_select_stock','mng_experience','mng_score']]

    def score_mng_bond(self, df):
        df.loc[:,'mng_ret_ability'] = score_rescale( 0.8 * score_rescale(df['MngAnnualRetDailyHistory']) + 0.2 * score_rescale(df['MngTotalRetDailyHistory']))
        df.loc[:,'mng_risk_ability'] = score_rescale(0.1 * score_rescale(-df['MngMddDailyHistory']) + 0.4 * score_rescale(-df['MngAnnualVolDailyHistory']) + 0.5 * score_rescale(-df['MngDownsideStdDailyHistory']))
        df.loc[:,'mng_select_time'] =  score_rescale(normalize(df['MngClAlphaWeeklyHistory']))
        df.loc[:,'mng_select_stock'] = score_rescale(normalize(df['MngClBetaWeeklyHistory']))
        df.loc[:,'mng_experience'] = score_rescale( 0.8 *  score_rescale(df['MngFundTypeTradingDays']) + 0.2 * score_rescale(df['MngFundSize']))
        df.loc[:,'mng_score'] = score_rescale(1.2 * df.loc[:,'mng_ret_ability'] +  df.loc[:,'mng_risk_ability'] + df.loc[:,'mng_select_time'] + df.loc[:,'mng_select_stock'] + 1.5 * df.loc[:,'mng_experience'])
        return df[['mng_id','mng_ret_ability','mng_risk_ability','mng_select_time','mng_select_stock','mng_experience','mng_score']]

    def score_mng_index(self, df):
        df.loc[:,'mng_ret_ability'] = score_rescale( 0.4 * score_rescale(df['MngAnnualRetDailyHistory']) + 0.6 * score_rescale(df['MngTotalRetDailyHistory']))
        df.loc[:,'mng_risk_ability'] = score_rescale(0.3 * score_rescale(-df['MngMddDailyHistory']) + 0.4 * score_rescale(-df['MngAnnualVolDailyHistory']) + 0.3 * score_rescale(-df['MngDownsideStdDailyHistory']))
        df.loc[:,'mng_experience'] = score_rescale( 0.4 *  score_rescale(df['MngFundTypeTradingDays']) + 0.6 * score_rescale(df['MngFundSize']))
        df.loc[:,'mng_score'] = score_rescale(df.loc[:,'mng_ret_ability'] + df.loc[:,'mng_risk_ability'] + 2 * df.loc[:,'mng_experience'] )
        return df[['mng_id','mng_ret_ability','mng_risk_ability','mng_experience','mng_score']]

    def score_mng_qdii(self, df):
        df.loc[:,'mng_ret_ability'] = score_rescale( 0.4 * score_rescale(df['MngAnnualRetDailyHistory']) + 0.6 * score_rescale(df['MngTotalRetDailyHistory']))
        df.loc[:,'mng_risk_ability'] = score_rescale(0.3 * score_rescale(-df['MngMddDailyHistory']) + 0.4 * score_rescale(-df['MngAnnualVolDailyHistory']) + 0.3 * score_rescale(-df['MngDownsideStdDailyHistory']))
        df.loc[:,'mng_experience'] = score_rescale( 0.8 *  score_rescale(df['MngFundTypeTradingDays']) + 0.2 * score_rescale(df['MngFundSize']))
        df.loc[:,'mng_score'] = score_rescale(df.loc[:,'mng_ret_ability'] + df.loc[:,'mng_risk_ability'] + 1.5 * df.loc[:,'mng_experience'])
        return df[['mng_id','mng_ret_ability','mng_risk_ability','mng_experience','mng_score']]

    def score_mng_mmf(self, df):
        df.loc[:,'mng_ret_ability'] = score_rescale(normalize(df['MngAnnualRetDailyHistory']))
        df.loc[:,'mng_experience'] = score_rescale( 0.8 *  score_rescale(df['MngFundTypeTradingDays']) + 0.2 * score_rescale(df['MngFundSize']))
        df.loc[:,'mng_score'] = score_rescale(df.loc[:,'mng_ret_ability'] + df.loc[:,'mng_experience'])
        return df[['mng_id','mng_ret_ability','mng_experience','mng_score']]

    def calc(self):
        #self.manager_score_data_prepare()
        date_list = sorted(self._factor.index.get_level_values(0).unique().tolist())
        result = []
        _t0 = time.time()
        for dt in date_list:
            #df_dt = self._factor.loc[dt]
            for fund_type in self.fund_type:
                df_i = self._factor.loc[dt,fund_type].copy()
                df_i = self.calc_mng(df_i, fund_type)
                result.append(df_i)
            dt_idx = date_list.index(dt)
            if dt_idx % 100 == 0:
                print(f'dt {dt} idx {dt_idx}')

        _t1 = time.time()
        print(_t1 - _t0)
        self._factor = pd.concat(result).dropna(subset=['mng_score'])
        self._factor = self._factor.reset_index()

class MngScoreV2(Factor, ScoreDataPrepare):
    
    def __init__(self):
        super().__init__(f_name='MngScoreV2', f_type=FundFactorType.DERIVED, f_level='score')

    def calc_mng(self, df, fund_type, dt):
        df = self.process_score(df)
        df = self.score_mng(df)
        df.loc[:,'fund_type'] = fund_type
        df.loc[:,'datetime'] = dt
        return df

    def score_mng(self, df):
        df.loc[:,'mng_score'] = self.score_rescale(0.3*df.MngAnnualRetDaily1Y+0.3*df.MngAnnualRetDaily3Y+0.1*df.MngClAlphaWeekly1Y+0.1*df.MngClBetaWeekly1Y+0.15*df.MngFundSize+0.15*df.MngFundTypeTradingDays)
        return df

    def score_rescale(self, df):
        return df.rank(pct=True) * 100

    def process_score(self, df):
        df = df.reset_index().set_index('mng_id').drop(columns=['datetime','fund_type'])
        return df.rank(pct=True) * 100
    
    def calc(self):
        self.manager_score_data_prepare_v2()
        date_list = sorted(self._factor.index.get_level_values(0).unique().tolist())
        result = []
        _t0 = time.time()
        for dt in date_list:
            #df_dt = self._factor.loc[dt]
            for fund_type in self.fund_type:
                df_i = self._factor.loc[dt,fund_type].copy()
                df_i = self.calc_mng(df_i, fund_type, dt)
                result.append(df_i)
            dt_idx = date_list.index(dt)
            if dt_idx % 100 == 0:
                print(f'dt {dt} idx {dt_idx}')

        _t1 = time.time()
        print(_t1 - _t0)
        self._factor = pd.concat(result).dropna(subset=['mng_score'])
        self._factor = self._factor.reset_index()
        
class FundScoreV1(Factor, ScoreDataPrepare):

    def __init__(self):
        super().__init__(f_name='FundScoreV1', f_type=FundFactorType.DERIVED, f_level='score')

    def calc_fund(self, df, fund_type, dt):
        df = self.process_score(df)
        if fund_type == 'stock':
            df = self.score_fund_stock(df)
        if fund_type == 'bond':
            df = self.score_fund_bond(df)
        if fund_type == 'index':
            df = self.score_fund_index(df)
        if fund_type == 'QDII':
            df = self.score_fund_qdii(df)
        if fund_type == 'mmf':
            df = self.score_fund_mmf(df)
        df.loc[:,'fund_type'] = fund_type
        df.loc[:,'datetime'] = dt
        return df

    def score_rescale(self, df):
        return df.rank(pct=True) * 100

    def process_score(self, df):
        df = df.reset_index().set_index('fund_id').drop(columns=['datetime','fund_type'])
        return df.rank(pct=True) * 100

    def score_fund_stock(self, df):
        ret_ability = self.score_rescale(0.4 * df.AnnualRetDailyHistory + 0.6 * df.TotalRetDailyHistory)
        risk_ability = self.score_rescale(0.3 * -df.MddDailyHistory + 0.4 * -df.AnnualVolDailyHistory + 0.3 * -df.DownsideStdDailyHistory)
        stable_ability = self.score_rescale(0.4 * df.TradeYear + 0.4 * df.ContinueRegValue + 0.2 * df.FundSizeCombine)
        select_time = df.FundClBetaHistoryWeekly
        select_stock = df.FundClAlphaHistoryWeekly
        #df['mng_score'] = df.mng_score
        df.loc[:,'fund_score'] = self.score_rescale(ret_ability + risk_ability + stable_ability + select_time + select_stock)
        df.loc[:,'total_score'] = self.score_rescale(5/6 * df.fund_score + 1/6 * df.mng_score)
        return df[['fund_score','mng_score','total_score']]

    def score_fund_bond(self, df):
        ret_ability = self.score_rescale(0.8 * df.AnnualRetDailyHistory + 0.2 * df.TotalRetDailyHistory)
        risk_ability = self.score_rescale(0.3 * -df.MddDailyHistory + 0.4 * -df.AnnualVolDailyHistory + 0.3 * -df.DownsideStdDailyHistory)
        stable_ability = self.score_rescale(0.4 * df.TradeYear + 0.4 * df.ContinueRegValue + 0.2 * df.FundSizeCombine)
        select_time = df.FundClBetaHistoryWeekly
        select_stock = df.FundClAlphaHistoryWeekly
        #df['mng_score'] = df.mng_score
        df.loc[:,'fund_score'] = self.score_rescale(ret_ability + risk_ability + stable_ability + select_time + select_stock)
        df.loc[:,'total_score'] = self.score_rescale(5/6 * df.fund_score + 1/6 * df.mng_score)
        return df[['fund_score','mng_score','total_score']]

    def score_fund_index(self, df):
        ret_ability = self.score_rescale( 0.4 * df.AnnualRetDailyHistory + 0.6 * df.TotalRetDailyHistory)
        risk_ability = self.score_rescale(0.3 * -df.MddDailyHistory + 0.4 * -df.AnnualVolDailyHistory + 0.3 * -df.DownsideStdDailyHistory)
        stable_ability = self.score_rescale(0.4 * df.TradeYear + 0.4 * df.ContinueRegValue + 0.2 * df.FundSizeCombine)
        #df['mng_score'] = df.mng_score
        df.loc[:,'fund_score'] = self.score_rescale(ret_ability + risk_ability + stable_ability)
        df.loc[:,'total_score'] = self.score_rescale(3/4 * df.fund_score + 1/4 * df.mng_score)
        return df[['fund_score','mng_score','total_score']]

    def score_fund_qdii(self, df):
        ret_ability = self.score_rescale( 0.4 * df.AnnualRetDailyHistory + 0.6 * df.TotalRetDailyHistory)
        risk_ability = self.score_rescale(0.3 * -df.MddDailyHistory + 0.4 * -df.AnnualVolDailyHistory + 0.3 * -df.DownsideStdDailyHistory)
        stable_ability = self.score_rescale(0.4 * df.TradeYear + 0.4 * df.ContinueRegValue + 0.2 * df.FundSizeCombine)
        #df['mng_score'] = df.mng_score
        df.loc[:,'fund_score'] = self.score_rescale(ret_ability + risk_ability + stable_ability)
        df.loc[:,'total_score'] = self.score_rescale(3/4 * df.fund_score + 1/4 * df.mng_score)
        return df[['fund_score','mng_score','total_score']]

    def score_fund_mmf(self, df):
        ret_ability = df.RecentMonthRet
        risk_ability = self.score_rescale(df.FundPersonalHold + df.FundSizeCombine)
        df.loc[:,'fund_score'] = self.score_rescale(ret_ability + risk_ability)
        #df['mng_score'] = df.mng_score
        df.loc[:,'total_score'] = self.score_rescale(2/3 * df.fund_score + 1/3 * df.mng_score)
        return df[['fund_score','mng_score','total_score']]

    def calc(self):
        self.fund_score_data_prepare()
        self.fund_score_data_prepare_2()
        self.fund_score_data_append()
        date_list = sorted(self.fund_score.index.unique().tolist())
        res = []
        lens_dt = len(date_list)
        _t0 = time.time()
        for dt in date_list:
            df_dt = self.fund_score.loc[dt].copy()
            df_dt.loc[:,'fund_type'] = df_dt.fund_id.map(lambda x : self.WIND_TYPE_DICT[self.wind_class_type[x]])

            _end_date = pd.to_datetime(dt).date()
            mng_dic = self.manager_info[(self.manager_info.end_date >= _end_date)
                                    & (self.manager_info.start_date <= _end_date)]['fund_id']
            _res = []
            mng_score = self.mng_score.loc[dt][['mng_id','mng_score','fund_type']].set_index('fund_type')
            for fund_type in self.fund_type:
                df_dt_fund_type = df_dt[df_dt['fund_type'] == fund_type]
                _mng_score = mng_score.loc[fund_type]
                _mng_score = _mng_score.join(mng_dic,on='mng_id')
                _mng_score = _mng_score.reset_index().groupby('fund_id').max()
                df_dt_fund_type = df_dt_fund_type.join(_mng_score[['mng_score']], on='fund_id')
                _res.append(self.calc_fund(df_dt_fund_type, fund_type, dt))
            res.append(pd.concat(_res))
            dt_idx = date_list.index(dt)
            if dt_idx % 100 == 0:
                _t1 = time.time()
                print(f' dt {dt} idx {dt_idx} total {lens_dt} cost {round(_t1 - _t0)}')
                _t0 = time.time()
        self._factor = pd.concat(res)

class FundScoreV2(Factor, ScoreDataPrepare):
    
    def __init__(self):
        super().__init__(f_name='FundScoreV2', f_type=FundFactorType.DERIVED, f_level='score')

    def calc_fund(self, df, fund_type, dt):
        df = self.process_score(df)
        df = self.score_fund(df)
        df.loc[:,'fund_type'] = fund_type
        df.loc[:,'datetime'] = dt
        return df.dropna(subset=['total_score'])

    def score_rescale(self, df):
        return df.rank(pct=True) * 100

    def process_score(self, df):
        df = df.reset_index().set_index('fund_id').drop(columns=['fund_type'])
        return df.rank(pct=True) * 100

    def score_fund(self, df):
        df.loc[:,'fund_score'] = self.score_rescale(0.3*df.AlphaDaily1yI+0.3*df.AlphaDaily3yI+0.1*df.FundClAlpha1YWeekly+0.1*df.FundClBeta1YWeekly+0.15*df.FundSizeCombine+0.15*df.TradeYear)
        df.loc[:,'total_score'] = self.score_rescale(3/4 * df.fund_score + 1/4 * df.mng_score)
        return df[['fund_score','mng_score','total_score']]

    def calc(self):
        self.fund_score_data_prepare_v2()
        self.fund_score_data_prepare_2_v2()
        self.fund_score.loc[:,'fund_type'] = self.fund_score.fund_id.map(lambda x : self.WIND_TYPE_DICT[self.wind_class_type[x]])
        date_list = sorted(self.fund_score.index.unique().tolist())
        res = []
        lens_dt = len(date_list)
        _t0 = time.time()
        for dt in date_list:
            df_dt = self.fund_score.loc[dt].set_index('fund_type').copy()
            mng_dic = self.manager_info[(self.manager_info.end_date >= dt)
                                      & (self.manager_info.start_date <= dt)]['fund_id']
            for fund_type in self.fund_type:
                df_dt_fund_type = df_dt.loc[fund_type]
                _mng_score = self.mng_score.loc[dt,fund_type][['mng_id','mng_score']]
                _mng_score = _mng_score.join(mng_dic,on='mng_id')
                # delete useless
                _mng_score = _mng_score.groupby('fund_id').max()
                df_dt_fund_type = df_dt_fund_type.join(_mng_score[['mng_score']], on='fund_id')
                res.append(self.calc_fund(df_dt_fund_type, fund_type, dt))
            dt_idx = date_list.index(dt)
            if dt_idx % 100 == 0:
                _t1 = time.time()
                print(f' dt {dt} idx {dt_idx} total {lens_dt} cost {round(_t1 - _t0)}')
                _t0 = time.time()
        self._factor = pd.concat(res, axis=0)

class UpdateDerivedScoreStart:
    pass
