"""데이터베이스 초기화 스크립트"""
import os
import sys
from pathlib import Path
import sqlite3
import logging

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.config import Config

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def init_database():
    """
    데이터베이스 초기화

    1. 스키마 생성
    2. 초기 데이터 삽입
    3. 그레인 텍스처 생성
    """
    try:
        # 1. 데이터베이스 경로 확인
        db_path = Config.BASE_DIR / 'database' / 'filmrecipe.db'
        schema_path = Config.BASE_DIR / 'database' / 'schema.sql'

        logger.info(f"Database path: {db_path}")
        logger.info(f"Schema path: {schema_path}")

        # 데이터베이스 디렉토리 생성
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # 2. 스키마 읽기
        if not schema_path.exists():
            logger.error(f"Schema file not found: {schema_path}")
            return False

        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # 3. 데이터베이스 연결 및 스키마 실행
        logger.info("Creating database schema...")
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # 스키마 실행 (여러 문장이므로 executescript 사용)
        cursor.executescript(schema_sql)
        conn.commit()

        # 4. 데이터 확인
        cursor.execute("SELECT COUNT(*) FROM films")
        film_count = cursor.fetchone()[0]
        logger.info(f"✓ Films created: {film_count}")

        cursor.execute("SELECT COUNT(*) FROM film_recipes")
        recipe_count = cursor.fetchone()[0]
        logger.info(f"✓ Recipes created: {recipe_count}")

        conn.close()

        # 5. 그레인 텍스처 생성
        logger.info("Generating grain textures...")
        from backend.app.utils.grain_generator import GrainGenerator

        grain_folder = Config.BASE_DIR / 'data' / 'grain_overlays'
        grain_folder.mkdir(parents=True, exist_ok=True)

        GrainGenerator.generate_all_mvp_grains(grain_folder)
        logger.info(f"✓ Grain textures generated in {grain_folder}")

        logger.info("\n✅ Database initialization completed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}", exc_info=True)
        return False


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("Film Recipe - Database Initialization")
    logger.info("=" * 60)

    success = init_database()
    sys.exit(0 if success else 1)
