"""Flask 애플리케이션 설정"""
from pathlib import Path
import os


class Config:
    """기본 설정 클래스"""

    # 기본 경로
    BASE_DIR = Path(__file__).parent.parent

    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{BASE_DIR}/database/filmrecipe.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # 연결 상태 확인
        'pool_recycle': 300,  # 5분마다 연결 재활용
    }

    # 업로드 설정
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'temp'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tiff', 'tif'}

    # 보안 설정
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # CORS 설정
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # 로깅 설정
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """프로덕션 환경 설정"""
    DEBUG = False
    TESTING = False

    # 프로덕션 최적화
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
    }

    # 프로덕션에서는 SECRET_KEY 필수
    @classmethod
    def init_app(cls, app):
        # SECRET_KEY 검증
        if app.config['SECRET_KEY'] == 'dev-secret-key-change-in-production':
            raise ValueError(
                'Production requires a proper SECRET_KEY environment variable. '
                'Generate one with: python -c "import secrets; print(secrets.token_hex(32))"'
            )

        # 로깅 설정
        import logging
        from logging.handlers import RotatingFileHandler
        import os

        # 로그 디렉토리 생성
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # 파일 핸들러 (10MB, 백업 10개)
        file_handler = RotatingFileHandler(
            'logs/filmrecipe.log',
            maxBytes=10 * 1024 * 1024,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Film Recipe production startup')


class TestConfig(Config):
    """테스트 환경 설정"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 메모리 DB 사용


# 환경별 설정 매핑
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,
    'default': DevelopmentConfig
}
