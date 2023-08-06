import json
import copy
import os
import traceback
import qrcode
# import qrcode_terminal
import uuid
from .. import util

from ..caller.dialogue_manager_caller import DialogueManagerCaller
from ..config import Config
from ..core.module import Module
from ..entity.exception import BfEngineException
from ..logger import log
from .task_engine import TaskEngine

module_name_map = {
    "qa": "faq",
    "kg": "domain_kg",
    "te": "task_engine",
    "chat": "chat",
    "remote_skill": "remote_skill",
    "backfill": "backfill"
}
module_template = {
    "ccs_id": "",
    "name": "",
    "url": "",
    "app_id": "",
    "modules": [],
    "request_header": "",
    "request_body": "",
    "active": True,
    "timeout": 3500,
    "scenario_id": "",
    "subscribeKeys": {},
    "publishKeys": {}
}
arg_template = {
    "ccs_id": "",
    "name": "",
    "path": "",
    "value": ""
}
model_template = {
    "ccs_id": "",
    "name": "",
    "url": "",
    "method": "post",
    "category": "external",
    "request_body": "",
    "request_header": "",
    "app_id": ""
}

phase_template = {
    "phase_id": "",
    "action_rules": [],
    "group": [],
    "dispatcher": {"applyCurTask": False, "applyPreTask": False, "dispatchers": []},
    "score_rules": [],
    "respond_rules": [],
    "priority_rules": [],
    "thresholds": [],
    "bots": [],
    "models": [],
    "actions": []
}

phase_group_template = {"name": "", "flowMode": "ALL", "bots": []}
phase_dispatcher_template = {"exclusive": False, "filter": {"op": "and", "operands": []}, "groups": []}

dispatcher_operands_template = {
    "op": "",
    "operand1": {
        "op": "select",
        "path": ""
    },
    "operand2": ""
}

threshold_template = {
    "condition": {},
    "threshold": 60,
    "bot": ""
}
config_template = {
    "ccs_id": "",
    "confid": 2020,
    "name": "dialogue_manager_config",
    "status": "active",
    "ranker": {"respond_rules": [], "priority_rules": [], "score_rules": [], "bots": []},
    "chat_config": {"chat_config": {"dispatchers": []}, "bots": [], "models": []},
    "workflow": []
}
init_models = [
    {
        "uid": "intent_model",
        "ccs_id": "",
        "name": "意图",
        "url": "http://172.17.0.1:9090//intent/predict",
        "method": "post",
        "category": "external",
        "request_body": {
            "text": "$.request.body.text",
        },
        "request_header": {
            "app_id": ""
        },
        "app_id": ""
    }
]
init_args = [
    {
        "uid": "intent_arg",
        "ccs_id": "",
        "name": "$intent",
        "path": "$.model.意图.data.text",
        "value": ""
    }
]
append_modules = ["remote_skill", "chat", "backfill"]


