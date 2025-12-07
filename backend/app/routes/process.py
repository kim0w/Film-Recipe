"""이미지 처리 및 다운로드 API"""
from flask import Blueprint, request, jsonify, send_file, Response
from pathlib import Path
from typing import List, Dict, Any, Tuple
import zipfile
import io
import logging
import time

from backend.config import Config
from backend.app.models.film import Film
from backend.app.services.image_processor import ImageProcessor

bp = Blueprint('process', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)


@bp.route('/process', methods=['POST'])
def process_images() -> Tuple[Response, int]:
    """
    이미지 처리 (필름 시뮬레이션 적용)

    Request:
        {
            "job_id": "abc123",
            "film_ids": [1, 2, 3, 4, 5],
            "options": {
                "output_quality": 95
            }
        }

    Returns:
        JSON: 처리 결과 및 다운로드 URL
    """
    start_time = time.time()

    try:
        # 1. 요청 데이터 파싱 및 검증
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        job_id = data.get('job_id', '').strip()
        film_ids = data.get('film_ids', [])

        # job_id 검증 (길이 및 문자 검증)
        if not job_id or len(job_id) != 12:
            return jsonify({
                'error': 'Invalid job_id format (must be 12 characters)'
            }), 400

        # film_ids 검증
        if not film_ids or not isinstance(film_ids, list):
            return jsonify({
                'error': 'film_ids must be a non-empty list'
            }), 400

        if len(film_ids) > 10:
            return jsonify({
                'error': f'Maximum 10 films allowed (got {len(film_ids)})'
            }), 400

        # film_ids가 모두 정수인지 확인
        if not all(isinstance(fid, int) for fid in film_ids):
            return jsonify({
                'error': 'All film_ids must be integers'
            }), 400

        logger.info(f"Processing request for job {job_id} with {len(film_ids)} films")

        # 2. Job 폴더 확인
        job_folder = Config.UPLOAD_FOLDER / job_id

        if not job_folder.exists():
            logger.error(f"Job folder not found: {job_id}")
            return jsonify({'error': f'Job {job_id} not found'}), 404

        if not job_folder.is_dir():
            logger.error(f"Job path is not a directory: {job_id}")
            return jsonify({'error': f'Invalid job path'}), 500

        # 3. 입력 이미지 파일 찾기
        input_files = list(job_folder.glob('*.[jJ][pP][gG]')) + \
                     list(job_folder.glob('*.[jJ][pP][eE][gG]')) + \
                     list(job_folder.glob('*.[pP][nN][gG]'))

        # UUID 접두사가 있는 파일만 (원본 파일)
        input_files = [f for f in input_files if len(f.stem) > 8 and '_' in f.stem]

        if not input_files:
            logger.error(f"No input images found in job {job_id}")
            return jsonify({'error': 'No input images found'}), 404

        logger.info(f"Found {len(input_files)} input image(s) for job {job_id}")

        # 4. 출력 폴더 생성
        output_folder = job_folder / 'processed'
        try:
            output_folder.mkdir(exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create output folder: {e}")
            return jsonify({'error': 'Failed to create output directory'}), 500

        # 5. 각 입력 이미지 × 각 필름별로 이미지 처리
        results = []
        failed_film_ids = []

        # MVP: 첫 번째 이미지만 처리 (성능 고려)
        # TODO: Phase 2에서 다중 이미지 × 다중 필름 처리 추가
        input_file = input_files[0]
        logger.info(f"Processing image: {input_file.name} with {len(film_ids)} film(s)")

        for idx, film_id in enumerate(film_ids, 1):
            logger.info(f"Processing film {idx}/{len(film_ids)}: ID={film_id}")

            # 필름 정보 조회
            try:
                film = Film.query.get(film_id)
            except Exception as e:
                logger.error(f"Database error querying film {film_id}: {e}", exc_info=True)
                failed_film_ids.append({
                    'film_id': film_id,
                    'error': 'Database error',
                    'status': 'failed'
                })
                continue

            if not film:
                logger.warning(f"Film not found: {film_id}")
                failed_film_ids.append({
                    'film_id': film_id,
                    'error': 'Film not found',
                    'status': 'failed'
                })
                continue

            if not film.recipes:
                logger.warning(f"No recipes found for film: {film.name} (ID={film_id})")
                failed_film_ids.append({
                    'film_id': film_id,
                    'film_name': film.name,
                    'error': 'No active recipe for this film',
                    'status': 'failed'
                })
                continue

            recipe = film.recipes[0]
            logger.debug(f"Using recipe for {film.name}: grain_intensity={recipe.grain_intensity}")

            # 출력 파일명 생성
            film_slug = film.name.lower().replace(' ', '_').replace('/', '_')

            # 원본 파일명에서 UUID 제거
            try:
                original_name = input_file.stem.split('_', 1)[1] if '_' in input_file.stem else input_file.stem
            except IndexError:
                original_name = input_file.stem

            output_filename = f"{original_name}_{film_slug}.jpg"
            output_path = output_folder / output_filename

            # 필름 레시피 딕셔너리 생성
            film_recipe_dict = {
                'film_name': film.name,
                'type': film.type,
                'grain_intensity': recipe.grain_intensity or 0.3,
                'bw_weight_r': recipe.bw_weight_r,
                'bw_weight_g': recipe.bw_weight_g,
                'bw_weight_b': recipe.bw_weight_b,
            }

            # 이미지 처리
            film_start_time = time.time()
            try:
                logger.info(f"Applying film simulation: {film.name}")
                ImageProcessor.apply_film_simulation(
                    str(input_file),
                    str(output_path),
                    film_recipe_dict
                )

                processing_time = time.time() - film_start_time
                logger.info(f"Successfully processed {film.name} in {processing_time:.2f}s")

                results.append({
                    'film_id': film.id,
                    'film_name': film.name,
                    'output_url': f"/api/download/{job_id}/{output_filename}",
                    'status': 'success',
                    'processing_time': round(processing_time, 2)
                })

            except Exception as e:
                processing_time = time.time() - film_start_time
                logger.error(
                    f"Failed to process film {film.name} after {processing_time:.2f}s: {e}",
                    exc_info=True
                )
                results.append({
                    'film_id': film.id,
                    'film_name': film.name,
                    'error': str(e),
                    'status': 'failed'
                })

        # 6. failed_film_ids를 results에 병합
        all_results = results + failed_film_ids

        # 7. 응답 생성
        total_time = time.time() - start_time
        success_count = len([r for r in all_results if r.get('status') == 'success'])
        failed_count = len([r for r in all_results if r.get('status') == 'failed'])

        response_data = {
            'job_id': job_id,
            'status': 'completed',
            'total': len(film_ids),
            'success': success_count,
            'failed': failed_count,
            'results': all_results,
            'zip_url': f"/api/download/{job_id}/all_films.zip" if success_count > 0 else None,
            'processing_time': round(total_time, 2)
        }

        # 여러 이미지 업로드 시 경고 메시지
        if len(input_files) > 1:
            response_data['warning'] = f"MVP에서는 첫 번째 이미지만 처리됩니다. (총 {len(input_files)}개 업로드됨)"
            logger.info(f"Multiple images uploaded ({len(input_files)}), but only first one processed")

        logger.info(
            f"Processing completed for job {job_id}: "
            f"{success_count} success, {failed_count} failed, "
            f"total time: {total_time:.2f}s"
        )

        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Unexpected error in process_images: {e}", exc_info=True)
        return jsonify({
            'error': 'Processing failed',
            'message': str(e)
        }), 500


@bp.route('/download/<job_id>/<filename>', methods=['GET'])
def download_file(job_id: str, filename: str) -> Tuple[Response, int]:
    """
    처리된 이미지 다운로드

    Args:
        job_id (str): Job ID
        filename (str): 파일명 또는 'all_films.zip'

    Returns:
        File: 이미지 파일 또는 ZIP 파일
    """
    try:
        # job_id 검증
        if not job_id or len(job_id) != 12:
            return jsonify({'error': 'Invalid job_id'}), 400

        # filename 검증 (기본 보안 체크)
        if not filename or '..' in filename or '/' in filename or '\\' in filename:
            logger.warning(f"Invalid filename requested: {filename}")
            return jsonify({'error': 'Invalid filename'}), 400

        # ZIP 다운로드 요청
        if filename == 'all_films.zip':
            return download_zip(job_id)

        # 개별 파일 다운로드
        file_path = Config.UPLOAD_FOLDER / job_id / 'processed' / filename

        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return jsonify({'error': 'File not found'}), 404

        if not file_path.is_file():
            logger.error(f"Path is not a file: {file_path}")
            return jsonify({'error': 'Invalid file path'}), 400

        # MIME type 결정
        ext = file_path.suffix.lower()
        mimetype = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png'
        }.get(ext, 'application/octet-stream')

        logger.info(f"Downloading file: {filename} for job {job_id}")

        return send_file(
            str(file_path),
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        logger.error(f"Download failed for {filename}: {e}", exc_info=True)
        return jsonify({
            'error': 'Download failed',
            'message': str(e)
        }), 500


def download_zip(job_id: str) -> Tuple[Response, int]:
    """
    선택한 필름들을 ZIP으로 묶어 다운로드

    Args:
        job_id (str): Job ID

    Returns:
        File: ZIP 파일
    """
    try:
        # job_id 검증
        if not job_id or len(job_id) != 12:
            return jsonify({'error': 'Invalid job_id'}), 400

        processed_folder = Config.UPLOAD_FOLDER / job_id / 'processed'

        if not processed_folder.exists():
            logger.warning(f"Processed folder not found for job {job_id}")
            return jsonify({'error': 'No processed images found'}), 404

        if not processed_folder.is_dir():
            logger.error(f"Processed path is not a directory: {processed_folder}")
            return jsonify({'error': 'Invalid processed folder'}), 500

        # 처리된 모든 이미지 파일 찾기
        image_files = list(processed_folder.glob('*.[jJ][pP][gG]')) + \
                     list(processed_folder.glob('*.[jJ][pP][eE][gG]')) + \
                     list(processed_folder.glob('*.[pP][nN][gG]'))

        # 실제 파일인지 확인 (디렉토리 제외)
        image_files = [f for f in image_files if f.is_file()]

        if not image_files:
            logger.warning(f"No processed images found in {processed_folder}")
            return jsonify({'error': 'No images to download'}), 404

        logger.info(f"Creating ZIP with {len(image_files)} file(s) for job {job_id}")

        # 메모리에 ZIP 파일 생성
        zip_buffer = io.BytesIO()

        try:
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for img_path in image_files:
                    try:
                        # ZIP 내부 파일명 (경로 없이 파일명만)
                        arcname = img_path.name
                        zip_file.write(str(img_path), arcname=arcname)
                        logger.debug(f"Added to ZIP: {arcname}")
                    except Exception as e:
                        logger.error(f"Failed to add {img_path.name} to ZIP: {e}")
                        # 일부 파일 실패해도 계속 진행

            zip_buffer.seek(0)

            logger.info(f"ZIP created successfully for job {job_id}")

            return send_file(
                zip_buffer,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f'filmrecipe_{job_id}.zip'
            )

        except zipfile.BadZipFile as e:
            logger.error(f"ZIP file creation failed: {e}", exc_info=True)
            return jsonify({
                'error': 'ZIP creation failed',
                'message': 'Invalid ZIP file'
            }), 500

    except Exception as e:
        logger.error(f"Unexpected error in download_zip for job {job_id}: {e}", exc_info=True)
        return jsonify({
            'error': 'ZIP creation failed',
            'message': str(e)
        }), 500
