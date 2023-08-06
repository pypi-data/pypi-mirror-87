import os
import random
import time
import traceback
import copy

from tqdm import tqdm

from .module import Module
from ..caller.knowledge_caller import KnowledgeGraphCaller
from ..entity.exception import BfEngineException
from ..logger import log

data_template = {
    "data": {
        "entities": [],
        "properties": [],
        "entity_properties": [],
        "synonyms": {"entity": [], "property": [], "value": []},
        "introductions": {"property": [], "entity": {"synonyms": [], "corpus": [], "introduction": []}},
        "values": []
    }
}

entity_template = {
    "id": -1,
    "name": "",
    "sub_entities": [
    ],
    "relation": "has_a"
}
property_template = {
    "id": -1,
    "name": "",
    "corpus": [
    ],
    "type": "文本",
    "unit": "",
    "speech": ""
}
value_template = {
    "id": -1,
    "entity": "",
    "property": "",
    "value": ""
}


class DataGenerator:

    @staticmethod
    def generate_data(raw_data: dict, caller: KnowledgeGraphCaller):
        kg_data = copy.deepcopy(data_template)
        entities = []
        entity_name_set = set()
        property_name_set = set()
        properties = []
        values = []
        kg_data['data']['entities'] = entities
        kg_data['data']['properties'] = properties
        kg_data['data']['values'] = values
        if raw_data and raw_data['data']:
            datas = raw_data['data']
            for data in datas:
                entity_name = data.get('entity')
                if entity_name not in entity_name_set:
                    entity_dict = DataGenerator._get_entity(entity_name)
                    entities.append(entity_dict)
                    entity_name_set.add(entity_name)
            for data in datas:
                property_name = data.get('property')
                value = data.get('value')
                unit = data.get('unit')
                if value in entity_name_set:
                    entity_type = True
                else:
                    value_entity = caller.load_entity(0, value)
                    if value_entity is not None and value_entity.get('type') == 1:
                        entity_type = True
                    else:
                        entity_type = False
                property_dict = DataGenerator._get_property(property_name, entity_type, unit)
                properties.append(property_dict)
                property_name_set.add(property_name)

            for data in datas:
                entity_name = data.get('entity')
                property_name = data.get('property')
                value = data.get('value')
                value_dict = DataGenerator._get_value(entity_name, property_name, value)
                values.append(value_dict)
        return kg_data

    @staticmethod
    def _get_property(property_name, entity_type, unit):
        if entity_type and unit is not None:
            log.error(property_name + '实体类型属性不能有单位')
        property_dict = copy.deepcopy(property_template)
        property_dict['name'] = property_name
        property_dict['corpus'].append("的" + property_name)
        if entity_type:
            property_dict['type'] = '实体'
        elif unit:
            property_dict['unit'] = unit
            property_dict['type'] = '数值'
        elif len(property_name) <= 20:
            property_dict['type'] = '关键字'
        return property_dict

    @staticmethod
    def _get_entity(entity_name):
        entity_dict = copy.deepcopy(entity_template)
        entity_dict['name'] = entity_name
        return entity_dict

    @staticmethod
    def _get_value(entity_name, property_name, value):
        value_dict = copy.deepcopy(value_template)
        value_dict['entity'] = entity_name
        value_dict['property'] = property_name
        value_dict['value'] = value
        return value_dict


