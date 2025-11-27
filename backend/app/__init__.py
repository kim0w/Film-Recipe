"""Flask 애플리케이션 팩토리"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 인스턴스 생성
db = SQLAlchemy()

def create_app(config_class='backend.config.Config'):
    """Flask 애플리케이션 생성 및 설정"""
    app = Flask(__name__)

    # 설정 로드
    app.config.from_object(config_class)

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
        from backend.app.routes import films
        app.register_blueprint(films.bp)

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
