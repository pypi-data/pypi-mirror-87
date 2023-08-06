from .dialogue_manager import DialogueManager
from .task_engine import TaskEngine
from .knowledge_graph import KnowledgeGraph
from .question_answering import QuestionAnswering
from .intent_answering import IntentAnswering
from .ner_parser import NERParser
from .dialogue_act import DialogueAct
from .config_manager import ConfigManager
from .log_statistic import LogStatistic
from .common_service import CommonService
from .chat_service import ChatService
from .skill_service import SkillService
from .set import Set


class Bot:
    """
    机器人
    """

    def __init__(self, app_id, init_module: bool, name=None):
        self.app_id = app_id
        self.set = Set()
        self.intent = IntentAnswering(app_id, self.set, init_module)
        self.qa = QuestionAnswering(app_id, self.set, init_module)
        self.kg = KnowledgeGraph(app_id, self.set, init_module)
        self.te = TaskEngine(app_id, self.set, init_module)
        self.dm = DialogueManager(app_id, self.set, init_module)
        self.ner = NERParser(app_id, self.set, init_module)
        self.act = DialogueAct(app_id, self.set, init_module)
        self.config = ConfigManager(app_id, self.set, init_module, name=name)
        self.statistic = LogStatistic(app_id, self.set, init_module)
        self.common_service = CommonService(app_id, self.set, init_module)
        self.chat = ChatService(app_id, self.set, init_module)
        self.skill = SkillService(app_id, self.set, init_module)
