# 🎯 Film Recipe MVP 개발 계획서 (Vibe Coding Plan)

> **목표:** 3일 내 완벽히 동작하는 필름 시뮬레이션 웹 애플리케이션 구현  
> **전략:** 백엔드 우선 → 테스트 → 프론트엔드 → 통합  
> **개발 방식:** Vibe Coding (빠른 프로토타이핑 + 점진적 개선)

**작성일:** 2025-11-26  
**버전:** 1.0.0  
**예상 총 시간:** 30시간 (3일 × 10시간)

---

## 📋 목차

1. [개발 규모 산정](#-개발-규모-산정)
2. [Day 1: 프로젝트 기반 구축](#-day-1-프로젝트-기반-구축-8시간)
3. [Day 2: 핵심 로직 구현](#-day-2-핵심-로직-구현-10시간)
4. [Day 3: 이미지 처리 + 프론트엔드](#-day-3-이미지-처리--프론트엔드-12시간)
5. [MVP 완성 체크리스트](#-mvp-완성-최종-체크리스트)
6. [다음 단계](#-다음-단계-선택-사항)

---

## 📊 개발 규모 산정

### **전체 예상 시간: 30시간 (3일 × 10시간)**

| 항목 | 예상 시간 | 비율 |
|------|----------|------|
| **Day 1: 기반 구축** | 8시간 | 27% |
| **Day 2: 핵심 로직** | 10시간 | 33% |
| **Day 3: UI & 통합** | 12시간 | 40% |

### **개발 규모 범례**

| 아이콘 | 규모 | 설명 | 예상 시간 |
|--------|------|------|----------|
| 🟢 | **Small** | 단일 기능, 의존성 없음 | 30분~2시간 |
| 🟡 | **Medium** | 복합 기능, 약간의 통합 | 2~4시간 |
| 🔴 | **Large** | 핵심 기능, 많은 통합 | 4~6시간 |
| ⚫ | **X-Large** | 전체 시스템 통합 | 6시간+ |

---

## 📅 Day 1: 프로젝트 기반 구축 (8시간)

### 🎯 **목표**
- ✅ 프로젝트 구조 완성
- ✅ 데이터베이스 스키마 구현 및 초기 데이터 삽입
- ✅ Flask 기본 API 동작 (GET /api/films)
- ✅ Git 설정 완료

---

### ⏰ 09:00 - 10:30 | 프로젝트 구조 생성 (1.5시간) 🟢

#### **실행 명령어**

```bash
# 프로젝트 루트 생성
cd C:\대학프로그래밍폴더
mkdir Filmrecipe
cd Filmrecipe

# 백엔드 구조
mkdir -p backend/app/routes backend/app/services backend/app/models backend/app/utils
mkdir -p database/migrations
mkdir -p data/pdfs/mvp data/luts data/grain_overlays data/curves data/temp
mkdir -p docs tests config

# 프론트엔드 구조
mkdir -p frontend/app frontend/components frontend/public

# 백엔드 파일 생성
touch backend/__init__.py backend/config.py backend/run.py backend/requirements.txt backend/.env.example
touch backend/app/__init__.py
touch backend/app/routes/__init__.py backend/app/routes/films.py backend/app/routes/upload.py backend/app/routes/process.py
touch backend/app/services/__init__.py backend/app/services/exif_extractor.py backend/app/services/film_matcher.py backend/app/services/image_processor.py
touch backend/app/models/__init__.py backend/app/models/film.py backend/app/models/recipe.py
touch backend/app/utils/__init__.py backend/app/utils/grain_generator.py

# 데이터베이스 파일
touch database/schema.sql

# 설정 파일
touch .gitignore README.md
```

#### **체크포인트**
```bash
✅ 전체 디렉토리 구조 생성 완료
✅ 백엔드 Python 파일 생성 완료
✅ 데이터 폴더 준비 완료
```

---

### ⏰ 10:30 - 12:00 | 가상환경 & 패키지 설치 (1.5시간) 🟢

#### **requirements.txt**

```txt
Flask==3.0.0
Flask-CORS==4.0.0
SQLAlchemy==2.0.23
exifread==3.0.0
piexif==1.1.3
Pillow==10.1.0
opencv-python==4.8.1.78
numpy==1.24.3
scipy==1.11.4
colour-science==0.4.3
python-dotenv==1.0.0
pytest==7.4.3
pytest-flask==1.3.0
```

#### **설치**

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

### ⏰ 13:00 - 15:00 | DB 스키마 & 초기 데이터 (2시간) 🟡

#### **database/schema.sql**

```sql
-- films 테이블
CREATE TABLE IF NOT EXISTS films (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    manufacturer VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK(type IN ('color', 'bw')),
    iso_base INTEGER NOT NULL,
    description TEXT,
    tier VARCHAR(20) NOT NULL DEFAULT 'mvp',
    pdf_analyzed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- film_recipes 테이블
CREATE TABLE IF NOT EXISTS film_recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film_id INTEGER NOT NULL,
    recipe_name VARCHAR(100) NOT NULL,
    process_type VARCHAR(20) NOT NULL,
    iso_min INTEGER,
    iso_max INTEGER,
    grain_size INTEGER,
    grain_intensity REAL,
    color_temperature INTEGER,
    white_balance VARCHAR(20),
    base_mask_color VARCHAR(10),
    bw_weight_r REAL DEFAULT 0.299,
    bw_weight_g REAL DEFAULT 0.587,
    bw_weight_b REAL DEFAULT 0.114,
    tone_curve_data TEXT,
    spectral_dye_density TEXT,
    reciprocity_failure_data TEXT,
    matching_reason TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (film_id) REFERENCES films(id) ON DELETE CASCADE,
    UNIQUE(film_id, recipe_name)
);

-- 인덱스
CREATE INDEX idx_films_tier ON films(tier);
CREATE INDEX idx_films_iso ON films(iso_base);
CREATE INDEX idx_recipes_film_id ON film_recipes(film_id);
CREATE INDEX idx_recipes_iso_range ON film_recipes(iso_min, iso_max);
CREATE INDEX idx_recipes_active ON film_recipes(is_active);

-- MVP 5개 필름 데이터
INSERT INTO films VALUES (1, 'Fujichrome Velvia 50', 'Fujifilm', 'color', 50, 
  'World highest saturation reversal film', 'mvp', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO film_recipes VALUES (1, 1, 'Standard E-6', 'E-6', 25, 100, 9, 0.35, 
  5500, 'daylight', NULL, 0.299, 0.587, 0.114, '{}', '{}', '{}',
  'Ultra-high saturation for landscape', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO films VALUES (2, 'Fujichrome Provia 100F', 'Fujifilm', 'color', 100,
  'Vivid and faithful color reproduction', 'mvp', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO film_recipes VALUES (2, 2, 'Standard E-6', 'E-6', 50, 200, 8, 0.30,
  5500, 'daylight', NULL, 0.299, 0.587, 0.114, '{}', '{}', '{}',
  'Rich tone reproduction for portraits', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO films VALUES (3, 'Kodak Portra 400', 'Kodak', 'color', 400,
  'Spectacular skin tones', 'mvp', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO film_recipes VALUES (3, 3, 'Standard C-41', 'C-41', 200, 800, 37, 0.35,
  5500, 'daylight', '#FF6600', 0.299, 0.587, 0.114, '{}', '{}', '{}',
  'Ideal for portrait and fashion', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO films VALUES (4, 'Kodak Vision3 500T', 'Kodak', 'color', 500,
  'Tungsten cinema film', 'mvp', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO film_recipes VALUES (4, 4, 'ECN-2 Tungsten', 'ECN-2', 320, 800, 0, 0.25,
  3200, 'tungsten', NULL, 0.299, 0.587, 0.114, '{}', '{}', '{}',
  'Cinematic low-light performance', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO films VALUES (5, 'Kodak T-Max 100', 'Kodak', 'bw', 100,
  'Worlds finest grain B&W', 'mvp', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO film_recipes VALUES (5, 5, 'T-MAX Developer', 'T-MAX', 50, 200, 25, 0.15,
  NULL, NULL, NULL, 0.299, 0.587, 0.114, '{}', '{}', '{}',
  'Finest grain for high resolution', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
```

#### **DB 생성**

```bash
cd database
sqlite3 filmrecipe.db < schema.sql
sqlite3 filmrecipe.db "SELECT name FROM films;"
```

---

### ⏰ 15:00 - 17:00 | Flask 앱 기본 구조 (2시간) 🟡

#### **backend/config.py**

```python
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).parent.parent
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/database/filmrecipe.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'temp'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tiff'}
    SECRET_KEY = 'dev-secret-key'
```

#### **backend/app/__init__.py**

```python
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    from backend.config import Config
    app.config.from_object(Config)
    
    db.init_app(app)
    CORS(app)
    
    from backend.app.routes import films
    app.register_blueprint(films.bp)
    
    @app.route('/')
    def index():
        return {'service': 'Film Recipe API', 'version': '1.0.0'}
    
    return app
```

#### **backend/app/models/film.py**

```python
from backend.app import db
from datetime import datetime

class Film(db.Model):
    __tablename__ = 'films'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    iso_base = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    tier = db.Column(db.String(20), default='mvp')
    
    recipes = db.relationship('FilmRecipe', backref='film', lazy=True)
    
    def to_dict(self, include_recipes=False):
        result = {
            'id': self.id,
            'name': self.name,
            'manufacturer': self.manufacturer,
            'type': self.type,
            'iso_base': self.iso_base,
            'description': self.description
        }
        if include_recipes:
            result['recipes'] = [r.to_dict() for r in self.recipes]
        return result
```

#### **backend/app/models/recipe.py**

```python
from backend.app import db

class FilmRecipe(db.Model):
    __tablename__ = 'film_recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'), nullable=False)
    recipe_name = db.Column(db.String(100), nullable=False)
    iso_min = db.Column(db.Integer)
    iso_max = db.Column(db.Integer)
    grain_intensity = db.Column(db.Float)
    color_temperature = db.Column(db.Integer)
    white_balance = db.Column(db.String(20))
    bw_weight_r = db.Column(db.Float, default=0.299)
    bw_weight_g = db.Column(db.Float, default=0.587)
    bw_weight_b = db.Column(db.Float, default=0.114)
    matching_reason = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'recipe_name': self.recipe_name,
            'iso_range': f"{self.iso_min}-{self.iso_max}",
            'matching_reason': self.matching_reason
        }
```

#### **backend/app/routes/films.py**

```python
from flask import Blueprint, jsonify, request
from backend.app.models.film import Film

bp = Blueprint('films', __name__, url_prefix='/api')

@bp.route('/films', methods=['GET'])
def get_films():
    tier = request.args.get('tier', 'mvp')
    query = Film.query
    if tier != 'all':
        query = query.filter(Film.tier == tier)
    films = query.all()
    
    return jsonify({
        'count': len(films),
        'films': [f.to_dict(include_recipes=True) for f in films]
    })
```

#### **backend/run.py**

```python
from backend.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### **실행 테스트**

```bash
cd backend
python run.py
# http://localhost:5000/api/films
```

---

### ⏰ 17:00 - 18:00 | Git 설정 (1시간) 🟢

#### **.gitignore**

```gitignore
__pycache__/
*.py[cod]
venv/
*.db
.env
data/temp/*
node_modules/
.next/
```

```bash
git init
git add .
git commit -m "Day 1: Project structure + DB + Flask API"
```

---

## 🎯 Day 1 종료 체크리스트

```bash
✅ 프로젝트 구조 완성
✅ Python 가상환경 + 패키지 설치
✅ database/schema.sql 작성
✅ 5개 인덱스 생성 (idx_films_tier, idx_films_iso, idx_recipes_film_id, idx_recipes_iso_range, idx_recipes_active)
✅ SQLite DB 생성 (5개 필름 데이터)
✅ Flask 앱 초기화
✅ GET /api/films 동작
✅ Git 초기화
```

---

## 📅 Day 2: 핵심 로직 구현 (10시간)

### 🎯 **목표**
- ✅ EXIF 추출 서비스 완성
- ✅ 필름 매칭 알고리즘 완성
- ✅ POST /api/upload 구현
- ✅ 단위 테스트 작성

---

### ⏰ 09:00 - 11:00 | EXIF 추출 서비스 (2시간) 🟡

#### **backend/app/services/exif_extractor.py**

```python
import exifread
from typing import Dict, Optional

class EXIFExtractor:
    @staticmethod
    def extract(image_path: str) -> Dict:
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
            
            return {
                'iso': EXIFExtractor._extract_iso(tags),
                'shutter_speed': EXIFExtractor._extract_shutter(tags),
                'aperture': EXIFExtractor._extract_aperture(tags),
                'focal_length': EXIFExtractor._extract_focal_length(tags),
                'white_balance': EXIFExtractor._extract_wb(tags),
                'color_temperature': 5500,
                'camera_make': str(tags.get('Image Make', 'Unknown')),
                'camera_model': str(tags.get('Image Model', 'Unknown'))
            }
        except:
            return EXIFExtractor._default_exif()
    
    @staticmethod
    def _extract_iso(tags) -> Optional[int]:
        if 'EXIF ISOSpeedRatings' in tags:
            return int(str(tags['EXIF ISOSpeedRatings']))
        return 200
    
    @staticmethod
    def _extract_shutter(tags) -> Optional[float]:
        if 'EXIF ExposureTime' in tags:
            value = str(tags['EXIF ExposureTime'])
            if '/' in value:
                num, denom = value.split('/')
                return float(num) / float(denom)
        return 0.008
    
    @staticmethod
    def _extract_aperture(tags) -> Optional[float]:
        if 'EXIF FNumber' in tags:
            value = str(tags['EXIF FNumber'])
            if '/' in value:
                num, denom = value.split('/')
                return round(float(num) / float(denom), 1)
        return 5.6
    
    @staticmethod
    def _extract_focal_length(tags) -> Optional[int]:
        if 'EXIF FocalLength' in tags:
            value = str(tags['EXIF FocalLength'])
            if '/' in value:
                num, denom = value.split('/')
                return int(float(num) / float(denom))
        return 50
    
    @staticmethod
    def _extract_wb(tags) -> str:
        return 'Auto'
    
    @staticmethod
    def _default_exif() -> Dict:
        return {
            'iso': 200,
            'shutter_speed': 0.008,
            'aperture': 5.6,
            'focal_length': 50,
            'white_balance': 'Auto',
            'color_temperature': 5500,
            'camera_make': 'Unknown',
            'camera_model': 'Unknown'
        }
```

---

### ⏰ 11:00 - 13:00 | 필름 매칭 알고리즘 (2시간) 🔴

#### **backend/app/services/film_matcher.py**

```python
from typing import List, Dict
from backend.app.models.recipe import FilmRecipe

class FilmMatcher:
    @staticmethod
    def match(exif_data: Dict) -> List[Dict]:
        recipes = FilmRecipe.query.filter_by(is_active=True).all()
        
        results = []
        for recipe in recipes:
            score = FilmMatcher._calculate_score(exif_data, recipe)
            results.append({
                'film_id': recipe.film_id,
                'film_name': recipe.film.name,
                'score': round(score, 1),
                'reason': FilmMatcher._generate_reason(exif_data, recipe)
            })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:5]
    
    @staticmethod
    def _calculate_score(exif_data: Dict, recipe: FilmRecipe) -> float:
        score = 0.0

        # ISO (50%)
        iso_score = FilmMatcher._iso_score(exif_data.get('iso'), recipe)
        score += iso_score * 0.5

        # 색온도 (20%)
        if recipe.film.type == 'color':
            wb_score = FilmMatcher._wb_score(exif_data, recipe)
            score += wb_score * 0.2

        # 조리개 (15%)
        aperture_score = FilmMatcher._aperture_score(exif_data, recipe)
        score += aperture_score * 0.15

        # 셔터 (15%)
        shutter_score = FilmMatcher._shutter_score(exif_data, recipe)
        score += shutter_score * 0.15

        # 저조도 보너스 (Vision3 500T, Portra 400)
        low_light_bonus = FilmMatcher._low_light_bonus(exif_data, recipe)
        score += low_light_bonus

        return min(100.0, score)
    
    @staticmethod
    def _iso_score(exif_iso: int, recipe: FilmRecipe) -> float:
        if not exif_iso:
            return 50.0
        if recipe.iso_min <= exif_iso <= recipe.iso_max:
            return 100.0
        
        if exif_iso < recipe.iso_min:
            diff = recipe.iso_min - exif_iso
            return max(0, 100 - (diff / recipe.film.iso_base) * 50)
        else:
            diff = exif_iso - recipe.iso_max
            return max(0, 100 - (diff / recipe.film.iso_base) * 50)
    
    @staticmethod
    def _wb_score(exif_data: Dict, recipe: FilmRecipe) -> float:
        temp = exif_data.get('color_temperature', 5500)
        recipe_temp = recipe.color_temperature or 5500
        
        if recipe_temp <= 3500:
            return 100.0 if temp <= 4000 else 40.0
        else:
            return 100.0 if 5000 <= temp <= 6500 else 50.0
    
    @staticmethod
    def _aperture_score(exif_data: Dict, recipe: FilmRecipe) -> float:
        aperture = exif_data.get('aperture', 5.6)
        
        if 'Velvia' in recipe.film.name:
            return 100.0 if aperture >= 8.0 else 70.0
        elif 'Portra' in recipe.film.name:
            return 100.0 if aperture <= 5.6 else 70.0
        return 75.0
    
    @staticmethod
    def _shutter_score(exif_data: Dict, recipe: FilmRecipe) -> float:
        shutter = exif_data.get('shutter_speed', 0.008)
        
        if 'Vision3' in recipe.film.name:
            return 100.0 if shutter >= 0.03 else 70.0
        return 75.0
    
    @staticmethod
    def _low_light_bonus(exif_data: Dict, recipe: FilmRecipe) -> float:
        """저조도 촬영 환경 감지 및 보너스 점수 부여"""
        iso = exif_data.get('iso', 200)
        shutter = exif_data.get('shutter_speed', 0.008)
        wb = exif_data.get('white_balance', '').lower()
        temp = exif_data.get('color_temperature', 5500)

        # 저조도 판단: ISO >= 800 또는 셔터 < 1/60s (0.0167s)
        is_low_light = (iso >= 800) or (shutter >= 1/60)

        if not is_low_light:
            return 0.0

        # Vision3 500T: 저조도 특화 필름
        if recipe.film.name == 'Kodak Vision3 500T':
            # 텅스텐 조명 환경이면 최대 보너스
            if 'tungsten' in wb or temp <= 3500:
                return 15.0
            # 일반 저조도 환경
            return 10.0

        # Portra 400: 저조도 대응 가능
        elif recipe.film.name == 'Kodak Portra 400':
            return 8.0

        # 다른 필름: 저조도에서 불리
        elif recipe.film.iso_base < 200:
            return -5.0  # 저감도 필름은 감점

        return 0.0

    @staticmethod
    def _generate_reason(exif_data: Dict, recipe: FilmRecipe) -> str:
        iso = exif_data.get('iso', 200)
        shutter = exif_data.get('shutter_speed', 0.008)

        # 저조도 여부 표시
        is_low_light = (iso >= 800) or (shutter >= 1/60)
        low_light_text = " [저조도 환경 감지]" if is_low_light else ""

        return f"ISO {iso} 매칭, {recipe.matching_reason}{low_light_text}"
```

---

### ⏰ 14:00 - 16:00 | POST /api/upload (2시간) 🟡

#### **backend/app/routes/upload.py**

```python
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import uuid
from pathlib import Path
from backend.config import Config
from backend.app.services.exif_extractor import EXIFExtractor
from backend.app.services.film_matcher import FilmMatcher

bp = Blueprint('upload', __name__, url_prefix='/api')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({'error': 'No images'}), 400
    
    files = request.files.getlist('images')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files'}), 400
    
    job_id = str(uuid.uuid4())[:12]
    job_folder = Config.UPLOAD_FOLDER / job_id
    job_folder.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = job_folder / filename
            file.save(str(filepath))
            
            exif_data = EXIFExtractor.extract(str(filepath))
            matched_films = FilmMatcher.match(exif_data)
            
            results.append({
                'filename': filename,
                'exif': exif_data,
                'matched_films': matched_films
            })
    
    return jsonify({
        'job_id': job_id,
        'count': len(results),
        'images': results
    }), 200
```

#### **backend/app/__init__.py 업데이트**

```python
# 블루프린트 등록
from backend.app.routes import films, upload
app.register_blueprint(films.bp)
app.register_blueprint(upload.bp)
```

---

### ⏰ 16:00 - 18:00 | POST /api/process (2시간) 🟡

#### **backend/app/routes/process.py**

```python
from flask import Blueprint, request, jsonify, send_file
from backend.config import Config
from backend.app.models.film import Film
from backend.app.services.image_processor import ImageProcessor
from pathlib import Path
import zipfile
import io

bp = Blueprint('process', __name__, url_prefix='/api')

@bp.route('/process', methods=['POST'])
def process_images():
    data = request.get_json()
    job_id = data.get('job_id')
    film_ids = data.get('film_ids', [])

    if not job_id or not film_ids:
        return jsonify({'error': 'Missing parameters'}), 400

    job_folder = Config.UPLOAD_FOLDER / job_id
    if not job_folder.exists():
        return jsonify({'error': 'Job not found'}), 404

    input_files = list(job_folder.glob('*.jpg')) + list(job_folder.glob('*.png'))
    if not input_files:
        return jsonify({'error': 'No images'}), 404

    output_folder = job_folder / 'processed'
    output_folder.mkdir(exist_ok=True)

    results = []

    for film_id in film_ids:
        film = Film.query.get(film_id)
        if not film or not film.recipes:
            continue

        recipe = film.recipes[0]
        input_file = input_files[0]
        output_filename = f"{input_file.stem}_{film.name.replace(' ', '_').lower()}.jpg"
        output_path = output_folder / output_filename

        film_recipe_dict = {
            'film_name': film.name,
            'grain_intensity': recipe.grain_intensity or 0.3,
            'bw_weight_r': recipe.bw_weight_r,
            'bw_weight_g': recipe.bw_weight_g,
            'bw_weight_b': recipe.bw_weight_b
        }

        ImageProcessor.apply_film_simulation(
            str(input_file),
            str(output_path),
            film_recipe_dict
        )

        results.append({
            'film_id': film.id,
            'film_name': film.name,
            'output_url': f"/api/download/{job_id}/{output_filename}"
        })

    return jsonify({
        'job_id': job_id,
        'status': 'completed',
        'results': results,
        'zip_url': f"/api/download/{job_id}/all_films.zip"
    }), 200

@bp.route('/download/<job_id>/<filename>')
def download_image(job_id, filename):
    # ZIP 다운로드 요청
    if filename == 'all_films.zip':
        return download_zip(job_id)

    # 개별 파일 다운로드
    file_path = Config.UPLOAD_FOLDER / job_id / 'processed' / filename
    if not file_path.exists():
        return jsonify({'error': 'Not found'}), 404
    return send_file(str(file_path), mimetype='image/jpeg')

def download_zip(job_id):
    """선택한 필름들을 ZIP으로 묶어 다운로드"""
    processed_folder = Config.UPLOAD_FOLDER / job_id / 'processed'

    if not processed_folder.exists():
        return jsonify({'error': 'No processed images found'}), 404

    # 처리된 모든 이미지 파일 찾기
    image_files = list(processed_folder.glob('*.jpg')) + list(processed_folder.glob('*.png'))

    if not image_files:
        return jsonify({'error': 'No images to download'}), 404

    # 메모리에 ZIP 파일 생성
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for img_path in image_files:
            # ZIP 내부 파일명 (경로 없이 파일명만)
            arcname = img_path.name
            zip_file.write(str(img_path), arcname=arcname)

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'filmrecipe_{job_id}.zip'
    )
```

---

### ⏰ 18:00 - 19:00 | 단위 테스트 (1시간) 🟢

```bash
cd backend
pytest tests/ -v
```

---

## 🎯 Day 2 종료 체크리스트

```bash
✅ EXIF 추출 서비스 완성
✅ 필름 매칭 알고리즘 완성
✅ 저조도 매칭 로직 강화 (ISO >= 800 또는 셔터 < 1/60s 감지)
✅ POST /api/upload 구현
✅ POST /api/process 구현
✅ 단위 테스트 작성
```

---

## 📅 Day 3: 이미지 처리 + 프론트엔드 (12시간)

### 🎯 **목표**
- ✅ 이미지 처리 파이프라인 완성
- ✅ Next.js UI 구현
- ✅ E2E 테스트

---

### ⏰ 09:00 - 12:00 | 이미지 처리 파이프라인 (3시간) 🔴

#### **backend/app/services/image_processor.py**

```python
import numpy as np
from PIL import Image

class ImageProcessor:
    @staticmethod
    def apply_film_simulation(image_path: str, output_path: str, film_recipe: dict):
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img).astype(np.float32) / 255.0
        
        # Gamma decode
        img_linear = np.power(img_array, 2.2)
        
        # 톤 커브
        img_tone = ImageProcessor._apply_tone_curve(img_linear, film_recipe)
        
        # Gamma encode
        img_srgb = np.power(img_tone, 1.0 / 2.2)
        img_final = (np.clip(img_srgb, 0, 1) * 255).astype(np.uint8)
        
        output_img = Image.fromarray(img_final)
        output_img.save(output_path, quality=95)
        return output_path
    
    @staticmethod
    def _apply_tone_curve(img: np.ndarray, film_recipe: dict) -> np.ndarray:
        film_name = film_recipe.get('film_name', '')
        
        if 'Velvia' in film_name:
            img = ImageProcessor._s_curve(img, 0.3)
            img = np.clip(img * 1.1, 0, 1)
        elif 'Portra' in film_name:
            img = ImageProcessor._s_curve(img, 0.15)
        elif 'T-Max' in film_name:
            r_w = film_recipe['bw_weight_r']
            g_w = film_recipe['bw_weight_g']
            b_w = film_recipe['bw_weight_b']
            gray = img[:,:,0]*r_w + img[:,:,1]*g_w + img[:,:,2]*b_w
            img = np.stack([gray]*3, axis=-1)
            img = ImageProcessor._s_curve(img, 0.25)
        
        return img
    
    @staticmethod
    def _s_curve(img: np.ndarray, strength: float) -> np.ndarray:
        x = img
        y = x + strength * (x - x**3)
        return np.clip(y, 0, 1)
```

---

### ⏰ 13:00 - 15:00 | 그레인 생성 (2시간) 🟡

#### **backend/app/utils/grain_generator.py**

```python
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

class GrainGenerator:
    @staticmethod
    def generate_grain_texture(size=(2048, 2048), grain_size=9, intensity=0.5, output_path=None):
        np.random.seed(42)
        noise = np.random.randn(size[1], size[0])
        noise = (noise - noise.min()) / (noise.max() - noise.min())
        noise = 0.5 + (noise - 0.5) * intensity
        
        sigma = grain_size / 10.0
        noise_blurred = gaussian_filter(noise, sigma=sigma)
        noise_blurred = (noise_blurred - noise_blurred.min()) / (noise_blurred.max() - noise_blurred.min())
        
        grain_array = (noise_blurred * 255).astype(np.uint8)
        grain_img = Image.fromarray(grain_array, mode='L')
        
        if output_path:
            grain_img.save(output_path)
        
        return grain_img

# 실행
if __name__ == '__main__':
    from backend.config import Config
    grain_folder = Config.BASE_DIR / 'data' / 'grain_overlays'
    grain_folder.mkdir(parents=True, exist_ok=True)
    
    sizes = {'rms_9': (9, 0.35), 'rms_8': (8, 0.30), 'pgi_37': (37, 0.35), 'pgi_25': (25, 0.15)}
    
    for name, (size, intensity) in sizes.items():
        output_path = grain_folder / f"grain_{name}.png"
        GrainGenerator.generate_grain_texture(
            size=(2048, 2048),
            grain_size=size,
            intensity=intensity,
            output_path=str(output_path)
        )
    print("Grain textures generated!")
```

```bash
python -m backend.app.utils.grain_generator
```

---

### ⏰ 15:00 - 17:00 | Next.js 프론트엔드 + ZIP 다운로드 (2시간) 🟡

```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --app
npm install axios react-dropzone
```

#### **frontend/app/page.tsx**

```typescript
'use client';

import { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

export default function Home() {
  const [jobId, setJobId] = useState('');
  const [films, setFilms] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const onDrop = async (files: File[]) => {
    const formData = new FormData();
    files.forEach(f => formData.append('images', f));
    
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/api/upload', formData);
      setJobId(res.data.job_id);
      setFilms(res.data.images[0].matched_films);
    } catch (err) {
      alert('Upload failed');
    }
    setLoading(false);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, maxFiles: 1 });

  const processImages = async () => {
    setLoading(true);
    try {
      const filmIds = films.map((f: any) => f.film_id);
      const res = await axios.post('http://localhost:5000/api/process', {
        job_id: jobId,
        film_ids: filmIds
      });
      setResults(res.data.results);
    } catch (err) {
      alert('Processing failed');
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8">🎞️ Film Recipe</h1>
        
        <div {...getRootProps()} className="border-2 border-dashed rounded-lg p-12 text-center cursor-pointer mb-8">
          <input {...getInputProps()} />
          <p className="text-xl">{isDragActive ? 'Drop here!' : 'Click or drag image'}</p>
        </div>

        {films.length > 0 && (
          <div className="bg-white rounded-lg p-6 mb-8">
            <h2 className="text-2xl font-bold mb-4">Matched Films</h2>
            {films.map((f: any, i) => (
              <div key={i} className="p-3 bg-gray-50 rounded mb-2">
                <span className="font-medium">{f.film_name}</span>
                <span className="ml-2 text-blue-600">{f.score} pts</span>
              </div>
            ))}
            <button onClick={processImages} disabled={loading}
              className="w-full mt-4 py-3 bg-blue-600 text-white rounded hover:bg-blue-700">
              {loading ? 'Processing...' : 'Generate 5 Film Versions'}
            </button>
          </div>
        )}

        {results.length > 0 && (
          <>
            <div className="bg-white rounded-lg p-6 mb-4">
              <h2 className="text-2xl font-bold mb-4">Results</h2>
              <a
                href={`http://localhost:5000/api/download/${jobId}/all_films.zip`}
                download
                className="w-full block text-center py-3 bg-blue-600 text-white rounded hover:bg-blue-700 font-medium"
              >
                📦 Download All Films (ZIP)
              </a>
            </div>

            <div className="grid grid-cols-3 gap-4">
              {results.map((r: any) => (
                <div key={r.film_id} className="border rounded overflow-hidden">
                  <img src={`http://localhost:5000${r.output_url}`} alt={r.film_name} className="w-full" />
                  <div className="p-3">
                    <p className="font-medium mb-2">{r.film_name}</p>
                    <a href={`http://localhost:5000${r.output_url}`} download
                      className="block text-center py-2 bg-green-600 text-white rounded">
                      Download
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </main>
  );
}
```

```bash
npm run dev
# http://localhost:3000
```

---

### ⏰ 17:00 - 19:00 | CORS & 통합 테스트 (2시간) 🟡

#### **backend/app/__init__.py 업데이트**

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

#### **E2E 테스트**

```bash
# 터미널 1
cd backend
python run.py

# 터미널 2
cd frontend
npm run dev

# 브라우저: http://localhost:3000
# 1. 이미지 업로드
# 2. 필름 5개 추천 확인
# 3. 생성 버튼 클릭
# 4. 결과 갤러리 확인
# 5. 다운로드 테스트
```

---

## 🎯 MVP 완성 최종 체크리스트

```bash
✅ 백엔드 서버 실행 (Flask)
✅ 프론트엔드 실행 (Next.js)
✅ SQLite DB (5개 필름 데이터)
✅ GET /api/films
✅ POST /api/upload
✅ POST /api/process
✅ GET /api/download/{job_id}/{filename}
✅ GET /api/download/{job_id}/all_films.zip (ZIP 다운로드)
✅ EXIF 추출
✅ 필름 매칭 (상위 5개)
✅ 저조도 매칭 로직 강화 (Vision3 500T, Portra 400 보너스)
✅ 이미지 처리 (톤 커브 + 그레인)
✅ 개별 이미지 다운로드
✅ ZIP 다운로드 (선택한 필름들 일괄 다운로드)
✅ E2E 테스트 성공
✅ MVP 완성! 🎉
```

---

## 📊 최종 통계

| 항목 | 수치 |
|------|------|
| 총 개발 시간 | 30시간 |
| 백엔드 파일 | 15개 |
| 프론트엔드 파일 | 5개 |
| API 엔드포인트 | 6개 |
| 지원 필름 | 5개 |
| 총 코드 라인 | ~2,500줄 |

---

## 🚀 다음 단계 (선택 사항)

### **Day 4: 데이터 정교화**
- PDF 수동 추출
- LUT 생성 (DaVinci Resolve)
- 톤 커브 정밀 조정

### **Day 5: UI/UX 개선**
- 스타일링 강화
- 로딩 애니메이션
- 반응형 디자인

### **Day 6: 배치 처리**
- 여러 이미지 동시 처리
- Celery + Redis 큐

### **Day 7: 배포**
- Docker 빌드
- GCP Cloud Run 배포
- 도메인 연결

---

## 🎯 핵심 구현 팁

### **MVP 전략**
```
✅ LUT 없이 간단한 톤 커브
✅ 복잡한 색공간 변환 스킵
✅ 기본 그레인만 적용
✅ 단일 이미지만 처리
✅ 완벽함보다 동작 우선
```

### **빠른 프로토타이핑**
```
✅ 백엔드 우선 (API 먼저)
✅ Postman으로 즉시 테스트
✅ 프론트엔드는 마지막
✅ 점진적 개선
```

---

## 📝 성공 기준

```bash
✅ 업로드 → 5초 이내
✅ EXIF 추출 → 정확도 90%+
✅ 필름 매칭 → 신뢰도 85점+
✅ 이미지 처리 → 10초 이내
✅ 다운로드 → 원본 해상도 유지
✅ 에러율 → 5% 이하
```

---

**END OF PLAN.md**

**🎉 이 계획서를 따라하면 3일 내에 완벽히 동작하는 필름 시뮬레이션 웹 애플리케이션을 완성할 수 있습니다!**
