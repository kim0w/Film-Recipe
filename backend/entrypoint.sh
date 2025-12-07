#!/bin/bash
# Backend entrypoint script

set -e

echo "========================================="
echo "Film Recipe Backend - Starting..."
echo "========================================="

# 데이터베이스 파일 확인
if [ ! -f "/app/database/filmrecipe.db" ]; then
    echo "Database not found. Initializing..."
    python /app/init_db.py

    if [ $? -eq 0 ]; then
        echo "✓ Database initialized successfully"
    else
        echo "✗ Database initialization failed"
        exit 1
    fi
else
    echo "✓ Database already exists"
fi

# 그레인 텍스처 확인
if [ ! -d "/app/data/grain_overlays" ] || [ -z "$(ls -A /app/data/grain_overlays)" ]; then
    echo "Grain textures not found. Generating..."
    python -c "from backend.app.utils.grain_generator import GrainGenerator; from pathlib import Path; GrainGenerator.generate_all_mvp_grains(Path('/app/data/grain_overlays'))"
    echo "✓ Grain textures generated"
else
    echo "✓ Grain textures already exist"
fi

# 임시 폴더 권한 설정
mkdir -p /app/data/temp
chmod 777 /app/data/temp

echo "========================================="
echo "Starting Gunicorn server..."
echo "========================================="

# CMD 실행
exec "$@"
