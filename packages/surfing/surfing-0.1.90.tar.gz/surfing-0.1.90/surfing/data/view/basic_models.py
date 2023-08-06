
from sqlalchemy import CHAR, Column, Integer, Index, BOOLEAN, text, TEXT, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE, DATE, TINYINT, DATETIME, MEDIUMTEXT

from ...constant import SectorType, IndexPriceSource


class Base():
    _update_time = Column('_update_time', DATETIME, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))  # 更新时间


# make this column at the end of every derived table
Base._update_time._creation_order = 9999
Base = declarative_base(cls=Base)


class SectorInfo(Base):
    '''板块信息表'''

    __tablename__ = 'sector_info'

    sector_id = Column(CHAR(64), primary_key=True)  # 板块ID
    sector_type = Column(Enum(SectorType), nullable=False)  # 板块类型 industry-行业 topic-主题
    sector_desc = Column(TEXT, nullable=False)  # 板块描述
    sector_name = Column(CHAR(16), nullable=False, unique=True)  # 板块名称
    main_index_id = Column(CHAR(16), nullable=False)  # 板块代表指数
    main_fund_id = Column(CHAR(16))  # 板块代表基金

class SectorFunds(Base):
    '''板块基金表'''

    __tablename__ = 'sector_funds'

    id = Column(Integer, primary_key=True)

    sector_id = Column(CHAR(64), nullable=False)  # 板块ID
    csi_index_id = Column(CHAR(16), nullable=False)  # Choice指数ID
    index_id = Column(CHAR(20), nullable=False)  # 指数ID
    em_fund_id = Column(CHAR(16))  # Choice基金ID
    fund_id = Column(CHAR(16))  # 基金ID


class IndexInfo(Base):
    '''指数信息表'''

    __tablename__ = 'index_info'
    index_id = Column(CHAR(20), primary_key=True)
    is_deleted = Column(BOOLEAN, default=False)  # 是否删除

    order_book_id = Column(CHAR(20))  # 米筐ID
    # web_id= Column(CHAR(20)) # 数据所在网页ID
    industry_tag = Column(CHAR(64))  # 行业标签
    tag_method = Column(CHAR(64))  # 估值评分采用方法
    desc_name = Column(CHAR(64), nullable=False, unique=True)  # 名称
    maker_name = Column(CHAR(32), nullable=False)  # 编制机构
    # publish_date = Column(DATE, nullable=False)  # 发布日期
    is_select = Column(BOOLEAN, nullable=False)  # 是否属于精选
    is_stock_factor_universe = Column(BOOLEAN)  # 是否是股票因子universe
    em_id = Column(CHAR(20))  # ChoiceID
    em_plate_id = Column(CHAR(20))  # Choice板块ID
    index_profile = Column(TEXT)  # 指数概况
    price_source = Column(Enum(IndexPriceSource), nullable=False)  # 指数价格来源标记


class IndexComponent(Base):

    __tablename__ = 'index_component'

    index_id = Column(CHAR(20), primary_key=True)
    datetime = Column(DATE, primary_key=True)  # 日期
    num = Column(Integer, nullable=False)  # 成分股数量
    id_cat = Column(Enum(SectorType), nullable=False)  # 所属类型 industry-行业 topic-主题
    sector = Column(TEXT, nullable=False)  # 所属板块
    top10 = Column(TEXT, nullable=False)  # 前10成分及权重
    related_funds = Column(TEXT)  # 相关产品
    all_constitu = Column(MEDIUMTEXT, nullable=False)  # 所有成分及权重(from Choice)


class StockInfo(Base):
    '''股票信息表'''

    __tablename__ = 'stock_info'
    stock_id = Column(CHAR(20), primary_key=True) # 股票ID
    rq_id = Column(CHAR(20)) # 米筐ID


class FundSize(Base):
    '''基金最新规模'''

    __tablename__ = 'fund_size'

    fund_id = Column(CHAR(10), primary_key=True) # 基金id
    latest_size = Column(DOUBLE(asdecimal=False)) # 最新规模


