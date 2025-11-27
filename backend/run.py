"""Flask 애플리케이션 실행"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트를 PYTHONPATH에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.app import create_app

# .env 파일 로드
load_dotenv()

# Flask 앱 생성
app = create_app()

if __name__ == '__main__':
    # 개발 서버 실행
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
