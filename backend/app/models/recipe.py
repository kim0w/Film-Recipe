"""FilmRecipe 모델"""
from backend.app import db
from datetime import datetime

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

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'film_id': self.film_id,
            'recipe_name': self.recipe_name,
            'process_type': self.process_type,
            'iso_range': f"{self.iso_min}-{self.iso_max}",
            'grain_size': self.grain_size,
            'grain_intensity': self.grain_intensity,
            'color_temperature': self.color_temperature,
            'white_balance': self.white_balance,
            'matching_reason': self.matching_reason
        }

    def __repr__(self):
        return f'<FilmRecipe {self.recipe_name} for Film ID {self.film_id}>'