class FundStatusLatest(Base):
    '''
    基金状态表 包含基金申赎状态等
    '''

    __tablename__ = 'fund_status_latest'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金ID

    PURCHSTATUS = Column('purch_status', CHAR(16))  # 申购状态
    REDEMSTATUS = Column('redem_status', CHAR(16))  # 赎回状态
    LPLIMIT = Column('lp_limit', DOUBLE(asdecimal=False))  # 暂停大额申购上限
    OTCLPLIMITJG = Column('otc_lp_limit_jg', DOUBLE(asdecimal=False))  # 场外暂停大额申购上限(机构)
    OTCLPLIMITGR = Column('otc_lp_limit_gr', DOUBLE(asdecimal=False))  # 场外暂停大额申购上限(个人)
    TRADESTATUS = Column('trade_status', CHAR(16))  # 交易状态
    PCHMINAMT = Column('pch_min_amt', DOUBLE(asdecimal=False))  # 申购金额下限
    REDMMINAMT = Column('redm_min_amt', DOUBLE(asdecimal=False))  # 单笔赎回份额下限


class FundInfo(Base):
    '''基金信息表'''

    __tablename__ = 'fund_info'
    fund_id = Column(CHAR(10), primary_key=True) # 基金ID

    wind_id = Column(CHAR(20), unique=True) # Wind基金ID
    transition = Column(Integer) # 基金变更次数
    order_book_id = Column(CHAR(10)) # RiceQuant基金ID
    desc_name = Column(CHAR(64)) # 基金名称
    start_date = Column(DATE) # 成立日期
    end_date = Column(DATE) # 关闭日期
    wind_class_1 = Column(CHAR(64)) # Wind基金类型
    wind_class_2 = Column(CHAR(64)) # Wind基金二级类型
    risk_level = Column(CHAR(2))  # 风险等级
    manager_id = Column(TEXT) # 基金经理
    company_id = Column(CHAR(64)) # 基金公司
    benchmark = Column(CHAR(255)) # 业绩基准
    full_name = Column(CHAR(255)) # 基金全名
    currency = Column(CHAR(20)) # 币种
    base_fund_id = Column(CHAR(20)) # 分级基金基础基金代号
    is_structured = Column(TINYINT(1)) # 是否为分级基金
    is_open = Column(TINYINT(1)) # 是否为日常开放申赎的基金 1是 0否， 排除掉封闭基金和定期开放基金
    is_regular_open_ended = Column(TINYINT(1)) # 是否为定期开放式基金 1是 0否
    is_closed_ended = Column(TINYINT(1)) # 是否为封闭基金 1是 0 否
    structure_type = Column(TINYINT(1))  # 是否为分级子基金  0/nan非   1母   2分级A  3 分级B 4 其他
    is_etf = Column(TINYINT(1)) # 是否是etf  0 非  1 etf
    asset_type = Column(CHAR(32)) # 资产类别
    tt_purchase_fee = Column(DOUBLE(asdecimal=False)) # 天天基金优惠申购费
    manage_fee = Column(DOUBLE(asdecimal=False)) # 管理费
    trustee_fee = Column(DOUBLE(asdecimal=False)) # 托管费
    purchase_fee = Column(DOUBLE(asdecimal=False)) # 申购费
    redeem_fee = Column(DOUBLE(asdecimal=False)) # 赎回费
    note = Column(CHAR(64)) # 附加信息
    track_index = Column(CHAR(20)) # 跟踪指数
    benchmark_1 = Column(CHAR(255)) # 业绩基准标的指数简称第一名
    benchmark_2 = Column(CHAR(255)) # 业绩基准标的指数简称第二名
    index_id = Column(CHAR(20)) # 基于第一业绩标准所标注的指数ID
    is_c =  Column("is_c", BOOLEAN)  #是否是etf  0 非  1 c
    is_a = Column("is_a", BOOLEAN)  #是否是etf  0 非  1 a
    ac_filter = Column("ac_filter", BOOLEAN) #是否ac均有要排除的a 0 排除  1 保留
    is_selected_mmf = Column(TINYINT(1)) # 是否基金规模最大的前50只货币基金(10年前有两只存在)  0 非  1 是
    national_debt_extension = Column(TINYINT(1)) # 纯债tag  0 非  1 是
    index_id_new = Column(CHAR(20)) # 基于第一业绩标准所标注的指数ID新
    subscr_fee_detail = Column(TEXT) # 认购费率详情
    purchase_fee_detail = Column(TEXT) # 申购费率详情
    redeem_fee_detail = Column(TEXT) # 赎回费率详情
    service_fee = Column(TEXT) # 销售服务费率
    fund_manager = Column(TEXT)  # 基金经理(现任)
    pre_fund_manager = Column(TEXT)  # 基金经理(历任)
    custodian_bank = Column(CHAR(64))  # 基金托管人
    foreign_custodian = Column(CHAR(64))  # 境外托管人
    frontend_fee_code = Column(CHAR(12))   # 前端收费代码
    backend_fee_code = Column(CHAR(12))  # 后端收费代码
    ar_code_in = Column(CHAR(12))  # 场内申赎代码


