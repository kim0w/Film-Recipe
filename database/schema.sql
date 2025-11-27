-- Film Recipe Database Schema
-- MVP Phase 1: 5 Films

-- films 테이블
CREATE TABLE IF NOT EXISTS films (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    manufacturer VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK(type IN ('color', 'bw')),
    iso_base INTEGER NOT NULL,
    description TEXT,
    tier VARCHAR(20) NOT NULL DEFAULT 'mvp' CHECK(tier IN ('mvp', 'core', 'extended', 'archive')),
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

    -- ISO 범위
    iso_min INTEGER,
    iso_max INTEGER,

    -- 그레인 특성
    grain_size INTEGER,
    grain_intensity REAL,

    -- 색온도 (컬러 필름만)
    color_temperature INTEGER,
    white_balance VARCHAR(20),
    base_mask_color VARCHAR(10),

    -- 흑백 RGB 가중치 (흑백 필름만)
    bw_weight_r REAL DEFAULT 0.299,
    bw_weight_g REAL DEFAULT 0.587,
    bw_weight_b REAL DEFAULT 0.114,

    -- 과학적 데이터 (JSON 저장)
    tone_curve_data TEXT,
    spectral_dye_density TEXT,
    reciprocity_failure_data TEXT,

    -- 매칭 로직
    matching_reason TEXT,
    is_active BOOLEAN DEFAULT TRUE,

    -- 타임스탬프
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 외래 키 제약조건
    FOREIGN KEY (film_id) REFERENCES films(id) ON DELETE CASCADE,
    UNIQUE(film_id, recipe_name)
);

-- 인덱스 생성 (성능 최적화)
CREATE INDEX IF NOT EXISTS idx_films_tier ON films(tier);
CREATE INDEX IF NOT EXISTS idx_films_iso ON films(iso_base);
CREATE INDEX IF NOT EXISTS idx_recipes_film_id ON film_recipes(film_id);
CREATE INDEX IF NOT EXISTS idx_recipes_iso_range ON film_recipes(iso_min, iso_max);
CREATE INDEX IF NOT EXISTS idx_recipes_active ON film_recipes(is_active);

-- MVP 5개 필름 데이터 삽입

-- 1. Fujifilm Velvia 50
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Fujichrome Velvia 50',
    'Fujifilm',
    'color',
    50,
    'World highest saturation reversal film. RMS 9, vibrant colors, ideal for landscape.',
    'mvp',
    TRUE
);

INSERT INTO film_recipes (
    film_id, recipe_name, process_type,
    iso_min, iso_max,
    grain_size, grain_intensity,
    color_temperature, white_balance,
    tone_curve_data, spectral_dye_density, reciprocity_failure_data,
    matching_reason, is_active
)
VALUES (
    1,
    'Standard E-6',
    'E-6',
    25, 100,
    9, 0.35,
    5500, 'daylight',
    '{}', '{}', '{"4": 4.3, "8": 8.5, "16": 17.3, "32": 35.7, "64": "not_recommended"}',
    'Ultra-high saturation for landscape and nature. ISO ≤ 100, f/8+, daylight WB.',
    TRUE
);

-- 2. Fujifilm Provia 100F
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Fujichrome Provia 100F',
    'Fujifilm',
    'color',
    100,
    'Vivid and faithful color reproduction. RMS 8, rich tone, bias-free highlights.',
    'mvp',
    TRUE
);

INSERT INTO film_recipes (
    film_id, recipe_name, process_type,
    iso_min, iso_max,
    grain_size, grain_intensity,
    color_temperature, white_balance,
    tone_curve_data, spectral_dye_density, reciprocity_failure_data,
    matching_reason, is_active
)
VALUES (
    2,
    'Standard E-6',
    'E-6',
    50, 200,
    8, 0.30,
    5500, 'daylight',
    '{}', '{}', '{"128": 132, "240": "not_recommended"}',
    'Vivid and faithful color with rich tone reproduction. Ideal for portraits, products, and general use.',
    TRUE
);

-- 3. Kodak Portra 400
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak Portra 400',
    'Kodak',
    'color',
    400,
    'Spectacular skin tones. PGI 37, ideal for portrait, fashion, and travel.',
    'mvp',
    TRUE
);

INSERT INTO film_recipes (
    film_id, recipe_name, process_type,
    iso_min, iso_max,
    grain_size, grain_intensity,
    color_temperature, white_balance, base_mask_color,
    tone_curve_data, spectral_dye_density, reciprocity_failure_data,
    matching_reason, is_active
)
VALUES (
    3,
    'Standard C-41',
    'C-41',
    200, 800,
    37, 0.35,
    5500, 'daylight', '#FF6600',
    '{}', '{}', '{"0.0001": 0.0001, "1": 1}',
    'Spectacular skin tones with fine grain. Ideal for portrait, fashion, travel, and low-light photography.',
    TRUE
);

-- 4. Kodak Vision3 500T
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak Vision3 500T',
    'Kodak',
    'color',
    500,
    'Tungsten 3200K cinema film. Extended highlight latitude (+2 stops), DLT technology.',
    'mvp',
    TRUE
);

INSERT INTO film_recipes (
    film_id, recipe_name, process_type,
    iso_min, iso_max,
    grain_size, grain_intensity,
    color_temperature, white_balance, base_mask_color,
    tone_curve_data, spectral_dye_density, reciprocity_failure_data,
    matching_reason, is_active
)
VALUES (
    4,
    'ECN-2 Tungsten',
    'ECN-2',
    320, 800,
    0, 0.25,
    3200, 'tungsten', NULL,
    '{}', '{}', '{"0.001": 0.001, "1": 1}',
    'Cinematic low-light performance with tungsten balance. Optimized for indoor/night shooting.',
    TRUE
);

-- 5. Kodak T-Max 100
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak T-Max 100',
    'Kodak',
    'bw',
    100,
    'World finest grain B&W film. T-GRAIN emulsion, 200 lines/mm resolving power, push +3 stop.',
    'mvp',
    TRUE
);

INSERT INTO film_recipes (
    film_id, recipe_name, process_type,
    iso_min, iso_max,
    grain_size, grain_intensity,
    bw_weight_r, bw_weight_g, bw_weight_b,
    tone_curve_data, reciprocity_failure_data,
    matching_reason, is_active
)
VALUES (
    5,
    'T-MAX Developer',
    'T-MAX',
    50, 200,
    25, 0.15,
    0.299, 0.587, 0.114,
    '{}', '{"1": 1, "10": 10, "100": 100}',
    'World finest grain B&W. T-GRAIN technology, extreme sharpness, high resolution.',
    TRUE
);
