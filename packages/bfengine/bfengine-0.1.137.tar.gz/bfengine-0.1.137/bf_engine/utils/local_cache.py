import shelve
from contextlib import closing

class LocalCache:
    def __init__(self, cache='var.pkl'):
        self.cache = cache

    def __setitem__(self, key, value):
        """
        key: 变量名
        value: 变量值
        cache: 缓存名
        """
        with closing(shelve.open(self.cache, 'c')) as shelf:
            shelf[key] = value

    def __getitem__(self, key):
        """
        key : 变量名
        return：变量值
        """
        with closing(shelve.open(self.cache, 'c')) as shelf:
            return shelf.get(key)

    def remove(self, key):
        """
    	key: 变量名

    	如果 变量存在则删除, 如果不存在，会抛出一个异常，由调用方去处理
    	"""
        with closing(shelve.open(self.cache, 'rc')) as shelf:
            del shelf[key]
            return True