class FundBenchmark(Base):
    '''基金业绩比较基准表'''

    __tablename__ = 'fund_benchmark'

    em_id = Column(CHAR(16), primary_key=True)  # 基金代码
    fund_id = Column(CHAR(16))  # 内部基金代码
    # datetime = Column(DATE, primary_key=True)  # 日期
    index_text = Column(TEXT, nullable=False)  # 业绩比较基准
    benchmark = Column(TEXT, nullable=False)  # 解析出来的业绩比较基准
    benchmark_s = Column(TEXT, nullable=False)  # index转换后的业绩比较基准
    benchmark_s_raw = Column(TEXT, nullable=False)  # index转换后的业绩比较基准(原始)
    assets = Column(CHAR(32))  # 追踪的标的
    industry = Column(CHAR(64))  # 行业分类

    # __table_args__ = (
    #     Index('idx_em_fund_benchmark_datetime', 'datetime'),
    # )


class TradingDayList(Base):
    '''交易日列表'''

    __tablename__ = 'trading_day_list'
    datetime = Column(DATE, primary_key=True)


class FundNav(Base):
    '''基金净值表'''

    __tablename__ = 'fund_nav'
    fund_id = Column(CHAR(20), primary_key=True) # 合约代码
    datetime = Column(DATE, primary_key=True) # 日期

    unit_net_value = Column(DOUBLE(asdecimal=False)) # 单位净值
    acc_net_value = Column(DOUBLE(asdecimal=False)) # 累计单位净值 基金公司公告发布的原始数据 单位净值 + 单位累计分红
    adjusted_net_value = Column(DOUBLE(asdecimal=False)) # 复权净值 考虑分红再投资后调整的单位净值
    change_rate = Column(DOUBLE(asdecimal=False)) # 涨跌幅
    daily_profit = Column(DOUBLE(asdecimal=False)) # 每万元收益（日结型货币基金专用）
    weekly_yield = Column(DOUBLE(asdecimal=False)) # 7日年化收益率（日结型货币基金专用）
    redeem_status = Column(Integer) # 赎回状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    subscribe_status = Column(Integer) # 订阅状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    fund_size = Column(DOUBLE(asdecimal=False)) # 基金规模

    __table_args__ = (
        Index('idx_fund_nav_datetime', 'datetime'),
    )


class IndexPrice(Base):
    '''指数价格表'''

    __tablename__ = 'index_price'
    index_id = Column(CHAR(20), primary_key=True) # 指数id
    datetime = Column(DATE, primary_key=True) # 日期

    volume = Column(DOUBLE(asdecimal=False)) # 交易量
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 成交额
    ret = Column(DOUBLE(asdecimal=False)) # 日收益

    __table_args__ = (
        Index('idx_index_price_datetime', 'datetime'),
    )

class StockPrice(Base):
    '''股票价格表'''

    __tablename__ = 'stock_price'
    stock_id = Column(CHAR(20), primary_key=True) # 指数id
    datetime = Column(DATE, primary_key=True) # 日期

    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    limit_up = Column(DOUBLE(asdecimal=False)) # 涨停价
    limit_down = Column(DOUBLE(asdecimal=False)) # 跌停价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    volume = Column(DOUBLE(asdecimal=False)) # 交易量
    num_trades = Column(DOUBLE(asdecimal=False)) # 交易笔数
    adj_close = Column(DOUBLE(asdecimal=False)) # 后复权价格
    post_adj_factor = Column(DOUBLE(asdecimal=False)) # 后复权因子

    __table_args__ = (
        Index('idx_stock_price_datetime', 'datetime'),
    )


