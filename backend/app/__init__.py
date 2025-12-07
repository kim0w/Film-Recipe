"""Flask 애플리케이션 팩토리"""
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 인스턴스 생성
db = SQLAlchemy()

def create_app(config_name=None):
    """Flask 애플리케이션 생성 및 설정

    Args:
        config_name (str): 설정 이름 ('development', 'production', 'test')
                          None인 경우 FLASK_ENV 환경변수 사용
    """
    app = Flask(__name__)

    # 환경 설정 결정
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    # 설정 로드
    from backend.config import config
    config_class = config[config_name]
    app.config.from_object(config_class)

    # 프로덕션 설정 초기화 (로깅 등)
    if hasattr(config_class, 'init_app'):
        config_class.init_app(app)

    # 확장 기능 초기화
    db.init_app(app)

    # CORS 설정
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type"]
        }
    })

    # 블루프린트 등록
    with app.app_context():
        from backend.app.routes import films, upload, process
        app.register_blueprint(films.bp)
        app.register_blueprint(upload.bp)
        app.register_blueprint(process.bp)

    # 기본 라우트
    @app.route('/')
    def index():
        return {
            'service': 'Film Recipe API',
            'version': '1.0.0',
            'status': 'running'
        }

    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    return app
