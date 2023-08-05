from ..caller.set_config import SetConfig


class Set:
    """
    机器人配置
    """

    def __init__(self):
        super().__init__()
        self.tag = SetConfig()
        self.intent_threshold=65