class FundRet(Base):
    '''基金历史收益'''

    __tablename__ = 'fund_ret'

    fund_id = Column(CHAR(10), primary_key=True) # 原始基金ID
    datetime = Column(DATE, primary_key=True) # 日期

    w1_ret = Column(DOUBLE(asdecimal=False)) # 近一周收益率
    m1_ret = Column(DOUBLE(asdecimal=False)) # 近一月收益率
    m3_ret = Column(DOUBLE(asdecimal=False)) # 近一季度收益率
    m6_ret = Column(DOUBLE(asdecimal=False)) # 近半年收益率
    y1_ret = Column(DOUBLE(asdecimal=False)) # 近一年收益率
    y3_ret = Column(DOUBLE(asdecimal=False)) # 近三年收益率
    y5_ret = Column(DOUBLE(asdecimal=False)) # 近五年收益率
    to_date_ret = Column(DOUBLE(asdecimal=False)) # 成立至今收益率
    mdd = Column(DOUBLE(asdecimal=False)) # 最大回撤（成立以来）
    annual_ret = Column(DOUBLE(asdecimal=False)) # 年化收益（成立以来）
    avg_size = Column(DOUBLE(asdecimal=False)) # 平均规模（成立以来）
    sharpe_ratio = Column(DOUBLE(asdecimal=False)) # 夏普率（成立以来）
    vol = Column(DOUBLE(asdecimal=False)) # 波动率（成立以来）
    info_ratio = Column(DOUBLE(asdecimal=False)) # 信息比率（成立以来）
    recent_y_ret = Column(DOUBLE(asdecimal=False)) # 年初至今收益率

class FundRatingLatest(Base):
    '''基金最新评级'''

    __tablename__ = 'fund_rating_latest'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金id
    zs = Column(DOUBLE(asdecimal=False))  # 招商评级
    sh3 = Column(DOUBLE(asdecimal=False))  # 上海证券评级三年期
    sh5 = Column(DOUBLE(asdecimal=False))  # 上海证券评级五年期
    jajx = Column(DOUBLE(asdecimal=False))  # 济安金信评级
    update_time = Column(DATE)  # 更新日期

    __table_args__ = (
        Index('idx_fund_rating_latest_datetime', 'update_time'),
    )


class StyleAnalysisStockFactor(Base):
    '''风格分析股票因子'''

    __tablename__ = 'style_analysis_stock_factor'

    stock_id = Column(CHAR(10), primary_key=True)  # EM股票ID
    datetime = Column(DATE, primary_key=True)  # 日期
    rate_of_return = Column(DOUBLE(asdecimal=False), nullable=False)  # 收益率
    latest_size = Column(DOUBLE(asdecimal=False))  # 规模
    bp = Column(DOUBLE(asdecimal=False))  # 价值
    short_term_momentum = Column(DOUBLE(asdecimal=False))  # 短期动量
    long_term_momentum = Column(DOUBLE(asdecimal=False))  # 长期动量
    high_low = Column(DOUBLE(asdecimal=False))  # 波动率

    __table_args__ = (
        Index('idx_style_analysis_stock_factor_datetime', 'datetime'),
    )

class BarraCNE5RiskFactor(Base):
    '''Barra CNE5风险因子'''

    __tablename__ = 'barra_cne5_risk_factor'

    stock_id = Column(CHAR(10), primary_key=True)  # EM股票ID
    datetime = Column(DATE, primary_key=True)  # 日期
    ret = Column(DOUBLE(asdecimal=False))
    leverage = Column(DOUBLE(asdecimal=False))
    logsize = Column(DOUBLE(asdecimal=False))
    momentum = Column(DOUBLE(asdecimal=False))
    book_price = Column(DOUBLE(asdecimal=False))
    earning_yields = Column(DOUBLE(asdecimal=False))
    liquidity = Column(DOUBLE(asdecimal=False))
    growth = Column(DOUBLE(asdecimal=False))
    resvol = Column(DOUBLE(asdecimal=False))

    __table_args__ = (
        Index('idx_barra_cne5_risk_factor_datetime', 'datetime'),
    )

class Fund_size_and_hold_rate(Base):
    '''基金规模和持有人比例'''

    __tablename__ = 'fund_size_and_hold_rate'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金id
    datetime = Column(DATE, primary_key=True)  # 日期
    size = Column(DOUBLE(asdecimal=False)) # 最新规模
    unit_total = Column(DOUBLE(asdecimal=False))  # 基金份额
    personal_holds = Column(DOUBLE(asdecimal=False)) # 个人持有比例 单位百分比
    institution_holds = Column(DOUBLE(asdecimal=False)) # 机构持有比例 单位百分比
    hold_num = Column(DOUBLE(asdecimal=False))  # 基金份额持有人户数

    __table_args__ = (
        Index('idx_fund_size_and_hold_rate_datetime', 'datetime'),
    )

