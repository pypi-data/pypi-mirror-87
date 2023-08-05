import time

from .module import Module
from ..caller.common_service_caller import CommonServiceCaller
from ..logger import log


class CommonService(Module):
    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'config', set)
        self.app_id = app_id
        self.caller = CommonServiceCaller(self.app_id)
        if init:
            self.init()

    def get_input_autofill(self, text: str, limit: int) -> list:
        try:
            limit = int(limit)
            return self.caller.get_auto_fill_questions(text, limit)
        except Exception as e:
            log.error(e)

