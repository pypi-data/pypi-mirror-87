import logging
import traceback

import requests

from .base import CallerBase


class DialogueActCaller(CallerBase):
    """
    对话行为分类器API
    """

    def __init__(self, app_id):
        super().__init__(app_id)
        self.app_id = app_id
        self.module = 'ner'
        self.act_predict_all_url = self.base_url + "/dialogActClassify/customClassifier/detectSystemActs"
        self.act_predict_url = self.base_url + "/tde/custtagger/ud_sys_dialog_act"
        self.sys_act_get_url = self.base_url + "/tde/custtagger/sys_dialog_acts"

    def _predict_all(self, sentence: str):
        params = {
            "useId": self.app_id,
            "query": sentence
        }
        try:
            response = requests.post(url=self.act_predict_all_url, json=params)
            if self._response_failed(response):
                logging.error("act: 调用对话行为分类器失败: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                acts = response.json()['data']['sysActs']
                return [
                    {
                        'act': act['sysActLogicName'], 'score': act['confidence']}
                    for act in acts
                ]
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.act_predict_all_url, traceback.format_exc())
            logging.error('act: 调用对话行为分类器失败， 原因：' + msg)

    def predict(self, sentence: str, acts: list = None):
        if not acts:
            return self._predict_all(sentence)
        else:
            params = {
                'query': sentence,
                'types': acts
            }
            try:
                response = requests.post(url=self.act_predict_url, json=params)
                if self._response_failed(response):
                    logging.error("act: 调用对话行为分类器失败: 接口异常。" + str(response.json()) if response is not None else '')
                else:
                    acts = response.json()['reply']['labels']
                    return [
                        {
                            'act': act['label'], 'score': act['confidence']}
                        for act in acts
                    ]
            except Exception:
                msg = "Exception When POST '{}' : {}".format(self.act_predict_url, traceback.format_exc())
                logging.error('act: 调用对话行为分类器失败， 原因：' + msg)

    def get_acts(self):
        response = requests.get(url=self.sys_act_get_url)
        if self._response_failed(response):
            logging.error("act: 调用对话行为分类器失败: 接口异常。" + str(response.json()) if response is not None else '')
        else:
            acts = response.json()['sys_dialog_acts']
            return [
                {
                    'name': act['cn_name'],
                    'id': act['name'],
                    'explanation': act['explaination'],
                    'samples': act['typical_expression']
                }
                for act in acts
            ]