class FundRate(Base):
    '''基金评级'''

    __tablename__ = 'fund_rate'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金id
    datetime = Column(DATE, primary_key=True)  # 日期
    mkt_3y_comp = Column(CHAR(5)) # 市场综合3年评级
    mornstar_3y =  Column(CHAR(5)) # 晨星3年评级
    mornstar_5y =  Column(CHAR(5)) # 晨星5年评级
    merchant_3y = Column(CHAR(5)) # 招商3年评级
    tx_comp = Column(CHAR(5)) # 天相投顾综合评级
    sh_3y_comp = Column(CHAR(5)) #上海证券3年评级(综合评级)
    sh_3y_stock = Column(CHAR(5)) #上海证券3年评级(选股能力)
    sh_3y_timeret = Column(CHAR(5)) #上海证券3年评级(择时能力)
    sh_3y_sharpe = Column(CHAR(5)) #上海证券3年评级(夏普比率)
    sh_5y_comp = Column(CHAR(5)) #上海证券5年评级(综合评级)
    sh_5y_stock = Column(CHAR(5)) #上海证券5年评级(选股能力)
    sh_5y_timeret = Column(CHAR(5)) #上海证券5年评级(择时能力)
    sh_5y_sharpe = Column(CHAR(5)) #上海证券5年评级(夏普比率)
    jian_comp = Column(CHAR(5)) #济安金信基金评级(综合评级)
    jian_earn = Column(CHAR(5)) #济安金信基金评级(盈利能力)
    jian_stable = Column(CHAR(5)) #济安金信基金评级(业绩稳定性)
    jian_risk = Column(CHAR(5)) #济安金信基金评级(抗风险能力)
    jian_stock = Column(CHAR(5)) #济安金信基金评级(选股能力)
    jian_timeret = Column(CHAR(5)) #济安金信基金评级(择时能力)
    jian_track = Column(CHAR(5)) #济安金信基金评级(基准跟踪能力)
    jian_alpha = Column(CHAR(5)) #济安金信基金评级(超额收益能力)
    jian_fee = Column(CHAR(5)) #济安金信基金评级(整体费用)

class FundHoldAsset(Base):
    '''基金持仓资产比例'''

    __tablename__ = 'fund_hold_asset'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金id
    datetime = Column(DATE, primary_key=True)  # 日期
    stock_nav_ratio = Column(DOUBLE(asdecimal=False)) # 股票市值占基金资产净值比
    bond_nav_ratio = Column(DOUBLE(asdecimal=False)) # 债券市值占基金资产净值比
    fund_nav_ratio = Column(DOUBLE(asdecimal=False)) # 基金市值占基金资产净值比
    cash_nav_ratio = Column(DOUBLE(asdecimal=False)) # 银行存款占基金资产净值比
    other_nav_ratio = Column(DOUBLE(asdecimal=False)) # 其他资产占基金资产净值比
    first_repo_to_nav = Column(DOUBLE(asdecimal=False))  # 报告期内债券回购融资余额占基金资产净值比例
    avg_ptm = Column(DOUBLE(asdecimal=False))  # 报告期末投资组合平均剩余期限

    __table_args__ = (
        Index('idx_fund_hold_asset_datetime', 'datetime'),
    )

class FundHoldIndustry(Base):
    '''基金持仓前三行业'''

    __tablename__ = 'fund_hold_industry'

    fund_id = Column(CHAR(10), primary_key=True) # 基金ID
    datetime = Column(DATE, primary_key=True) # 日期
    rank1_indname = Column(CHAR(50)) #第一排名行业名称
    rank1_indweight = Column(DOUBLE(asdecimal=False)) #第一排名行业市值占基金资产总值比
    rank2_indname = Column(CHAR(50)) #第二排名行业名称
    rank2_indweight = Column(DOUBLE(asdecimal=False)) #第二排名行业市值占基金资产总值比
    rank3_indname = Column(CHAR(50)) #第三排名行业名称
    rank3_indweight = Column(DOUBLE(asdecimal=False)) #第三排名行业市值占基金资产总值比

