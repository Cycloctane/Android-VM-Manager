
from init_db import DatabaseInitializer

from intercept_tencent_news import TencentNewsInterceptor

addons = [DatabaseInitializer(), TencentNewsInterceptor()]
