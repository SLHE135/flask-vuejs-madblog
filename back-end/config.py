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
    POSTS_PER_PAGE = 10  # 每页显示的文章数量
    USERS_PER_PAGE = 10  # 每页显示的用户数量
    COMMENTS_PER_PAGE = 10  # 每页显示的评论数量
    MESSAGES_PER_PAGE = 10  # 每页显示的消息数量
    # 发送qq邮件的配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER')  # 邮件服务器地址
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or '25')  # 邮件服务器端口
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', 'on', '1']  # 是否使用SSL
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 邮件用户名
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 邮件密码
    MAIL_SENDER = os.environ.get('MAIL_SENDER')
    # 发送邮件的配置
    ADMINS = ['1357667054@qq.com']  # 管理员邮箱