class FundHoldStock(Base):
    '''基金持仓前十股票'''

    __tablename__ = 'fund_hold_stock'

    fund_id = Column(CHAR(10), primary_key=True) # 基金ID
    datetime = Column(DATE, primary_key=True) # 日期
    rank1_stock = Column(CHAR(20)) #股票名
    rank1_stock_code = Column(CHAR(16))  # 股票ID
    rank1_stockval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank1_stockweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank2_stock = Column(CHAR(20)) #股票名
    rank2_stock_code = Column(CHAR(16))  # 股票ID
    rank2_stockval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank2_stockweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank3_stock = Column(CHAR(20)) #股票名
    rank3_stock_code = Column(CHAR(16))  # 股票ID
    rank3_stockval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank3_stockweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank4_stock = Column(CHAR(20)) #股票名
    rank4_stock_code = Column(CHAR(16))  # 股票ID
    rank4_stockval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank4_stockweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank5_stock = Column(CHAR(20)) #股票名
    rank5_stock_code = Column(CHAR(16))  # 股票ID
    rank5_stockval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank5_stockweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank6_stock = Column(CHAR(20)) #股票名
    rank6_stock_code = Column(CHAR(16))  # 股票ID
    rank6_stockval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank6_stockweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank7_stock = Column(CHAR(20)) #股票名
    rank7_stock_code = Column(CHAR(16))  # 股票ID
    rank7_stockval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank7_stockweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank8_stock = Column(CHAR(20)) #股票名
    rank8_stock_code = Column(CHAR(16))  # 股票ID
    rank8_stockval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank8_stockweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank9_stock = Column(CHAR(20)) #股票名
    rank9_stock_code = Column(CHAR(16))  # 股票ID
    rank9_stockval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank9_stockweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank10_stock = Column(CHAR(20)) #股票名
    rank10_stock_code = Column(CHAR(16))  # 股票ID
    rank10_stockval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank10_stockweight = Column(DOUBLE(asdecimal=False)) #持仓权重

class FundHoldBond(Base):
    '''东财基金重仓债'''

    __tablename__ = 'fund_hold_bond'
    fund_id = Column(CHAR(20), primary_key=True) # 基金ID
    datetime = Column(DATE, primary_key=True) # 日期
    rank1_bond = Column(CHAR(30)) #债券名
    rank1_bond_code =  Column(CHAR(15)) # 债券id
    rank1_bondval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank1_bondweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank2_bond = Column(CHAR(30)) #债券名
    rank2_bond_code =  Column(CHAR(15)) # 债券id
    rank2_bondval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank2_bondweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank3_bond = Column(CHAR(30)) #债券名
    rank3_bond_code =  Column(CHAR(15)) # 债券id
    rank3_bondval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank3_bondweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank4_bond = Column(CHAR(30)) #债券名
    rank4_bond_code =  Column(CHAR(15)) # 债券id
    rank4_bondval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank4_bondweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank5_bond = Column(CHAR(30)) #债券名
    rank5_bond_code =  Column(CHAR(15)) # 债券id
    rank5_bondval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank5_bondweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank6_bond = Column(CHAR(30)) #债券名
    rank6_bond_code =  Column(CHAR(15)) # 债券id
    rank6_bondval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank6_bondweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank7_bond = Column(CHAR(30)) #债券名
    rank7_bond_code =  Column(CHAR(15)) # 债券id
    rank7_bondval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank7_bondweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank8_bond = Column(CHAR(30)) #债券名
    rank8_bond_code =  Column(CHAR(15)) # 债券id
    rank8_bondval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank8_bondweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank9_bond = Column(CHAR(30)) #债券名
    rank9_bond_code =  Column(CHAR(15)) # 债券id
    rank9_bondval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank9_bondweight = Column(DOUBLE(asdecimal=False)) #持仓权重
    rank10_bond = Column(CHAR(30)) #债券名
    rank10_bond_code =  Column(CHAR(15)) # 债券id
    rank10_bondval = Column(DOUBLE(asdecimal=False)) #持仓市值
    rank10_bondweight = Column(DOUBLE(asdecimal=False)) #持仓权重

