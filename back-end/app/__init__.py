import rq
from flask import Flask
from redis import Redis

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
    # 整合RQ任务队列
    app.redis = Redis.from_url(app.config['REDIS_URL'])  # 创建 Redis 实例
    # 创建 RQ 队列。设置任务队列中各任务的执行最大超时时间为 1 小时
    app.task_queue = rq.Queue('madblog-tasks', connection=app.redis, default_timeout=3600)


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
