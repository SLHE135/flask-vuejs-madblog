import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件的绝对路径
load_dotenv(os.path.join(basedir, '.env'), encoding='utf-8')  # 加载.env文件


class Config(object):
    pass
