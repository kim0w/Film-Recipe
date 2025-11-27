# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Film Recipe** is a web application that simulates analog film photography effects on digital images using scientific data from film datasheets. The system analyzes EXIF metadata from uploaded images and automatically recommends the top 5 matching films based on ISO, color temperature, aperture, and shutter speed.

## Development Timeline & Strategy

**MVP Target:** 3 days (30 hours) - See PLAN.md for detailed breakdown
**Development Order:** Backend → Testing → Frontend → Integration

## Core Architecture

### Three-Tier Architecture

```
Frontend (Next.js)
    ↓ HTTP/REST API
Backend (Flask)
    ↓ SQLAlchemy ORM
Database (SQLite → PostgreSQL)
```

### Film Matching Algorithm

**Weight Distribution:**

- ISO matching: 50%
- Color temperature: 20%
- Aperture: 15%
- Shutter speed: 15%

**Low-light detection logic:**

- Trigger: `ISO >= 800` OR `shutter_speed < 1/60s`
- Vision3 500T bonus: +15 points (tungsten) or +10 points (general low-light)
- Portra 400 bonus: +8 points
- Low ISO films (< 200): -5 points penalty

### Image Processing Pipeline

```
Original Image
    → Linear RGB (gamma decode)
    → 3D LUT application
    → Tone curve (Characteristic Curves data)
    → Grain overlay
    → sRGB (gamma encode)
    → Final output
```

## Key Technical Decisions

### Why These Films?

The MVP includes 5 professional films covering ISO 50-500:

1. **Velvia 50** - Ultra-high saturation reversal (landscape)
2. **Provia 100F** - Natural reversal (portraits/general)
3. **Portra 400** - Best-in-class skin tones (portraits/low-light)
4. **Vision3 500T** - Tungsten cinema film (indoor/night)
5. **T-Max 100** - Finest grain B&W (fine art)

Selection criteria: ISO coverage + type diversity + data completeness + professional quality

### Database Schema Critical Points

**5 indexes required** (performance optimization):

```sql
idx_films_tier
idx_films_iso
idx_recipes_film_id
idx_recipes_iso_range
idx_recipes_active  -- Added for filtering active recipes
```

**JSON fields** for scientific data:

- `tone_curve_data` - Characteristic Curves from datasheets
- `spectral_dye_density` - Color response curves
- `reciprocity_failure_data` - Long exposure corrections

### File Processing Workflow

1. User uploads image → generates `job_id` (UUID first 12 chars)
2. Store in `data/temp/{job_id}/`
3. Process → store in `data/temp/{job_id}/processed/`
4. Return URLs for individual downloads + ZIP download
5. ZIP contains all user-selected film versions

## Commands

### Backend Setup & Development

```bash
# Initial setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Database initialization
cd ../database
sqlite3 filmrecipe.db < schema.sql

# Verify database
sqlite3 filmrecipe.db "SELECT name FROM films;"

# Run backend server
cd ../backend
python run.py
# Access: http://localhost:5000/api/films

# Run tests
pytest tests/ -v
pytest tests/test_matcher.py -v  # Single test file

# Generate grain textures (one-time setup)
python -m backend.app.utils.grain_generator
```

### Frontend Setup & Development

```bash
cd frontend
npm install
npm run dev
# Access: http://localhost:3000

# Build for production
npm run build
npm start
```

### Docker Deployment

```bash
# Full stack
docker-compose up -d

# Backend only
docker build -t filmrecipe-api ./backend
docker run -p 5000:8080 filmrecipe-api
```

## Development Workflow

### Day 1: Project Foundation (8 hours)

1. Create directory structure following PLAN.md
2. Set up Python virtual environment
3. Create `database/schema.sql` with **all 5 indexes**
4. Initialize SQLite DB with MVP 5 films
5. Implement Flask basic structure + Film/FilmRecipe models
6. Test `GET /api/films` endpoint
7. Git commit

### Day 2: Core Logic (10 hours)

