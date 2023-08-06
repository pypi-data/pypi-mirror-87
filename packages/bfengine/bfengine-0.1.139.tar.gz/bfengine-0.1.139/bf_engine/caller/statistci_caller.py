import traceback

import requests

from ..entity.exception import BfEngineException, ErrorCode
from .base import CallerBase
from ..config import Config


class StatisticCaller(CallerBase):
    def __init__(self, app_id):
        super().__init__(app_id)
        self.app_id = app_id
        self.top_n_hot_question_url = Config.base_url + '/api/v1/stats/question'
        self.log_query_url = Config.base_url + '/api/v2/stats/records/query'
        self.header = {
            "X-locale": "zh-cn",
            "app_id": self.app_id,
            "X-Appid": self.app_id,
            "user_id": "bf-engine-sdk",
            "Authorization": "Bearer EMOTIBOTDEBUGGER",
            "Accept": "application/json,text/plain, */*"
        }

    def get_hot_questions(self, start_time, end_time: str, top_n: int):
        url = '{}?t1={}&t2={}&top={}&type=top'.format(self.top_n_hot_question_url, start_time, end_time, top_n)
        try:
            response = requests.get(url, headers=self.header)
            if self._response_failed(response):
                msg = "log: 获取热点问题失败：原因: 接口返回异常。" + str(response.text) if response is not None else ''
                raise BfEngineException(ErrorCode.dm_load_error, msg)
            return response.json()['data']
        except Exception:
            msg = "log: 获取热点问题失败， 原因: Exception When POST '{}' : {}".format(url, traceback.format_exc())
            raise BfEngineException(ErrorCode.dm_load_error, msg)


    def get_records(self, start_time: int, end_time: int, limit: int, page: int):
        params = {
            "start_time": start_time,
            "end_time": end_time,
            "limit": limit,
            "page": page
        }
        try:
            response = requests.post(self.log_query_url, headers=self.header, json=params)
            if self._response_failed(response):
                msg = "log: 获取日志数据失败：原因: 接口返回异常。" + str(response.text) if response is not None else ''
                raise BfEngineException(ErrorCode.dm_load_error, msg)
            return response.json()
        except Exception:
            msg = "log: 获取日志数据失败， 原因: Exception When POST '{}' : {}".format(self.log_query_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.dm_load_error, msg)
