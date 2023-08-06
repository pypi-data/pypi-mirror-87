import traceback
import time
import requests

from ..entity.exception import BfEngineException, ErrorCode
from .base import CallerBase
from ..config import Config


class SkillServiceCaller(CallerBase):
    def __init__(self, app_id):
        super().__init__(app_id)
        self.app_id = app_id
        self.remote_skill_list_url = Config.base_url + '/adm/skill/list/{}?categoryId=0&query='
        self.remote_skill_update_status_url = Config.base_url + '/adm/skill/update/{}/{}/{}'
        self.header = {
            "X-locale": "zh-cn",
            "app_id": self.app_id,
            "X-Appid": self.app_id,
            "user_id": "bf-engine-sdk",
            "Authorization": "Bearer EMOTIBOTDEBUGGER",
            "Accept": "application/json,text/plain, */*"
        }

    def get_remote_skill_list(self):
        try:
            response = requests.get(self.remote_skill_list_url.format(self.app_id))
            if self._response_failed(response):
                msg = "log: 获取技能列表失败：原因: 接口返回异常。" + str(response.text) if response is not None else ''
                raise BfEngineException(ErrorCode.dm_load_error, msg)
            return response.json()['result']
        except Exception:
            msg = "log: 获取技能列表失败， 原因: Exception When GET '{}' : {}".format(self.remote_skill_list_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.dm_load_error, msg)

    def update_remote_skill_status(self, skill_id: int, status: bool):
        try:
            response = requests.post(self.remote_skill_update_status_url.format(self.app_id, skill_id, 'true' if status else 'false'))
            time.sleep(3)
            if self._response_failed(response):
                msg = "log: 更新技能状态失败：原因: 接口返回异常。" + str(response.text) if response is not None else ''
                raise BfEngineException(ErrorCode.dm_load_error, msg)
            return response.json()['result']
        except Exception:
            msg = "log: 更新技能状态失败， 原因: Exception When GET '{}' : {}".format(self.remote_skill_update_status_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.dm_load_error, msg)

