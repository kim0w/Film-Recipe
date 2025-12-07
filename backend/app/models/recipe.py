"""FilmRecipe 모델"""
from backend.app import db
from datetime import datetime
import json

class FilmRecipe(db.Model):
    """필름 레시피 모델"""

    __tablename__ = 'film_recipes'

    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'), nullable=False)
    recipe_name = db.Column(db.String(100), nullable=False)
    process_type = db.Column(db.String(20), nullable=False)

    # ISO 범위
    iso_min = db.Column(db.Integer)
    iso_max = db.Column(db.Integer)

    # 그레인 특성
    grain_size = db.Column(db.Integer)
    grain_intensity = db.Column(db.Float)

    # 색온도 (컬러 필름만)
    color_temperature = db.Column(db.Integer)
    white_balance = db.Column(db.String(20))
    base_mask_color = db.Column(db.String(10))

    # 흑백 RGB 가중치 (흑백 필름만)
    bw_weight_r = db.Column(db.Float, default=0.299)
    bw_weight_g = db.Column(db.Float, default=0.587)
    bw_weight_b = db.Column(db.Float, default=0.114)

    # 과학적 데이터 (JSON 문자열)
    tone_curve_data = db.Column(db.Text)
    spectral_dye_density = db.Column(db.Text)
    reciprocity_failure_data = db.Column(db.Text)

    # 매칭 로직
    matching_reason = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    # 타임스탬프
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def tone_curve(self):
        """톤 커브 데이터를 파이썬 딕셔너리로 반환"""
        if self.tone_curve_data:
            try:
                return json.loads(self.tone_curve_data)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    @property
    def spectral_dye(self):
        """스펙트럴 염료 밀도를 파이썬 딕셔너리로 반환"""
        if self.spectral_dye_density:
            try:
                return json.loads(self.spectral_dye_density)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    @property
    def reciprocity_failure(self):
        """상반칙 불궤 데이터를 파이썬 딕셔너리로 반환"""
        if self.reciprocity_failure_data:
            try:
                return json.loads(self.reciprocity_failure_data)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def to_dict(self, include_scientific_data=False):
        """딕셔너리로 변환"""
        result = {
            'id': self.id,
            'film_id': self.film_id,
            'recipe_name': self.recipe_name,
            'process_type': self.process_type,
            'iso_range': f"{self.iso_min}-{self.iso_max}",
            'grain_size': self.grain_size,
            'grain_intensity': self.grain_intensity,
            'matching_reason': self.matching_reason
        }

        # 필름 타입에 따라 적절한 속성만 포함
        if self.film and self.film.type == 'color':
            # 컬러 필름: 색온도 정보 포함
            result['color_temperature'] = self.color_temperature
            result['white_balance'] = self.white_balance
            if self.base_mask_color:
                result['base_mask_color'] = self.base_mask_color
        elif self.film and self.film.type == 'bw':
            # 흑백 필름: RGB 가중치 포함
            result['bw_weights'] = {
                'r': self.bw_weight_r,
                'g': self.bw_weight_g,
                'b': self.bw_weight_b
            }

        if include_scientific_data:
            result['tone_curve'] = self.tone_curve
            result['spectral_dye'] = self.spectral_dye
            result['reciprocity_failure'] = self.reciprocity_failure

        return result

    def __repr__(self):
        return f'<FilmRecipe {self.recipe_name} for Film ID {self.film_id}>'
