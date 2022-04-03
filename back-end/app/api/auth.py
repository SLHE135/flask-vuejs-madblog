from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.api.errors import error_response
from app.models import User

basic_auth = HTTPBasicAuth()  # 创建认证对象
token_auth = HTTPTokenAuth()  # 创建认证对象


@basic_auth.verify_password  # 定义认证函数
def verify_password(username, password):
    """
    验证用户名和密码
    """
    user = User.query.filter_by(username=username).first()  # 查询用户
    if user is None:
        return False
    g.current_user = user  # 将用户保存到g对象中
    return user.check_password(password)


@basic_auth.error_handler  # 定义错误处理函数
def basic_auth_error():
    """
    返回错误信息
    """
    return error_response(401)


@token_auth.verify_token  # 定义认证函数
def verify_token(token):
    """
    用于检查用户请求是否有token，并且token真实存在，还在有效期内
    """
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler  # 定义错误处理函数
def token_auth_error():
    """
    用于在 Token Auth 认证失败的情况下返回错误响应
    """
    return error_response(401)
