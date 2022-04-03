from flask import g, jsonify

from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    """
    获取当前用户的token
    """
    token = g.current_user.get_token()  # 获取当前用户的token
    db.session.commit()  # 提交数据库
    return jsonify({'token': token})  # 返回token


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    """
    删除当前用户的token
    """
    g.current_user.revoke_token()  # 删除当前用户的token
    db.session.commit()  # 提交数据库
    return '', 204  # 返回状态码204，表示删除成功
