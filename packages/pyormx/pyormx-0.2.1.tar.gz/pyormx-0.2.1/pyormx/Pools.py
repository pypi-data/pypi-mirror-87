import json
import threading

from .PooledDB import PooledDB

class Pool(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Pool, "_instance"):
            with Pool._instance_lock:
                if not hasattr(Pool, "_instance"):
                    Pool._instance = object.__new__(cls)
        return Pool._instance

    def __init__(self, *args, **kw):
        ''' 使用的数据库名字，目前支持mysql和postgresql
        --
            @param kw 连接参数，可选以下参数:
                maxconnections:连接池允许的最大连接数，0和None表示不限制连接数
                mincached:初始化时，链接池中至少创建的空闲的链接，0表示不创建
                maxcached:链接池中最多闲置的链接，0和None不限制
                maxshared:链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
                blocking:连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                maxusage:一个链接最多被重复使用的次数，None表示无限制
                setsession:开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
                ping:MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
                host:服务器地址
                port：端口
                user：账户
                password：密码
                database：数据库名
                charset：字符集
        '''
        self._kw = kw

    def conn(self):
        ''' 从连接池获取一个连接
        '''
        if not hasattr(self, 'POOL'):
            with Pool._instance_lock:
                if not hasattr(self, 'POOL'):
                    self._connect()
        return self.POOL.connection()

    def _connect(self):
        if hasattr(self, 'POOL'):
            return

        self.POOL = PooledDB(**self._kw)
