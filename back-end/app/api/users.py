import re

from flask import jsonify, request, url_for

from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User


@bp.route('/users', methods=['POST'])
def create_user():
    """注册一个新用户"""
    data = request.get_json()
    if not data:
        return bad_request('您必须发布 JSON 数据。')
    message = {}
    if 'username' not in data or not data.get('username', None):
        message['username'] = '请提供有效的用户名。'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = '请提供一个有效的电子邮件地址。'
    if 'password' not in data or not data.get('password', None):
        message['password'] = '请提供有效密码。'

    if User.query.filter_by(username=data.get('username', None)).first():
        message['username'] = '用户名已经存在，请使用不同的用户名。'
    if User.query.filter_by(email=data.get('email', None)).first():
        message['email'] = '电子邮件地址已经存在，请使用不同的电子邮件地址。'
    if message:
        return bad_request(message)

    user = User()
    user.from_dict(data, new_user=True)  # 新用户
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())  # 返回用户信息
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.status_code = 201
    # 设置新资源URL
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    """返回用户列表"""
    page = request.args.get('page', 1, type=int)  # 获取页数
    per_page = min(request.args.get('per_page', 10, type=int), 100)  # 获取每页数量
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')  # 获取用户列表
    return jsonify(data)


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    """返回一个用户"""
    return jsonify(User.query.get_or_404(id).to_dict())  # jsonify()将对象转换为JSON


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """更新一个用户"""
    user = User.query.get_or_404(id)
    data = request.get_json()  # 获取json数据
    if not data:
        return bad_request('您必须发布 JSON 数据。')
    message = {}
    if 'username' in data and not data.get('username', None):
        message['username'] = '请提供有效的用户名。'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' in data and not re.match(pattern, data.get('email', None)):
        message['email'] = '请提供一个有效的电子邮件地址。'

    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        message['username'] = '用户名已经存在，请使用不同的用户名。'
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        message['email'] = '电子邮件地址已经存在，请使用不同的电子邮件地址。'

    if message:
        return bad_request(message)

    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """删除一个用户"""
    pass