class KnowledgeGraph(Module):
    """
    知识图谱
    """

    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'kg', set)
        self.caller = KnowledgeGraphCaller(app_id)
        if init:
            self.init()

    def init(self):
        try:
            self.caller.init_data()
        except Exception:
            log.warning('kg: fail to init')

    # 下面是 second version 增量训练

    def add_triple_value(self, data: dict) -> bool:
        """
        增量批量添加三元组数值
        :param data: 三元组数据
        "return: 添加是否成功
        """
        try:
            log.info('kg: batch add triple')
            # 整理数据
            data = DataGenerator.generate_data(data, self.caller)
            self._upload_triple_value(data)

        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error("kg: batch add triple error")
            log.error(e)
            traceback.print_exc()
            return False

    def add_intro(self, data: dict) -> bool:
        """
        增量批量添加实体和属性简介
        :param data: 简介数据格式 {type, name, intro}
        "return: 添加是否成功
        """
        try:
            log.info('kg: batch add intro')
            # 整理数据
            for single in data['data']:
                if single['type'] == 'entity':
                    entity = self.caller.load_entity(0, single['name'])
                    if entity is not None:
                        result = self.caller.update_entity_intro(entity.get('id'), single['intro'])
                        if not result:
                            log.error("更新实体简介失败：" + single['name'])
                elif single['type'] == 'property':
                    property = self.caller.load_property(single['name'])
                    if property is not None:
                        result = self.caller.update_property_intro(property.get('id'), single['intro'])
                        if not result:
                            log.error("更新属性简介失败：" + single['name'])
            return True
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error("kg: batch add intro error")
            log.error(e)
            traceback.print_exc()
            return False

    def add_property_corpus(self, data: dict) -> bool:
        """
        增量批量添加属性语料
        :param data: 语料数据格式 {name, corpus}
        "return: 添加是否成功
        """
        try:
            log.info('kg: batch add property corpus')
            # 整理数据
            for single in data['data']:
                property = self.caller.load_property(single['name'])
                if property is not None:
                    result = self.caller.add_property_corpus(property, single['corpus'])
                    if not result:
                        log.error("添加属性语料失败：" + single['name'])
            return True
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error("kg: batch add property corpus error")
            log.error(e)
            traceback.print_exc()
            return False

    def update_property_speech(self, data: dict) -> bool:
        """
        增量批量添加属性语料
        :param data: 语料数据格式 {name, speech}
        "return: 添加是否成功
        """
        try:
            log.info('kg: batch add property speech')
            # 整理数据
            for single in data['data']:
                property = self.caller.load_property(single['name'])
                if property is not None:
                    result = self.caller.update_property_speech(property, single['speech'])
                    if not result:
                        log.error("更新属性话术失败：" + single['name'])
            return True
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error("kg: batch update property speech error")
            log.error(e)
            traceback.print_exc()
            return False

    def add_word_synonym(self, word_name: str, synonym: list):
        return self.caller.add_word_synonym(word_name, synonym)

    def update_word_synonym(self, word_name: str, synonym: list):
        return self.caller.update_word_synonym(word_name, synonym)

    def delete_word_synonym(self, word_name):
        return self.caller.delete_word_synonym(word_name)

    def get_word_synonym(self, word_name):
        return self.caller.get_word_synonym(word_name)

    def publish(self):
        """
        发布KG 从线下到线上
        :return: 训练是否成功
        """
        try:
            self._sync_with_bar()
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error("kg: 发布异常")
            log.error(e)
            traceback.print_exc()
            return False

    # 下面是 first version
    def train(self, data: dict = None, path: str = None) -> bool:
        """
        训练kg  传入data(json) 或者 path(数据文件) 同时传入优先取data

        如果已经导入过数据， data和path可以为空， 表示直接开始训练
        :param path: 导入文件的路径
        :param data: 训练数据
        :return: 训练是否成功
        """
        try:
            log.info('kg: prepare train')
            if data is not None:
                data = DataGenerator.generate_data(data, self.caller)
                self._upload_data(data)
            elif path is not None:
                if os.path.exists(path):
                    self._upload_file(path, True)
                else:
                    log.warning('file not fond in path ' + path)
                    return False
            self._train()
            self.caller.sync_data()
            time.sleep(2)
            if data is not None or path is not None:
                self._sync()
            return True
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error("kg: 训练异常")
            log.error(e)
            traceback.print_exc()
            return False

    def train_by_path(self, data_path: str, use_old: bool = None) -> bool:
        """
        训练kg
        :param data_path: 训练数据文件路径
        :return: 训练是否成功
        """
        try:
            self._upload_file(data_path, use_old)
            self._train()
            self._sync()
            return True
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error("kg: 训练异常")
            log.error(e)
            traceback.print_exc()
            return False

    def _upload_data(self, data):
        # log.info("kg: 开始上传训练数据")
        self.caller.load_data(data)
        # log.info("kg: 训练数据上传成功")

    def _upload_file(self, file_path, use_old):
        # log.info("kg: 开始上传训练数据")
        self.caller.load_file(file_path, use_old)
        # log.info("kg: 训练数据上传成功")

    def _upload_triple_value(self, data):
        # log.info("kg: upload triple value")
        # 更新实体
        for entity in data['data']['entities']:
            result = self.caller.load_entity(0, entity['name'])
            if result is None:
                entity_id = self.caller.add_entity(entity['name'])
                if -1 == entity_id:
                    log.error(self, entity + '实体新增失败')
                    continue
            else:
                entity_id = result.get('id')
            entity['id'] = entity_id
        # 更新属性
        i = 0
        for property in data['data']['properties']:

            if property['type'] == '关键字':
                category = 5
            elif property['type'] == '文本':
                category = 2
            elif property['type'] == '数值':
                category = 3
            elif property['type'] == '实体':
                category = 1

            result = self.caller.load_property(property['name'])
            if result is None:
                property_id = self.caller.add_property(property['name'], category, property['unit'])
                if -1 == property_id:
                    log.error(self, property + '属性新增失败')
                    continue
            else:
                property_id = result.get('id')
                # 更新补充属性：
                if str(category) != result.get('category') or property['unit'] != result.get('unit'):
                    entity = data['data']['entities'][i]
                    extra_property = self.caller.load_extra_property(property['name'], entity['name'])
                    if extra_property is None:
                        result = self.caller.add_extra_property(property_id, entity['id'], category,
                                                                property['unit'])
                        if not result:
                            log.error(
                                'kg: add extra property failed, entity=' + entity['name'] + ', property=' + property[
                                    'name'])
                    else:
                        result = self.caller.update_extra_property(property['name'], entity['name'], category,
                                                                   property['unit'])
                        if not result:
                            log.error(
                                'kg: add extra property failed, entity=' + entity['name'] + ', property=' + property[
                                    'name'])
            property['id'] = property_id
            i+=1
        # 更新值
        for entity_property in data['data']['values']:
            entity = self.caller.load_entity(0, entity_property['entity'])
            property = self.caller.load_property(entity_property['property'])
            # 实体类型怎么处理
            relation = self.caller.load_value(entity.get('id'), property.get('id'))
            if not relation:
                value_id = None
                if property.get('category') == '1':
                    value_entity = self.caller.load_entity(0, entity_property['value'])
                    if value_entity:
                        value_id = value_entity.get('id')
                value = entity_property['value']
                self.caller.add_value(entity, property, value_id, value)
            # else:
            #     self.caller.update_value(relation.get('id'), entity, property, relation.get('idTo'), entity_property['value'])
        # log.info("kg: upload triple value success")

    def _train(self):
        log.info("kg: start training")
        self.caller.trigger_train()
        progress = 0
        completed = False
        with tqdm(total=100) as bar:
            bar.set_description("kg training...")
            while not completed:
                completed = self.caller.status('train')
                if progress < 100:
                    inc = random.randint(1, 4)
                    bar.update(inc)
                    progress += inc
                time.sleep(1)
            bar.update(100 - progress)
            bar.set_description("kg train finished")

    def _sync(self):
        # log.info("kg: 开始同步数据")
        self.caller.sync_sandbox()
        # log.info("kg: 同步成功")
        time.sleep(2)
        completed = False
        while not completed:
            completed = self.caller.status('sync')
            # log.info('kg: 数据同步中..')
            time.sleep(1)
        # log.info("kg: 同步出话层数据")
        self.caller.sync_data()
        # log.info("kg: 同步成功")
        time.sleep(2)

    def _sync_with_bar(self):
        log.info("kg: start publishing")
        # log.info("kg: 开始同步数据")
        self.caller.sync_sandbox()
        # log.info("kg: 同步成功")
        time.sleep(2)
        progress = 0
        completed = False
        with tqdm(total=100) as bar:
            bar.set_description("kg publishing...")
            while not completed:
                completed = self.caller.status('sync')
                if progress < 100:
                    inc = random.randint(1, 4)
                    bar.update(inc)
                    progress += inc
                time.sleep(1)
            self.caller.sync_data()
            time.sleep(2)
            bar.update(100 - progress)
            bar.set_description("kg publish finished")

    # 预测出话
    def query(self, text, online: bool = None):
        """
        :param msg: 用户问
        :online: 线上 True 线下 False
        :return: 机器人回答
        """
        return self.caller.call(text, online)