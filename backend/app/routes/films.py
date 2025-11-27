"""필름 관련 API 엔드포인트"""
from flask import Blueprint, jsonify, request
from backend.app.models.film import Film
from backend.app.models.recipe import FilmRecipe

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
    # Query 파라미터 읽기
    tier = request.args.get('tier', 'mvp')
    film_type = request.args.get('type', 'all')

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
        'films': films_data
    }), 200


@bp.route('/films/<int:film_id>', methods=['GET'])
def get_film_by_id(film_id):
    """
    특정 필름 상세 정보 조회

    Args:
        film_id (int): 필름 ID

    Returns:
        JSON: 필름 상세 정보 (레시피 포함)
    """
    film = Film.query.get_or_404(film_id)

    return jsonify({
        'film': film.to_dict(include_recipes=True)
    }), 200
