# 创建迁移存储库 flask db init
# 生成迁移脚本 flask db migrate -m "add users table"
# 执行迁移脚本 flask db upgrade
# 回滚上次的迁移脚本 flask db downgrade
import base64
import os
from datetime import datetime, timedelta

from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class PaginatedAPIMixin(object):
    """
    分页查询
    """

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        """
        将分页后的数据转换成字典
        :param query: 查询对象
        :param page: 页码
        :param per_page: 每页显示的数据条数
        :param endpoint: 路由名称
        :param kwargs: 其他参数
        :return: 字典
        """
        resources = query.paginate(page, per_page, False)  # 分页查询
        data = {
            'items': [item.to_dict() for item in resources.items],  # 将查询结果转换成字典
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },  # 将分页信息转换成字典
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None,
            },  # 将链接转换成字典
        }
        return data


class User(PaginatedAPIMixin, db.Model):
    """
    用户表模型
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 把密码加密存储，不能直接存储明文密码
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)  # token过期时间

    # 返回用户名
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # 对密码进行加密
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码是否正确
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 将用户对象转换成字典
    def to_dict(self, include_email=False):
        """
        将用户对象转换成字典
        :param include_email: 是否包含邮箱
        :return: 字典
        """
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
            },
        }
        if include_email:  # 如果包含邮箱，则添加邮箱
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        """
        将字典转换成用户对象
        """
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        """
        生成token
        :param expires_in: token过期时间
        :return: token
        """
        now = datetime.utcnow()  # 获取当前时间
        if self.token and self.token_expiration > now + timedelta(seconds=60):  # 如果token存在且过期时间大于当前时间+60秒
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')  # 生成24位随机字符串
        self.token_expiration = now + timedelta(seconds=expires_in)  # 设置过期时间
        db.session.add(self)
        return self.token

    def revoke_token(self):
        """
        撤销token
        """
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        """
        检查token
        """
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
