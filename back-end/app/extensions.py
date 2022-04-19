#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 创建这些flask扩展的实例 """
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Flask-Cors plugin
cors = CORS()
# Flask-SQLAlchemy plugin
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
# Flask-Migrate plugin
migrate = Migrate(render_as_batch=True)
# Flask-Mail plugin
mail = Mail()
