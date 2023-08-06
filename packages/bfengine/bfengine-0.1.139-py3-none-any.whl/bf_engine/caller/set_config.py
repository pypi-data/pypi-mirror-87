import traceback

from ..entity.exception import BfEngineException, ErrorCode
from ..logger import log


class SetConfig():
    """
    机器人配置
    """
    def __init__(self):
        self.data = {}
    def add(self, name: str,value):
        """
        :param name: 字典key
        :param value: 字典value
        :return: 训练是否成功
        """
        try:
            if name in self.data.keys():
                self.data.pop(name)
            self.data[name]=value
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error(e)
            traceback.print_exc()
            return False
        return True
    def get(self,key:str=None):
        if key in self.data.keys():
            return self.data[key]
        return None
    def exits(self,key:str=None) -> bool:
        if not self.data:
            return False
        return key in self.data.keys()
    def clear(self):
        self.data.clear()

