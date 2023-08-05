import requests

from ..logger import log
from .base import CallerBase
from ..config import Config
from ..entity.enums import QuestionType, QuestionMode, QuestionField
from ..entity.exception import BfEngineException
from .set_config import SetConfig
from .langconv import Converter
import random

class QACaller(CallerBase):
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
            "user_id": "bf-engine-sdk",
            "Authorization": "Bearer EMOTIBOTDEBUGGER",
            "Accept": "application/json,text/plain, */*"
        }
        self.upload_faq_upload_url = Config.base_url + "/ssm/dac/upload"
        self.upload_faq_upload_status_url = Config.base_url + "/ssm/dac/upload/"
        self.upload_faq_train_url = Config.base_url + "/ssm/dac/train"
        self.upload_faq_train_status_url = Config.base_url + "/ssm/dac/trainhistory"
        self.upload_faq_json_sq_url = Config.base_url + "/ssm/dac/sq"
        self.upload_faq_json_lq_url = Config.base_url + "/ssm/dac/lq"
        self.upload_faq_json_answer_url = Config.base_url + "/ssm/dac/answer"
        self.upload_faq_json_publish_url = Config.base_url + "/ssm/dac/release/online"
        self.upload_faq_json_publish_status_url = Config.base_url + "/ssm/dac/release/progress"
        self.upload_faq_json_publish_status_url = Config.base_url + "/ssm/dac/release/progress"
        self.upload_faq_json_tag_url = Config.base_url + "/ssm/dac/tag"
        self.download_faq_download_url = Config.base_url + "/ssm/dac/download"
        self.download_faq_download_export_url = Config.base_url + "/ssm/dac/common/minio/excelfile"
        self.search_faq_json_question_list_url = Config.base_url + "/ssm/dac/info"
        self.search_faq_json_corpus_list_url = Config.base_url + "/ssm/dac/lq"
        self.search_faq_json_related_sq_list_url = Config.base_url + "/ssm/dac/sq/related_candidate"
        self.operate_faq_category_url  = Config.base_url + "/ssm/dac/category"
        self.get_faq_sub_category_url  = Config.base_url + "/ssm/dac/category/sub"
        self.get_predict_qa_list_url = Config.base_url + "/qa/predict"
    def upload(self, data_type: QuestionType, data_model: QuestionMode, file_path: str) -> str:
        """
        上传标注问/语料
        :param data_type: 上传类型 (SQ_ANS|LQ|TQ)
        :param data_model: 上传模型 (全量|增量)
        :param file_path: 上传文件路径
        :return 上传id
        """
        # 上传问题$答案
        files = {"file": (self.app_id + ".xlsx", open(file_path, 'rb'))}
        data = {"type": data_type, "mode": data_model, "comment": "BFEngine 导入 qa"}
        resp = requests.request("POST", self.upload_faq_upload_url, headers=self.header, data=data, files=files).json()

        # 问题$答案上传进度
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return str(resp["data"])

    def upload_status(self, data_id: str, is_log: bool = True) -> int:
        """
        查询上传状态
        :param is_log: 是否打日志
        :param data_id: 上传id
        :return 上传进度
        """
        resp = requests.get(self.upload_faq_upload_status_url + "/" + data_id, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        progress = resp["data"]["progress"]
        # if is_log:
        #     log.info(self.module + ": 上传进度==" + str(progress) + "%")
        return progress

    def download_launch(self, data_type: QuestionType) -> str:
        """
        发起导出标注问/语料
        :param data_type: 下载类型 (SQ_ANS|LQ|TQ)
        :param file_path: 下载文件路径
        :return 服务器文件下载路径
        """
        resp = requests.get(self.download_faq_download_url + "?type=" + data_type, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]

    def download(self, file_path: str, service_file_path: str, is_log: bool = True):
        """
        从服务获取文件
        :param is_log: 是否打日志
        :param file_path: 本地文件保存路径
        :param data_path: 服务文件路径
        :return 上传进度
        """
        resp = requests.get(self.download_faq_download_export_url + "?filename=" + service_file_path, stream=True)
        with open(file_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=512):
                f.write(chunk)

    def upload_json_sq(self, tag: SetConfig = SetConfig(), data: dict = {}) -> str:
        """
        上传标准问（新增标准问）
        :param tag:  标签
        :param data: 上传数据
        :return id
        """
        tag_id_list = []
        if "tags" in data.keys():
            temps = self._tags_add(data["tags"])
            for temp in temps:
                tag_id_list.append(temp)
        related_sq_id_list = []
        if "related" in data.keys():
            temps = self._related_sq_search(data["related"])
            for temp in temps:
                related_sq_id_list.append(temp["id"])
        answers = []
        if "answers" in data.keys():
            for answer in data["answers"]:
                answer["related_sq_id_list"]=related_sq_id_list
                if "time_tag" in answer.keys():
                    if not tag.exits(answer["time_tag"]):
                        answer.pop("time_tag")
                        answers.append(answer)
                        continue
                    answer.update(tag.get(answer["time_tag"]))
                    answer.pop("time_tag")
                    answers.append(answer)
                else:
                    answers.append(answer)
        else:
            answers.append(
                {
                    "answer": data["answer"],
                    "property": {
                        "dimension_id_list": []
                    },
                    "start_time": "",
                    "end_time": "",
                    "period_type": 0,
                    "related_sq_id_list": related_sq_id_list
                }
            )
        data = {
            "sq": data["sq"],
            "category_id": int(data["category_id"]),
            "tag_id_list": tag_id_list,
            "answers": answers
        }
        resp = requests.post(self.upload_faq_json_sq_url, headers=self.header, json=data).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]["id"]

    def upload_json_lq(self, data_id: str, data: dict) -> bool:
        """
        上传标准问语料
        :param data_id: 上传id
        :return 上传进度
        """
        data = {
            "records": [
                {
                    "sq_id": data_id,
                    "lq_list": list(map(lambda lq: {'lq': lq}, data["lq"] if "lq" in data.keys() else []))
                }
            ]
        }
        resp = requests.post(self.upload_faq_json_lq_url, headers=self.header, json=data).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return True

    def train(self):
        """
        训练标准问题
        :return 训练id
        """
        resp = requests.get(self.upload_faq_train_url, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return str(resp["data"])

    def train_status(self, train_id):
        """
        查询训练状态
        :param train_id: 训练id
        :return 训练进度
        """
        resp = requests.get(self.upload_faq_train_status_url + "/" + train_id, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        progress = resp["data"]["progress"]
        # log.info(self.module + ": training..." + str(progress) + "%")
        return progress

    def publish(self):
        """
        开始发布
        :return 发布id
        """
        resp = requests.get(self.upload_faq_json_publish_url, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return str(resp["data"])

    def publish_status(self, publish_id) -> int:
        """
        查询发布状态
        :param publish_id: 发布id
        :return 发布进度
        """
        resp = requests.get(self.upload_faq_json_publish_status_url + "/" + publish_id, headers=self.header,
                            json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        progress = int(resp["data"])
        return progress

    def qa_tag_add(self, name: str = None):
        """
        添加qa标签
        :param name 标签名称
        :return 标签ID
        """
        data = {"name": name}
        resp = requests.post(self.upload_faq_json_tag_url, headers=self.header,
                             json=data).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]["id"]

    def qa_tag_list(self):
        """
        获取标签列表
        :return 标签列表
        """
        resp = requests.get(self.upload_faq_json_tag_url, headers=self.header,
                            json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]

    def qa_list(self, field: QuestionField) -> str:
        data = self.sq_list(field)
        return data

    def sq_list(self, field: QuestionField) -> str:
        """
        标准问列表查询
        :return 标准问列表
        """
        data = {"search": [{"keyword": "", "field": str(field)}]}
        resp = requests.post(self.search_faq_json_question_list_url, headers=self.header, json=data).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        for sq_data in resp["data"]:
            sq_data['id'] = str(sq_data['id'])
            sq_data['category_id'] = str(sq_data.get('category_id'))
            for answer in sq_data['answers']:
                answer['id'] = str(answer['id'])
                answer['sq_id'] = str(answer['sq_id'])

        return resp["data"]

    def lq_list(self, qa_id: str):
        """
        查询标准问下语料
        :return 语料列表
        """
        resp = requests.get(self.search_faq_json_corpus_list_url + "/" + qa_id, headers=self.header,
                            json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]["list"]

    def _related_sq_search(self, relates):
        """
        获取相关问列表
        :return 语料列表
        """
        related_list = []
        resp = requests.get(self.search_faq_json_related_sq_list_url, headers=self.header,
                            json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        data_list = resp["data"]
        for data in data_list:
            if data["content"] in relates:
                related_list.append(data)
        return related_list

    def _tags_add(self, tags):
        """
        添加标签集
        :return 返回添加后的标签ID集
        """
        tag_ids = []
        exist_tag_name_list = []  # 已存在标签名称
        tmp = list(set(tags))
        for tag in tmp:
            try:
                tag_ids.append(self.qa_tag_add(tag))
            except BfEngineException as bfe:
                exist_tag_name_list.append(tag)
        exist_tag_list = self._qa_tag_search(exist_tag_name_list)
        for exist_tag in exist_tag_list:
            if "id" in exist_tag.keys():
                tag_ids.append(exist_tag["id"])
        return tag_ids

    def _qa_tag_search(self, tags):
        """
        查询已经存在标签的IDS
        :param 查询tags
        :return 标签列表
        """
        tag_objs = []
        tag_obj_list = self.qa_tag_list()
        for tag_name in tags:
            for tag_obj in tag_obj_list:
                if tag_name == tag_obj["name"]:
                    tag_objs.append(tag_obj)
        return tag_objs

    def update_corpus(self, question_id, corpus_id, corpus):
        """
        更新单条语料
        :return:
        """
        params = {
            'records': [
                {
                    'sq_id': int(question_id),
                    'lq_list': [
                        {
                            'id': int(corpus_id),
                            'lq': corpus
                        }
                    ]
                }
            ]
        }
        resp = requests.put(self.upload_faq_json_lq_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0 and msg!="语料重复":
            raise BfEngineException(code=code, msg=msg)
        return True

    def add_corpus(self, question_id, corpus):
        """
        增加语料
        :return:
        """
        params = {
            'records': [
                {
                    'sq_id': int(question_id),
                    'lq_list': [
                        {
                            'lq': corpus
                        }
                    ]
                }
            ]
        }
        resp = requests.post(self.upload_faq_json_lq_url, headers=self.header, json=params, timeout=30).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        lq_id = ""
        lq_list = self.lq_list(question_id)
        for lq in lq_list:
            if lq['content'] == str(corpus):
                lq_id = lq['id']
        return lq_id

    def add_corpus_list(self, question_id, corpus_list):
        """
        增加语料
        :return:
        """
        params = {
            'records': [
                {
                    'sq_id': int(question_id),
                    'lq_list': corpus_list
                }
            ]
        }
        resp = requests.post(self.upload_faq_json_lq_url, headers=self.header, json=params, timeout=30).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return True

    def delete_corpus(self, question_id, corpus_id):
        """
        删除语料
        :return:
        """
        params = {
            'records': [
                {
                    'lq_list': [
                        {
                            'id': int(corpus_id)
                        }
                    ],
                    'sq_id': int(question_id),
                }
            ]
        }
        resp = requests.delete(self.upload_faq_json_lq_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return True

    def delete_corpus_list(self, question_id, corpus_id_list):
        """
        删除语料
        :return:
        """
        params = {
            'records': [
                {
                    'sq_id': int(question_id),
                    'lq_list': corpus_id_list
                }
            ]
        }
        resp = requests.delete(self.upload_faq_json_lq_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return True

    def query_corpus(self, question_id, keyword=None, page=None, size=None):
        url = self.upload_faq_json_lq_url + '/' + str(question_id)
        if keyword:
            url = url + "?keyword=" + keyword.strip()
        if page is not None and size is not None:
            url = url + "&page_size=" + size + "&page_index=" + page
        resp = requests.get(url, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]["list"]

    def update_question(self, data: dict) -> str:
        """
        更新问题
        :param question:
        :return:
        """
        ## 问题调更新接口，语料删除重插
        question_id = data.get('id')
        data["id"] = int(data["id"])
        if( "tag_id_list" not in data.keys()):
            data.update({"tag_id_list": []})
        if("category_id" in data.keys()):
             data["category_id"] = int(data["category_id"])
        else:
             data.update({"category_id": -1})
        requests.put(self.upload_faq_json_sq_url, headers=self.header, json=data).json()
        related_sq_id_list = []
        if "related" in data.keys():
            temps = self._related_sq_search(data["related"])
            for temp in temps:
                related_sq_id_list.append(temp["id"])
        if("lq" in data.keys()):
            lq_request_list= data.get("lq")
            if(len(lq_request_list) > 0):
               lq_list = self.query_corpus(question_id)
               lq_id_list = []
               for lq in lq_list:
                  lq_id_list.append({"id":lq['id']})
               self.delete_corpus_list(question_id,lq_id_list)
               lq_insert_list=[]
               for lq in lq_request_list:
                   lq_insert_list.append({"lq":lq})
               self.add_corpus_list(question_id,lq_insert_list)
        if("answers" in data.keys()):
             answer_request_list = data.get("answers")
             if(len(answer_request_list) > 0):
               ans_resp = requests.get(self.upload_faq_json_answer_url + "/" + str(question_id), headers=self.header, json={}).json()
               code = int(ans_resp["code"])
               msg = str(ans_resp["message"])
               if code != 0:
                 raise BfEngineException(code=code, msg=msg)
               answer_id_list= []
               for ans in ans_resp['data']:
                   answer_id_list.append(ans['id'])
               self.delete_answer_list(answer_id_list)
               for insert_answer in answer_request_list:
                   insert_data = {
                       "answer":insert_answer['answer'],
                       "start_time":"",
                       "end_time":"",
                       "sq_id":int(question_id),
                       "property":{
                           "dimension_id_list":[

                           ]
                       },
                       "tag_id_list": [],
                       "related_sq_id_list":related_sq_id_list
                   }
                   self.add_answer(insert_data)
        return question_id

    def delete_question(self, question_id):
        """
        删除问题
        :param question:
        :return:
        """

        params = {
            'records': [
                int(question_id)
            ]
        }
        resp = requests.delete(self.upload_faq_json_sq_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return True

    def add_answer(self, data: dict):
        """
        新增答案
        :return:
        """
        resp = requests.post(self.upload_faq_json_answer_url, headers=self.header, json=data).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp['data']['id']

    def update_answer(self, data: dict):
        """
        更新答案
        :return:
        """
        """
        新增答案
        :return:
        """
        data["id"] = int(data["id"])
        data["sq_id"] = int(data["sq_id"])
        resp = requests.put(self.upload_faq_json_answer_url, headers=self.header, json=data).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return True

    def delete_answer(self, answer_id):
        """
        删除答案
        :return:
        """
        params = {
            'records': [answer_id]
        }
        resp = requests.delete(self.upload_faq_json_answer_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return

    def delete_answer_list(self, answer_id_list):
        """
        删除答案
        :return:
        """
        params = {
            'records': answer_id_list
        }
        resp = requests.delete(self.upload_faq_json_answer_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return

    def query_category_list(self):
        resp = requests.get(self.operate_faq_category_url, headers=self.header,
                            json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]

    def add_category(self,parent_id,name:str):
        params = {
            'parent_id': int(parent_id),
            'name': name
        }
        resp = requests.post(self.operate_faq_category_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp['data']['id']

    def update_category(self,id,name:str,parent_folder_id=None):
        params = {
            'id': int(id),
            'name': name,
            'parent_folder_id':parent_folder_id
        }
        resp = requests.put(self.operate_faq_category_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp['data']['id']

    def delete_category(self,id):
        params = {
            'id': int(id)
        }
        resp = requests.delete(self.operate_faq_category_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return

    def get_similar_recomend_qa_list(self,user_inputs:str,type:str):
        sq_result = []
        converter = Converter('zh-hans')
        params = {"Text":converter.convert(user_inputs).lower(),'UniqueId':str(random.randint(100,10000)),"IsRelease": False,'Robot':self.app_id}
        print("params: "+str(params))
        print("predict request url: "+self.get_predict_qa_list_url)
        resp = requests.request("POST", self.get_predict_qa_list_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        print(resp['data'])
        if code != 0:
           raise BfEngineException(code=code, msg=msg)
        change_range = 0
        if(type == "similar"):
           change_range = 3
        elif(type == "recommend"):
             change_range = 25

        for match_sq in resp['data']:
            if match_sq["score"] > match_sq["threshold"]-change_range and len(sq_result)<3:
                sq_result.append(match_sq)
        return sq_result

    def get_similar_qa_list(self,user_inputs:str,max_topn,category_ids,online: bool=True):
        similar_sq_result = []
        sq_list = [];
        sq_map = {};
        answer_map = {};
        log.info(self.module + "开始")
        category_ids_list = self.get_all_sub_list(category_ids)
        log.info(self.module + "子目录查询完毕"+str(category_ids_list))
        self.get_all_sq_under_input_folders(sq_list, sq_map, answer_map)
        log.info(self.module + "sq获取完毕")
        converter = Converter('zh-hans')
        params = {"Text":converter.convert(user_inputs).lower(),'UniqueId':str(random.randint(100,10000)),"IsRelease": online,'Robot':self.app_id}
        log.info("params: "+str(params))
        log.info("predict request url: "+self.get_predict_qa_list_url)
        resp = requests.request("POST", self.get_predict_qa_list_url, headers=self.header, json=params).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        log.info(resp['data'])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        log.info(self.module + "预测结果获取完毕")
        self.process_predict_result(category_ids_list, resp, similar_sq_result, sq_list, sq_map)
        log.info(self.module + "结果处理完毕")
        similar_sq_result = self.get_topn_result(answer_map, max_topn, similar_sq_result)
        log.info(self.module + "返回结果")
        return similar_sq_result

    def get_topn_result(self, answer_map, max_topn, similar_sq_result):
        topn = int(max_topn)
        similar_sq_result = sorted(similar_sq_result, key=lambda x: x["score"], reverse=True)[:topn]
        for result_sq in similar_sq_result:
            ans_list = [];
            ans_resp_list = [];
            ans_resp_list = answer_map.get(result_sq['sqId'])
            for ans in ans_resp_list:
                ans_list.append(ans['answer'])
            result_sq['answer'] = ans_list
        return similar_sq_result

    def process_predict_result(self, category_ids_list, resp, similar_sq_result, sq_list, sq_map):
        for match_sq in resp['data']:
            if 'sqId' in match_sq and match_sq['sqId'] in sq_list:
                match_sq['category_id'] = str(sq_map.get(match_sq['sqId']))
                if (len(category_ids_list) > 0) and int(match_sq['category_id']) in category_ids_list:
                    similar_sq_result.append(match_sq)
                elif (len(category_ids_list) == 0):
                    similar_sq_result.append(match_sq)

    def get_all_sq_under_input_folders(self, sq_list, sq_map,answer_map):
        data = {"search": [{"keyword": "", "field": "sq"}],
                "conditions": {"category": {"id_list": [], "logical_op": "and"}}}
        sq_resp = requests.post(self.search_faq_json_question_list_url, headers=self.header, json=data).json()
        code = int(sq_resp["code"])
        msg = str(sq_resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        for sq in sq_resp['data']:
            sq_list.append(sq['id'])
            kv = {sq['id']: sq['category_id']}
            sq_map.update(kv)
            kvanswer = {sq['id']: sq['answers']}
            answer_map.update(kvanswer)

    def get_all_sub_list(self, category_ids):
        category_ids_list = []
        for category_id in category_ids:
            header = self.header
            header.update({"folder_id": str(category_id)})
            result = requests.get(self.get_faq_sub_category_url, headers=header, json={}).json()
            category_sub_ids_list = result["data"]["idList"]
            for category_sub_id in category_sub_ids_list:
                if not category_ids_list.__contains__(category_sub_id):
                    category_ids_list.append(category_sub_id)
        return category_ids_list




