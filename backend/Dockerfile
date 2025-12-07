# Backend Dockerfile for Flask API
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 라이브러리 설치
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사
COPY requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 필요한 디렉토리 생성
RUN mkdir -p /app/data/temp /app/data/grain_overlays /app/database /app/logs

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_HOST=0.0.0.0 \
    FLASK_PORT=8080

# 포트 노출
EXPOSE 8080

# 데이터베이스 초기화 및 서버 시작 스크립트
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Entrypoint 설정
ENTRYPOINT ["/app/entrypoint.sh"]

# 기본 명령어 (Gunicorn 서버)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "backend.app:create_app()"]
