"""이미지 업로드 및 EXIF 분석 API"""
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from pathlib import Path
from PIL import Image
from typing import List, Dict, Any
import uuid
import os
import logging

from backend.config import Config
from backend.app.services.exif_extractor import EXIFExtractor
from backend.app.services.film_matcher import FilmMatcher

bp = Blueprint('upload', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

# 상수
MAX_FILES = 10
MAX_FILE_SIZE = Config.MAX_CONTENT_LENGTH


def allowed_file(filename: str) -> bool:
    """
    허용된 파일 확장자 검사

    Args:
        filename (str): 파일명

    Returns:
        bool: 허용 여부
    """
    if not filename or '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS


def verify_image_file(filepath: Path) -> bool:
    """
    실제 이미지 파일인지 검증 (보안 강화)

    Args:
        filepath (Path): 파일 경로

    Returns:
        bool: 유효한 이미지 파일 여부
    """
    try:
        with Image.open(filepath) as img:
            img.verify()  # 파일이 손상되지 않았는지 검증
        return True
    except Exception as e:
        logger.warning(f"Image verification failed for {filepath}: {e}")
        return False


@bp.route('/upload', methods=['POST'])
def upload_images():
    """
    이미지 업로드 및 EXIF 추출 + 필름 자동 매칭

    Request:
        multipart/form-data
        - images: 이미지 파일 (최대 10개, 각 최대 50MB)

    Returns:
        JSON: job_id, 이미지 정보, EXIF 데이터, 매칭된 필름 목록
    """
    try:
        # 1. 파일 검증
        if 'images' not in request.files:
            return jsonify({
                'error': 'No images field in request'
            }), 400

        files = request.files.getlist('images')

        if not files or files[0].filename == '':
            return jsonify({
                'error': 'No files selected'
            }), 400

        # 최대 파일 개수 제한
        if len(files) > MAX_FILES:
            return jsonify({
                'error': f'Maximum {MAX_FILES} images allowed',
                'count': len(files)
            }), 400

        # 파일 크기 제한 사전 검증
        for file in files:
            if file and file.filename:
                # 파일 크기 체크 (seek을 사용한 크기 확인)
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(0)  # 파일 포인터 원위치

                if file_size > MAX_FILE_SIZE:
                    return jsonify({
                        'error': f'File {file.filename} exceeds maximum size',
                        'file_size_mb': round(file_size / 1024 / 1024, 2),
                        'max_size_mb': round(MAX_FILE_SIZE / 1024 / 1024)
                    }), 413  # 413 Payload Too Large

                if file_size == 0:
                    return jsonify({
                        'error': f'File {file.filename} is empty'
                    }), 400

        # 2. Job ID 생성 (UUID 앞 12자리)
        job_id = str(uuid.uuid4())[:12]

        # 3. Job 폴더 생성
        job_folder = Config.UPLOAD_FOLDER / job_id
        job_folder.mkdir(parents=True, exist_ok=True)

        # 4. 각 이미지 처리
        results = []

        for file in files:
            if not file or file.filename == '':
                continue

            if not allowed_file(file.filename):
                continue

            # 파일명 안전하게 처리
            original_filename = secure_filename(file.filename)
            filename = f"{uuid.uuid4().hex[:8]}_{original_filename}"
            filepath = job_folder / filename

            try:
                # 파일 저장
                file.save(str(filepath))

                # 이미지 파일 검증 (보안 강화)
                if not verify_image_file(filepath):
                    logger.warning(f"Invalid image file uploaded: {original_filename}")
                    filepath.unlink()  # 유효하지 않은 파일 삭제
                    continue

                # EXIF 추출
                exif_data = EXIFExtractor.extract(str(filepath))
                logger.info(
                    f"EXIF extracted from {original_filename}: "
                    f"ISO {exif_data.get('iso')}, "
                    f"f/{exif_data.get('aperture')}"
                )

                # 필름 매칭 (상위 5개)
                matched_films = FilmMatcher.match(exif_data, limit=5)
                logger.info(
                    f"Top matched film for {original_filename}: "
                    f"{matched_films[0]['film_name']} "
                    f"(score: {matched_films[0]['score']})"
                    if matched_films else "No matches"
                )

                # 결과 추가
                results.append({
                    'filename': filename,
                    'original_filename': original_filename,
                    'exif': exif_data,
                    'matched_films': matched_films
                })

            except Exception as e:
                logger.error(
                    f"Failed to process file {original_filename}: {e}",
                    exc_info=True
                )
                # 에러 발생 시 저장된 파일 삭제
                if filepath.exists():
                    try:
                        filepath.unlink()
                    except Exception as unlink_error:
                        logger.error(f"Failed to delete file {filepath}: {unlink_error}")
                continue

        if not results:
            # 저장된 파일이 없으면 에러
            return jsonify({
                'error': 'No valid images uploaded'
            }), 400

        # 5. 응답 반환
        return jsonify({
            'job_id': job_id,
            'count': len(results),
            'images': results
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Upload failed',
            'message': str(e)
        }), 500


@bp.route('/jobs/<job_id>', methods=['GET'])
def get_job_info(job_id: str):
    """
    Job 정보 조회

    Args:
        job_id (str): Job ID

    Returns:
        JSON: Job 폴더 내 파일 목록
    """
    try:
        job_folder = Config.UPLOAD_FOLDER / job_id

        if not job_folder.exists():
            return jsonify({
                'error': f'Job {job_id} not found'
            }), 404

        # 원본 이미지 파일 목록
        original_files = list(job_folder.glob('*.[jJ][pP][gG]')) + \
                        list(job_folder.glob('*.[pP][nN][gG]')) + \
                        list(job_folder.glob('*.[jJ][pP][eE][gG]'))

        # 처리된 이미지 폴더
        processed_folder = job_folder / 'processed'
        processed_files = []

        if processed_folder.exists():
            processed_files = list(processed_folder.glob('*.[jJ][pP][gG]')) + \
                            list(processed_folder.glob('*.[pP][nN][gG]'))

        return jsonify({
            'job_id': job_id,
            'original_count': len(original_files),
            'processed_count': len(processed_files),
            'status': 'completed' if processed_files else 'uploaded'
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to get job info',
            'message': str(e)
        }), 500