class ConfigGenerator:
    @staticmethod
    def get_init_models(app_id, url=None):
        models = copy.deepcopy(init_models)
        for model in models:
            request_header = model.get('request_header')
            request_body = model.get('request_body')
            model['ccs_id'] = app_id
            model['app_id'] = app_id
            if url is not None:
                model['url'] = url
            if type(request_header) == dict:
                model['request_header']['app_id'] = app_id
                model['request_header'] = json.dumps(request_header)
            if type(request_body) == dict:
                model['request_body']['Robot'] = app_id
                model['request_body'] = json.dumps(request_body)
        return models

    @staticmethod
    def get_module(module: str, app_id: str, url: str, request_header: dict = {}, request_body: dict = {}):
        module = module_name_map[module]
        name = util.random_uuid()
        module_object = copy.deepcopy(module_template)
        module_object['ccs_id'] = app_id
        module_object['name'] = name
        module_object['url'] = url
        module_object['app_id'] = app_id
        module_object['modules'].append(module)
        module_object['request_header'] = json.dumps(request_header)
        module_object['request_body'] = json.dumps(request_body)
        return module_object

    @staticmethod
    def get_model(app_id: str, name: str, url: str, request_header: dict, request_body: dict, method='post',
                  category='external'):
        assert name and url
        model = copy.deepcopy(model_template)
        model['ccs_id'] = app_id
        model['app_id'] = app_id
        model['name'] = name
        model['method'] = method
        model['url'] = url
        model['request_header'] = json.dumps(request_header, indent=2)
        model['request_body'] = json.dumps(request_body, indent=2)
        model['category'] = category
        return model

    @staticmethod
    def get_arg(app_id: str, name: str, json_path: str):
        arg = copy.deepcopy(arg_template)
        arg['name'] = name
        arg['ccs_id'] = app_id
        arg['path'] = json_path
        return arg

    @staticmethod
    def get_config(app_id: str):
        config = copy.deepcopy(config_template)
        config['ccs_id'] = app_id
        return config

    @staticmethod
    def get_phase():
        return copy.deepcopy(phase_template)

    @staticmethod
    def get_phase_group():
        return copy.deepcopy(phase_group_template)

    @staticmethod
    def get_phase_dispatcher():
        return copy.deepcopy(phase_dispatcher_template)

    @staticmethod
    def get_dispatcher_operand(arg_value, path, condition='eq'):
        operand = copy.deepcopy(dispatcher_operands_template)
        operand['op'] = condition
        operand['operand1']['path'] = path
        operand['operand2'] = arg_value
        return operand

    @staticmethod
    def get_threshold(module_name: str, threshold_score: int):
        threshold = copy.deepcopy(threshold_template)
        threshold['bot'] = module_name
        threshold['threshold'] = threshold_score
        return threshold

    @staticmethod
    def get_score_rule(module_name: str, score: int):
        return {
            "adjustment": str(score),
            "condition": {},
            "unit": module_name,
            "id": util.random_uuid()
        }


