import time

from .module import Module
from ..caller.skill_service_caller import SkillServiceCaller
from ..logger import log
from ..entity.answer import Answer


class SkillService(Module):
    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'config', set)
        self.app_id = app_id
        self.caller = SkillServiceCaller(self.app_id)
        if init:
            self.init()

    def skill_list(self) -> list:
        """
            获取技能列表，返回list
        :return: skill list
             [
                {
                    name: 'skill_name',
                    status: 开关状态，布尔值,
                    desc: 描述，
                    skillId： 技能的id,调用时使用
                    demo: 示例列表 list
                        [
                            {
                                title: 主题,
                                question: 示例问法列表 list
                                        [
                                        "一句话让催婚的人闭嘴",
                                        "如何理直气壮地赖床"
                                        ]
                            }
                        ]
                }
             ]
        """
        try:
            skill_list = self.caller.get_remote_skill_list()
            for skill in skill_list:
                del skill['online']
            return skill_list

        except Exception as e:
            log.error(e)

    def update_status(self, skill_id: int, status: bool):
        """

        :param skill_id: 技能id
        :param status: 需要更新的状态
        :return:
        """
        assert skill_id is not None and status is not None, 'need skill_id(int) and status(bool)'
        return self.caller.update_remote_skill_status(skill_id, status)

    def query(self, text: str, online: bool = True) -> Answer:
        """
        :param online: 线上线下, 部分模块会需要线上线下的状态区分
        :param text: 用户问
        :return: 机器人回答
        """
        return self.caller.call_module('remote_skill', text, online)
