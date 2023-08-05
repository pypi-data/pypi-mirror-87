import os

from .util import random_str


class Config:
    default_app_id = os.environ.get('BF_ENGINE_DEFAULT_APP_ID', 'emotibotisthebestrobotoftheworld')
    base_url = os.environ.get('BF_ENGINE_BASE_URL', 'https://capricorn.emotibot.com')
    user_id = os.environ.get('BF_ENGINE_DEFAULT_USER_ID', 'bf-engine-user')
    session_id = os.environ.get('BF_ENGINE_DEFAULT_SESSION_ID', 'bf-engine-session' + random_str(8))
    robot_url = os.environ.get('BF_ENGINE_ROBOT_URL', 'openapi/v1/robot')
    chat_url = os.environ.get('BF_ENGINE_CHAT_URL', 'chatbot/#/robotchat')
    remote_url = os.environ.get('BF_ENGINE_REMOTE_URL', 'https://capricorn.emotibot.com')
    backfill_speech = '我还在学习'
