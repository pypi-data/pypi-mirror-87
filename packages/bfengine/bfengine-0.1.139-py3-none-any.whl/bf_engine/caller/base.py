import json

import requests

from ..entity.answer import Answer
from ..config import Config


class CallerBase:
    """
    api调用
    """

    def __init__(self, app_id):
        self.app_id = app_id
        self.base_url = Config.base_url
        self.robot_url = '{}/{}'.format(Config.base_url, Config.robot_url)

    def call_module(self, module: str, text: str, online: bool = False) -> Answer:
        """
        robot接口访问
        :param module: 模块名称
        :param text: 用户问
        :return: 机器人回答
        """
        header = {
            "Content-Type": "application/json"
        }
        data = {
            "user_id": 'bf-engine',
            "method": "inquiry",
            "app_id": self.app_id,
            "question": text,
            "included_modules": [module],
            "request_data": {
                "online": online
            }
        }
        resp = requests.post(self.robot_url, headers=header, json=data)
        params = json.loads(resp.text)
        results = params['results']
        if results:
            result = results[0]
            text = result['answer'][0]['value']
            score = result['answer_score']
            answer = Answer(text=text, score=score)
            if len(result["answer"]) == 1:
                return answer
            answer_data = result['answer'][1]["data"]
            answer.related = answer_data if answer_data else []
            return answer
        return Answer(text=Config.backfill_speech, score=60)

    @staticmethod
    def _response_failed(response):
        return response is None or response.status_code != 200 or response.json() is None
