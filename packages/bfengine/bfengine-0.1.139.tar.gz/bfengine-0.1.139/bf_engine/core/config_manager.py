import time

from .module import Module
from ..caller.config_manager_caller import ConfigManagerCaller


class ConfigManager(Module):
    def __init__(self, app_id, set, init, name=None):
        super().__init__(app_id, 'config', set)
        self.app_id = app_id
        self.caller = ConfigManagerCaller(self.app_id)
        self.botname = name
        if init:
            self.init()

    def init(self):
        self.caller.init_bot_config(self.botname)

    def get_backfill_answers(self) -> list:
        """
        获取未知回复列表
        :return:
        """
        answers = self.caller.get_backfill()
        return [answer['content'] for answer in answers]

    def set_backfill_answer(self, answers: list) -> bool:
        result = self.caller.set_backfill(answers)
        # todo delete
        time.sleep(1.5)
        #

        return result
