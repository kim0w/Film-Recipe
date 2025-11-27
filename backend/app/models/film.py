"""Film 모델"""
from backend.app import db
from datetime import datetime

class Film(db.Model):
    """필름 정보 모델"""

    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'color' or 'bw'
    iso_base = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    tier = db.Column(db.String(20), default='mvp')  # 'mvp', 'core', 'extended', 'archive'
    pdf_analyzed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계: 하나의 필름은 여러 레시피를 가질 수 있음
    recipes = db.relationship('FilmRecipe', backref='film', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_recipes=False):
        """딕셔너리로 변환"""
        result = {
            'id': self.id,
            'name': self.name,
            'manufacturer': self.manufacturer,
            'type': self.type,
            'iso_base': self.iso_base,
            'description': self.description,
            'tier': self.tier
        }

        if include_recipes:
            result['recipes'] = [recipe.to_dict() for recipe in self.recipes]

        return result

    def __repr__(self):
        return f'<Film {self.name}>'
