import unittest

from flask import current_app

from app import create_app, db
from tests import TestConfig


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        """每次调试之前执行"""
        self.app = create_app(TestConfig)  # 创建flask应用
        self.app_context = self.app.app_context()  # 激活（或推送）flask应用上下文
        self.app_context.push()  # 推送flask应用上下文
        db.create_all()  # 通过SQLAlchemy来使用SQLite内存数据库，db.create_all()快速创建所有的数据库表

    def tearDown(self):
        """每次调试之后执行"""
        db.session.remove()  # 删除数据库会话
        db.drop_all()  # 删除所有的数据库表
        self.app_context.pop()  # 删除flask应用上下文

    def test_app_exists(self):
        """测试flask应用是否存在"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """测试flask应用是否在测试模式"""
        self.assertTrue(current_app.config['TESTING'])