class DialogueManager(Module):
    """
    对话管理
    """

    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'dm', set)
        self.app_id = app_id
        self.module_call_url = '{}/{}'.format(Config.base_url, Config.robot_url)
        self.chat_url = '{}/{}?appId={}'.format(Config.base_url, Config.chat_url, app_id)
        self.caller = DialogueManagerCaller(app_id)
        tmp_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.default_dm_config_path = tmp_dir + "/data/default_dm.json"
        self.task_engine_service = TaskEngine(app_id, set, init)
        if init:
            self.init()

    def init(self):
        self.load()

    """
    加载对话管理配置，不传配置数据则加载默认配置
    
    """

    def load(self, data: dict = None, path: str = None):
        try:

            if not data and path:
                data = json.load(open(path))
            elif not data:
                data = json.load(open(self.default_dm_config_path))
            config = self._config_generate(data)
            return self.caller.load_config(config)
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error("dm: 加载对话配置异常")
            log.error(e)
            traceback.print_exc()
            return False

    def load_by_path(self, config_path: str = None):
        simple_phases = json.load(open(config_path))
        if not config_path:
            simple_phases = json.load(open(self.default_dm_config_path))
        return self.load(simple_phases)

    """
    根据传入参数生成出话配置
    """

    def _config_preprocess(self, phases):
        modules = []
        for phase in phases:
            for module_name, module_strategy in phase.items():
                assert module_name in module_name_map, 'module just accept in [te, kg, qa]'
                module_object = ConfigGenerator.get_module(module_name, self.app_id, self.module_call_url)
                if type(module_strategy) == dict:
                    module_strategy['module_name'] = module_object['name']
                    if module_name == 'te' and 'name' in module_strategy:
                        scenario_name = module_strategy['name']
                        if scenario_name:
                            scenario_id = self.task_engine_service.get_taskengine_scenario_id(scenario_name)
                            assert scenario_id, 'te scenario name [{}] not found'.format(scenario_name)
                            module_object['scenario_id'] = scenario_id
                elif type(module_strategy) == int:
                    phase[module_name] = {
                        'threshold': int(module_strategy),
                        'module_name': module_object['name']
                    }
                if 'threshold' not in phase[module_name]:
                    phase[module_name]['threshold'] = 60
                modules.append(module_object)
        return modules

    def _config_generate(self, data):
        workflow = []
        simple_phases = data
        args = copy.deepcopy(init_args)
        arg_map = {
            arg['name']: arg
            for arg in args
        }
        modules = self._config_preprocess(simple_phases)
        config = ConfigGenerator.get_config(self.app_id)
        config['workflow'] = workflow

        # 现在只有预置模型服务
        models = ConfigGenerator.get_init_models(self.app_id)
        init_module_name_map = {}
        # 增加预置的模块
        for init_module in append_modules:
            init_module_module_object = ConfigGenerator.get_module(init_module, self.app_id, self.module_call_url)
            init_module_name_map[init_module] = init_module_module_object
            modules.append(init_module_module_object)

        # current task for te
        init_phase = ConfigGenerator.get_phase()
        init_phase['phase_id'] = util.random_uuid()
        init_phase['dispatcher']['applyCurTask'] = True
        init_phase['bots'] = modules
        for module in modules:
            if "task_engine" in module['modules']:
                threshold = ConfigGenerator.get_threshold(module['name'], 90)
                init_phase['thresholds'].append(threshold)
        workflow.append(init_phase)

        for simple_phase in simple_phases:
            phase = ConfigGenerator.get_phase()
            for phase_module in simple_phase.keys():
                module_condition = simple_phase[phase_module]
                threshold_score = module_condition['threshold']
                group = ConfigGenerator.get_phase_group()
                group_name = util.random_uuid()
                group['name'] = group_name
                group['bots'].append(module_condition['module_name'])
                phase['group'].append(group)

                dispatcher = ConfigGenerator.get_phase_dispatcher()
                dispatcher['groups'].append(group_name)
                phase['dispatcher']['dispatchers'].append(dispatcher)
                if 'condition' in module_condition:
                    condition = module_condition['condition']
                    for arg_key in condition:
                        if arg_key in arg_map:
                            path = arg_map[arg_key]['path']
                            operand = ConfigGenerator.get_dispatcher_operand(condition[arg_key], path)
                            dispatcher['filter']['operands'].append(operand)
                        else:
                            log.warning("arg {} not found".format(arg_key))

                threshold = ConfigGenerator.get_threshold(module_condition['module_name'], threshold_score)
                phase['thresholds'].append(threshold)

            phase['phase_id'] = util.random_uuid()

            phase['bots'] = modules
            phase['models'] = models
            workflow.append(phase)
        # 附加 当前多轮 追问出话策略
        task_engine_rewind_phase = ConfigGenerator.get_phase()
        task_engine_rewind_phase['phase_id'] = util.random_uuid()
        task_engine_rewind_phase['dispatcher']['applyCurTask'] = True
        task_engine_rewind_phase['bots'] = modules
        for module in modules:
            if "task_engine" in module['modules']:
                threshold = ConfigGenerator.get_threshold(module['name'], 75)
                task_engine_rewind_phase['thresholds'].append(threshold)
        workflow.append(task_engine_rewind_phase)

        # 附加预置模块
        for init_module in append_modules:
            append_phase = ConfigGenerator.get_phase()
            append_phase['phase_id'] = util.random_uuid()
            append_phase['bots'] = modules
            group = ConfigGenerator.get_phase_group()
            group_name = util.random_uuid()
            group['name'] = group_name
            group['bots'].append(init_module_name_map[init_module]['name'])
            append_phase['group'].append(group)
            backfill_dispatcher = ConfigGenerator.get_phase_dispatcher()
            backfill_dispatcher['groups'].append(group_name)
            append_phase['dispatcher']['dispatchers'].append(backfill_dispatcher)
            if init_module == 'backfill':
                append_phase['score_rules'].append(ConfigGenerator.get_score_rule(init_module_name_map[init_module]['name'], 90))
            workflow.append(append_phase)

        return config

    def qrcode(self, filePath: str = None):
        if filePath:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
            qr.add_data(self.chat_url)
            qr.make(fit=True)
            img = qr.make_image()
            img.save(filePath)
        else:
            return
            # qrcode_terminal.draw(self.chat_url)

    def query(self, msg):
        try:
            answer = self.caller.call(msg)
            return answer
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception:
            log.error("dm: 出话异常")
            traceback.print_exc()
            return False

    """
    检查传入配置
    """

    def _check_config(self):
        # todo check model arg module repeat name
        pass
