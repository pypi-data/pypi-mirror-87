import requests

import json
from .base import CallerBase
from ..config import Config
from ..entity.exception import BfEngineException
from ..utils.request_form_data import RequestFormData


class IntentCaller(CallerBase):
    """
    QA api调用
    """

    def __init__(self, app_id):
        super().__init__(app_id)
        self.app_id = app_id
        self.module = 'qa'
        self.header = {
            "X-locale": "zh-cn",
            "app_id": app_id,
            "X-Appid": app_id,
            "user_id": "bf-engine-sdk",
            "Authorization": "Bearer EMOTIBOTDEBUGGER",
            "Accept": "application/json,text/plain, */*"
        }

        self.upload_intent_json_open_default_group_url = Config.base_url + "/intent/v3/updateIntentGroupSwitch?groupType=1&onOff=true"
        self.upload_intent_json_close_default_group_url = Config.base_url + "/intent/v3/updateIntentGroupSwitch?groupType=1&onOff=false"
        self.upload_intent_json_add_group_url = Config.base_url+"/intent/v3/addIntentGroup"
        self.upload_intent_json_list_group_url = Config.base_url + "/intent/v3/getIntentGroupStatus"

        self.upload_intent_json_list_intents_url = Config.base_url + "/intent/v3/intents"

        self.upload_intent_form_add_intent_url    = Config.base_url+"/api/v3/intents/intent"
        self.upload_intent_json_update_intent_url = Config.base_url+"/intent/v3/update/"

        self.upload_intent_json_train_url = Config.base_url+"/api/v3/intents/train?engine=intent_engine"
        self.upload_intent_json_train_status_url = Config.base_url + "/api/v3/intents/status"
        self.upload_intent_json_predict_intent_url = Config.base_url + "/adm/intent/v3/predict"

        # self.upload_intent_json_open_default_group_url = "http://172.16.102.160" + "/intent/v3/updateIntentGroupSwitch?groupType=1&onOff=true"
        # self.upload_intent_json_add_group_url = "http://172.16.102.160" + "/intent/v3/addIntentGroup"
        # self.upload_intent_json_list_group_url = "http://172.16.102.160" + "/intent/v3/getIntentGroupStatus"
        #
        # self.upload_intent_json_list_intents_url = "http://172.16.102.160" + "/intent/v3/intents"
        #
        # self.upload_intent_form_add_intent_url = "http://172.16.102.160" + "/api/v3/intents/intent"
        # self.upload_intent_json_update_intent_url = "http://172.16.102.160" + "/intent/v3/update/"
        #
        # self.upload_intent_json_train_url = "http://172.16.102.160" + "/api/v3/intents/train?engine=intent_engine"
        # self.upload_intent_json_train_status_url = "http://172.16.102.160" + "/api/v3/intents/status"
        # self.upload_intent_json_predict_intent_url = "http://172.16.102.160" + "/adm/intent/v3/predict"


    def open_default_intent(self):
        group_ids = []
        group_obj_list = self.intent_group_list()
        for group_obj in group_obj_list:
            group_ids.append(group_obj["groupId"])
        for groud_id in group_ids:
            resp = requests.get(self.upload_intent_json_open_default_group_url+"&groupId="+groud_id,headers=self.header, json={}).json()
            code = resp["status"]

    def close_default_intent(self):
        group_ids = []
        group_obj_list = self.intent_group_list()
        for group_obj in group_obj_list:
            group_ids.append(group_obj["groupId"])
        for group_id in group_ids:
            resp = requests.get(self.upload_intent_json_close_default_group_url + "&groupId=" + group_id,
                                headers=self.header, json={}).json()
            code = resp["status"]

    def open_intent_group(self, group_id: str = None):
        resp = requests.get(self.upload_intent_json_open_default_group_url + "&groupId=" + group_id,
                            headers=self.header, json={}).json()
    def close_intent_group(self,group_id:str=None):
        resp = requests.get(self.upload_intent_json_close_default_group_url + "&groupId=" + group_id,
                            headers=self.header, json={}).json()
        code = resp["status"]
    def add_group(self,domain:str):
        """
        添加意图集
        :return 返回添加后的意图group ID集
        """
        group_ids = []
        exist_group_name_list = []  # 已存在意图组名称
        try:
            group_ids.append(self._group_add(domain))
        except BfEngineException as bfe:
            exist_group_name_list.append(domain)
        exist_group_list = self._intent_group_search(exist_group_name_list)
        for exist_group in exist_group_list:
            if "groupId" in exist_group.keys():
                group_ids.append(exist_group["groupId"])
        return group_ids[0] if len(group_ids)>0 else None
    def add_intent(self,group_id:str=None,intent:str=None):
        intent_ids = []
        exist_intent_name_list = []  # 已存在意图组名称
        try:
            self._intent_add(group_id=group_id, intent=intent)
        except BfEngineException as bfe:
            exist_intent_name_list.append(intent["name"])

        exist_intents_list = self._intent_intents_search(group_id=group_id,intents=exist_intent_name_list)
        for exist_intent in exist_intents_list:
            if "id" in exist_intent.keys():
                intent_ids.append(exist_intent["id"])
        return intent_ids[0] if len(intent_ids) > 0 else None
    def intent_group_list(self):
        """
        预测标准问
        :param text: 用户query
        :param online: 线上|线下
        :return 上传id
        """
        resp = requests.get(self.upload_intent_json_list_group_url + "?appId=" + self.app_id+"&&groupType=0", headers=self.header, json={}).json()

        # 意图$组名称
        code = int(resp["status"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["result"]

    def intent_intents_list(self,group_id:str=None):
        """
        预测标准问
        :param text: 用户query
        :param online: 线上|线下
        :return 上传id
        """
        resp = requests.get(self.upload_intent_json_list_intents_url + "?groupId=" + group_id,
                            headers=self.header, json={}).json()

        # 意图$组名称
        code = int(resp["status"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["result"]["intentList"] if "result" in resp.keys() else []
    def _group_add(self, domain):

        data = {
            "groupName": domain,
            "appId": self.app_id
        }
        resp = requests.post(self.upload_intent_json_add_group_url, headers=self.header, json=data).json()

        # 意图$组名称
        code = int(resp["status"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["result"]
    def _intent_group_search(self, groups):
        """
        查询已经存在标签的IDS
        :param 查询tags
        :return 标签列表
        """
        group_objs = []
        group_obj_list = self.intent_group_list()
        for group in groups:
            for group_obj in group_obj_list:
                if group == group_obj["name"]:
                    group_objs.append(group_obj)
        return group_objs
    def _intent_add(self,group_id:str=None,intent:str=None):
        params = {
            "innerIntentId": -1,
            "groupId": group_id,
            "name": intent["name"],
            "positive": json.dumps(intent["corpus"]["positive"]),
            "negative": json.dumps(intent["corpus"]["negative"])
        }
        resp = requests.post(self.upload_intent_form_add_intent_url,headers=self.header, data=params).json()
        code = int(resp["status"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["result"]

    def _intent_intents_search(self, group_id:str=None,intents:list=[]):
        intent_objs = []
        intent_obj_list = self.intent_intents_list(group_id=group_id)
        for intent_name in intents:
            for intent_obj in intent_obj_list:
                if intent_name == intent_obj["name"]:
                    intent_objs.append(intent_obj)
        return intent_objs

    def train(self,group_id:str=None):
        data = {}
        resp = requests.post(self.upload_intent_json_train_url+ "&groupId=" + group_id, headers=self.header, json=data).json()
        # 问题$答案上传进度
        code = int(resp["status"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["result"]
    def train_status(self,group_id:str=None):
        resp = requests.get(self.upload_intent_json_train_status_url+"?groupId=" + group_id).json()

        code = int(resp["status"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        status = resp["result"]["status"]
        if status == "NEED_TRAIN":
            return 100
        return resp["result"]["progress"]
    def predict(self, text: str, online: bool = False) -> list:
        group_ids = []
        group_obj_list = self.intent_group_list()
        for group_obj in group_obj_list:
            group_ids.append(group_obj["groupId"])

        """
        预测标准问
        :param text: 用户query
        :param online: 线上|线下
        :return 上传id
        """
        data = {
            "sentence": text,
            "app_id": self.app_id,
            "group_ids":group_ids
        }
        resp = requests.post(self.upload_intent_json_predict_intent_url, headers=self.header, json=data).json()
        status = resp["status"]
        if status == "OK":
            return resp["predictions"]
        # 问题$答案上传进度
        code = int(resp["status"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["result"]
