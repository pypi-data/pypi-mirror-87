
import os
from ...util.config import SurfingConfigurator

# 在to_parquet/read_parquet中通过storage_options传递如下参数的方法不好用，这里直接设置环境变量
conf = SurfingConfigurator().get_aws_settings()
os.environ['AWS_ACCESS_KEY_ID'] = conf.aws_access_key_id
os.environ['AWS_SECRET_ACCESS_KEY'] = conf.aws_secret_access_key
os.environ['AWS_DEFAULT_REGION'] = conf.region_name
