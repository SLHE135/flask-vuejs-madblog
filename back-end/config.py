import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件的绝对路径
load_dotenv(os.path.join(basedir, '.env'), encoding='utf-8')  # 加载.env文件


class Config(object):
    """配置类"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')  # 数据库地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭追踪数据库修改
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # 密钥
