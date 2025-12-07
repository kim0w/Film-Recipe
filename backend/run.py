"""Flask 애플리케이션 실행"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 프로젝트 루트를 PYTHONPATH에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.app import create_app

# Flask 앱 생성
app = create_app()

if __name__ == '__main__':
    # 환경변수에서 설정 읽기
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')  # 기본값은 localhost만
    port = int(os.getenv('FLASK_PORT', '5000'))

    # 개발 서버 실행
    app.run(
        debug=debug_mode,
        host=host,
        port=port
    )
