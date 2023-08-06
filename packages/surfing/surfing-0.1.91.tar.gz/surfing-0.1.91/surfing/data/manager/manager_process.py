import pandas as pd
from ...stock.factor.fund_derived_factors import *
from ...stock.factor.fund_derived_score import FundScoreV1, FundScoreV2

FACTOR_LIST = ['FeeRate', 'AlphaDaily3yI', 'BetaDaily3yI', 'AlphaDaily1yI', 'BetaDaily1yI', 'TrackerrDaily1yI', 'TrackerrDaily3yI', 'TradeYear']
FACTOR_LIST_ORIGIN = ['AnnualRetDailyHistory','TotalRetDailyHistory','MddDailyHistory','AnnualVolDailyHistory','DownsideStdDailyHistory','ContinueRegValue','FundSizeCombine','FundClAlphaHistoryWeekly','FundClBetaHistoryWeekly','FundPersonalHold','RecentMonthRet']
FACTOR_LIST_ADV = ['FundClAlpha1YWeekly','FundClBeta1YWeekly']

def combine_factor():
    filtered_fund_info_whole = FilteredFundInfoWhole().get()   
    fund_pool = filtered_fund_info_whole.fund_id.tolist()     
    active_fund_info_ = ActiveFundInfo().get()
    filtered_fund_info = FilteredFundInfoI().get()
    fund_index_dic = filtered_fund_info.dropna(subset=['index_id']).set_index('fund_id').to_dict()['index_id']
    fund_index_dic_active = active_fund_info_.dropna(subset=['index_id']).set_index('fund_id').to_dict()['index_id']
    fund_index_dic.update(fund_index_dic_active)
    update_factor_list = FACTOR_LIST
    factor_list = update_factor_list
    result = []
    for fac_name in factor_list:
        fac = eval(fac_name)().get()
        fac = fac[fac.columns.intersection(fund_pool)]
        fac.columns = pd.MultiIndex.from_product([[fac_name], fac.columns])
        result.append(fac)
        del fac
        del eval(fac_name)._instances[eval(fac_name)]
    df = pd.concat(result, axis=1).stack()
    df = df.reset_index().dropna(subset=FACTOR_LIST, how='any')
    df.loc[:,'index_id'] = df.fund_id.map(lambda x : fund_index_dic.get(x, None))
    df.loc[:,'active'] = (1 * ~df.fund_id.isin(filtered_fund_info.fund_id))
    return df

def combine_active():
    # 内存异常   free： per 3s
    # 9.1G  5.5G    6.3G    2.5G    0.6G    6.9G    10G
    filtered_fund_info_whole = FilteredFundInfoWhole().get()   
    fund_pool = filtered_fund_info_whole.fund_id.tolist()     
    active_fund_info_ = ActiveFundInfo().get()
    filtered_fund_info = FilteredFundInfoI().get()
    fund_score = FundScoreV1().get() #FundScoreV1 change score here
    fund_score = fund_score.set_index(['fund_id','datetime'])
    fund_index_dic = filtered_fund_info.dropna(subset=['index_id']).set_index('fund_id').to_dict()['index_id']
    fund_index_dic_active = active_fund_info_.dropna(subset=['index_id']).set_index('fund_id').to_dict()['index_id']
    fund_index_dic.update(fund_index_dic_active)
    update_factor_list = FACTOR_LIST + FACTOR_LIST_ORIGIN + FACTOR_LIST_ADV
    factor_list = update_factor_list
    result = []
    # 合并因子
    for fac_name in factor_list:
        fac = eval(fac_name)().get()
        fac = fac[fac.columns.intersection(fund_pool)]
        fac.columns = pd.MultiIndex.from_product([[fac_name], fac.columns])
        result.append(fac)
        del fac
        del eval(fac_name)._instances[eval(fac_name)]

    #score_list = ['fund_score','mng_score','total_score']
    score_list = ['mng_score']
    # 合并分数
    for fac_name in score_list:
        fac = fund_score[[fac_name]].reset_index().pivot_table(index='datetime',columns='fund_id',values=fac_name).copy()
        fac = fac[fac.columns.intersection(fund_pool)]
        fac.columns = pd.MultiIndex.from_product([[fac_name], fac.columns])
        td = pd.to_datetime(fac.index)
        td = [i.date() for i in td]
        fac.index = td
        fac.index.name = 'datetime'
        result.append(fac)
    # append one delete one, keep memory same
    df = pd.DataFrame()
    while len(result) > 0:
        if df.empty:
            df = result.pop(0)
        else:
            df = df.join(result.pop(0))
    df = df.stack()
    df = df.reset_index().dropna(subset=FACTOR_LIST, how='any')
    df.loc[:,'index_id'] = df.fund_id.map(lambda x : fund_index_dic.get(x, None))
    df.loc[:,'active'] = (1 * ~df.fund_id.isin(filtered_fund_info.fund_id))
    df = df.replace(np.Inf,np.nan).replace(-np.Inf,np.nan)
    df[score_list] = df[score_list].fillna(0)
    df = df.rename(columns={'level_0':'datetime'})
    return df