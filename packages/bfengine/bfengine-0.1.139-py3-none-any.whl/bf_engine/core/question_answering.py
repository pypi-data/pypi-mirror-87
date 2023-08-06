import time
import traceback
import os

from tqdm import tqdm

from .module import Module
from ..caller.qa_caller import QACaller
from ..entity.answer import Answer
from ..entity.enums import QuestionType, QuestionMode,QuestionField
from ..entity.exception import BfEngineException, ErrorCode
from ..logger import log


class QuestionAnswering(Module):
    """
    问答
    """
    tmp_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    faq_sq_empty_path = tmp_dir + "/data/问答上传模板.xlsx"
    faq_lq_empty_path = tmp_dir + "/data/语料上传模板.xlsx"

    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'qa',set)
        self.caller = QACaller(app_id)
        if init:
            self.init()

    def train(self, data: str = None, question_path: str = None, corpus_path: str = None,append: bool = False,show_progress:bool=True):
        """
        :param data:
        :param question_path: 标准问路径
        :param corpus_path: 语料路径
        :param append: 是否追加，True
        :return: 训练是否成功
        """
        try:
            log.info('qa: prepare train')
            if data:
                # 清空FAQ
                if not append:
                    self.upload_question(self.faq_sq_empty_path, is_log=False)
                    self.upload_corpus(self.faq_lq_empty_path, is_log=False)
                self._upload_json(data)
            else:
                if question_path:
                    self.upload_question(question_path, append)
                if corpus_path:
                    self.upload_corpus(corpus_path, append)
            return self._train(show_progress)
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error('unknown exception')
            log.error(e)
            traceback.print_exc()
            return False
        return True
    def train_status(self,train_id:str=None):
        if not train_id:
            raise BfEngineException(code=-1, msg="train_id is null")
        return self.caller.train_status(train_id)
    def publish(self):
        """
        :发布
        :return: 机器人回答
        """
        self._pulish()
    def export(self,sq_path: str = None, lq_path: str = None):
        """
        导出问答和语料文件
        :param sq_path 问答文件路径
        :param lq_path 语料文件路径
        """
        self._export(sq_path,lq_path)

    def query(self, text: str,online: bool=False) -> Answer:
        """
        :param text: 用户问
        :return: 机器人回答
        """
        return self.caller.call_module('faq', text,online)
    def qa_tag_list(self):
        """
        获取标签列表
        """
        return self.caller.qa_tag_list()
    def qa_tag_add(self,name:str=None):
        """
        添加标签
        :param name 标签名称
        """
        return self.caller.qa_tag_add(name)
    def qa_list(self) -> str:
        """
        : 查询标准问列表
        :return: 标准问列表
        """
        return self.caller.qa_list(QuestionField.SQ)
    def question_list(self) -> str:
        """
        : 查询标准问列表
        :return: 标准问列表
        """
        return self.caller.sq_list(QuestionField.ALL)

    def corpus_list(self,question_id) -> str:
        """
        : 查询标准问下语料列表
        :return: 标准问列表
        """
        return self.caller.lq_list(question_id)
    def _train(self,show_progress:bool=True):
        log.info('qa: start training')
        train_id = self.caller.train()
        if not show_progress:
            return train_id
        progress = 0

        with tqdm(total=100) as bar:
            bar.set_description("qa training...")
            while progress < 100:
                old_progress = progress
                progress = self.caller.train_status(train_id)
                bar.update(progress - old_progress)
                time.sleep(1)
            bar.set_description("qa train finished")
        time.sleep(5)
    def _pulish(self):
        log.info('qa: start release')
        publish_id = self.caller.publish()
        progress = 0

        with tqdm(total=100) as bar:
            bar.set_description("qa release...")
            while progress < 100:
                old_progress = progress
                progress = self.caller.publish_status(publish_id)
                bar.update(progress - old_progress)
                time.sleep(1)
            bar.set_description("qa release finished")
        time.sleep(5)
    def _upload_json(self, content):
        """
        获取从路径中json
        """
        try:
            data = content["data"]
            for item in data:
                data_id = self.caller.upload_json_sq(self.set.tag,item)
                self.caller.upload_json_lq(data_id, item)
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            return None

    def upload_corpus(self, corpus_path, is_log: bool = True, append: bool = False):
        """
        上传qa语料
        :param corpus_path 语料路径
        :param append True:增量,false:全量
        """
        data_id = self.caller.upload(QuestionType.LQ, QuestionMode.INCRE if append else QuestionMode.FULL, corpus_path)

        progress = 0
        while progress < 100:
            progress = self.caller.upload_status(data_id, is_log=is_log)
            time.sleep(1)

    def upload_question(self, question_path, is_log=True, append: bool = False):
        if not question_path:
            raise BfEngineException(ErrorCode.argument_missing_error, 'missing question path')

        data_id = self.caller.upload(QuestionType.SQ_ANS, QuestionMode.INCRE if append else QuestionMode.FULL, question_path)

        progress = 0
        while progress < 100:
            progress = self.caller.upload_status(data_id, is_log=is_log)
            time.sleep(1)
    def _export(self,sq_path: str = None, lq_path: str = None):
        """
        导出问答和语料文件
        :param sq_path 问答文件路径
        :param lq_path 语料文件路径
        """
        try:
            if sq_path:
                data_path = self.caller.download_launch(QuestionType.SQ_ANS)
                self.caller.download(sq_path,data_path)
            if lq_path:
                data_path = self.caller.download_launch(QuestionType.LQ)
                self.caller.download(lq_path, data_path)
        except BfEngineException as bfe:
            log.error(bfe)
        except Exception as e:
            log.error(e)

    def update_corpus(self, question_id, corpus_id, corpus):
        """
        更新语料
        :return:
        """
        return self.caller.update_corpus(question_id, corpus_id, corpus)

    def add_corpus(self, question_id, corpus):
        """
        增加语料
        :return:
        """
        lq_id = self.caller.add_corpus(question_id, corpus)
        return lq_id

    def delete_corpus(self,question_id, corpus_id):
        """
        删除语料
        :return:
        """
        return self.caller.delete_corpus(question_id, corpus_id)

    def add_question(self, question_data: dict):
        """
        添加问题
        :param question_data:
        :return:
        """
        question_id = self.caller.upload_json_sq(data=question_data)
        self.caller.upload_json_lq(question_id, question_data)
        return question_id


    def delete_question(self, question_id: int):
        """
        删除问题
        :param question_id:
        :return:
        """
        return self.caller.delete_question(question_id)

    def update_question(self, question_data: dict):
        """
        更新问题
        :param question_data:
        :return:
        """
        return self.caller.update_question(question_data)

    def update_answer(selfs, answer_data: dict):
        """
        更新答案
        """
        return  selfs.caller.update_answer(answer_data)

    def query_category_list(self) -> str:
        return self.caller.query_category_list()

    def add_category(self,parent_id,name:str):
        return self.caller.add_category(parent_id,name)

    def update_category(self,id,name:str,parent_folder_id=None):
        return self.caller.update_category(id,name,parent_folder_id)

    def delete_category(self,id):
        return self.caller.delete_category(id)

    def get_similar_qa_list(self,user_inputs:str,max_topn,category_ids,online: bool=True) -> str:
        return self.caller.get_similar_qa_list(user_inputs,max_topn,category_ids,online)

    def get_similar_recomend_qa_list(self,user_inputs:str,type:str) -> str:
        """
        获取相似问/推荐问
        :param user_inputs 用户问
        :param type similar:相似问，recommend:推荐问
        """
        return self.caller.get_similar_recomend_qa_list(user_inputs,type)

