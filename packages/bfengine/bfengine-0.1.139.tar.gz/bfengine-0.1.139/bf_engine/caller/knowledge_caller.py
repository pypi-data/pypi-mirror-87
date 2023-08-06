import logging
import traceback

import requests
from ..config import Config
from .base import CallerBase
from ..entity.answer import Answer
from ..entity.exception import BfEngineException, ErrorCode
from ..logger import log as logging


class KnowledgeGraphCaller(CallerBase):
    """
    知识图谱
    """

    def __init__(self, app_id):
        super().__init__(app_id)
        # 导入数据
        self.app_id = app_id
        base_url = Config.base_url
        self.data_load_url = '{}/xeonKgDal/{}/importJson'.format(base_url, app_id)
        # 触发异步训练
        self.trigger_train_url = '{}/xeonKgDal/{}/ftTrainTrigger?env=sandbox'.format(base_url, app_id)
        # 通知出话层更新数据
        self.sync_data_url = '{}/api/v1/kbqa/syncData?appid={}'.format(base_url, app_id)
        # 线下数据同步到线上
        self.sync_sandbox_url = '{}/xeonKgDal/{}/synchronizeSandbox'.format(base_url, app_id)
        # 预测出话接口
        self.predict_url = '{}/api/v1/kbqa'.format(base_url)
        # 获取训练结果
        self.train_status_url = '{}/xeonKgDal/syncHandler/{}/getSyncRecord'.format(base_url, app_id)

        self.file_load_url = '{}/xeonKgDal/{}/import/all'.format(base_url, app_id)
        self.new_file_load_url = '{}/xeonKgDal/{}/import/all/v1'.format(base_url, app_id)
        # 检查实体是否重复
        self.check_entity_repeat_url \
            = '{}/xeonKgDal/entityManager/{}/checkRepeat/entity?entityName={}&entityId=&entityType=1'
        # 获取实体 app_id, parent_entity_id, keyword
        self.load_entity_url \
            = '{}/xeonKgDal/entityProfile/{}/showEntityProfileDetail/{}?page=1&entityListKeyword={}'
        # 新增一级实体
        self.add_entity_url = '{}/xeonKgDal/entityManager/{}/addEntity/root'.format(base_url, app_id)
        # 获取属性
        self.load_property_url = '{}/xeonKgDal/{}/property/allCommon?page=1&keyword={}'
        # 新增屬性
        self.add_property_url = '{}/xeonKgDal/{}/property'.format(base_url, app_id)
        # 查询属性值
        self.load_relation_url = '{}/xeonKgDal/relation/{}/getDataOverViewRelationByRootEntity/{}?page=1&limit=20&entityListKeyword='
        # 新增属性值
        self.add_relation_url = '{}/xeonKgDal/relation/{}/addRelation'.format(base_url, app_id)
        # 更新属性值
        self.update_relation_url = '{}/xeonKgDal/relation/{}/updateRelation'.format(base_url, app_id)
        # 更新实体简介
        self.update_entity_intro_url = '{}/xeonKgDal/entityProfile/{}/addEntityProfile/{}'
        # 更新属性简介
        self.update_property_intro_url = '{}/xeonKgDal/{}/property/desc'.format(base_url, app_id)
        # 添加属性语料
        self.add_property_corpus_url = '{}/xeonKgDal/{}/property/{}'
        # 查询特殊属性
        self.load_extra_property_url = '{}/xeonKgDal/extraPropertyManager/{}/getAll?page=1&keyword={}&limit=10'
        # 更新特殊属性
        self.update_extra_property_url = '{}/xeonKgDal/extraPropertyManager/{}/update'.format(base_url, app_id)

        # 词库 新增同义词 实体/属性
        self.wordbank_add_url = '{}/xeonKgDal/synonym/{}/addSynonym'.format(base_url, app_id) + "/{}?type={}"
        # 词库 更新同义词 实体/属性
        self.wordbank_update_url = '{}/xeonKgDal/synonym/{}/updateSynonym'.format(base_url,
                                                                                  app_id) + "/{}?type={}"
        # 词库 删除同义词 实体/属性
        self.wordbank_delete_url = '{}/xeonKgDal/synonym/{}/deleteSynonym'.format(base_url,
                                                                                  app_id) + "/{}?type={}"
        # 词库 查询同义词 实体/属性
        self.wordbank_get_url = '{}/xeonKgDal/synonym/{}/showSynonym'.format(base_url,
                                                                             app_id) + "?show=matchId&type={}&object_id={}"

        # 词库 新增值同义词
        self.wordbank_value_add_url = '{}/xeonKgDal/propertyKeyword/{}/addKeywordSynonym'.format(base_url, app_id)
        # 词库 更新值同义词
        self.wordbank_value_update_url = '{}/xeonKgDal/propertyKeyword/{}/updateKeywordSynonym'.format(base_url,
                                                                                                       app_id)
        # 词库 删除同义词
        self.wordbank_value_delete_url = '{}/xeonKgDal/propertyKeyword/{}/deleteKeywordSynonym'.format(base_url,
                                                                                                       app_id)
        # 词库 查询值同义词
        self.wordbank_value_get_url = '{}/xeonKgDal/propertyKeyword/{}?target=getAll'.format(base_url, app_id)

        # 初始知识库
        self.init_url = '{}/xeonKgDal/property/{}/initialProperty'.format(base_url, app_id)

    def init_data(self):
        """
        出话kg知识库
        :param data: kg数据
        """
        response = requests.get(self.init_url)
        if self._response_failed(response):
            msg = "kg: 初始化数据失败：原因: 接口异常。" + str(response.json()) if response is not None else ''
            raise BfEngineException(ErrorCode.kg_init_error, msg)


    def load_data(self, data: dict):
        """
        加载json格式训练数据
        :param data: kg数据
        """
        try:
            response = requests.post(self.data_load_url, json=data)
            if self._response_failed(response):
                msg = "kg: 上传训练数据失败：原因: 上传数据接口异常。" + str(response.json()) if response is not None else ''
                raise BfEngineException(ErrorCode.kg_import_error, msg)
        except BfEngineException as bfe:
            raise bfe
        except Exception:
            msg = "kg: 上传数据失败， 原因: Exception When POST '{}' : {}".format(self.data_load_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.kg_import_error, msg)

    def load_file(self, file_path: str, use_old):
        """
        加载文件格式训练数据
        :param file_path: kg数据文件路径
        """
        try:
            files = {"file": (open(file_path, 'rb'))}
            file_load_url = self.new_file_load_url
            if use_old is not None and use_old:
                file_load_url = self.file_load_url
            response = requests.post(file_load_url, files=files)
            if self._response_failed(response):
                msg = "kg: 上传训练数据失败：原因: 上传数据接口异常。" + str(response.json()) if response is not None else ''
                raise BfEngineException(ErrorCode.kg_import_error, msg)
        except BfEngineException as bfe:
            raise bfe
        except Exception:
            msg = "kg: 上传数据失败， 原因: Exception When POST '{}' : {}".format(self.data_load_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.kg_import_error, msg)

    def trigger_train(self):
        """
        触发训练 异步
        """
        try:
            response = requests.get(url=self.trigger_train_url)
            if self._response_failed(response):
                msg = "kg: 触发训练失败：原因: 接口异常。" + str(response.json()) if response is not None else ''
                raise BfEngineException(ErrorCode.kg_train_error, msg)
        except BfEngineException as bfe:
            raise bfe
        except Exception:
            msg = "kg: 触发训练失败， 原因: Exception When POST '{}' : {}".format(self.trigger_train_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.kg_import_error, msg)

    def sync_data(self):
        """
        同步出话层数据
        """
        try:
            response = requests.get(url=self.sync_data_url)
            if self._response_failed(response):
                msg = "kg: 同步出话层数据：原因: 接口异常。" + str(response.json()) if response is not None else ''
                raise BfEngineException(ErrorCode.kg_train_error, msg)
        except BfEngineException as bfe:
            raise bfe
        except Exception:
            msg = "kg: 同步出话层数据， 原因: Exception When POST '{}' : {}".format(self.sync_data_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.kg_train_error, msg)

    def sync_sandbox(self):
        """
        同步数据至线上
        """
        try:
            response = requests.post(url=self.sync_sandbox_url)
            if self._response_failed(response):
                msg = "kg: 同步数据失败：原因: 接口异常。" + str(response.json()) if response is not None else ''
                raise BfEngineException(ErrorCode.kg_train_error, msg)
        except BfEngineException as bfe:
            raise bfe
        except Exception:
            msg = "kg: 同步数据失败， 原因: Exception When POST '{}' : {}".format(self.trigger_train_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.kg_train_error, msg)

    def status(self, wait_type):
        """
        等待中 并记录日志
        :param wait_type: train | sync
        :return: 是否成功
        """
        try:
            response = requests.get(url=self.train_status_url)
            if self._response_failed(response):
                msg = "kg: 获取状态失败：原因: 接口异常。" + str(response.json()) if response is not None else ''
                raise BfEngineException(ErrorCode.kg_train_error, msg)

            data = response.json().get('data')
            if data:
                train_status = data.get('trainingStatus')
                sync_status = data.get('syncStatus')
                if wait_type == 'train' and train_status == 2:
                    return True
                if wait_type == 'sync' and sync_status == 2:
                    return True
            return False
        except BfEngineException as bfe:
            raise bfe
        except Exception:
            msg = "kg: 获取状态失败， 原因: Exception When POST '{}' : {}".format(self.train_status_url, traceback.format_exc())
            raise BfEngineException(ErrorCode.kg_train_error, msg)

    def call(self, msg, online):
        """
        预测出话
        :param msg: 用户问
        :param online：线上 True 线下 False
        :return: 机器人回答
        """
        answer = Answer(text='', score=0)
        if online is None or online:
            env = "production"
        else:
            env = "sandbox"
        param = {
            "userid": "test",
            "sessionid": "test",
            "uniqueid": "test",
            "appid": self.app_id,
            "env": env,
            "modeltype": "ft",
            "text": msg,
            "skg": "on"
        }
        try:
            response = requests.post(url=self.predict_url, json=param)
            if self._response_failed(response):
                logging.error("kg: 预测失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('response'):
                    answer = Answer(text=response_json.get('response'), score=response_json.get('score'))
                else:
                    pass
                    # logging.warning('kg: 预测为空 [{}]'.format(msg))
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.predict_url, traceback.format_exc())
            logging.error('kg: 对话失败， 原因: ' + msg)
        finally:
            if not answer.text:
                answer.value = Config.backfill_speech
                answer.score = 60
            return answer

    def check_entity_repeat(self, name):
        """
        检查实体重复
        :param name: 实体名称
        :return: 结果
        """
        try:
            response = requests.get(self.check_entity_repeat_url.format(Config.base_url, self.app_id, name))
            if self._response_failed(response):
                logging.error("kg: 检查实体重复失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data'):
                    data = response.json().get('data')
                    if data:
                        return data.get('found')
                    else:
                        return False
                else:
                    return False
        except Exception:
            msg = "Exception When GET '{}' : {}".format(self.check_entity_repeat_url, traceback.format_exc())
            logging.error('kg: 检查实体重复失败， 原因：' + msg)
            return -1

    def load_entity(self, parent_entity_id, name):
        """
        获取实体
        :param parent_entity_id: 父实体id
        :param name: 实体名称
        :return: 结果
        """
        try:
            response = requests.get(self.load_entity_url.format(Config.base_url, self.app_id, parent_entity_id, name))
            if self._response_failed(response):
                logging.error("kg: 获取实体失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('dataDetail'):
                    data = response.json().get('dataDetail')
                    if data:
                        return data[0]
                    else:
                        return None
                else:
                    return None
        except Exception:
            msg = "Exception When GET '{}' : {}".format(self.load_entity_url, traceback.format_exc())
            logging.error('kg: 获取实体失败， 原因：' + msg)
            return -1

    def add_entity(self, name):
        """
        新增一级实体
        :param name: 实体名称
        :return: 结果
        """
        param = {
            "name": name
        }
        try:
            response = requests.post(url=self.add_entity_url, json=param)
            if self._response_failed(response):
                logging.error("kg: 新增一级实体失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data'):
                    data = response.json().get('data')
                    if data:
                        return data.get('freshEntityId')
                    else:
                        return -1
                else:
                    return -1
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.add_entity_url, traceback.format_exc())
            logging.error('kg: 新增一级实体失败， 原因：' + msg)
            return -1

    def load_property(self, name):
        """
        获取实体
        :param name: 实体名称
        :return: 结果
        """
        try:
            response = requests.get(self.load_property_url.format(Config.base_url, self.app_id, name))
            if self._response_failed(response):
                logging.error("kg: 获取属性失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data'):
                    data = response.json().get('data')
                    if data:
                        return data[0]
                    else:
                        return None
                else:
                    return None
        except Exception:
            msg = "Exception When GET '{}' : {}".format(self.load_property_url, traceback.format_exc())
            logging.error('kg: 获取属性失败， 原因：' + msg)
            return -1

    def add_property(self, name, category, unit):
        """
        新增属性
        :param name: 实体名称
        :param category: 1 entity 2 stringValue 3 integerValue(deprecated) 4 匿名实体 6 空实体 7 日期 8 浮点数
        :param unit: 单位
        :return: 结果
        """
        param = {
            "name": name,
            "corpus": [],
            "category": category,
            "unit": unit,
            "speech": "{\"answer\":\"\",\"property\":{\"dimension_id_list\":[]}}",
            "slotInfo": {
                "url": "",
                "slotList": []
            },
            "parentId": -1,
            "speechType": "201"
        }
        try:
            response = requests.post(url=self.add_property_url, json=param)
            if self._response_failed(response):
                logging.error("kg: 新增屬性失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data'):
                    data = response.json().get('data')
                    if data:
                        return data
                    else:
                        return -1
                else:
                    return -1
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.add_property_url, traceback.format_exc())
            logging.error('kg: 新增屬性失败， 原因：' + msg)
            return -1

    def load_value(self, entity_id, property_id):
        """
        获取实体
        :entity_id: 实体id
        :property_id: 属性id
        :return: 结果
        """
        try:
            response = requests.get(self.load_relation_url.format(Config.base_url, self.app_id, entity_id))
            if self._response_failed(response):
                logging.error("kg: 获取属性失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data').get('data'):
                    data = response.json().get('data').get('data')
                    if data:
                        return data[0].get('propertyValue').get('entityPropertyValueTable')[str(entity_id)][
                            str(property_id)]
                    else:
                        return None
                else:
                    return None
        except Exception:
            msg = "Exception When GET '{}' : {}".format(self.load_property_url, traceback.format_exc())
            logging.error('kg: 获取属性失败， 原因：' + msg)
            return -1

    def add_value(self, from_entity, property, to_entity_id, to_entity_name):
        """
        新增属性
        :param name: 实体名称
        :param category: 1 entity 2 stringValue 3 integerValue(deprecated) 4 匿名实体 6 空实体 7 日期 8 浮点数
        :return: 结果
        """
        category = property.get('category')
        # if category != 1:
        #     value = "{\\\"answer\\\":\\\"" + to_entity_name + "\\\",\\\"property\\\":{\\\"dimension_id_list\\\":[]}}"
        # else:
        #     value = to_entity_name
        param = {
            "fromEntityId": from_entity.get('id'),
            "fromEntityName": from_entity.get('name'),
            "propertyId": property.get('id'),
            "category": category,
            "toEntityId": [
                to_entity_id
            ],
            "toEntityName": [
                to_entity_name
            ],
            "isInheritParent": False,
            "inheritedParentEntityId": "-1",
            "subCategory": "201"
        }

        try:
            response = requests.post(url=self.add_relation_url, json=param)
            if self._response_failed(response):
                logging.error("kg: 新增值失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data'):
                    data = response.json().get('data')
                    if data:
                        return data.get('id')
                    else:
                        return -1
                else:
                    return -1
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.add_relation_url, traceback.format_exc())
            logging.error('kg: 新增值失败， 原因：' + msg)
            return -1

    def update_value(self, relation_id, from_entity, property, to_entity_id, to_entity_name):
        """
        新增属性
        :param name: 实体名称
        :param category: 1 entity 2 stringValue 3 integerValue(deprecated) 4 匿名实体 6 空实体 7 日期 8 浮点数
        :return: 结果
        """
        category = property['category']
        if category != 1:
            value = "{\"answer\":\"" + to_entity_name + "\",\"property\":{\"dimension_id_list\":[]}}"
        else:
            value = to_entity_name
        param = {
            "id": relation_id,
            "fromEntityId": from_entity['id'],
            "fromEntityName": from_entity['name'],
            "propertyId": property['id'],
            "propertyName": property['name'],
            "category": category,
            "unit": property['unit'],
            "toEntityId": [
                to_entity_id
            ],
            "toEntityName": [
                value
            ],
            "isInheritParent": False,
            "inheritedParentEntityId": "-1",
            "subCategory": "201"
        }

        try:
            response = requests.post(url=self.update_relation_url, json=param)
            if self._response_failed(response):
                logging.error("kg: 更新值失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data'):
                    data = response.json().get('data')
                    if data:
                        return data.get('id')
                    else:
                        return -1
                else:
                    return -1
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.update_relation_url, traceback.format_exc())
            logging.error('kg: 更新值失败， 原因：' + msg)

    def update_entity_intro(self, entity_id, intro):
        """
        新增实体简介
        :param intro: 实体简介
        :return: 结果
        """
        param = {
            "introduction": "[{\"type\":\"INTRODUCTION\",\"entity\":[],\"property\":[],\"value\":\"{\\\"answer\\\":\\\"" + intro + "\\\",\\\"property\\\":{\\\"dimension_id_list\\\":[]}}\",\"subCategory\":\"201\"}]"
        }

        try:
            response = requests.post(url=self.update_entity_intro_url.format(Config.base_url, self.app_id, entity_id),
                                     json=param)
            if self._response_failed(response):
                logging.error("kg: 更新实体简介失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.update_entity_intro_url, traceback.format_exc())
            logging.error('kg: 更新实体简介失败， 原因：' + msg)
            return False

    def update_property_intro(self, property_id, intro):
        """
        新增属性简介
        :property_id: 属性id
        :param intro: 属性简介
        :return: 结果
        """
        param = {
            "propertyId": property_id,
            "introduction": "[{\"type\":\"INTRODUCTION\",\"entity\":[],\"property\":[],\"value\":\"{\\\"answer\\\":\\\"" + intro + "\\\",\\\"property\\\":{\\\"dimension_id_list\\\":[]}}\",\"subCategory\":\"201\"}]"
        }
        try:
            response = requests.post(url=self.update_property_intro_url, json=param)
            if self._response_failed(response):
                logging.error("kg: 更新属性简介失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.update_property_intro_url, traceback.format_exc())
            logging.error('kg: 更新属性简介失败， 原因：' + msg)
            return False

    def add_property_corpus(self, property, corpus):
        """
        新增属性简介
        :property: 属性
        :corpus: 新增的语料
        :return: 结果
        """
        if corpus not in property.get('corpus'):
            property.get('corpus').append(corpus)
        param = {
            "name": property.get('name'),
            "corpus": property.get('corpus'),
            "category": property.get('category'),
            "unit": property.get('unit'),
            "speech": property.get('speech'),
            "parentId": -1,
            "slotInfo": {
                "url": "",
                "slotList": []
            },
            "speechType": str(property.get('speechType'))
        }
        try:
            response = requests.put(
                url=self.add_property_corpus_url.format(Config.base_url, self.app_id, property.get('id')), json=param)
            if self._response_failed(response):
                logging.error("kg: 新增属性语料失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.add_property_corpus_url, traceback.format_exc())
            logging.error('kg: 新增属性语料失败， 原因：' + msg)
            return False

    def update_property_speech(self, property, speech):
        """
        新增属性简介
        :property: 属性
        :corpus: 新增的语料
        :return: 结果
        """
        if not speech:
            return True
        param = {
            "name": property.get('name'),
            "corpus": property.get('corpus'),
            "category": property.get('category'),
            "unit": property.get('unit'),
            "speech": "{\"answer\":\"" + speech + "\",\"property\":{\"dimension_id_list\":[]}}",
            "parentId": -1,
            "slotInfo": {
                "url": "",
                "slotList": []
            },
            "speechType": str(property.get('speechType'))
        }
        try:
            response = requests.put(
                url=self.add_property_corpus_url.format(Config.base_url, self.app_id, property.get('id')), json=param)
            if self._response_failed(response):
                logging.error("kg: 更新属性话术失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.add_property_corpus_url, traceback.format_exc())
            logging.error('kg: 更新属性话术失败，原因：' + msg)
            return False

    def _get_wordbank_synonym(self, type, object_id):
        try:
            url = self.wordbank_get_url.format(type, object_id)
            response = requests.get(url=url)
            if self._response_failed(response):
                logging.error("kg: 查询同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data'):
                    return response_json.get('data')
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_get_url, traceback.format_exc())
            logging.error('kg: 查询同义词失败， 原因：' + msg)

    def add_word_synonym(self, word_name: str, synonym: list):
        """
        增加词典同义词

        :param word_name: 要添加的词条
        :param synonym: 同义词列表
        :return:
        """
        return self._add_entity_synonym(word_name, synonym) or self._add_property_synonym(word_name, synonym) or \
               self._add_value_synonym(word_name, synonym)

    def update_word_synonym(self, word_name: str, synonym: list):
        """
        更新词典同义词
        :param word_name: 要更新的词条
        :param synonym: 同义词列表
        :return:
        """
        return self._update_entity_synonym(word_name, synonym) or self._update_property_synonym(word_name, synonym) or \
               self._update_value_synonym(word_name, synonym)

    def delete_word_synonym(self, word_name: str):
        """
        删除词典词条及同义词
        :param word_name: 要删除的词条
        :return:
        """
        return self._delete_entity_synonym(word_name) or self._delete_property_synonym(word_name) or \
               self._delete_value_synonym(word_name)

    def get_word_synonym(self, word_name: str):
        """
        获取词典的同义词
        :param word_name: 要查询的词条
        :return:
        """
        return self._get_entity_synonym(word_name) or self._get_property_synonym(word_name) or \
               self._get_value_synonym(word_name)

    def _add_entity_synonym(self, entity_name: str, synonym: list):
        """
        新增实体同义词
        :param entity_name: 实体名称
        :param synonym: 实体的同义词列表
        :return:
        """
        try:
            entity_object = self.load_entity(0, entity_name)
            if entity_object is not None:
                entity_id = entity_object['id']
                entity_exist = self._get_wordbank_synonym('entity', entity_id) is not None
                if entity_exist:
                    return self._update_entity_synonym(entity_name, synonym)
                else:
                    url = self.wordbank_add_url.format(entity_id, 'entity')
                    param = {
                        "id": entity_id,
                        "synonym": synonym
                    }
                    response = requests.post(url=url, json=param)
                    if self._response_failed(response):
                        logging.error("kg: 保存实体同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
                    else:
                        return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_add_url, traceback.format_exc())
            logging.error('kg: 保存实体同义词失败， 原因：' + msg)

    def _update_entity_synonym(self, entity_name: str, synonym: list):
        """
        更新实体的同义词
        :param entity_name: 实体名称
        :param synonym: 实体同义词 列表
        :return:
        """
        try:
            entity_object = self.load_entity(0, entity_name)
            if entity_object is not None:
                entity_id = entity_object['id']
                url = self.wordbank_update_url + "/{}?type=entity".format(entity_id)
                param = {
                    "id": entity_id,
                    "synonym": synonym
                }
                response = requests.put(url=url, json=param)
                if self._response_failed(response):
                    logging.error("kg: 保存实体同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
                else:
                    return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_update_url, traceback.format_exc())
            logging.error('kg: 保存实体同义词失败， 原因：' + msg)

    def _delete_entity_synonym(self, entity_name):
        """
        删除实体的同义词
        :param entity_name: 实体名称
        :return:
        """
        try:
            entity_object = self.load_entity(0, entity_name)
            if entity_object is not None:
                entity_id = entity_object['id']
                url = self.wordbank_update_url + "/{}?type=entity".format(entity_id)
                response = requests.delete(url=url)
                if self._response_failed(response):
                    logging.error("kg: 删除实体同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
                else:
                    return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_update_url, traceback.format_exc())
            logging.error('kg: 删除实体同义词失败， 原因：' + msg)

    def _get_entity_synonym(self, entity_name):
        """
        获取实体的同义词
        :param entity_name: 实体名称
        :return:
        """
        try:
            entity_object = self.load_entity(0, entity_name)
            if entity_object is not None:
                entity_id = entity_object['id']
                return self._get_wordbank_synonym('entity', entity_id)
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_update_url, traceback.format_exc())
            logging.error('kg: 获取实体同义词失败， 原因：' + msg)

    def _add_property_synonym(self, property_name: str, synonym: list):
        """
        新增实体同义词
        :param property_name: 属性名称
        :param synonym: 属性的同义词列表
        :return:
        """
        try:
            property_object = self.load_property(property_name)
            if property_object is not None:
                property_id = property_object['id']
                property_exist = self._get_wordbank_synonym('property', property_id) is not None
                if property_exist:
                    return self._update_property_synonym(property_name, synonym)
                else:
                    url = self.wordbank_add_url.format(property_id, 'property')
                    param = {
                        "id": property_id,
                        "synonym": synonym
                    }
                    response = requests.post(url=url, json=param)
                    if self._response_failed(response):
                        logging.error("kg: 保存属性同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
                    else:
                        return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_add_url, traceback.format_exc())
            logging.error('kg: 保存属性同义词失败， 原因：' + msg)

    def _update_property_synonym(self, property_name: str, synonym: list):
        """
        更新属性的同义词
        :param property_name: 属性名称
        :param synonym: 属性同义词 列表
        :return:
        """
        try:
            property_object = self.load_property(property_name)
            if property_object is not None:
                property_id = property_object['id']
                url = self.wordbank_update_url.format(property_id, "property")
                param = {
                    "id": property_id,
                    "synonym": synonym
                }
                response = requests.put(url=url, json=param)
                if self._response_failed(response):
                    logging.error("kg: 保存属性同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
                else:
                    return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_update_url, traceback.format_exc())
            logging.error('kg: 保存属性同义词失败， 原因：' + msg)

    def _delete_property_synonym(self, property_name: str):
        """
        删除属性的同义词
        :param property_name: 属性名称
        :return:
        """
        try:
            property_object = self.load_property(property_name)
            if property_object is not None:
                property_id = property_object['id']
                url = self.wordbank_update_url.format(property_id, "property")
                response = requests.delete(url=url)
                if self._response_failed(response):
                    logging.error("kg: 删除属性同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
                else:
                    return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_update_url, traceback.format_exc())
            logging.error('kg: 删除属性同义词失败， 原因：' + msg)

    def _get_property_synonym(self, property_name: str):
        """
        获取属性的同义词
        :param property_name: 属性名称
        :return:
        """
        try:
            property_object = self.load_property(property_name)
            if property_object is not None:
                property_id = property_object['id']
                return self._get_wordbank_synonym("property", property_id)
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_update_url, traceback.format_exc())
            logging.error('kg: 获取属性同义词失败， 原因：' + msg)

    def _add_value_synonym(self, value_name: str, synonym: list):
        """
        增加值的同义词
        :param value_name: 值名称
        :param synonym: 值的同义词
        :return:
        """
        try:
            value_object = self._get_value_synonym(value_name)
            if value_object is not None:
                self._update_value_synonym(value_name, synonym)
            else:
                param = {
                    'name': value_name,
                    'synonym': synonym
                }

                response = requests.post(url=self.wordbank_value_add_url, json=param)
                if self._response_failed(response):
                    logging.error("kg: 新增值同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
                else:
                    return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_update_url, traceback.format_exc())
            logging.error('kg: 删除属性同义词失败， 原因：' + msg)

    def _get_value_synonym(self, value_name: str):
        """
        获取值的同义词
        :param value_name: 值名称
        :return:
        """
        try:
            response = requests.get(url=self.wordbank_value_get_url)
            if self._response_failed(response):
                logging.error("kg: 查询值同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
            else:
                data = response.json().get('data')
                if data and type(data) == 'list':
                    filter_objects = list(filter(lambda x: x['name'] == value_name, data))
                    if len(filter_objects) > 0:
                        return filter_objects[0]
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_update_url, traceback.format_exc())
            logging.error('kg: 查询值同义词失败， 原因：' + msg)

    def _update_value_synonym(self, value_name: str, synonym: list):
        """
        更新值的同义词
        :param value_name: 值名称
        :param synonym: 值的同义词 列表
        :return:
        """
        try:
            param = {
                'name': value_name,
                'synonym': synonym
            }
            response = requests.post(url=self.wordbank_value_update_url, json=param)
            if self._response_failed(response):
                logging.error("kg: 更新值同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
            else:
                return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_update_url, traceback.format_exc())
            logging.error('kg: 更新值同义词失败， 原因：' + msg)

    def _delete_value_synonym(self, value_name: str):
        """
        删除值的同义词
        :param value_name:  值名称
        :return:
        """
        try:
            param = {
                'name': value_name,
            }
            response = requests.delete(url=self.wordbank_value_update_url, json=param)
            if self._response_failed(response):
                logging.error("kg: 删除值同义词失败：原因: 接口异常。" + str(response.text) if response is not None else '')
            else:
                return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.wordbank_update_url, traceback.format_exc())
            logging.error('kg: 删除值同义词失败， 原因：' + msg)

    def load_extra_property(self, property_name, entity_name):
        """
        获取实体
        :property_name: 属性名称
        :entity_name: 实体名称
        :return: 结果
        """
        try:
            response = requests.get(self.load_extra_property_url.format(Config.base_url, self.app_id, property_name))
            if self._response_failed(response):
                logging.error("kg: 获取特殊属性失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data').get('result'):
                    results = response.json().get('data').get('result')
                    if results:
                        for result in results:
                            if result.get('entityName') == entity_name:
                                return result
                        return None
                    else:
                        return None
                else:
                    return None
        except Exception:
            msg = "Exception When GET '{}' : {}".format(self.load_property_url, traceback.format_exc())
            logging.error('kg: 获取特殊属性失败， 原因：' + msg)
            return None

    def add_extra_property(self, property_id, entity_id, category, unit):
        """
        获取实体
        :property_id: 属性id
        :entity_id: 实体id
        :category: 属性类型
        :unit: 单位
        :return: 结果
        """
        param = {
            "propertyId": property_id,
            "extraProperties": [{
                "entityId": entity_id,
                "category": category,
                "unit": unit,
                "speech": "{\"answer\":\"\",\"property\":{\"dimension_id_list\":[]}}",
                "speechType": "201",
                "extra_content": {}
            }]
        }
        try:
            response = requests.post(url=self.update_extra_property_url, json=param)
            if self._response_failed(response):
                logging.error("kg: 更新特殊属性失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                return True
        except Exception:
            msg = "Exception When POST '{}' : {}".format(self.update_extra_property_url, traceback.format_exc())
            logging.error('kg: 更新特殊属性失败， 原因：' + msg)
            return False

    def update_extra_property(self, property_name, entity_name, category, unit):
        """
        获取实体
        :property_name: 属性名称
        :entity_name: 实体名称
        :return: 结果
        """
        param = {
            "propertyId": 0,
            "extraProperties": [{
                "entityId": 0,
                "category": category,
                "unit": unit,
                "speech": "{\"answer\":\"\",\"property\":{\"dimension_id_list\":[]}}",
                "speechType": "201",
                "extra_content": {}
            }]
        }
        try:
            response = requests.get(self.load_extra_property_url.format(Config.base_url, self.app_id, property_name))
            if self._response_failed(response):
                logging.error("kg: 获取特殊属性失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
            else:
                response_json = response.json()
                if response_json.get('data').get('result'):
                    results = response.json().get('data').get('result')
                    if results:
                        for result in results:
                            if result.get('entityName') == entity_name:
                                result['category'] = category
                                result['unit'] = unit
                                param['propertyId'] = result.get('propertyId')
                                result['extra_content'] = result['extraContent']
                                param['extraProperties'] = result
                                response = requests.post(url=self.update_extra_property_url, json=param)
                                if self._response_failed(response):
                                    logging.error(
                                        "kg: 更新特殊属性失败：原因: 接口异常。" + str(response.json()) if response is not None else '')
                                    return False
                return True
        except Exception:
            msg = "Exception When GET '{}' : {}".format(self.load_property_url, traceback.format_exc())
            logging.error('kg: 获取特殊属性失败， 原因：' + msg)
            return False
