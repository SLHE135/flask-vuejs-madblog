from functools import wraps

from flask import g

from app.api.errors import error_response
from app.models import Permission


def permission_required(permission):
    """检查用户是否具有指定的权限"""

    def decorator(f):
        @wraps(f)  # wraps是一个装饰器，用于保留函数的原始信息
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):  # 用户通过了Basic Auth认证后，就会在当前会话中附带 g.current_user
                return error_response(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    """检查用户是否具有管理员权限"""
    return permission_required(Permission.ADMIN)(f)