class FundStockPortfolio(Base):
    '''基金的股票全部持仓'''

    __tablename__ = 'fund_stock_portfolio'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金代码
    datetime = Column(DATE, primary_key=True)  # 报告期
    stock_id = Column(CHAR(10), primary_key=True)  # 股票代码
    hold_number = Column(DOUBLE(asdecimal=True), nullable=False)  # 持股数量(万股)
    semi_change = Column(DOUBLE(asdecimal=True))  # 半年度持股变动(万股)
    stock_mv = Column(DOUBLE(asdecimal=True))  # 持股市值(万元)
    net_asset_ratio = Column(DOUBLE(asdecimal=True))  # 占净值比(%)
    mv_ratio = Column(DOUBLE(asdecimal=True))  # 占股票投资市值比(%)

class MngInfo(Base):
    '''基金经理信息表'''

    __tablename__ = 'mng_info'

    start_mng_date = Column(DATE, primary_key=True) # 最早任职基金经理日期
    mng_name = Column(CHAR(25), primary_key=True) # 基金经理
    fund_id = Column(CHAR(10), primary_key=True) # 代码
    desc_name = Column(CHAR(70)) # 名称
    fund_size = Column(DOUBLE(asdecimal=False)) # 在管基金规模(亿元)
    start_date = Column(DATE) # 任职日期
    work_days = Column(DOUBLE(asdecimal=False)) # 任职天数
    his_ret = Column(DOUBLE(asdecimal=False)) # 任职以来回报(%)
    his_annual_ret = Column(DOUBLE(asdecimal=False)) # 任职以来年化回报(%)
    benchmark = Column(TEXT) # 业绩比较基准
    fund_type = Column(CHAR(25)) # 基金类型
    company_name = Column(CHAR(25)) # 管理公司
    coworkers = Column(CHAR(40)) # 共同任职经理
    mng_work_year = Column(DOUBLE(asdecimal=False)) # 基金经理年限
    worked_funds_num = Column(DOUBLE(asdecimal=False)) # 任职基金数
    worked_com_num = Column(DOUBLE(asdecimal=False)) # 任职基金公司数
    fund_total_geo_ret = Column(DOUBLE(asdecimal=False)) # 任职基金几何总回报(%)
    geo_annual_ret = Column(DOUBLE(asdecimal=False)) # 几何平均年化收益率(%)
    cal_annual_ret = Column(DOUBLE(asdecimal=False)) # 算术平均年化收益率(%)
    gender = Column(CHAR(2)) # 性别
    birth_year = Column(CHAR(4)) # 出生年份
    age =  Column(DOUBLE(asdecimal=False)) # 年龄
    education = Column(CHAR(4)) # 学历
    nationality =  Column(CHAR(10)) # 国籍
    resume = Column(TEXT) # 简历

    __table_args__ = (
        Index('idx_mng_info_fund_id', 'fund_id'),
    )

class FundMngChange(Base):
    '''基金经理变更表'''

    __tablename__ = 'fund_mng_change'

    fund_id = Column(CHAR(10), primary_key=True) # 代码
    desc_name = Column(CHAR(70)) # 名称
    mng_now = Column(CHAR(40)) # 现任基金经理
    mng_now_start_date = Column(TEXT) # 现任经理最新任职日期
    mng_begin = Column(CHAR(40)) # 最早任职基金经理
    mng_begin_date = Column(DATE) # 最早任职基金经理日期
    mng_now_work_year = Column(DOUBLE(asdecimal=False)) # 现任基金经理年限
    same_type_fund_work_year = Column(DOUBLE(asdecimal=False)) # 同类型基金现任基金经理年限均值
    resign_mngs = Column(TEXT) # 已离任基金经理
    total_mng_num = Column(DOUBLE(asdecimal=False)) # 已离任基金经理
    total_mng_avg_work_year = Column(DOUBLE(asdecimal=False)) # 历任基金经理人均任职年限
    fund_type = Column(CHAR(25)) # 基金类型
    company = Column(CHAR(35)) # 管理公司
    region = Column(CHAR(5)) # 监管辖区

