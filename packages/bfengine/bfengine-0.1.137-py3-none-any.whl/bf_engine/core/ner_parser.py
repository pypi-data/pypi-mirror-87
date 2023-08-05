from ..logger import log

from .module import Module
from ..caller.parser_caller import NERParserCaller


class PredictAnswer:
    def __init__(self, slot_content, slot_name, slot_desc):
        """
        :param slot_content: 槽位预测内容
        :param slot_name: 槽位标签名称
        :param slot_desc: 槽位描述
        """
        self.slot_content = slot_content
        self.slot_name = slot_name
        self.slot_desc = slot_desc


class Parser:
    def __init__(self, name, parserId, desc, slots, userId):
        """
        解析器信息
        :param name: 解析器名称
        :param parserId: 解析器调用ID
        :param desc: 解析器用途描述
        :param slots: 解析器所能抽取出的槽位列表 list(ParserSlot)
        :param userId: 解析器所属的用户id
        """
        self.name = name
        self.parserId = parserId
        self.desc = desc
        self.userId = userId
        self.slots = slots


class ParserSlot:
    def __init__(self, name, desc):
        """
        解析器抽取的槽位信息
        :param name: 槽位名称
        :param desc: 槽位的描述
        """
        self.name = name
        self.desc = desc


class NERParser(Module):

    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'ner', set)
        self.app_id = app_id
        self.caller = NERParserCaller(app_id)
        if init:
            self.init()

    def init(self):
        try:
            self.caller.register_tde_user(self.app_id)
            sys_parsers = {parser['parserId'].replace('@1', ''): parser['parserId'] for parser in
                           self.caller.get_parser_library()}
            self.sys_parser_id_map = sys_parsers
        except Exception:
            log.warning("ner: fail to init")


    def predict(self, sentence, parsers: list):
        """
        解析器预测
        :param sentence: 用户输入
        :param parsers: 需要使用的解析器列表
        :return:  list(PredictAnswer)
        """
        answers = []
        for parser_id in parsers or []:
            parser_id = self.sys_parser_id_map[parser_id] if parser_id in self.sys_parser_id_map else parser_id
            results = self.caller.predict(sentence, parser_id)
            if results is not None:
                results = [PredictAnswer(result['slotContent'], result['slotName'], result['slotDesc']) for result in
                           results]
                answers.extend(results)

        return answers

    def get_parsers(self):
        """
        获取机器人能调用的所有parser
        :return: list(Parser)
        """
        # todo custom parser
        user_parsers = self.caller.get_parser_library() or []
        parsers = []
        for parser in user_parsers:
            slots = []
            for slot in parser.get('slotInfo') or []:
                slots.append(ParserSlot(slot['slotName'], slot['slotDesc']))
            parsers.append(Parser(parser['name'], parser['parserId'].replace('@1', ''), parser['description'], slots,
                                  parser['userId']))

        return parsers
