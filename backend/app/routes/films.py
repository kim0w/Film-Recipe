"""필름 관련 API 엔드포인트"""
from flask import Blueprint, jsonify, request
from backend.app.models.film import Film
from backend.app.models.recipe import FilmRecipe
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('films', __name__, url_prefix='/api')


@bp.route('/films', methods=['GET'])
def get_films():
    """
    필름 목록 조회 API

    Query Parameters:
        tier (str): 필름 tier 필터 ('mvp', 'core', 'extended', 'all')
        type (str): 필름 타입 필터 ('color', 'bw', 'all')

    Returns:
        JSON: 필름 목록과 개수
    """
    try:
        # Query 파라미터 읽기
        tier = request.args.get('tier', 'mvp')
        film_type = request.args.get('type', 'all')

        # 유효한 tier 값 검증
        valid_tiers = ['mvp', 'core', 'extended', 'archive', 'all']
        if tier not in valid_tiers:
            return jsonify({
                'error': f'Invalid tier. Must be one of {valid_tiers}'
            }), 400

        # 유효한 type 값 검증
        valid_types = ['color', 'bw', 'all']
        if film_type not in valid_types:
            return jsonify({
                'error': f'Invalid type. Must be one of {valid_types}'
            }), 400

        # 쿼리 시작
        query = Film.query

        # tier 필터링
        if tier != 'all':
            query = query.filter(Film.tier == tier)

        # type 필터링
        if film_type != 'all':
            query = query.filter(Film.type == film_type)

        # ISO 순으로 정렬
        query = query.order_by(Film.iso_base)

        # 결과 조회
        films = query.all()

        # JSON 변환 (레시피 포함)
        films_data = [film.to_dict(include_recipes=True) for film in films]

        return jsonify({
            'count': len(films_data),
            'films': films_data,
            'filters': {
                'tier': tier,
                'type': film_type
            }
        }), 200

    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Database error occurred',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@bp.route('/films/<int:film_id>', methods=['GET'])
def get_film_by_id(film_id):
    """
    특정 필름 상세 정보 조회

    Args:
        film_id (int): 필름 ID

    Returns:
        JSON: 필름 상세 정보 (레시피 포함)
    """
    try:
        film = Film.query.get(film_id)

        if not film:
            return jsonify({
                'error': f'Film with ID {film_id} not found'
            }), 404

        return jsonify({
            'film': film.to_dict(include_recipes=True)
        }), 200

    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Database error occurred',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500