1. Implement `exif_extractor.py` (ISO, shutter, aperture, WB, color temp)
2. Implement `film_matcher.py` with **low-light bonus logic**
3. Implement `POST /api/upload` (multipart/form-data)
4. Implement `POST /api/process` with **ZIP generation**
5. Write unit tests

### Day 3: Image Processing + UI (12 hours)

1. Implement `image_processor.py` (gamma correction, LUT, tone curve, grain)
2. Create grain textures using `grain_generator.py`
3. Build Next.js UI with drag-and-drop upload
4. Add **ZIP download button** in results section
5. E2E testing

## Critical Implementation Notes

### Film Matcher - Low-Light Logic

```python
def _low_light_bonus(exif_data, recipe):
    iso = exif_data.get('iso', 200)
    shutter = exif_data.get('shutter_speed', 0.008)

    # Trigger condition
    is_low_light = (iso >= 800) or (shutter >= 1/60)

    if not is_low_light:
        return 0.0

    # Apply bonuses/penalties
    if recipe.film.name == 'Kodak Vision3 500T':
        # Check tungsten environment
        if wb == 'tungsten' or temp <= 3500:
            return 15.0
        return 10.0
    elif recipe.film.name == 'Kodak Portra 400':
        return 8.0
    elif recipe.film.iso_base < 200:
        return -5.0  # Penalty for low-ISO films

    return 0.0
```

### ZIP Download Implementation

**Backend:** Use `io.BytesIO()` + `zipfile` for in-memory ZIP creation
**Frontend:** Single button downloads all processed images
**Filename:** `filmrecipe_{job_id}.zip`

### Color Space Handling

Always use `colour-science` library for scientific accuracy:

```python
import colour

# Decode sRGB → Linear
img_linear = colour.cctf_decoding(img_array, function='sRGB')

# Encode Linear → sRGB
img_srgb = colour.cctf_encoding(img_linear, function='sRGB')
```

## API Endpoints

### GET /api/films

Query params: `tier` (mvp|core|extended|all), `type` (color|bw|all)

### POST /api/upload

Accepts multipart/form-data, returns `job_id` + matched films with scores

### POST /api/process

Accepts JSON with `job_id` and `film_ids[]`, returns individual URLs + `zip_url`

### GET /api/download/{job_id}/{filename}

Special case: `filename = "all_films.zip"` triggers ZIP download

## Project File Organization

```
backend/app/
├── services/      # Core business logic (EXIF, matching, processing)
├── routes/        # API endpoints (upload, films, process)
├── models/        # SQLAlchemy models (Film, FilmRecipe)
└── utils/         # Helpers (LUT loader, grain generator, tone curve)

data/
├── pdfs/mvp/      # Film datasheets (source of scientific data)
├── luts/          # 3D LUT files (.cube format, 33×33×33)
├── grain_overlays/# Pre-generated grain textures (2048×2048 PNG)
├── curves/        # Tone curve JSON (extracted from PDFs)
└── temp/          # Job folders (auto-cleanup recommended)

database/
├── schema.sql     # CREATE TABLE + INSERT initial data
└── filmrecipe.db  # SQLite database (dev only)
```

## Testing Strategy

**Unit tests:** `exif_extractor.py`, `film_matcher.py` (test low-light logic)
**Integration tests:** API endpoints with sample images
**E2E test:** Upload → Match → Process → Download ZIP

## MVP Success Criteria

- Upload → response < 5 seconds
- EXIF extraction accuracy: 90%+
- Film matching confidence: 85+ points for top recommendation
- Image processing: < 10 seconds per film
- ZIP download: includes all user-selected films
- Error rate: < 5%

## Phase 2/3 Expansion

After MVP completion, add:

- Phase 2: 8 more films (total 13), batch processing, RAW support
- Phase 3: 7 more films (total 20), user accounts, custom recipes, push/pull simulation

See SRS.md section 10 for detailed roadmap.

## Rule

모든 답변은 한국어로 한다.
코드는 읽기쉽게 작성한다.
리펙토링이 필요 없게 코드를 깔끔하고 효율적으로 작성한다.
