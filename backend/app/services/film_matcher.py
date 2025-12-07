"""필름 매칭 알고리즘 서비스"""
from typing import List, Dict
import logging
from backend.app.models.film import Film
from backend.app.models.recipe import FilmRecipe

logger = logging.getLogger(__name__)


class FilmMatcher:
    """EXIF 데이터를 기반으로 최적의 필름을 매칭하는 클래스"""

    @staticmethod
    def match(exif_data: Dict, limit: int = 5) -> List[Dict]:
        """
        EXIF 데이터를 기반으로 필름 매칭

        Args:
            exif_data (Dict): EXIF 메타데이터
            limit (int): 반환할 필름 개수 (기본 5개)

        Returns:
            List[Dict]: 매칭된 필름 목록 (점수 순 정렬)
        """
        try:
            # 활성화된 레시피만 조회
            recipes = FilmRecipe.query.filter_by(is_active=True).all()

            if not recipes:
                logger.warning("No active film recipes found in database")
                return []

            logger.debug(f"Found {len(recipes)} active recipes for matching")
        except Exception as e:
            logger.error(f"Database error while querying recipes: {e}", exc_info=True)
            return []

        results = []

        for recipe in recipes:
            # 각 레시피에 대해 점수 계산
            score = FilmMatcher._calculate_score(exif_data, recipe)

            results.append({
                'film_id': recipe.film_id,
                'film_name': recipe.film.name,
                'manufacturer': recipe.film.manufacturer,
                'tier': recipe.film.tier,
                'recipe_id': recipe.id,
                'recipe_name': recipe.recipe_name,
                'score': round(score, 1),
                'reason': FilmMatcher._generate_reason(exif_data, recipe, score),
                'iso_base': recipe.film.iso_base,
                'type': recipe.film.type,
            })

        # 점수 순으로 정렬 (높은 점수가 먼저)
        results.sort(key=lambda x: x['score'], reverse=True)

        # 상위 N개만 반환
        return results[:limit]

    @staticmethod
    def _calculate_score(exif_data: Dict, recipe: FilmRecipe) -> float:
        """
        EXIF 데이터와 필름 레시피를 비교하여 매칭 점수 계산

        가중치:
        - ISO: 50%
        - 색온도: 20%
        - 조리개: 15%
        - 셔터 속도: 15%

        Returns:
            float: 0 ~ 100 점수
        """
        score = 0.0

        # 1. ISO 매칭 (50% 가중치)
        iso_score = FilmMatcher._calculate_iso_score(exif_data.get('iso', 200), recipe)
        score += iso_score * 0.5

        # 2. 색온도 매칭 (20% 가중치 - 컬러 필름만)
        if recipe.film.type == 'color':
            wb_score = FilmMatcher._calculate_wb_score(exif_data, recipe)
            score += wb_score * 0.2
        else:
            # 흑백 필름은 색온도 점수 기본 80점
            score += 80 * 0.2

        # 3. 조리개 매칭 (15% 가중치)
        aperture_score = FilmMatcher._calculate_aperture_score(exif_data, recipe)
        score += aperture_score * 0.15

        # 4. 셔터 속도 매칭 (15% 가중치)
        shutter_score = FilmMatcher._calculate_shutter_score(exif_data, recipe)
        score += shutter_score * 0.15

        # 5. 저조도 보너스 (추가 점수)
        low_light_bonus = FilmMatcher._calculate_low_light_bonus(exif_data, recipe)
        score += low_light_bonus

        # 최종 점수는 0~100 범위로 제한
        return min(100.0, max(0.0, score))

    @staticmethod
    def _calculate_iso_score(exif_iso: int, recipe: FilmRecipe) -> float:
        """
        ISO 점수 계산 (0~100)

        Args:
            exif_iso (int): 촬영 ISO
            recipe (FilmRecipe): 필름 레시피

        Returns:
            float: ISO 매칭 점수
        """
        iso_min = recipe.iso_min or recipe.film.iso_base
        iso_max = recipe.iso_max or recipe.film.iso_base
        iso_base = recipe.film.iso_base or 100  # Division by zero 방지

        # ISO 범위 내에 있으면 100점
        if iso_min <= exif_iso <= iso_max:
            return 100.0

        # 범위 밖이면 거리에 따라 감점
        if exif_iso < iso_min:
            # 촬영 ISO가 필름 최소 ISO보다 낮음
            diff = iso_min - exif_iso
            penalty = (diff / iso_base) * 50
            return max(0.0, 100.0 - penalty)

        else:
            # 촬영 ISO가 필름 최대 ISO보다 높음
            diff = exif_iso - iso_max
            penalty = (diff / iso_base) * 50
            return max(0.0, 100.0 - penalty)

    @staticmethod
    def _calculate_wb_score(exif_data: Dict, recipe: FilmRecipe) -> float:
        """
        화이트 밸런스/색온도 점수 계산 (0~100)

        Args:
            exif_data (Dict): EXIF 데이터
            recipe (FilmRecipe): 필름 레시피

        Returns:
            float: WB 매칭 점수
        """
        wb = exif_data.get('white_balance', 'Auto')
        color_temp = exif_data.get('color_temperature', 5500)
        film_temp = recipe.color_temperature or 5500

        # Vision3 500T: 텅스텐 필름 특화
        if 'Vision3' in recipe.film.name and '500T' in recipe.film.name:
            if wb in ['Tungsten', 'Manual'] or color_temp <= 3500:
                # 명시적 텅스텐 환경
                return 100.0
            elif color_temp <= 4000:
                # 저색온도 환경
                return 90.0
            else:
                # 주광 환경 (불리)
                return 40.0

        # Daylight 필름 (5500K)
        if film_temp >= 5000:
            if wb in ['Daylight', 'Auto', 'Flash', 'Fine Weather'] or color_temp >= 5000:
                return 100.0
            elif color_temp >= 4500:
                return 85.0
            else:
                # 색온도 차이가 큼
                diff = abs(color_temp - film_temp)
                return max(40.0, 100.0 - (diff / 50))

        # 기본 점수
        return 75.0

    @staticmethod
    def _calculate_aperture_score(exif_data: Dict, recipe: FilmRecipe) -> float:
        """
        조리개 점수 계산 (0~100)

        조리개 크기와 필름 특성 매칭
        - 큰 조리개 (f/8+): 풍경 필름에 유리 (Velvia)
        - 작은 조리개 (≤f/2.8): 인물 필름에 유리 (Portra)

        Args:
            exif_data (Dict): EXIF 데이터
            recipe (FilmRecipe): 필름 레시피

        Returns:
            float: 조리개 매칭 점수
        """
        aperture = exif_data.get('aperture', 5.6)
        matching_reason = recipe.matching_reason or ''

        # Velvia: 풍경 필름 (큰 조리개 선호)
        if 'Velvia' in recipe.film.name:
            if aperture >= 8.0:
                return 100.0  # f/8 이상 → 심도 깊음 (풍경)
            elif aperture >= 5.6:
                return 85.0
            else:
                return 65.0

        # Portra: 인물 필름 (작은 조리개 선호)
        if 'Portra' in recipe.film.name:
            if aperture <= 2.8:
                return 100.0  # f/2.8 이하 → 얕은 심도 (인물)
            elif aperture <= 4.0:
                return 90.0
            elif aperture <= 5.6:
                return 80.0
            else:
                return 65.0

        # Provia: 만능형
        if 'Provia' in recipe.film.name:
            if 2.8 <= aperture <= 8.0:
                return 95.0  # 중간 범위
            else:
                return 75.0

        # Ektar: 풍경 특화, 최고 입자
        if 'Ektar' in recipe.film.name:
            if aperture >= 8.0:
                return 100.0  # 풍경 촬영 (큰 조리개)
            elif aperture >= 5.6:
                return 90.0
            else:
                return 75.0

        # Ektachrome: 중립적 리버설
        if 'Ektachrome' in recipe.film.name:
            if 4.0 <= aperture <= 8.0:
                return 90.0  # 중간 범위
            else:
                return 80.0

        # Gold/UltraMax: 소비자용, 웜톤
        if 'Gold' in recipe.film.name or 'UltraMax' in recipe.film.name:
            return 75.0  # 기본 점수

        # ProImage: 저가형
        if 'ProImage' in recipe.film.name:
            return 70.0  # 기본 점수 낮음

        # T-Max 400: 고감도 흑백
        if 'T-Max 400' in recipe.film.name:
            if aperture <= 4.0:
                return 90.0  # 저조도/액션
            else:
                return 80.0

        # Rollei RPX: 전통 흑백
        if 'Rollei' in recipe.film.name or 'RPX' in recipe.film.name:
            return 78.0  # 중간 점수

        # 기타 필름: 중립적 점수
        return 80.0

    @staticmethod
    def _calculate_shutter_score(exif_data: Dict, recipe: FilmRecipe) -> float:
        """
        셔터 속도 점수 계산 (0~100)

        Args:
            exif_data (Dict): EXIF 데이터
            recipe (FilmRecipe): 필름 레시피

        Returns:
            float: 셔터 속도 매칭 점수
        """
        shutter_speed = exif_data.get('shutter_speed', 0.008)  # 초 단위

        # 장노출 (1/10s 이상, >= 0.1초)
        if shutter_speed >= 0.1:
            # 상반칙 불궤 데이터가 있으면 유리
            if recipe.reciprocity_failure:
                return 100.0
            else:
                return 70.0

        # 초고속 셔터 (1/1000s 이하, <= 0.001초)
        elif shutter_speed <= 0.001:
            # 고감도 필름에 유리
            if recipe.film.iso_base >= 400:
                return 100.0
            else:
                return 75.0

        # 일반 셔터 속도 (1/60 ~ 1/500s)
        else:
            return 85.0

    @staticmethod
    def _calculate_low_light_bonus(exif_data: Dict, recipe: FilmRecipe) -> float:
        """
        저조도 환경 보너스 점수 계산

        저조도 판단 기준:
        - ISO >= 800 OR
        - 셔터 속도 >= 1/60s (0.0167초, 느린 셔터 = 저조도)
          주의: 셔터 속도는 초 단위이므로 큰 값 = 느린 셔터
          예) 1/30s = 0.033초, 1/125s = 0.008초

        보너스:
        - Vision3 500T: +15점 (텅스텐) / +10점 (일반 저조도)
        - Portra 400: +8점
        - 저감도 필름 (ISO < 200): -5점 (패널티)

        Args:
            exif_data (Dict): EXIF 데이터
            recipe (FilmRecipe): 필름 레시피

        Returns:
            float: 보너스 점수
        """
        iso = exif_data.get('iso', 200)
        shutter_speed = exif_data.get('shutter_speed', 0.008)
        wb = exif_data.get('white_balance', 'Auto')
        color_temp = exif_data.get('color_temperature', 5500)

        # 저조도 판단 (ISO 높거나 셔터 느림)
        LOW_LIGHT_SHUTTER_THRESHOLD = 1.0 / 60.0  # 0.0167초
        is_low_light = (iso >= 800) or (shutter_speed >= LOW_LIGHT_SHUTTER_THRESHOLD)

        if not is_low_light:
            return 0.0

        # Vision3 500T: 저조도 특화 필름
        if 'Vision3' in recipe.film.name and '500T' in recipe.film.name:
            # 텅스텐 조명 환경
            if wb in ['Tungsten', 'Manual'] or color_temp <= 3500:
                return 15.0  # 최대 보너스
            else:
                return 10.0  # 일반 저조도

        # Portra 400: 저조도 대응 가능
        if 'Portra' in recipe.film.name and recipe.film.iso_base == 400:
            return 8.0

        # 저감도 필름: 저조도에서 불리
        if recipe.film.iso_base < 200:
            return -5.0  # 패널티

        return 0.0

    @staticmethod
    def _generate_reason(exif_data: Dict, recipe: FilmRecipe, score: float) -> str:
        """
        매칭 이유 생성

        Args:
            exif_data (Dict): EXIF 데이터
            recipe (FilmRecipe): 필름 레시피
            score (float): 매칭 점수

        Returns:
            str: 매칭 이유 설명
        """
        iso = exif_data.get('iso', 200)
        shutter_speed = exif_data.get('shutter_speed', 0.008)
        aperture = exif_data.get('aperture', 5.6)

        # 저조도 여부 (동일한 로직 재사용)
        LOW_LIGHT_SHUTTER_THRESHOLD = 1.0 / 60.0
        is_low_light = (iso >= 800) or (shutter_speed >= LOW_LIGHT_SHUTTER_THRESHOLD)
        low_light_text = " [저조도 환경]" if is_low_light else ""

        # 기본 매칭 이유
        reason = f"ISO {iso}, f/{aperture}"

        # 필름별 특징 추가
        if score >= 85:
            reason += f" - {recipe.matching_reason}"
        elif score >= 70:
            reason += " - 적합"
        else:
            reason += " - 사용 가능"

        # 저조도 표시
        reason += low_light_text

        return reason
