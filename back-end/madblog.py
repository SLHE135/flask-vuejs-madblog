import os
import sys

import click

from app import create_app
from app.extensions import db
from app.models import User, Post, Comment, Role, Notification, Message
from config import Config

app = create_app(Config)

# 创建coverage实例
COV = None
# 如果环境变量FLASK_COVERAGE为真，则创建coverage实例
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Comment': Comment
    }


@app.cli.command()  # 注册为命令
@click.option('--coverage/--no-coverage', default=False, help='在代码覆盖范围内运行测试。')
def test(coverage):
    """运行单元测试."""
    # 如果执行 flask test --coverage，但是FLASK_COVERAGE环境变量不存在时，给它配置上
    if not os.environ.get('FLASK_COVERAGE') and not os.environ.get('FLASK_COVERAGE'):
        import subprocess  # subprocess模块是用来执行外部程序的
        os.environ['FLASK_COVERAGE'] = '1'  # 设置环境变量
        sys.exit(subprocess.call(sys.argv))  # 重新执行当前命令

    import unittest
    tests = unittest.TestLoader().discover('tests')  # 找到测试文件
    unittest.TextTestRunner(verbosity=2).run(tests)  # 执行测试

    if COV:
        COV.stop()  # 停止coverage
        COV.save()
        print('覆盖范围摘要：')
        COV.report()  # 打印覆盖范围摘要
        basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件所在目录
        covdir = os.path.join(basedir, 'tmp/coverage')  # 覆盖范围摘要文件存放目录
        COV.html_report(directory=covdir)  # 生成html报告
        print('HTML版本: file://%s/index.html' % covdir)
        COV.erase()  # 清除coverage数据


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Role': Role, 'User': User, 'Post': Post, 'Comment': Comment,
            'Notification': Notification, 'Message': Message}
