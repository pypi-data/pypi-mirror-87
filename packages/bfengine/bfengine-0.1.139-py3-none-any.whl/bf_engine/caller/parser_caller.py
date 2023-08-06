import logging
import traceback

import requests

from .base import CallerBase



class NERParserCaller(CallerBase):
    """
    通用解析器API
    """
    def __init__(self, app_id):
        super().__init__(app_id)
        self.app_id = app_id
        self.module = 'ner'
        self.tde_user_register_url = self.base_url + '/nerFactoryDal/userManager/register'
        self.predict_url = self.base_url + '/nerfactory/predict'
        self.parser_get_url = self.base_url + '/nerFactoryDal/parserLibraryList'


    def register_tde_user(self, user_name=None):
        if user_name is None:
            user_name = self.app_id
        params = {
            'userId': self.app_id,
            'userName': user_name
        }
        response = requests.post(url=self.tde_user_register_url, json=params)
        if self._response_failed(response):
            logging.error("ner: 初始化解析器用户失败: 接口异常。" + str(response.json()) if response is not None else '')
        else:
            response_json = response.json()
            return response_json.get('status') == 'success'


    def predict(self, sentence: str, parser_id: str):
        params = {
            "companyId": self.app_id,
            "parserId": parser_id,
            "sentence": sentence
        }
        try:
            response = requests.post(url=self.predict_url, json=params)
            if self._response_failed(response):
                logging.error("ner: 调用解析器失败: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                return response.json()['data']['predictResult']
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.predict_url, traceback.format_exc())
            logging.error('ner: 调用解析器失败， 原因：' + msg)

    def get_parser_library(self):
        try:
            response = requests.get(url=self.parser_get_url + "?userId=" + self.app_id)
            if self._response_failed(response):
                logging.error("ner: 调用解析器失败: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                return response.json()['data']
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.parser_get_url, traceback.format_exc())
            logging.error('ner: 调用解析器失败， 原因：' + msg)
