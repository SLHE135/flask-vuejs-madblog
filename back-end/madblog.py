from app import create_app, db
from app.models import User

app = create_app()  # 把app对象传给create_app()函数


# 启动程序
@app.shell_context_processor
def make_shell_context():
    """
    在flask shell命令行中可以使用的上下文
    """
    return {'db': db, 'User': User}
