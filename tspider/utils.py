import warnings
import ssl
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# ssl._create_default_https_context = ssl._create_unverified_context  # 绕过ssl验证
warnings.filterwarnings("ignore")


class PdSql(object):

    def __init__(self, db_name: str, root_dir=None, db_type='sqlite'):
        if not root_dir:
            self.ROOT_DIR = "E:/Databases/xgeocoding"
        else:
            self.ROOT_DIR = root_dir
        if db_name.endswith('.db'):
            db_name = db_name.split('.')[0]
        self.DB_NAME = db_name
        self.DB_TYPE = db_type

    @property
    def engine(self):
        dict_connects = {
            'sqlite': f'sqlite:///{self.ROOT_DIR}/{self.DB_NAME}.db',
            'mysql': f'mysql+pymysql://root:174873lms@localhost:3306/{self.DB_NAME}?charset=utf8'
        }
        connect_info = dict_connects[self.DB_TYPE]
        return create_engine(connect_info).connect()

    def to_sql(self, data: pd.DataFrame, table, dtypes=None, method='append'):
        # self.data = data
        # self.data.to_sql(
        data.to_sql(
            table,
            con=self.engine,
            if_exists=method,
            index=False,
            chunksize=10,
            dtype=dtypes,
        )

    def read_sql(self, sql):
        # self.df = pd.read_sql(sql, con=self.engine)
        return pd.read_sql(sql, con=self.engine)

    def execute(self, sql):
        """
        mainly for executes of sql like 'CREATE' 'ALTER' 'DROP'
        other sql involving data feedback, please refer to func 'to_sql'&'read_sql'
        :param sql:
        """
        self.engine.execute(sql)

    def close(self):
        self.engine.close()


def trans_cookie(cookie_str):
    cookies = {}
    items = cookie_str.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        cookies[key] = value
    return cookies