
import os

from ...util.config import SurfingConfigurator

from .fin_quality_factors import GrossMarginFactor, ReturnOnAssetsFactor, ReturnOnEquityFactor, TurnoverRateOfFAFactor, MixFinQualityFactor
from .growth_factors import IncomeGrowthFactor, NetProfitOfNonRecurringGoLFactor, OperationalCashFlowFactor, MixGrowthFactor
from .leverage_factors import FloatRatioFactor, StockDebtRatioFactor, CashFlowRatioFactor, MixLeverageFactor
from .liquidity_factors import Turnover30DFactor, Turnover60DFactor, Turnover90DFactor, MixLiquidityFactor
from .momentum_factors import AdjMomentum3MFactor, AdjMomentum6MFactor, AdjMomentum12MFactor, MixMomentumFactor
from .scale_factors import MarketValueFloatedFactor
from .tech_factors import ReverseFactor, BiasFactor, RSIFactor, MixTechFactor
from .value_factors import NAToMVFactor, NPToMVFactor, SPSToPFactor, DividendYieldFactor, EBITDAToMVFactor, EBITDAToEVFactor, MixValueFactor
from .volatility_factors import BetaSSEIFactor, Vol250DFactor, ResidualVolSSEIFactor, MixVolatilityFactor

conf = SurfingConfigurator().get_aws_settings()
# 在to_parquet/read_parquet中通过storage_options传递如下参数的方法不好用，这里直接设置环境变量
os.environ['AWS_ACCESS_KEY_ID'] = conf.aws_access_key_id
os.environ['AWS_SECRET_ACCESS_KEY'] = conf.aws_secret_access_key
os.environ['AWS_DEFAULT_REGION'] = conf.region_name


for obj in (GrossMarginFactor, ReturnOnAssetsFactor, ReturnOnEquityFactor, TurnoverRateOfFAFactor, MixFinQualityFactor,
            IncomeGrowthFactor, NetProfitOfNonRecurringGoLFactor, OperationalCashFlowFactor, MixGrowthFactor,
            FloatRatioFactor, StockDebtRatioFactor, CashFlowRatioFactor, MixLeverageFactor,
            Turnover30DFactor, Turnover60DFactor, Turnover90DFactor, MixLiquidityFactor,
            AdjMomentum3MFactor, AdjMomentum6MFactor, AdjMomentum12MFactor, MixMomentumFactor,
            MarketValueFloatedFactor,
            ReverseFactor, BiasFactor, RSIFactor, MixTechFactor,
            NAToMVFactor, NPToMVFactor, SPSToPFactor, DividendYieldFactor, EBITDAToMVFactor, EBITDAToEVFactor, MixValueFactor,
            BetaSSEIFactor, Vol250DFactor, ResidualVolSSEIFactor, MixVolatilityFactor):
    obj().register()
