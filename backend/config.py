"""Flask 애플리케이션 설정"""
from pathlib import Path
import os

class Config:
    """기본 설정 클래스"""

    # 기본 경로
    BASE_DIR = Path(__file__).parent.parent

    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/database/filmrecipe.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 업로드 설정
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'temp'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tiff'}

    # 보안 설정
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # CORS 설정
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
