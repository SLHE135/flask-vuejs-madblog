from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from app import db
from app.api import bp


def error_response(status_code, message=None):
    """
    返回错误信息
    :param status_code: HTTP 状态码
    :param message: 错误信息
    :return: 错误信息json格式
    """
    # 如果没有指定message，则使用HTTP状态码对应的错误信息
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)  # 将字典转换为json格式
    response.status_code = status_code  # 设置HTTP状态码
    return response


def bad_request(message):
    """
    返回400错误
    :param message: 错误信息
    :return: 错误信息json格式
    """
    return error_response(400, message)


def unauthorized(message):
    """
    返回401错误
    :param message: 错误信息
    :return: 错误信息json格式
    """
    return error_response(401, message)


def forbidden(message):
    """
    返回403错误
    :param message: 错误信息
    :return: 错误信息json格式
    """
    return error_response(403, message)


# 404错误
@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)


# 505错误
@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()  # 回滚数据库
    return error_response(500)
