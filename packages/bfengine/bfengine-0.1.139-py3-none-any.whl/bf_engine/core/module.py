from ..core.test import TestRunner
from ..entity.answer import Answer
from .set import Set


class Module:
    """
    出话模块
    """
    def __init__(self, app_id, name, set):
        self.app_id = app_id
        self.name = name
        self.set = set

    def query(self, text: str, online: bool) -> Answer:
        """
        :param text: 用户问
        :param online: True 线上出话 False 线下出话
        :return: 机器人回答
        """
        raise NotImplemented

    def test(self, dataset):
        """
        :param dataset:
        :return: 测试结果
        """
        runner = TestRunner(dataset, self)
        result = runner.run()
        return result

    def init(self):
        pass
