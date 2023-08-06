import time

from ..entity.exception import BfEngineException
from .module import Module
from ..caller.statistci_caller import StatisticCaller
from ..logger import log


class LogStatistic(Module):
    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'config', set)
        self.app_id = app_id
        self.caller = StatisticCaller(self.app_id)
        if init:
            self.init()

    def get_hot_questions(self, start_time: str, end_time: str, top_n: int) -> list:
        """
        :param start_time: 起始时间 yyyyMMdd格式
        :param end_time:  截止时间 yyyyMMdd格式
        :param top_n: 返回数据量限制
        :return:
        """
        if start_time is None or end_time is None:
            raise BfEngineException(code=-1, msg='start_time or end_time not none')
        try:
            top_n = int(top_n)
            hot_questions = self.caller.get_hot_questions(start_time, end_time, top_n)
            result = []
            for hot_question in hot_questions:
                result.append({
                    'rank': hot_question['rank'],
                    'question': hot_question['question'],
                    'count': hot_question['q'],
                    'module': hot_question['module']
                })
            return result
        except Exception as e:
            log.error(e)

    def get_records(self, start_time: int, end_time: int, size: int, page: int):
        """
        获取对话日志
        :param start_time: 起始时间的unix时间戳 秒数
        :param end_time:  截止时间的Unix时间戳秒数
        :param size: 分页 每页条数
        :param page: 分页 当前页数
        :return:
        """
        try:
            if start_time is None or end_time is None:
                raise BfEngineException(code=-1, msg='start_time or end_time not none')
            if size is None or size < 0:
                size = 20
            if page is None or page < 0:
                page = 1
            data = self.caller.get_records(start_time=start_time, end_time=end_time, limit=size, page=page)
            records = data['data']
            result = {
                "data": [],
                "total_size": data['total_size'],
                "page": data['page'],
                "size": data['limit']
            }
            for record in records:
                result['data'].append({
                    "unique_id": record["unique_id"],
                    "session_id": record["session_id"],
                    "user_id": record["user_id"],
                    "question": record["user_q"],
                    "faq": record["std_q"],
                    "score": record["score"],
                    "emotion": record["emotion"],
                    "intent": record["intent"],
                    "log_time": record["log_time"],
                    "cost": record["tspan"],
                    "answer": record["answer"],
                    "json_answer": record['raw_answer'],
                    "scenario_name": record["scenario_name"],
                    "module": record["module"]
                })
            return result
        except Exception as e:
            log.error(e)
