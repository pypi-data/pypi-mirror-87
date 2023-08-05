import time

from .module import Module
from ..logger import log
from ..entity.answer import Answer
from ..caller.base import CallerBase

class ChatService(Module):
    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'config', set)
        self.app_id = app_id
        self.caller = CallerBase(app_id)
        if init:
            self.init()

    def query(self, text: str, online: bool = True) -> Answer:
        """
        :param online: 线上线下, 部分模块会需要线上线下的状态区分
        :param text: 用户问
        :return: 机器人回答
        """
        return self.caller.call_module('chat', text, online)
