import pandas as pd
import traceback
from sqlalchemy import distinct, func
from ...wrapper.mysql import ViewDatabaseConnector
from ...view.view_models import ManagerInfoCollection


class ManagerInfoCollectionProcessor:

    def append_data(self, table_name, data_append_directly_data_df):
        if not data_append_directly_data_df.empty:
            with ViewDatabaseConnector().managed_session() as mn_session:
                try:
                    mn_session.execute(f'TRUNCATE TABLE {table_name}')
                    mn_session.commit()
                except Exception as e:
                    print(f'Failed to truncate table {table_name} <err_msg> {e}')
            data_append_directly_data_df.to_sql(table_name, ViewDatabaseConnector().get_engine(), index = False, if_exists = 'append')
            print('新数据已插入')
        else:
            print('没有需要插入的新数据')

    def collection_daily(self):
        mng_info = [
            {
                'mng_id':'16E872',
                'mng_name':'萧楠',
                'introduction':'消费之王，坚守价值投资，屡获奖项',
                'fund_type': 'stock',
            },
            {
                'mng_id':'170F31',
                'mng_name':'谢治宇',
                'introduction':'自下而上精选个股，行业均衡，成长投资，代表作7年6倍',
                'fund_type': 'stock',
            },
            {
                'mng_id':'7CABBB',
                'mng_name':'袁芳',
                'introduction':'擅长行业消费+科技，风格均衡，高换手分散持股',
                'fund_type': 'stock',
            },
            {
                'mng_id':'17109A',
                'mng_name':'曲扬',
                'introduction':'投资风格以稳健著称，获得第七届英华奖五年期股票投资最佳基金经理奖项',
                'fund_type': 'stock',
            },
            {
                'mng_id':'16E885',
                'mng_name':'张坤',
                'introduction':'收益优秀，8年6倍，700亿规模',
                'fund_type': 'stock',
            },
            {
                'mng_id':'7C3A95',
                'mng_name':'杨浩',
                'introduction':'TMT行业有着深入的研究，交银三剑客',
                'fund_type': 'stock',
            },
            {
                'mng_id':'7B55CF',
                'mng_name':'谭小兵',
                'introduction':'任职四年半回报230%',
                'fund_type': 'stock',
            },
            {
                'mng_id':'18377A',
                'mng_name':'王君正',
                'introduction':'通过稳健的投资框架，获得过金牛奖、明星基金奖和金基金奖共6座，业内少有的大满贯基金经理',
                'fund_type': 'stock',
            },
            {
                'mng_id':'7BE82B',
                'mng_name':'何帅',
                'introduction':'绝对收益；成长价值；性价比为王；长期优异；交银三剑客',
                'fund_type': 'stock',
            },
            {
                'mng_id':'78F3D1',
                'mng_name':'孙伟',
                'introduction':'连续5年金牛奖，全市场获此荣誉的基金经理仅3人三次获得明星基金奖',
                'fund_type': 'stock',
            },
            {
                'mng_id':'19A22E',
                'mng_name':'张清华',
                'introduction':'股债双修研究深入，择时能力突出',
                'fund_type': 'bond',
            },
            {
                'mng_id':'01109',
                'mng_name':'桂跃强',
                'introduction':'股债配置能力强，投资权益的风格就属于稳健型，擅长使用权益类资产进行稳定增强',
                'fund_type': 'bond',
            },
            {
                'mng_id':'4F9879',
                'mng_name':'姚秋',
                'introduction':'股债全能的投资界“名将”，宏观层面把握机会，追求长期稳健回报资产配置能力出色',
                'fund_type': 'bond',
            },
            {
                'mng_id':'4F9865',
                'mng_name':'张雅君',
                'introduction':'金牛债券基金经理，同类产品连续六年正收益，金牛基金、明星基金，五星债券基金',
                'fund_type': 'bond',
            },
            {
                'mng_id':'C3B3E7',
                'mng_name':'蒋利娟',
                'introduction':'第六届中国基金业英华奖三年期纯债投资最佳基金经理、泰康资产公募事业部固收投资负责人',
                'fund_type': 'bond',
            },
            {
                'mng_id':'00707',
                'mng_name':'苏玉平',
                'introduction':'五年期二级债最佳基金经理奖”，连续三年在英华奖评选中榜上有名',
                'fund_type': 'bond',
            },
            {
                'mng_id':'17036A',
                'mng_name':'于泽雨',
                'introduction':'2019年金牛奖最佳人气金牛基金经理得主、擅长分析基本面 擅长长周期操作',
                'fund_type': 'bond',
            },
            {
                'mng_id':'7A8375',
                'mng_name':'张雪',
                'introduction':'擅长使用久期择时，杠杆择时，注重风险调整后收益，夏普比率2.58',
                'fund_type': 'bond',
            },
            {
                'mng_id':'B9F063',
                'mng_name':'邬传雁',
                'introduction':'现任泓德基金副总经理。风格稳健型，股债研究均深入，擅长股债择时，权益类增强',
                'fund_type': 'bond',
            },
            {
                'mng_id':'00524',
                'mng_name':'李建',
                'introduction':'擅长股债择时和大类资产配置，严控回撤同时实现长期正收益的灵活配置型代表',
                'fund_type': 'stock',
            },
            {
                'mng_id':'7BEBB3',
                'mng_name':'刘博',
                'introduction':'选股能力出色，风险敞口低，近两年表现出色，任职年化收益45.39%。',
                'fund_type': 'stock',
            },
            {
                'mng_id':'16094C',
                'mng_name':'庄园',
                'introduction':'灵活配置股债，回撤控制和收益能力出色，获债券型优胜金牛基金等高含金量奖项',
                'fund_type': 'stock',
            },
            {
                'mng_id':'164E99',
                'mng_name':'宋炳珅',
                'introduction':'8次获得金牛奖，代表作年化收益7.63%，回撤控制在5.05%水平。工银瑞信“固收+”王牌团队成员',
                'fund_type': 'bond',
            },
        ]        
        self.result = pd.DataFrame(mng_info)

    def insert(self):
        self.append_data(ManagerInfoCollection.__tablename__, self.result)