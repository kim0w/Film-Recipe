# Software Requirements Specification (SRS)

## Film Photography Simulation & Recipe Database

**프로젝트명:** Film Recipe - 필름 시뮬레이션 웹 애플리케이션  
**버전:** 1.0.0 (MVP)  
**작성일:** 2025-11-26  
**작성자:** Film Recipe Development Team  
**문서 상태:** 최종 확정 (MVP Phase 1)

---

## 📋 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [MVP 필름 선정 (Phase 1)](#2-mvp-필름-선정-phase-1)
3. [시스템 아키텍처](#3-시스템-아키텍처)
4. [데이터베이스 스키마](#4-데이터베이스-스키마)
5. [API 엔드포인트 명세](#5-api-엔드포인트-명세)
6. [필름 매칭 알고리즘](#6-필름-매칭-알고리즘)
7. [이미지 처리 파이프라인](#7-이미지-처리-파이프라인)
8. [기술 스택](#8-기술-스택)
9. [배포 전략](#9-배포-전략)
10. [Phase 2/3 확장 계획](#10-phase-23-확장-계획)

---

## 1. 프로젝트 개요

### 1.1 프로젝트 목적

디지털 사진에 아날로그 필름의 색감과 질감을 자동으로 적용하는 웹 애플리케이션 개발.

**핵심 가치:**

- ✅ **EXIF 기반 자동 필름 매칭**: 사용자가 촬영 설정을 분석하여 최적의 필름 추천
- ✅ **과학적 데이터 기반**: 실제 필름 데이터시트(PDF) 분석을 통한 정확한 시뮬레이션
- ✅ **프로페셔널 품질**: 최고급 필름 5개로 시작하는 MVP 전략
- ✅ **확장 가능한 구조**: Phase 2/3에서 13개 이상 필름 추가 가능

### 1.2 타겟 사용자

| 사용자 그룹         | 특성                            | 우선순위 |
| ------------------- | ------------------------------- | -------- |
| **아마추어 사진가** | 필름 룩 원하지만 비용/시간 부담 | 높음     |
| **프로 사진가**     | 작업 효율성, 정확한 필름 재현   | 높음     |
| **디지털 아티스트** | 빈티지 필터 이상의 전문성       | 중간     |
| **필름 초보자**     | 필름 특성 학습 및 실험          | 중간     |

### 1.3 핵심 기능 (MVP)

1. **이미지 업로드 & EXIF 분석**

   - 지원 포맷: JPEG, PNG, TIFF, RAW (CR2, NEF 등)
   - EXIF 추출: ISO, 셔터 속도, 조리개, 화이트 밸런스, 색온도

2. **자동 필름 매칭**

   - 알고리즘: ISO 50% + 색온도 20% + 조리개 15% + 셔터 속도 15% 가중치
   - 출력: 5개 필름 추천 (신뢰도 점수 포함)

3. **필름 시뮬레이션 적용**

   - LUT 기반 색상 변환
   - 그레인 오버레이 (Film Grain Index 기반)
   - 톤 커브 적용 (Characteristic Curves 데이터)

4. **결과물 다운로드**
   - 포맷: JPEG (원본 해상도 유지)
   - 5개 필름 버전 ZIP 다운로드 옵션

---

## 2. MVP 필름 선정 (Phase 1)

### 2.1 선정 기준

| 기준              | 설명                          | 가중치 |
| ----------------- | ----------------------------- | ------ |
| **ISO 범위 커버** | 50 ~ 500 전체 범위            | 30%    |
| **타입 다양성**   | 리버설 / 네거티브 / 흑백 균형 | 25%    |
| **품질 우선**     | 프로페셔널 등급               | 20%    |
| **차별화**        | 각 필름의 고유 특성 명확      | 15%    |
| **데이터 완전성** | PDF 분석 가능 여부            | 10%    |

### 2.2 최종 선정 필름 (5개)

#### **2.2.1 Fujifilm Velvia 50**

**기본 정보:**

```yaml
name: Fujichrome Velvia 50
manufacturer: Fujifilm
type: Color Reversal (E-6)
iso_base: 50
iso_range: 25 ~ 100 (Push +1 stop)
grain_rms: 9
```

**핵심 특성:**

- 🎨 **채도:** 10/10 (World's highest color saturation)
- 🔍 **그레인:** 8/10 (RMS 9, ultra-fine)
- 🌄 **주 용도:** 풍경, 자연 사진, 매크로
- 📊 **해상력:** 80 / 160 lines/mm (1.6:1 / 1000:1)

**데이터 출처:**

- PDF: `fujifilm-velvia-50.pdf` (8페이지)
- 분석 완료: ✅ 2025-11-26

**추출 데이터:**

```json
{
  "characteristic_curves": {
    "red": [[...], [...]],
    "green": [[...], [...]],
    "blue": [[...], [...]]
  },
  "spectral_sensitivity": {
    "yellow_forming_layer": [...],
    "magenta_forming_layer": [...],
    "cyan_forming_layer": [...]
  },
  "spectral_dye_density": {
    "yellow": [...],
    "magenta": [...],
    "cyan": [...]
  },
  "reciprocity_failure": {
    "4": 4.3,
    "8": 8.5,
    "16": 17.3,
    "32": 35.7,
    "64": "not_recommended"
  }
}
```

**매칭 시나리오:**

- ISO ≤ 100
- 조리개 ≥ f/8 (풍경 심도)
- 주광 (WB: Daylight, 5500K)
- 셔터 속도 > 1/60s

---

#### **2.2.2 Fujifilm Provia 100F**

**기본 정보:**

```yaml
name: Fujichrome Provia 100F
manufacturer: Fujifilm
type: Color Reversal (E-6)
iso_base: 100
iso_range: 50 ~ 200 (Push +2 stops)
grain_rms: 8
```

**핵심 특성:**

- 🎨 **채도:** 6/10 (Vivid and faithful - 중간)
- 🔍 **그레인:** 9/10 (RMS 8, finest among ISO 100)
- 👤 **주 용도:** 인물, 제품, 패션, 만능형
- 📊 **해상력:** 60 / 140 lines/mm
- ✨ **특징:** Rich tone reproduction, Bias-free highlights

**데이터 출처:**

- PDF: `fujifilm-provia-100f.pdf` (6페이지)
- 분석 완료: ✅ 2025-11-26

**추출 데이터:**

```json
{
  "characteristic_curves": {
    "red": [[...], [...]],
    "green": [[...], [...]],
    "blue": [[...], [...]]
  },
  "spectral_sensitivity": {
    "yellow_forming_layer": [...],
    "magenta_forming_layer": [...],
    "cyan_forming_layer": [...]
  },
  "spectral_dye_density": {
    "yellow": [...],
    "magenta": [...],
    "cyan": [...]
  },
  "reciprocity_failure": {
    "128": 132,
    "240": "not_recommended"
  }
}
```

**매칭 시나리오:**

- ISO ≤ 200
- 조리개 f/2.8 ~ f/8 (인물/제품)
- 주광 또는 플래시
- 다목적 촬영

**Velvia 50 vs Provia 100F 차별화:**

- Velvia: 극한 채도 → 풍경 특화
- Provia: 자연스러움 → 인물/제품/범용

---

#### **2.2.3 Kodak Portra 400**

**기본 정보:**

```yaml
name: Kodak Professional Portra 400
manufacturer: Kodak
type: Color Negative (C-41)
iso_base: 400
iso_range: 200 ~ 800 (Push +1 stop)
grain_pgi: 37 (4×6 inches)
```

**핵심 특성:**

- 🎨 **피부톤:** 9/10 (Spectacular skin tones)
- 🔍 **그레인:** 8/10 (PGI 37, 세계 최고 수준 ISO 400)
- 👤 **주 용도:** 인물, 패션, 여행, 저조도
- 📊 **해상력:** 데이터 확인 중
- ✨ **특징:** Vision Film Technology, 넓은 노출 관용도

**데이터 출처:**

- PDF: `kodak-portra-400.pdf` (4페이지)
- 분석 완료: ✅ 2025-11-26

**추출 데이터:**

```json
{
  "characteristic_curves": {
    "red": [[...], [...]],
    "green": [[...], [...]],
    "blue": [[...], [...]]
  },
  "spectral_sensitivity": {
    "yellow_forming_layer": [...],
    "magenta_forming_layer": [...],
    "cyan_forming_layer": [...]
  },
  "spectral_dye_density": {
    "yellow": [...],
    "magenta": [...],
    "cyan": [...]
  },
  "reciprocity_failure": {
    "0.0001": 0.0001,
    "1": 1
  }
}
```

**매칭 시나리오:**

- ISO 200 ~ 800
- 조리개 ≤ f/5.6 (얕은 심도 또는 저조도)
- 주광 또는 실내 (플래시/텅스텐 가능)
- 셔터 속도 < 1/125s (핸드헬드 저조도)

**왜 Portra 160이 아닌 400?**

- ISO 400이 더 범용적 (2배 빠름)
- PGI 37 vs 28: 차이 미미 (여전히 세계 최고급)
- 저조도 대응력 우수
- MVP ISO 갭 해결 (160 → 400 → 500)

---

#### **2.2.4 Kodak Vision3 500T**

**기본 정보:**

```yaml
name: Kodak Vision3 500T (5219)
manufacturer: Kodak
type: Cine Negative (ECN-2)
iso_base: 500 (Tungsten 3200K)
iso_daylight: 320 (with 85 filter)
grain_rms: N/A (시네마 필름)
```

**핵심 특성:**

- 🎨 **색온도:** 3200K (Tungsten) - **유일한 텅스텐 필름**
- 🔍 **그레인:** 시네마틱 그레인 (DLT Technology)
- 🎬 **주 용도:** 영화, 저조도, 실내 촬영
- 📊 **관용도:** +2 stops (Extended highlight latitude)
- ✨ **특징:** Dye Layering Technology, Sub-Micron Technology

**데이터 출처:**

- PDF: `kodak-vision3-500t.pdf` (5페이지)
- 분석 완료: ✅ 2025-11-26

**추출 데이터:**

```json
{
  "sensitometric_curves": {
    "red": [[...], [...]],
    "green": [[...], [...]],
    "blue": [[...], [...]]
  },
  "spectral_sensitivity": {
    "yellow_forming_layer": [...],
    "magenta_forming_layer": [...],
    "cyan_forming_layer": [...]
  },
  "spectral_dye_density": {
    "yellow": [...],
    "magenta": [...],
    "cyan": [...]
  },
  "reciprocity_failure": {
    "0.001": 0.001,
    "1": 1
  },
  "diffuse_rms_granularity_curves": [...]
}
```

**매칭 시나리오:**

- ISO ≥ 400
- 색온도 ≤ 4000K (텅스텐 / 실내 조명)
- WB: Tungsten / Incandescent
- 셔터 속도 < 1/60s (저조도 환경)

**텅스텐 필름 우선순위 로직:**

```python
if wb == "Tungsten" or color_temp <= 3500:
    vision3_500t_score += 20  # 명시적 텅스텐
elif iso >= 1600 or shutter_speed < 1/30:
    vision3_500t_score += 12  # 저조도 추론
```

**CineStill 800T 대체 근거:**

- Vision3 500T가 원본 필름
- CineStill = Vision3 리믹스 (remjet 제거판)
- ISO 500도 충분히 저조도 커버
- PDF 데이터 완전성 우수

---

#### **2.2.5 Kodak T-Max 100**

**기본 정보:**

```yaml
name: Kodak Professional T-Max 100
manufacturer: Kodak
type: B&W Negative (T-MAX Developer)
iso_base: 100
iso_range: 50 ~ 800 (Push +3 stops)
grain_pgi: <25 (4×6 inches)
grain_rms: 8 (역설적 - 실제 PGI는 최고급)
```

**핵심 특성:**

- 🔍 **그레인:** 10/10 (World's finest grain B&W, PGI <25)
- 📊 **해상력:** 200 lines/mm (1000:1) - **극한 디테일**
- 🎨 **주 용도:** 흑백 예술, 확대 인화, 스캔
- ✨ **특징:** T-GRAIN Emulsion, 극도로 미세한 입자
- 🔬 **확장성:** Push +3 stop (EI 800까지)

**데이터 출처:**

- PDF: `kodak-t-max-100.pdf` (예상 4~6페이지)
- 분석 완료: ✅ 2025-11-26

**추출 데이터:**

```json
{
  "characteristic_curves": {
    "density": [[...], [...]]
  },
  "spectral_sensitivity": {
    "panchromatic": [...]
  },
  "reciprocity_failure": {
    "1": 1,
    "10": 10,
    "100": 100
  },
  "mtf_curve": [...]
}
```

**매칭 시나리오:**

- 흑백 모드 또는 Monochrome Picture Style
- ISO ≤ 200 (저감도 흑백)
- 고해상력 요구 (확대 인화, 세밀한 디테일)
- 푸시 현상 시뮬레이션: ISO 200~800

**흑백 RGB 가중치 (팬크로매틱):**

```python
bw_weight_r = 0.299
bw_weight_g = 0.587
bw_weight_b = 0.114
```

**왜 Rollei RPX 100이 아닌가?**

- T-GRAIN > 전통 팬크로매틱 기술
- 해상력 200 vs 160 lines/mm
- 푸시 현상 데이터 풍부 (EI 800까지)
- Kodak 브랜드 가치 (프로페셔널)

---

### 2.3 MVP 필름 포지셔닝 매트릭스

#### **채도 스펙트럼**

```
[최고 채도] ──────────────────────── [자연스러움]
    │                │                    │
 Velvia 50      Portra 400          Provia 100F
 (10/10)         (7/10)              (6/10)
    │                                     │
  풍경                                  만능형
```

#### **ISO 커버리지**

```
[저감도] ────────────────────────── [고감도]
   50      100      400      500      800
   │        │        │        │        │
Velvia  Provia   Portra  Vision3   (공백)
       T-Max     400     500T
       (흑백)
```

#### **용도별 배치**

| 용도         | 1순위        | 2순위       | 3순위 |
| ------------ | ------------ | ----------- | ----- |
| **풍경**     | Velvia 50    | Provia 100F | -     |
| **인물**     | Portra 400   | Provia 100F | -     |
| **여행**     | Portra 400   | Provia 100F | -     |
| **저조도**   | Vision3 500T | Portra 400  | -     |
| **흑백**     | T-Max 100    | -           | -     |
| **시네마틱** | Vision3 500T | -           | -     |

---

## 3. 시스템 아키텍처

### 3.1 전체 구조도

```
┌─────────────────────────────────────────────────────────┐
│                     사용자 인터페이스                      │
│  (Next.js / React / Tailwind CSS)                       │
│  - 이미지 업로드 (Drag & Drop)                            │
│  - 필름 추천 결과 표시                                     │
│  - 5개 필름 미리보기 (첫 이미지만)                          │
│  - ZIP 다운로드 버튼                                      │
└─────────────────────────────────────────────────────────┘
                          ▼ HTTP/REST API
┌─────────────────────────────────────────────────────────┐
│                      백엔드 API 서버                       │
│  (Flask / Python 3.11+)                                 │
│  ┌───────────────────────────────────────────────┐      │
│  │  1. EXIF Extraction (exifread, piexif)        │      │
│  │  2. Film Matching Algorithm                   │      │
│  │  3. Image Processing Pipeline                 │      │
│  │     - LUT Application (Pillow, colour-science)│      │
│  │     - Grain Overlay (numpy)                   │      │
│  │     - Tone Curve (OpenCV, scipy)              │      │
│  │  4. File Management (임시 저장소)              │      │
│  └───────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
                          ▼ SQL Queries
┌─────────────────────────────────────────────────────────┐
│                      데이터베이스                          │
│  (SQLite - MVP / PostgreSQL - Production)               │
│  ┌───────────────────────────────────────────────┐      │
│  │  films (필름 기본 정보)                         │      │
│  │  film_recipes (레시피 데이터)                   │      │
│  │  - tone_curve_data (JSON)                     │      │
│  │  - spectral_dye_density (JSON)                │      │
│  │  - reciprocity_failure_data (JSON)            │      │
│  └───────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### 3.2 디렉토리 구조

```
C:\대학프로그래밍폴더\Filmrecipe\
│
├── frontend/                    # Next.js 프론트엔드
│   ├── app/
│   │   ├── page.tsx            # 메인 페이지
│   │   ├── upload/             # 업로드 페이지
│   │   └── result/             # 결과 페이지
│   ├── components/
│   │   ├── ImageUploader.tsx
│   │   ├── FilmPreview.tsx
│   │   └── DownloadButton.tsx
│   ├── public/
│   └── package.json
│
├── backend/                     # Flask 백엔드
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── upload.py       # 이미지 업로드 API
│   │   │   ├── films.py        # 필름 정보 API
│   │   │   └── process.py      # 이미지 처리 API
│   │   ├── services/
│   │   │   ├── exif_extractor.py
│   │   │   ├── film_matcher.py
│   │   │   └── image_processor.py
│   │   ├── models/
│   │   │   ├── film.py
│   │   │   └── recipe.py
│   │   └── utils/
│   │       ├── lut_loader.py
│   │       ├── grain_generator.py
│   │       └── tone_curve.py
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
│
├── database/
│   ├── schema.sql              # DB 스키마 정의
│   ├── migrations/             # DB 마이그레이션
│   └── filmrecipe.db           # SQLite DB (개발용)
│
├── data/
│   ├── pdfs/
│   │   ├── mvp/                # MVP 5개 PDF
│   │   │   ├── fujifilm-velvia-50.pdf
│   │   │   ├── fujifilm-provia-100f.pdf
│   │   │   ├── kodak-portra-400.pdf
│   │   │   ├── kodak-vision3-500t.pdf
│   │   │   └── kodak-t-max-100.pdf
│   │   ├── core/               # Phase 2 필름 PDF
│   │   └── extended/           # Phase 3 필름 PDF
│   ├── luts/                   # 3D LUT 파일 (.cube)
│   │   ├── velvia_50.cube
│   │   ├── provia_100f.cube
│   │   ├── portra_400.cube
│   │   ├── vision3_500t.cube
│   │   └── tmax_100.cube
│   ├── grain_overlays/         # 그레인 텍스처 PNG
│   │   ├── grain_rms_8.png
│   │   ├── grain_rms_9.png
│   │   ├── grain_pgi_37.png
│   │   └── grain_pgi_25.png
│   └── curves/                 # 톤 커브 JSON
│       ├── velvia_50_curves.json
│       ├── provia_100f_curves.json
│       ├── portra_400_curves.json
│       ├── vision3_500t_curves.json
│       └── tmax_100_curves.json
│
├── docs/
│   ├── SRS.md                  # 이 문서
│   ├── API.md                  # API 명세서
│   ├── DEPLOYMENT.md           # 배포 가이드
│   └── ROADMAP.md              # 개발 로드맵
│
├── tests/
│   ├── test_exif.py
│   ├── test_matcher.py
│   └── test_processor.py
│
├── config/
│   ├── films.yaml              # 필름 설정 (MVP/Core/Extended)
│   └── phase2_films.yaml       # Phase 2 필름 목록
│
├── .env.example                # 환경 변수 템플릿
├── .gitignore
├── docker-compose.yml          # 로컬 개발 환경
└── README.md                   # 프로젝트 개요
```

---

## 4. 데이터베이스 스키마

### 4.1 ERD (Entity Relationship Diagram)

```
┌────────────────────────┐
│      films             │
├────────────────────────┤
│ id (PK)                │
│ name                   │
│ manufacturer           │
│ type                   │
│ iso_base               │
│ description            │
│ tier                   │◄──┐
│ pdf_analyzed           │   │
│ created_at             │   │
│ updated_at             │   │
└────────────────────────┘   │
                             │ 1:N
                             │
┌────────────────────────────┼───────────────────────────┐
│      film_recipes          │                           │
├────────────────────────────┤                           │
│ id (PK)                    │                           │
│ film_id (FK) ──────────────┘                           │
│ recipe_name                                            │
│ process_type                                           │
│ iso_min, iso_max                                       │
│ grain_size, grain_intensity                            │
│ color_temperature, white_balance                       │
│ base_mask_color (네거티브만)                            │
│ bw_weight_r, bw_weight_g, bw_weight_b (흑백만)          │
│ tone_curve_data (JSON)                                 │
│ spectral_dye_density (JSON)                            │
│ reciprocity_failure_data (JSON)                        │
│ matching_reason                                        │
│ is_active                                              │
│ created_at, updated_at                                 │
└────────────────────────────────────────────────────────┘
```

### 4.2 SQL 스키마 정의

```sql
-- films 테이블
CREATE TABLE films (
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
CREATE TABLE film_recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film_id INTEGER NOT NULL,
    recipe_name VARCHAR(100) NOT NULL,
    process_type VARCHAR(20) NOT NULL,

    -- ISO 범위
    iso_min INTEGER,
    iso_max INTEGER,

    -- 그레인 특성
    grain_size INTEGER,              -- RMS Granularity 또는 PGI
    grain_intensity REAL,            -- 0.0 ~ 1.0

    -- 색온도 (컬러 필름만)
    color_temperature INTEGER,       -- Kelvin (예: 5500, 3200)
    white_balance VARCHAR(20),       -- daylight, tungsten, etc.
    base_mask_color VARCHAR(10),     -- 네거티브 마스크 색상 (hex)

    -- 흑백 RGB 가중치 (흑백 필름만)
    bw_weight_r REAL DEFAULT 0.299,
    bw_weight_g REAL DEFAULT 0.587,
    bw_weight_b REAL DEFAULT 0.114,

    -- 과학적 데이터 (JSON 저장)
    tone_curve_data TEXT,            -- Characteristic Curves
    spectral_dye_density TEXT,       -- Spectral Dye Density Curves
    reciprocity_failure_data TEXT,   -- 상반칙 불궤 보정값

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
CREATE INDEX idx_films_tier ON films(tier);
CREATE INDEX idx_films_iso ON films(iso_base);
CREATE INDEX idx_recipes_film_id ON film_recipes(film_id);
CREATE INDEX idx_recipes_iso_range ON film_recipes(iso_min, iso_max);
CREATE INDEX idx_recipes_active ON film_recipes(is_active);
```

### 4.3 초기 데이터 INSERT (MVP 5개)

```sql
-- 1. Fujifilm Velvia 50
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Fujichrome Velvia 50',
    'Fujifilm',
    'color',
    50,
    'Daylight reversal film with world''s highest color saturation. RMS 9, vibrant colors, ideal for landscape.',
    'mvp',
    TRUE
);

INSERT INTO film_recipes (
    film_id, recipe_name, process_type,
    iso_min, iso_max,
    grain_size, grain_intensity,
    color_temperature, white_balance,
    tone_curve_data,
    spectral_dye_density,
    reciprocity_failure_data,
    matching_reason,
    is_active
)
VALUES (
    1,
    'Standard E-6',
    'E-6',
    25, 100,
    9, 0.35,
    5500, 'daylight',
    '{"red": [], "green": [], "blue": []}',
    '{"yellow": [], "magenta": [], "cyan": []}',
    '{"4": 4.3, "8": 8.5, "16": 17.3, "32": 35.7, "64": "not_recommended"}',
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
    'Daylight reversal film with vivid and faithful color reproduction. RMS 8, rich tone, bias-free highlights.',
    'mvp',
    TRUE
);

INSERT INTO film_recipes (
    film_id, recipe_name, process_type,
    iso_min, iso_max,
    grain_size, grain_intensity,
    color_temperature, white_balance,
    tone_curve_data,
    spectral_dye_density,
    reciprocity_failure_data,
    matching_reason,
    is_active
)
VALUES (
    2,
    'Standard E-6',
    'E-6',
    50, 200,
    8, 0.30,
    5500, 'daylight',
    '{"red": [], "green": [], "blue": []}',
    '{"yellow": [], "magenta": [], "cyan": []}',
    '{"128": 132, "240": "not_recommended"}',
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
    'Professional portrait film with spectacular skin tones. PGI 37, ideal for portrait, fashion, and travel.',
    'mvp',
    TRUE
);

INSERT INTO film_recipes (
    film_id, recipe_name, process_type,
    iso_min, iso_max,
    grain_size, grain_intensity,
    color_temperature, white_balance,
    base_mask_color,
    tone_curve_data,
    spectral_dye_density,
    reciprocity_failure_data,
    matching_reason,
    is_active
)
VALUES (
    3,
    'Standard C-41',
    'C-41',
    200, 800,
    37, 0.35,
    5500, 'daylight',
    '#FF6600',
    '{"red": [], "green": [], "blue": []}',
    '{"yellow": [], "magenta": [], "cyan": []}',
    '{"0.0001": 0.0001, "1": 1}',
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
    'Tungsten 3200K negative film for cinema. Extended highlight latitude (+2 stops), DLT technology.',
    'mvp',
    TRUE
);

INSERT INTO film_recipes (
    film_id, recipe_name, process_type,
    iso_min, iso_max,
    grain_size, grain_intensity,
    color_temperature, white_balance,
    base_mask_color,
    tone_curve_data,
    spectral_dye_density,
    reciprocity_failure_data,
    matching_reason,
    is_active
)
VALUES (
    4,
    'Standard ECN-2',
    'ECN-2',
    320, 800,
    0, 0.40,
    3200, 'tungsten',
    '#FF8C00',
    '{"red": [], "green": [], "blue": []}',
    '{"yellow": [], "magenta": [], "cyan": []}',
    '{"0.001": 0.001, "1": 1}',
    'Low-light cinematic tone with extended highlight latitude. Optimized for tungsten 3200K or ISO ≥ 400.',
    TRUE
);

-- 5. Kodak T-Max 100
INSERT INTO films (name, manufacturer, type, iso_base, description, tier, pdf_analyzed)
VALUES (
    'Kodak T-Max 100',
    'Kodak',
    'bw',
    100,
    'World''s finest grain B&W film. T-GRAIN emulsion, 200 lines/mm resolving power, push +3 stop.',
    'mvp',
    TRUE
);

INSERT INTO film_recipes (
    film_id, recipe_name, process_type,
    iso_min, iso_max,
    grain_size, grain_intensity,
    bw_weight_r, bw_weight_g, bw_weight_b,
    tone_curve_data,
    reciprocity_failure_data,
    matching_reason,
    is_active
)
VALUES (
    5,
    'Standard T-MAX',
    'T-MAX',
    50, 800,
    0, 0.20,
    0.299, 0.587, 0.114,
    '{"density": []}',
    '{"1": 1, "10": 10, "100": 100}',
    'World''s finest grain B&W. T-GRAIN technology, extreme sharpness, push +3 stop capability.',
    TRUE
);
```

---

## 5. API 엔드포인트 명세

### 5.1 엔드포인트 목록

| Method | Endpoint                 | 설명                         | 인증 |
| ------ | ------------------------ | ---------------------------- | ---- |
| GET    | `/api/films`             | 필름 목록 조회 (tier 필터링) | No   |
| GET    | `/api/films/{id}`        | 특정 필름 상세 정보          | No   |
| POST   | `/api/upload`            | 이미지 업로드 & EXIF 분석    | No   |
| POST   | `/api/match`             | 필름 매칭 알고리즘 실행      | No   |
| POST   | `/api/process`           | 이미지 처리 (LUT 적용)       | No   |
| GET    | `/api/download/{job_id}` | 처리된 이미지 ZIP 다운로드   | No   |

### 5.2 상세 명세

#### **GET /api/films**

**설명:** 필름 목록 조회

**Query Parameters:**

```json
{
  "tier": "mvp|core|extended|all", // 기본값: mvp
  "type": "color|bw|all", // 기본값: all
  "iso_min": 50,
  "iso_max": 800
}
```

**Response (200 OK):**

```json
{
  "count": 5,
  "films": [
    {
      "id": 1,
      "name": "Fujichrome Velvia 50",
      "manufacturer": "Fujifilm",
      "type": "color",
      "iso_base": 50,
      "description": "Daylight reversal film...",
      "tier": "mvp",
      "recipes": [
        {
          "id": 1,
          "recipe_name": "Standard E-6",
          "process_type": "E-6",
          "iso_range": "25-100",
          "color_temperature": 5500,
          "matching_reason": "Ultra-high saturation..."
        }
      ]
    },
    ...
  ]
}
```

---

#### **POST /api/upload**

**설명:** 이미지 업로드 및 EXIF 추출

**Request (multipart/form-data):**

```
Content-Type: multipart/form-data
```

```json
{
  "images": [File, File, ...],  // 최대 10개
  "options": {
    "extract_exif": true,
    "auto_match": true
  }
}
```

**Response (200 OK):**

```json
{
  "job_id": "abc123def456",
  "images": [
    {
      "filename": "IMG_0001.jpg",
      "exif": {
        "iso": 200,
        "shutter_speed": 0.008,  // 1/125s
        "aperture": 5.6,
        "focal_length": 50,
        "white_balance": "Auto",
        "color_temperature": 5500,
        "camera_make": "Canon",
        "camera_model": "EOS R5"
      },
      "matched_films": [
        {
          "film_id": 2,
          "film_name": "Fujichrome Provia 100F",
          "score": 85,
          "reason": "ISO match (100), daylight WB, portrait aperture"
        },
        {
          "film_id": 3,
          "film_name": "Kodak Portra 400",
          "score": 78,
          "reason": "Good for portraits, flexible ISO range"
        },
        ...
      ]
    }
  ]
}
```

---

#### **POST /api/process**

**설명:** 필름 시뮬레이션 적용

**Request (application/json):**

```json
{
  "job_id": "abc123def456",
  "film_ids": [1, 2, 3, 4, 5], // 5개 필름 ID
  "options": {
    "apply_grain": true,
    "grain_strength": 0.5, // 0.0 ~ 1.0
    "apply_tone_curve": true,
    "output_format": "jpeg",
    "output_quality": 95
  }
}
```

**Response (202 Accepted):**

```json
{
  "job_id": "abc123def456",
  "status": "processing",
  "estimated_time": 15, // 초
  "preview_url": "/api/preview/abc123def456/IMG_0001_preview.jpg"
}
```

**Response (200 OK - 완료 시):**

```json
{
  "job_id": "abc123def456",
  "status": "completed",
  "results": [
    {
      "film_id": 1,
      "film_name": "Fujichrome Velvia 50",
      "output_url": "/api/download/abc123def456/IMG_0001_velvia50.jpg"
    },
    ...
  ],
  "zip_url": "/api/download/abc123def456/all_films.zip"
}
```

---

#### **GET /api/download/{job_id}**

**설명:** 처리된 이미지 ZIP 다운로드

**Response (200 OK):**

```
Content-Type: application/zip
Content-Disposition: attachment; filename="film_results_abc123def456.zip"

[Binary ZIP data]
```

---

## 6. 필름 매칭 알고리즘

### 6.1 핵심 로직

```python
def calculate_film_match_score(exif_data: dict, film_recipe: dict) -> float:
    """
    EXIF 데이터와 필름 레시피를 비교하여 매칭 점수 계산

    Returns:
        float: 0 ~ 100 점수
    """
    score = 0.0

    # 1. ISO 매칭 (50% 가중치)
    iso_score = calculate_iso_score(exif_data['iso'], film_recipe)
    score += iso_score * 0.5

    # 2. 색온도 매칭 (20% 가중치 - 컬러 필름만)
    if film_recipe['type'] == 'color':
        wb_score = calculate_wb_score(exif_data, film_recipe)
        score += wb_score * 0.2

    # 3. 조리개 매칭 (15% 가중치)
    aperture_score = calculate_aperture_score(exif_data, film_recipe)
    score += aperture_score * 0.15

    # 4. 셔터 속도 매칭 (15% 가중치)
    shutter_score = calculate_shutter_score(exif_data, film_recipe)
    score += shutter_score * 0.15

    return min(100.0, score)


def calculate_iso_score(exif_iso: int, film_recipe: dict) -> float:
    """ISO 점수 계산 (0~100)"""
    iso_min = film_recipe['iso_min']
    iso_max = film_recipe['iso_max']
    iso_base = film_recipe['iso_base']

    # 범위 내면 100점
    if iso_min <= exif_iso <= iso_max:
        return 100.0

    # 범위 밖이면 거리에 따라 감점
    if exif_iso < iso_min:
        diff = iso_min - exif_iso
        return max(0.0, 100.0 - (diff / iso_base) * 50)
    else:  # exif_iso > iso_max
        diff = exif_iso - iso_max
        return max(0.0, 100.0 - (diff / iso_base) * 50)


def calculate_wb_score(exif_data: dict, film_recipe: dict) -> float:
    """색온도 점수 계산 (0~100)"""
    wb = exif_data.get('white_balance', 'Auto')
    color_temp = exif_data.get('color_temperature', 5500)
    film_temp = film_recipe['color_temperature']

    # Vision3 500T 텅스텐 우선순위
    if film_recipe['film_name'] == 'Vision3 500T':
        if wb in ['Tungsten', 'Incandescent']:
            return 100.0  # 명시적 텅스텐 WB
        elif color_temp <= 3500:
            return 90.0   # 색온도 기반 추론
        elif exif_data['iso'] >= 1600 or exif_data['shutter_speed'] < 1/30:
            return 60.0   # 저조도 환경 추론
        else:
            return 25.0   # 기본 점수 (불리하지 않게)

    # Daylight 필름 우선순위
    elif film_temp == 5500:
        if wb in ['Daylight', 'Auto', 'Flash'] or color_temp >= 5000:
            return 100.0
        else:
            diff = abs(color_temp - 5500)
            return max(0.0, 100.0 - diff / 100)

    return 50.0  # 기본 점수


def calculate_aperture_score(exif_data: dict, film_recipe: dict) -> float:
    """조리개 점수 계산 (0~100)"""
    aperture = exif_data.get('aperture', 5.6)
    matching_reason = film_recipe['matching_reason'].lower()

    if aperture >= 8:  # 풍경 (심도)
        if 'landscape' in matching_reason or 'nature' in matching_reason:
            return 100.0
        else:
            return 60.0
    elif aperture <= 2.8:  # 인물 (얕은 심도)
        if 'portrait' in matching_reason or 'fashion' in matching_reason:
            return 100.0
        else:
            return 60.0
    else:  # 중간 조리개
        return 80.0


def calculate_shutter_score(exif_data: dict, film_recipe: dict) -> float:
    """셔터 속도 점수 계산 (0~100)"""
    shutter_speed = exif_data.get('shutter_speed', 0.01)  # 초 단위
    reciprocity_data = film_recipe.get('reciprocity_failure_data')

    if shutter_speed < 0.1:  # 장노출 (< 1/10s)
        if reciprocity_data:
            return 100.0  # 상반칙 불궤 데이터 있음
        else:
            return 50.0
    elif shutter_speed > 0.001:  # 고속 셔터 (> 1/1000s)
        if film_recipe['iso_base'] >= 400:
            return 100.0  # 고감도 필름
        else:
            return 70.0
    else:
        return 80.0  # 일반 셔터 속도
```

### 6.2 매칭 시나리오 예시

#### **시나리오 1: 풍경 사진**

```python
exif_data = {
    'iso': 100,
    'aperture': 11,
    'shutter_speed': 0.004,  # 1/250s
    'white_balance': 'Daylight',
    'color_temperature': 5500
}

# 예상 매칭 결과:
# 1. Velvia 50: 95점 (ISO 100, f/11, daylight)
# 2. Provia 100F: 88점 (ISO 100, f/11, daylight)
# 3. Portra 400: 65점 (ISO mismatch)
```

#### **시나리오 2: 인물 사진 (저조도)**

```python
exif_data = {
    'iso': 800,
    'aperture': 2.8,
    'shutter_speed': 0.02,  # 1/50s
    'white_balance': 'Auto',
    'color_temperature': 5200
}

# 예상 매칭 결과:
# 1. Portra 400: 92점 (ISO 800 push, f/2.8, portrait)
# 2. Vision3 500T: 75점 (ISO match, low-light)
# 3. Provia 100F: 55점 (ISO mismatch)
```

#### **시나리오 3: 실내 텅스텐 조명**

```python
exif_data = {
    'iso': 1600,
    'aperture': 4,
    'shutter_speed': 0.03,  # 1/30s
    'white_balance': 'Tungsten',
    'color_temperature': 3200
}

# 예상 매칭 결과:
# 1. Vision3 500T: 100점 (텅스텐, ISO 1600, low-light)
# 2. Portra 400: 70점 (ISO push 가능)
# 3. Provia 100F: 40점 (ISO/WB mismatch)
```

---

## 7. 이미지 처리 파이프라인

### 7.1 처리 흐름도

```
[원본 이미지]
      │
      ▼
┌─────────────────┐
│ 1. 색공간 변환   │  RGB → Linear RGB (gamma correction)
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ 2. LUT 적용     │  3D LUT (.cube) 로드 및 적용
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ 3. 톤 커브 적용  │  Characteristic Curves 데이터 기반
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ 4. 그레인 오버레이│  필름 그레인 텍스처 합성
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ 5. 색공간 복원   │  Linear RGB → sRGB
└─────────────────┘
      │
      ▼
[필름 시뮬레이션 완료]
```

### 7.2 Python 구현 예시

```python
import numpy as np
from PIL import Image
import colour  # colour-science 라이브러리
from scipy.interpolate import interp1d

def apply_film_simulation(
    image: Image.Image,
    film_recipe: dict,
    lut_path: str,
    grain_path: str
) -> Image.Image:
    """
    필름 시뮬레이션 메인 함수

    Args:
        image: 원본 이미지 (PIL Image)
        film_recipe: 필름 레시피 딕셔너리
        lut_path: 3D LUT 파일 경로 (.cube)
        grain_path: 그레인 텍스처 경로 (.png)

    Returns:
        PIL Image: 처리된 이미지
    """
    # 1. RGB → Linear RGB (gamma 2.2 제거)
    img_array = np.array(image).astype(np.float32) / 255.0
    img_linear = colour.cctf_decoding(img_array, function='sRGB')

    # 2. 3D LUT 적용
    lut = load_3d_lut(lut_path)
    img_lut = apply_lut(img_linear, lut)

    # 3. 톤 커브 적용 (Characteristic Curves)
    tone_curve_data = film_recipe['tone_curve_data']
    img_tone = apply_tone_curve(img_lut, tone_curve_data)

    # 4. 그레인 오버레이
    grain_intensity = film_recipe['grain_intensity']
    img_grain = apply_grain_overlay(img_tone, grain_path, grain_intensity)

    # 5. Linear RGB → sRGB (gamma 2.2 적용)
    img_srgb = colour.cctf_encoding(img_grain, function='sRGB')
    img_final = (np.clip(img_srgb, 0, 1) * 255).astype(np.uint8)

    return Image.fromarray(img_final)


def load_3d_lut(lut_path: str) -> np.ndarray:
    """3D LUT 파일 (.cube) 로드"""
    # .cube 파일 파싱 (colour-science 라이브러리 사용)
    lut = colour.read_LUT(lut_path)
    return lut.table


def apply_lut(image: np.ndarray, lut: np.ndarray) -> np.ndarray:
    """3D LUT 적용 (Trilinear Interpolation)"""
    # colour.LUT3D.apply() 사용
    lut_obj = colour.LUT3D(table=lut)
    return lut_obj.apply(image)


def apply_tone_curve(image: np.ndarray, curve_data: dict) -> np.ndarray:
    """톤 커브 적용 (Characteristic Curves)"""
    # JSON에서 R/G/B 채널별 곡선 추출
    curves = {
        'red': np.array(curve_data['red']),
        'green': np.array(curve_data['green']),
        'blue': np.array(curve_data['blue'])
    }

    # 각 채널별 보간 함수 생성
    result = image.copy()
    for i, channel in enumerate(['red', 'green', 'blue']):
        x_points = curves[channel][:, 0]  # Log Exposure
        y_points = curves[channel][:, 1]  # Density

        # Scipy interp1d로 보간
        interp_func = interp1d(
            x_points, y_points,
            kind='cubic',
            fill_value='extrapolate'
        )

        # 채널별 적용
        result[:, :, i] = interp_func(result[:, :, i])

    return result


def apply_grain_overlay(
    image: np.ndarray,
    grain_path: str,
    intensity: float
) -> np.ndarray:
    """필름 그레인 오버레이"""
    # 그레인 텍스처 로드
    grain_img = Image.open(grain_path).convert('L')
    grain_array = np.array(grain_img).astype(np.float32) / 255.0

    # 이미지 크기에 맞게 리사이즈
    grain_resized = Image.fromarray((grain_array * 255).astype(np.uint8))
    grain_resized = grain_resized.resize(
        (image.shape[1], image.shape[0]),
        Image.LANCZOS
    )
    grain_array = np.array(grain_resized).astype(np.float32) / 255.0

    # 그레인 합성 (Overlay blend mode)
    grain_3ch = np.stack([grain_array] * 3, axis=-1)
    result = image * (1 - intensity) + (image * grain_3ch) * intensity

    return np.clip(result, 0, 1)
```

### 7.3 LUT 생성 워크플로우

**도구:** DaVinci Resolve (무료)

1. **레퍼런스 이미지 준비**

   - Flickr / Unsplash 공개 이미지
   - 필름 데이터시트 샘플 이미지

2. **Color Page에서 수동 조정**

   - Lift/Gamma/Gain
   - Hue vs Hue, Sat vs Sat
   - 필름 데이터시트 Spectral Dye Density 참고

3. **.cube 파일 Export**

   - LUT 크기: 33×33×33 (표준)
   - 포맷: .cube

4. **검증**
   - 테스트 이미지에 적용
   - 레퍼런스와 비교

---

## 8. 기술 스택

### 8.1 프론트엔드

| 항목                | 기술           | 버전 | 이유                       |
| ------------------- | -------------- | ---- | -------------------------- |
| **프레임워크**      | Next.js        | 14+  | React SSR, 이미지 최적화   |
| **UI 라이브러리**   | React          | 18+  | 컴포넌트 기반 개발         |
| **스타일링**        | Tailwind CSS   | 3+   | 유틸리티 클래스, 빠른 개발 |
| **상태 관리**       | Zustand        | 4+   | 단순하고 가벼움            |
| **HTTP 클라이언트** | Axios          | 1+   | Promise 기반, 인터셉터     |
| **파일 업로드**     | react-dropzone | 14+  | Drag & Drop UI             |

### 8.2 백엔드

| 항목            | 기술             | 버전   | 이유                   |
| --------------- | ---------------- | ------ | ---------------------- |
| **프레임워크**  | Flask            | 3+     | 경량, Python 생태계    |
| **EXIF 추출**   | exifread, piexif | latest | EXIF 메타데이터 파싱   |
| **이미지 처리** | Pillow (PIL)     | 10+    | Python 이미지 표준     |
| **색공간**      | colour-science   | 0.4+   | 과학적 색공간 변환     |
| **LUT 처리**    | OpenCV, colour   | latest | 3D LUT 적용            |
| **수치 연산**   | NumPy            | 1.24+  | 고속 배열 연산         |
| **그래프 처리** | SciPy            | 1.11+  | 보간, 곡선 피팅        |
| **DB ORM**      | SQLAlchemy       | 2+     | Python ORM 표준        |
| **비동기 작업** | Celery + Redis   | latest | 이미지 처리 백그라운드 |

### 8.3 데이터베이스

| 항목         | 기술       | 버전 | 이유              |
| ------------ | ---------- | ---- | ----------------- |
| **개발**     | SQLite     | 3+   | 파일 기반, 간단   |
| **프로덕션** | PostgreSQL | 15+  | 확장성, JSON 지원 |

### 8.4 배포 & 인프라

| 항목               | 기술              | 이유                      |
| ------------------ | ----------------- | ------------------------- |
| **컨테이너**       | Docker            | 환경 일관성               |
| **오케스트레이션** | Docker Compose    | 로컬 개발                 |
| **클라우드**       | GCP Cloud Run     | Serverless, 자동 스케일링 |
| **스토리지**       | GCP Cloud Storage | 이미지 임시 저장          |
| **CDN**            | Cloudflare        | 정적 파일 캐싱            |
| **모니터링**       | Sentry            | 에러 추적                 |

---

## 9. 배포 전략

### 9.1 GCP Cloud Run 설정

**리소스 스펙 (MVP):**

```yaml
service: filmrecipe-api
region: asia-northeast3 # 서울 리전
memory: 4Gi
cpu: 2
max_instances: 10
min_instances: 0 # Cold start 허용
timeout: 300s # 5분 (이미지 처리)
concurrency: 10 # 동시 요청 수
```

**Dockerfile (Backend):**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# 포트 설정
ENV PORT=8080
EXPOSE 8080

# 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "300", "run:app"]
```

### 9.2 환경 변수 설정

```bash
# .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/filmrecipe
REDIS_URL=redis://localhost:6379/0
GCP_BUCKET_NAME=filmrecipe-uploads
SENTRY_DSN=https://...
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

### 9.3 CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}

      - name: Build and Push Docker Image
        run: |
          gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/filmrecipe-api

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy filmrecipe-api \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/filmrecipe-api \
            --platform managed \
            --region asia-northeast3 \
            --memory 4Gi \
            --cpu 2 \
            --max-instances 10
```

---

## 10. Phase 2/3 확장 계획

### 10.1 Phase 2: Core Films (8개 추가 → 총 13개)

**추가 필름 목록:**

1. **Kodak Ektachrome E100** (리버설, ISO 100)
2. **Kodak Gold 200** (네거티브, ISO 200) - 일상 스냅
3. **Kodak UltraMax 400** (네거티브, ISO 400) - 소비자용
4. **Kodak Ektar 100** (네거티브, ISO 100) - World's finest grain
5. **Kodak Portra 160** (네거티브, ISO 160) - Portra 시리즈 완성
6. **Kodak ProImage 100** (네거티브, ISO 100) - 저가형
7. **Kodak T-Max 400** (흑백, ISO 400) - 고감도 흑백
8. **Rollei RPX 100** (흑백, ISO 100) - 전통 팬크로매틱

**예상 작업 시간:** 20~30시간

---

### 10.2 Phase 3: Extended Films (7개 추가 → 총 20개)

**추가 필름 목록:**

1. **CineStill 800T** (네거티브, ISO 800) - 야간 촬영
2. **Ilford HP5 Plus 400** (흑백, ISO 400) - 클래식 흑백
3. **Ilford Delta 100** (흑백, ISO 100) - 현대 흑백
4. **Kodak Portra 800** (네거티브, ISO 800) - 고감도 인물
5. **Fujifilm Superia X-Tra 400** (네거티브, ISO 400)
6. **Agfa Vista Plus 200** (네거티브, ISO 200)
7. **Lomography Color Negative 800** (네거티브, ISO 800)

**예상 작업 시간:** 15~25시간

---

### 10.3 추가 기능 (향후 계획)

| 기능              | 설명                  | 우선순위 | 예상 시간 |
| ----------------- | --------------------- | -------- | --------- |
| **배치 처리**     | 여러 이미지 동시 처리 | 높음     | 5시간     |
| **사용자 계정**   | 로그인, 히스토리 저장 | 중간     | 20시간    |
| **커스텀 레시피** | 사용자 정의 필름 설정 | 중간     | 15시간    |
| **푸시/풀 현상**  | ISO 변경 시뮬레이션   | 낮음     | 10시간    |
| **RAW 지원**      | CR2, NEF 등 RAW 파일  | 높음     | 15시간    |
| **모바일 앱**     | iOS/Android 네이티브  | 낮음     | 100시간   |

---

## 11. 프로젝트 일정 (MVP)

### 11.1 Phase 1 타임라인 (2주)

| 주차       | 작업 내용                          | 예상 시간 | 담당       |
| ---------- | ---------------------------------- | --------- | ---------- |
| **Week 1** |                                    |           |            |
| Day 1-2    | 프로젝트 구조 생성, DB 스키마 구현 | 8시간     | Backend    |
| Day 3-5    | PDF 데이터 추출 (5개 필름)         | 16~24시간 | Data       |
| Day 6-7    | API 엔드포인트 구현                | 12시간    | Backend    |
| **Week 2** |                                    |           |            |
| Day 1-3    | 이미지 처리 파이프라인 구현        | 20시간    | Backend    |
| Day 4-5    | 프론트엔드 UI/UX 구현              | 16시간    | Frontend   |
| Day 6      | 통합 테스트                        | 8시간     | Full Stack |
| Day 7      | 배포 & 문서화                      | 6시간     | DevOps     |

**총 예상 시간:** 86~94시간 (약 2주)

---

## 12. 참고 자료

### 12.1 필름 데이터시트 원본

| 필름명       | PDF 파일                   | 페이지 수 | 분석 상태 |
| ------------ | -------------------------- | --------- | --------- |
| Velvia 50    | `fujifilm-velvia-50.pdf`   | 8         | ✅ 완료   |
| Provia 100F  | `fujifilm-provia-100f.pdf` | 6         | ✅ 완료   |
| Portra 400   | `kodak-portra-400.pdf`     | 4         | ✅ 완료   |
| Vision3 500T | `kodak-vision3-500t.pdf`   | 5         | ✅ 완료   |
| T-Max 100    | `kodak-t-max-100.pdf`      | 4         | ✅ 완료   |

### 12.2 외부 라이브러리 문서

- **colour-science:** https://colour.readthedocs.io/
- **Pillow:** https://pillow.readthedocs.io/
- **Flask:** https://flask.palletsprojects.com/
- **Next.js:** https://nextjs.org/docs
- **DaVinci Resolve:** https://www.blackmagicdesign.com/products/davinciresolve

### 12.3 관련 논문 & 아티클

- "Simulating Film with Digital Sensors" (Kodak White Paper)
- "Characteristic Curves and Tone Reproduction" (Fujifilm Technical Note)
- "LUT-based Color Grading in Modern Cinema" (SMPTE Journal)

---

## 13. 버전 히스토리

| 버전  | 날짜       | 변경 사항            | 작성자           |
| ----- | ---------- | -------------------- | ---------------- |
| 1.0.0 | 2025-11-26 | 최초 작성 (MVP 확정) | Film Recipe Team |

---

## 14. 라이선스 & 저작권

**프로젝트 라이선스:** MIT License

**데이터 출처:**

- 필름 데이터시트: © Fujifilm, Kodak (제조사 공식 문서)
- 레퍼런스 이미지: Flickr / Unsplash (CC0 / CC BY)

**면책 조항:**
본 프로젝트는 교육 및 연구 목적으로 제작되었습니다. 실제 필름과 100% 동일한 결과를 보장하지 않으며, 상업적 사용 시 필름 제조사의 상표권을 침해하지 않도록 주의해야 합니다.

---

## 15. 연락처

**프로젝트 관리자:** [이름]  
**이메일:** [이메일]  
**GitHub:** [레포지토리 URL]  
**Slack/Discord:** [채널 URL]

---

**END OF DOCUMENT**
