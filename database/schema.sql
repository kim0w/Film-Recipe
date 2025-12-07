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

-- ============================================================
-- Phase 2: Core Films (8개 필름 추가 → 총 13개)
-- ============================================================

-- 6. Kodak Ektachrome E100
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak Ektachrome E100',
    'Kodak',
    'color',
    100,
    'Vibrant color reversal film. Fine grain, neutral tones, excellent for scanning.',
    'core',
    FALSE
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
    6,
    'Standard E-6',
    'E-6',
    50, 200,
    9, 0.28,
    5500, 'daylight',
    '{}', '{}', '{}',
    'Vibrant colors with neutral tones. Excellent for landscape, portrait, and general photography.',
    TRUE
);

-- 7. Kodak Gold 200
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak Gold 200',
    'Kodak',
    'color',
    200,
    'Consumer color negative film. Warm tones, ideal for everyday snapshots and travel.',
    'core',
    FALSE
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
    7,
    'Standard C-41',
    'C-41',
    100, 400,
    40, 0.38,
    5500, 'daylight', '#FFB366',
    '{}', '{}', '{}',
    'Warm tones perfect for everyday snapshots. Great for travel, family photos, and general use.',
    TRUE
);

-- 8. Kodak UltraMax 400
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak UltraMax 400',
    'Kodak',
    'color',
    400,
    'Consumer color negative film. Saturated colors, ideal for action and sports.',
    'core',
    FALSE
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
    8,
    'Standard C-41',
    'C-41',
    200, 800,
    42, 0.40,
    5500, 'daylight', '#FF9966',
    '{}', '{}', '{}',
    'Saturated colors for action photography. Versatile ISO 400 for sports, events, and travel.',
    TRUE
);

-- 9. Kodak Ektar 100
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak Ektar 100',
    'Kodak',
    'color',
    100,
    'World finest grain color negative film. Ultra-vivid saturation, PGI 25.',
    'core',
    FALSE
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
    9,
    'Standard C-41',
    'C-41',
    50, 200,
    25, 0.20,
    5500, 'daylight', '#FF8844',
    '{}', '{}', '{}',
    'World finest grain negative film with ultra-vivid saturation. Perfect for landscape and commercial photography.',
    TRUE
);

-- 10. Kodak Portra 160
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak Portra 160',
    'Kodak',
    'color',
    160,
    'Professional portrait film with fine grain. PGI 28, exceptional skin tones.',
    'core',
    FALSE
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
    10,
    'Standard C-41',
    'C-41',
    100, 320,
    28, 0.28,
    5500, 'daylight', '#FF7755',
    '{}', '{}', '{}',
    'Finest grain Portra with exceptional skin tones. Ideal for studio portraits and fashion.',
    TRUE
);

-- 11. Kodak ProImage 100
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak ProImage 100',
    'Kodak',
    'color',
    100,
    'Budget-friendly color negative film. Good color reproduction, affordable price.',
    'core',
    FALSE
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
    11,
    'Standard C-41',
    'C-41',
    50, 200,
    35, 0.35,
    5500, 'daylight', '#FFAA66',
    '{}', '{}', '{}',
    'Affordable color negative with good color reproduction. Great for beginners and everyday use.',
    TRUE
);

-- 12. Kodak T-Max 400
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak T-Max 400',
    'Kodak',
    'bw',
    400,
    'High-speed B&W film. T-GRAIN emulsion, push +3 stop capability.',
    'core',
    FALSE
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
    12,
    'T-MAX Developer',
    'T-MAX',
    200, 1600,
    35, 0.30,
    0.299, 0.587, 0.114,
    '{}', '{"1": 1, "10": 10, "100": 100}',
    'High-speed B&W with fine grain. Excellent for low-light, sports, and photojournalism.',
    TRUE
);

-- 13. Rollei RPX 100
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Rollei RPX 100',
    'Rollei',
    'bw',
    100,
    'Traditional panchromatic B&W film. Classic grain structure, affordable price.',
    'core',
    FALSE
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
    13,
    'Standard D-76',
    'D-76',
    50, 200,
    30, 0.25,
    0.299, 0.587, 0.114,
    '{}', '{}',
    'Classic panchromatic B&W with traditional grain. Great for general B&W photography.',
    TRUE
);
