import logging
import traceback

import requests

from ..config import Config
from ..entity.answer import Answer
from ..entity.exception import BfEngineException, ErrorCode
from .base import CallerBase


class DialogueManagerCaller(CallerBase):

    def __init__(self, app_id):
        super().__init__(app_id)
        self.app_id = app_id
        self.load_config_url = "{}/validate".format(Config.base_url)
        self.call_url = "{}/v1/ccs/openapi".format(Config.base_url)

    def load_config(self, data: dict) -> bool:
        """
        加载配置
        :param data:
        :return:
        """
        ret = True
        try:
            response = requests.post(self.load_config_url, json=data)
            if self._response_failed(response) or response.json().get('code') != 'Success':
                msg = "kg: 加载对话配置失败：原因: 接口返回异常。" + str(response.json()) if response is not None else ''
                raise BfEngineException(ErrorCode.dm_load_error, msg)
        except BfEngineException as bfe:
            raise bfe
        except Exception:
            msg = "kg: 加载对话配置失败， 原因: Exception When POST '{}' : {}".format(self.load_config_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.dm_load_error, msg)
        return ret

    def call(self, msg):
        """
       预测出话
       :param msg: 用户问
       :return: 机器人回答
       """
        answer = Answer(text='', score=0)
        param = {
            "text": msg,
            "extendData": {
                "online": False
            },
        }
        header = {
            'appId': self.app_id,
            'sessionId': Config.session_id,
            'userId': Config.user_id,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url=self.call_url, headers=header, json=param)
            if self._response_failed(response):
                logging.error("dm: 预测失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data'):
                    datas = response_json['data']
                    answer_text = ";".join([data.get('value') or '' for data in datas])
                    score = 100
                    if response_json.get('info') and response_json['info']['textScore']:
                        score = float(response_json['info']['textScore'])
                    answer = Answer(text=answer_text, score=score)
                else:
                    pass
                    # logging.warning('dm: 预测为空 [{}]'.format(msg))
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.call_url, traceback.format_exc())
            logging.error('dm: 对话失败， 原因: ' + msg)
        finally:
            if answer.text == '无候选答案' or not answer.text:
                answer.text = Config.backfill_speech
                answer.score = 60
            return answer
