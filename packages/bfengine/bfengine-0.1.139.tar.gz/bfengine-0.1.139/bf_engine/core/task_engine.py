import json
import time
import traceback
import os
from selenium import webdriver
from selenium.webdriver.remote.command import Command
from webdriver_manager.chrome import ChromeDriverManager

import requests
from requests import Session, Request

from .module import Module
from ..config import Config
from ..entity.answer import Answer
from ..logger import log


class TaskEngine(Module):
    """
    任务引擎
    """

    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'te', set)
        self.app_id = app_id
        self.sess = Session()
        self.api_server = Config.base_url
        tmp_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.chrome_path_bin = tmp_dir + "/data/bin"
        # 获取scenario列表
        self.query_scenarios_url = '{}/php/api/ApiKey/task_engine_app.php'.format(
            self.api_server)
        # 获取scenario详细信息
        self.query_scenario_info_url = '{}/php/api/ApiKey/task_engine_scenario.php'.format(
            self.api_server)
        self.editor_url = '{}/?appid={}#/task-engine-scenario-v2'.format(
            self.api_server, self.app_id)
        # 获取scenario详细信息
        self.query_url = '{}/task_engine/ET'.format(self.api_server)
        self.headers = {
            'X-Appid': self.app_id,
            'X-Userid': Config.user_id
        }
        if init:
            self.init()

    def load(self, path):
        """
        加载scenario 的json
        """
        scenario_json = self._get_scenariojson_from_path(path)
        scenario_id, scenario_name = self._add_scenarios(scenario_json)
        if scenario_id is None:
            return False
        else:
            if self.enable_scenario(scenario_id):
                if self._public_scenario(scenario_id):
                    time.sleep(10)
                    log.info("te: load scenario【" + scenario_name + "】success")
                    return True
        log.error("te: load scenario【" + scenario_name + "】failed")
        return False

    def editor(self,path:str=None,syn:bool=True):
        """

        """
        if path:
            self.load(path)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        if driver:
            driver.get(self.editor_url)
            # while self.driver_status(driver):
            #     time.sleep(5)
            # func()
        log.info("正在为您打开页面:" + self.editor_url)
        if syn:
            log.info("任务引擎编辑: 编辑好后请按[return]键进行下一步操作")
            while True:
                file_content = input()
                if file_content == '':
                    break

    def driver_status(self,driver:webdriver)->bool:
        try:
            driver.execute(Command.STATUS)
            return True
        except Exception:
            return False
    def query(self, txt):
        """
        获取对话信息
        """
        try:
            task_engine_json = self._get_taskengine_json(txt, self.app_id)
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            resp = requests.post(self.query_url, json=task_engine_json, headers=headers).json()
            if "TTSText" not in resp or resp["TTSText"] is None:
                Answer(text=Config.backfill_speech, score=60)
            else:
                return Answer(text=resp["TTSText"], score=100)
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.query_url, traceback.format_exc())
            log.error('te: 对话失败， 原因: ' + msg)
        return Answer(text=Config.backfill_speech, score=60)

    def _query_scenarios(self):
        """
        查询scenario列表
        """
        try:
            params = {"appid": self.app_id, "type": 0}
            req = Request('GET', self.query_scenarios_url, headers=self.headers, params=params)
            resp = self.sess.send(req.prepare(), verify=False, timeout=2).json()
            return resp['msg']
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.query_scenarios_url, traceback.format_exc())
            log.error('te: 查询scenario列表失败， 原因: ' + msg)
        return []

    def _query_scenario_info(self, scenario_id):
        """
         查询scenario详细信息
         """
        try:
            params = {"scenarioid": scenario_id}
            req = Request('GET', self.query_scenario_info_url, headers=self.headers, params=params)
            resp = self.sess.send(req.prepare(), verify=False, timeout=2).json()
            return resp
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.query_scenario_info_url, traceback.format_exc())
            log.error('te: 查询scenario【' + scenario_id + '】信息， 原因: ' + msg)
        return []

    def _add_scenarios(self, scenario_json):
        """
        导入scenario
        """
        try:
            metadata = None
            scenario_id, scenario_name = self._get_scenario_info(scenario_json)
            scenario_lists = self._query_scenarios()
            for scenario in scenario_lists:
                if 'scenarioID' in scenario and scenario['scenarioID'] == scenario_id:
                    metadata = self._create_scenario(scenario_name)
                    if metadata is None:
                        return None, None
                    break
            content = scenario_json['taskScenario']
            layout = scenario_json['taskLayouts']
            params = {
                'content': json.dumps(content),
                'scenarioid': scenario_id,
                "appid": self.app_id,
                'layout': json.dumps(layout),
                'method': 'PUT'
            }
            if metadata is not None:
                content['metadata'] = metadata
                scenario_id = metadata['scenario_id']
                scenario_name = metadata['scenario_name']
            else:
                params['upload'] = 1
                params['type'] = 0

            resp = requests.post(url=self.query_scenario_info_url, data=params, headers=self.headers)
            if resp is None or resp.status_code != 200:
                return None, None
            return scenario_id, scenario_name
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.query_scenario_info_url, traceback.format_exc())
            log.error('te: 导入scenario失败， 原因: ' + msg)

        return None, None

    def _get_scenario_info(self, scenario_json):
        """
        获取scenario配置信息
        """
        try:
            return scenario_json["taskScenario"]["metadata"]["scenario_id"], scenario_json["taskScenario"]["metadata"][
                "scenario_name"]
        except Exception:
            pass
        return None, None

    def enable_scenario(self, scenario_id):
        """
        启动scenario
        """
        try:
            params = {'scenarioid': scenario_id, "appid": self.app_id, 'enable': 'true'}
            req = Request('POST', self.query_scenarios_url, headers=self.headers, params=params)
            resp = self.sess.send(req.prepare(), verify=False, timeout=2)
            if resp is None or resp.status_code != 200:
                log.error("te: 启用scenario【" + scenario_id + "】失败。")
                return False
            return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.query_scenarios_url, traceback.format_exc())
            log.error('te: 启用scenario【' + scenario_id + '】失败， 原因: ' + msg)
        return False

    def _disable_scenario(self, scenario_id):
        """
        停用scenario
        """
        try:
            params = {'scenarioid': scenario_id, "appid": self.app_id, 'enable': 'false'}
            req = Request('POST', self.query_scenarios_url, headers=self.headers, params=params)
            resp = self.sess.send(req.prepare(), verify=False, timeout=2)
            if resp is None or resp.status_code != 200:
                log.error("te: 停用scenario【" + scenario_id + "】失败。")
                return False
            return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.query_scenarios_url, traceback.format_exc())
            log.error('te: 停用scenario【' + scenario_id + '】失败， 原因: ' + msg)
        return False

    def _public_scenario(self, scenario_id):
        """
        发布scenario
        """
        try:
            params = {'scenarioid': scenario_id, "appid": self.app_id, 'publish': 1}
            req = Request('PUT', self.query_scenario_info_url, headers=self.headers, params=params)
            resp = self.sess.send(req.prepare(), verify=False, timeout=2)
            if resp is None or resp.status_code != 200:
                log.error("te: 发布scenario【" + scenario_id + "】失败。")
                return False
            return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.query_scenario_info_url, traceback.format_exc())
            log.error('te: 发布scenario【' + scenario_id + '】失败， 原因: ' + msg)
            return False
        finally:
            time.sleep(1)

    def _create_scenario(self, scenario_name):
        """
        新建scenario
        """
        try:
            params = {"scenarioName": scenario_name, "template": '', "appid": self.app_id, "type": 0}
            req = Request('POST', self.query_scenario_info_url, headers=self.headers, params=params)
            resp = self.sess.send(req.prepare(), verify=False, timeout=2).json()
            return resp['template']['metadata']
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.query_scenario_info_url, traceback.format_exc())
            log.error('te: 新建scenario【' + scenario_name + '】失败， 原因: ' + msg)
        return None

    def _del_scenarios(self, scenario_id):
        """
        删除scenario
        """
        try:
            params = {"scenarioid": scenario_id, "delete": 1}
            req = Request('PUT', self.query_scenario_info_url, headers=self.headers, params=params)
            resp = self.sess.send(req.prepare(), verify=False, timeout=2)
            if resp is None or resp.status_code != 200:
                log.error("te: 删除scenario【" + scenario_id + "】失败。")
                return False
            return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.query_scenario_info_url, traceback.format_exc())
            log.error('te: 删除scenario【' + scenario_id + '】失败， 原因: ' + msg)

        return False

    def _get_scenariojson_from_path(self, path):
        """
        获取从路径中json
        """
        try:
            with open(path, encoding='utf-8-sig', errors='ignore') as f:
                data = json.load(f, strict=False)
                if type(data) is list:
                    return data[0]
                elif type(data) is dict:
                    return data
        except Exception:
            return None

    def _get_taskengine_json(self, txt, app_id):
        """
        生成scenario对话json
        """
        te_json = {}
        text_conversion = {'text_simplified': txt, 'text_traditional': txt}
        te_json["TextConversion"] = text_conversion
        te_json["Text"] = txt
        te_json["UserID"] = Config.user_id
        te_json["ExtendData"] = {}
        te_json["SessionID"] = Config.session_id
        te_json["UniqueID"] = Config.user_id + Config.session_id
        te_json["AppID"] = app_id
        config = {"webapi_timeout": 1000}
        te_json["Config"] = config
        return te_json

    def get_taskengine_scenario_id(self, scenario_name):
        try:
            scenario_list = self._query_scenarios() or []
            scenario = list(filter(lambda x: x['scenarioName'] == scenario_name, scenario_list))
            if len(scenario) > 0:
                return scenario[0]['scenarioID']
        except Exception:
            return None
