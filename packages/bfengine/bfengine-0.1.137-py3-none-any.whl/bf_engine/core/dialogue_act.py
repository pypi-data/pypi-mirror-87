from ..logger import log
from .module import Module
from ..caller.act_caller import DialogueActCaller


class ActAnswer:
    def __init__(self, name, code, score):
        """
        :param name: 命中对话行为分类器的名称
        :param code: 命中对话行为分类器的code
        :param score: 对话行为分类器的出分
        """
        self.name = name
        self.code = code
        self.score = score


class Act:
    def __init__(self, name, code, explanation, sample):
        """
        :param name: 对话行为分类器名称
        :param code: 对话行为分类器调用code
        :param explanation: 对话行为分类器作用释义
        :param sample: 调用示例
        """
        self.name = name
        self.code = code
        self.explanation = explanation
        self.sample = sample


class DialogueAct(Module):

    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'ner', set)
        self.app_id = app_id
        self.caller = DialogueActCaller(app_id)
        if init:
            self.init()

    def init(self):
        try:
            act_code_map = {}
            acts = self.get_acts()
            for act in acts:
                act_code_map[act.code] = act
            self.act_code_map = act_code_map
        except Exception:
            log.warning("act: fail to init")

    def predict(self, sentence: str, acts: list = None):
        """
        行为分类器预测接口
        :param sentence: 用户输入
        :param acts: 调用分类器的code列表， 为空或者不传则默认调用所有分类器
        :return: list(ActAnswer)
        """
        results = self.caller.predict(sentence, acts)
        answers = []
        if results:
            for result in results:
                hit_act = result['act']
                answers.append(
                    ActAnswer(hit_act, self.act_code_map.get(hit_act).name if hit_act in self.act_code_map else '',
                              result['score']))
        return answers

    def get_acts(self):
        """
        获取系统内存在的对话行为分类器列表
        :return: list(Act)
        """
        acts = self.caller.get_acts() or []
        return [
            Act(act['name'], act['id'], act['explanation'], act['samples'])
            for act in acts
        ]
