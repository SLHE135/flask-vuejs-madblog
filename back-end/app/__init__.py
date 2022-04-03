from flask import Flask
from flask_cors import CORS

from config import Config


# 创建Flask应用程序实例
def create_app(config_class=Config):
    app = Flask(__name__)  # 创建Flask应用程序实例
    app.config.from_object(config_class)  # 加载配置

    # 初始化CORS
    CORS(app)

    # 注册blueprint
    from app.api import bp as api_bp  # 导入蓝图
    app.register_blueprint(api_bp, url_prefix='/api')  # 注册蓝图

    return app  # 返回应用程序实例
