import logging
import traceback

import requests

from ..config import Config
from .base import CallerBase
from .. import util

backfill_answer_type = 3


class ConfigManagerCaller(CallerBase):

    def __init__(self, app_id):
        super().__init__(app_id)
        self.app_id = app_id
        self.update_robot_config_url = "{}/api/v1/robot/config".format(Config.base_url)
        # 获取预设话术url
        self.get_default_response_url = "{}/api/v2/robot/chats".format(Config.base_url)
        self.backfill_answer_url = "{}/api/v2/robot/chat/3/content".format(Config.base_url)
        self.create_bot_url = "{}/auth/v6/enterprise/bb3e3925f0ad11e7bd860242ac120003/app".format(Config.base_url)
        self.header = {
            "X-locale": "zh-cn",
            "app_id": self.app_id,
            "X-Appid": self.app_id,
            "user_id": "bf-engine-sdk",
            "Authorization": "Bearer EMOTIBOTDEBUGGER",
            "Accept": "application/json,text/plain, */*"
        }

    def init_bot_config(self, name=None):
        try:
            if not name:
                name = util.random_uuid()
            response = requests.post(url=self.create_bot_url, headers=self.header, files={
                'name': (None, name),
                'description': (None, ''),
                'app_type': (None, '0'),
                'props': (None, '[{"id":1},{"id":3}]'),
                'appId': (None, self.app_id)
            })
            if response.status_code == 400:
                pass
            elif self._response_failed(response):
                logging.error(
                    "configManager: 初始化机器人失败: 接口异常。" + str(response.json()) if response is not None else '')
        except Exception:
            msg = "Exception When GET '{}' : {}".format(self.get_default_response_url, traceback.format_exc())
            logging.error('configManager: 初始化机器人失败， 原因：' + msg)

    def update_robot_config(self, config_key: str, value):
        try:
            response = requests.post(url=self.update_robot_config_url, headers=self.header, files={
                'configName': (None, config_key),
                'module': (None, 'controller'),
                'value': (None, value)
            })
            if self._response_failed(response):
                logging.error(
                    "configManager: 更新配置失败: 接口异常。" + str(response.json()) if response is not None else '')
        except Exception:
            msg = "Exception When GET '{}' : {}".format(self.update_robot_config_url, traceback.format_exc())
            logging.error('configManager: 更新配置失败， 原因：' + msg)

    def get_backfill(self):
        try:
            response = requests.get(url=self.get_default_response_url, headers=self.header)
            if self._response_failed(response):
                logging.error(
                    "configManager: 获取预设未知回复话术失败: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                backfill_answers = []
                response_json = response.json()
                all_default_answers = response_json['result']
                filters_backfill_answers = list(
                    filter(lambda x: x['type'] == backfill_answer_type, all_default_answers))
                if len(filters_backfill_answers) > 0:
                    backfill_answers = filters_backfill_answers[0]['contents']
                return backfill_answers
        except Exception:
            msg = "Exception When GET '{}' : {}".format(self.get_default_response_url, traceback.format_exc())
            logging.error('configManager: 获取预设未知回复话术失败， 原因：' + msg)

    def set_backfill(self, backfill_answers: list) -> bool:
        try:
            original_answers = self.get_backfill()
            for answer in original_answers:
                requests.delete(self.backfill_answer_url + "/" + str(answer['id']), headers=self.header)
            for answer in backfill_answers:
                requests.post(self.backfill_answer_url, headers=self.header, files={
                    'content': (None, answer)
                })
            return True
        except Exception:
            msg = "Exception When GET '{}' : {}".format(self.get_default_response_url, traceback.format_exc())
            logging.error('configManager: 设置未知回复话术失败， 原因：' + msg)
            return False

    def set_profess(self, profess: str):
        """
        设置机器人自称
        :param profess: 自称
        :return:
        """
