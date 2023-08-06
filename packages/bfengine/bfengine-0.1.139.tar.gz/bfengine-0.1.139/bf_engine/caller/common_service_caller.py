import traceback

import requests

from ..entity.exception import BfEngineException, ErrorCode
from .base import CallerBase
from ..config import Config


class CommonServiceCaller(CallerBase):
    def __init__(self, app_id):
        super().__init__(app_id)
        self.app_id = app_id
        self.auto_fill_url = Config.base_url + '/adm/emotibot_utils/v2/autofill'
        self.header = {
            "X-locale": "zh-cn",
            "app_id": self.app_id,
            "X-Appid": self.app_id,
            "user_id": "bf-engine-sdk",
            "Authorization": "Bearer EMOTIBOTDEBUGGER",
            "Accept": "application/json,text/plain, */*"
        }

    def get_auto_fill_questions(self, text:str, limit: int):
        params = {
            "appId": self.app_id,
            "limit": limit,
            "text": text
        }
        try:
            response = requests.post(self.auto_fill_url, json=params)
            if self._response_failed(response):
                msg = "log: 获取联想问题失败：原因: 接口返回异常。" + str(response.text) if response is not None else ''
                raise BfEngineException(ErrorCode.dm_load_error, msg)
            return response.json()['result']
        except Exception:
            msg = "log: 获取联想问题失败， 原因: Exception When POST '{}' : {}".format(self.auto_fill_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.dm_load_error, msg)