class FundCompMngChange(Base):
    '''基金公司经理变更表'''

    __tablename__ = 'fund_comp_mng_change'

    company = Column(CHAR(35),  primary_key=True ) # 管理公司
    total_mng_num = Column(DOUBLE(asdecimal=False)) # 基金经理数
    mng_avg_year = Column(DOUBLE(asdecimal=False)) # 基金经理平均年限
    mng_max_year = Column(DOUBLE(asdecimal=False)) # 基金经理最大年限
    team_stability = Column(DOUBLE(asdecimal=False)) # 团队稳定性
    new_mng_num = Column(DOUBLE(asdecimal=False)) # 新聘基金经理数
    resign_mng_num = Column(DOUBLE(asdecimal=False)) # 离职基金经理数
    mng_turnover_rate = Column(DOUBLE(asdecimal=False)) # 基金经理变动率
    exp_less_than_1 = Column(DOUBLE(asdecimal=False)) # 1年以内
    exp_1_to_2 = Column(DOUBLE(asdecimal=False)) # 1-2年
    exp_2_to_3 = Column(DOUBLE(asdecimal=False)) # 2-3年
    exp_3_to_4 = Column(DOUBLE(asdecimal=False)) # 3-4年
    exp_more_than_4 = Column(DOUBLE(asdecimal=False)) # 4年以上
    
class FundCompCoreMng(Base):
    '''基金公司核心人员稳定性'''

    __tablename__ = 'fund_comp_core_mng'

    fund_id = Column(CHAR(10), primary_key=True) # 代码
    desc_name = Column(CHAR(70)) # 名称
    fund_resign_mng_num = Column(DOUBLE(asdecimal=False)) # 本基金离职基金经理人数
    company = Column(CHAR(35)) # 管理公司
    com_mng_num = Column(DOUBLE(asdecimal=False)) # 基金公司基金经理数	
    com_resign_mng_num = Column(DOUBLE(asdecimal=False)) # 基金公司离职基金经理数
    com_resign_mng_rate = Column(DOUBLE(asdecimal=False)) # 基金公司基金经理离职率(%)	
    com_core_mng_num = Column(DOUBLE(asdecimal=False)) # 基金公司核心人员人数
    com_core_mng_resign_num = Column(DOUBLE(asdecimal=False)) #基金公司核心人员离职人数
    com_core_mng_resign_rate = 	Column(DOUBLE(asdecimal=False)) #基金公司核心人员离职率(%)
    fund_type = Column(CHAR(25)) # 基金类型
    region = Column(CHAR(5)) # 监管辖区

class FundIPOStats(Base):
    '''基金打新收益率统计'''

    __tablename__ = 'fund_ipo_stats'

    fund_id = Column(CHAR(10), primary_key=True) # 代码
    end_date = Column(DATE, primary_key=True) # 结束统计日
    ipo_allocation_num = Column(Integer) # 打中新股数量
    ipo_allocation_share_num = Column(DOUBLE(asdecimal=False)) # 累计获配股数(万股)
    ipo_allocation_amount = Column(DOUBLE(asdecimal=False)) # 累计获配金额(万元)
    ipo_allocation_ret = Column(DOUBLE(asdecimal=False)) # 打新收益率(%)
    start_date = Column(DATE)  # 开始统计日期
    size = Column(DOUBLE(asdecimal=False)) # 基金规模
    ipo_allocation_weight = Column(DOUBLE(asdecimal=False)) # 基金打新比例

class FundConvStats(Base):
    '''基金可转债比例'''

    __tablename__ = 'fund_conv_stats'

    fund_id = Column(CHAR(10), primary_key=True) # 代码
    datetime = Column(DATE, primary_key=True) # 日期
    conv_weights = Column(DOUBLE(asdecimal=False)) # 可转债权重

class FundOpenInfo(Base):
    '''基金定开信息'''

    __tablename__ = 'fund_open_info'

    fund_id = Column(CHAR(10), primary_key=True) # 代码
    desc_name = Column(CHAR(64)) # 基金名称

class StockInFund(Base):
    '''基金重仓股'''

    __tablename__ = 'stock_in_fund'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金代码
    stock_id = Column(CHAR(10), primary_key=True) # 股票代码
    datetime = Column(DATE, primary_key=True) # 日期
    stock_name = Column(CHAR(64)) # 股票名称
    stock_weight = Column(DOUBLE(asdecimal=False)) # 股票在基金权重
    fund_name = Column(CHAR(64)) # 基金名称

class BondInFund(Base):
    '''基金重仓股'''

    __tablename__ = 'bond_in_fund'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金代码
    bond_id = Column(CHAR(10), primary_key=True) # 债券代码
    datetime = Column(DATE, primary_key=True) # 日期
    bond_name = Column(CHAR(64)) # 债券名称
    bond_weight = Column(DOUBLE(asdecimal=False)) # 债券在基金权重
    fund_name = Column(CHAR(64)) # 基金名称
    