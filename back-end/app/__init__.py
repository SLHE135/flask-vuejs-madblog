from flask import Flask

from app.api import bp as api_bp
from app.extensions import cors, db, migrate, mail


def create_app(config_class=None):
    """工厂模式：创建 Flask 应用程序。"""
    app = Flask(__name__)

    # Initialization flask app
    configure_app(app, config_class)
    configure_blueprints(app)
    configure_extensions(app)
    # 不使用 Jinja2，用不到模版过滤器和上下文处理器
    # configure_template_filters(app)
    # configure_context_processors(app)
    configure_before_handlers(app)
    configure_after_handlers(app)
    configure_errorhandlers(app)

    return app


def configure_app(app, config_class):
    app.config.from_object(config_class)
    # 不检查路由中最后是否有斜杠/
    app.url_map.strict_slashes = False


def configure_blueprints(app):
    # 注册 blueprint
    app.register_blueprint(api_bp, url_prefix='/api')


def configure_extensions(app):
    """配置扩展。"""
    # Enable CORS
    cors.init_app(app)
    # Init Flask-SQLAlchemy
    db.init_app(app)
    # Init Flask-Migrate
    migrate.init_app(app, db)
    # Init Flask-Mail
    mail.init_app(app)


def configure_before_handlers(app):
    """配置请求前处理程序"""
    pass


def configure_after_handlers(app):
    """配置请求后处理程序"""
    pass


def configure_errorhandlers(app):
    """配置错误处理程序"""
    pass
