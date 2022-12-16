import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "rv;Hd`B?:KeX>Fh`!Z#o*R^]vnT,TAOJb=mGkGm!,gCb_BS;=ZMptp!Q.@my<cP"  # 如果出现\x，则会报错，需要删除\x

DEBUG = True

TORTOISE_ORM = {
    "connections": {
        "default": os.getenv('DB_URL') or "sqlite://fast_store_backend.sqlite3",
    },
    'apps': {
        'fast_tmp': {
            'models': ['fast_tmp.models'],  # 注册app.models
            'default_connection': 'default',
        },
        'models': {
            'models': ['fast_store_backend.models'],
            'default_connection': 'default',
        }
    }
}
EXTRA_SCRIPT = []  # 自定义执行脚本

PATH = "http://127.0.0.1:8000"
WECHAT_SECRET = "123"
WECHAT_APPID = "123"
WECHAT_MCHID = "123"

WECHAT_PAY_NOTIFY_URL = "123"
