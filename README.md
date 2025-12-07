# 🎞️ Film Recipe - 필름 시뮬레이션 웹 애플리케이션

> **디지털 사진에 아날로그 필름의 색감과 질감을 과학적으로 재현**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 14+](https://img.shields.io/badge/next.js-14+-black.svg)](https://nextjs.org/)
[![Flask 3+](https://img.shields.io/badge/flask-3+-green.svg)](https://flask.palletsprojects.com/)

---

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [핵심 기능](#-핵심-기능)
- [MVP 필름 (5개)](#-mvp-필름-5개)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [개발 계획 (상세)](#-개발-계획-상세)
- [설치 및 실행](#-설치-및-실행)
- [API 문서](#-api-문서)
- [로드맵](#-로드맵)
- [기여 가이드](#-기여-가이드)
- [라이선스](#-라이선스)

---

## 🎯 프로젝트 개요

### 문제 정의

**필름 사진의 독특한 감성을 디지털로 재현하고 싶지만...**

- 💸 실제 필름 촬영은 비용이 많이 듦 (필름값 + 현상비)
- ⏰ 현상 시간이 오래 걸림 (1주일 이상)
- 🤔 어떤 필름이 내 사진에 맞는지 모름
- 🎨 단순한 필터는 전문성이 부족함

### 해결책

**Film Recipe는 과학적 데이터 기반으로 필름을 정확히 시뮬레이션합니다.**

1. **EXIF 자동 분석**: 사진의 촬영 설정을 자동으로 읽어서 최적의 필름 추천
2. **실제 필름 데이터**: Fujifilm, Kodak의 공식 데이터시트를 기반으로 정확한 재현
3. **프로페셔널 품질**: 5개 최고급 필름으로 시작 (Velvia 50, Provia 100F, Portra 400, Vision3 500T, T-Max 100)
4. **원클릭 적용**: 이미지 업로드 → 필름 선택 → 다운로드 (5초 이내)

---

## ✨ 핵심 기능

### 1. 🔍 **EXIF 기반 자동 필름 매칭**

```python
# 알고리즘 가중치
ISO 매칭:      50%  # 가장 중요
색온도 매칭:   20%  # 텅스텐/주광 구분
조리개 매칭:   15%  # 풍경(f/8+) vs 인물(f/2.8)
셔터 속도:     15%  # 장노출/고속 셔터
```

**예시:**

- ISO 100, f/11, 1/250s, Daylight → **Velvia 50** 추천 (풍경 필름)
- ISO 800, f/2.8, 1/50s, Tungsten → **Vision3 500T** 추천 (저조도 필름)

### 2. 🎨 **과학적 필름 시뮬레이션**

```
[원본 이미지]
    ↓
[색공간 변환] RGB → Linear RGB
    ↓
[3D LUT 적용] 필름 색상 재현
    ↓
[톤 커브] Characteristic Curves 데이터
    ↓
[그레인 오버레이] 필름 입자감
    ↓
[최종 출력] 필름 시뮬레이션 완료
```

**데이터 출처:**

- Characteristic Curves (톤 커브)
- Spectral Dye Density (색상 곡선)
- Spectral Sensitivity (파장 감도)
- RMS Granularity (입자 크기)

### 3. 📥 **간편한 다운로드**

- **단일 파일**: 선택한 필름 1개 (JPEG, 원본 해상도)
- **ZIP 패키지**: 5개 필름 버전 전체 (한 번에 다운로드)
- **메타데이터 보존**: EXIF 정보 유지

---

## 🎞️ MVP 필름 (5개)

### **선정 기준**

| 기준           | 설명                     |
| -------------- | ------------------------ |
| ✅ ISO 범위    | 50 ~ 500 전체 커버       |
| ✅ 타입 다양성 | 리버설 / 네거티브 / 흑백 |
| ✅ 품질 우선   | 프로페셔널 등급          |
| ✅ 차별화      | 각 필름의 고유 특성 명확 |

---

### 1️⃣ **Fujifilm Velvia 50** (리버설, ISO 50)

<details>
<summary><b>📊 상세 정보 보기</b></summary>

```yaml
이름: Fujichrome Velvia 50
제조사: Fujifilm
타입: Color Reversal (E-6)
ISO: 50 (Push +1 stop까지)
그레인: RMS 9 (ultra-fine)
```

**특성:**

- 🎨 **채도 10/10** - World's highest color saturation
- 🌄 **주 용도** - 풍경, 자연, 매크로
- 📊 **해상력** - 80 / 160 lines/mm

**추천 시나리오:**

- ISO ≤ 100
- 조리개 ≥ f/8 (심도 깊은 풍경)
- 주광 (Daylight WB, 5500K)

</details>

---

### 2️⃣ **Fujifilm Provia 100F** (리버설, ISO 100)

<details>
<summary><b>📊 상세 정보 보기</b></summary>

```yaml
이름: Fujichrome Provia 100F
제조사: Fujifilm
타입: Color Reversal (E-6)
ISO: 100 (Push +2 stop까지)
그레인: RMS 8 (finest among ISO 100)
```

**특성:**

- 🎨 **채도 6/10** - Vivid and faithful (자연스러움)
- 👤 **주 용도** - 인물, 제품, 패션, 만능형
- ✨ **특징** - Rich tone reproduction, Bias-free highlights

**추천 시나리오:**

- ISO ≤ 200
- 조리개 f/2.8 ~ f/8
- 다목적 촬영

**Velvia 50 vs Provia 100F:**

- Velvia: 극한 채도 → 풍경 특화
- Provia: 자연스러움 → 인물/제품/범용

</details>

---

### 3️⃣ **Kodak Portra 400** (네거티브, ISO 400)

<details>
<summary><b>📊 상세 정보 보기</b></summary>

```yaml
이름: Kodak Professional Portra 400
제조사: Kodak
타입: Color Negative (C-41)
ISO: 400 (Push +1 stop까지)
그레인: PGI 37 (세계 최고 수준)
```

**특성:**

- 🎨 **피부톤 9/10** - Spectacular skin tones
- 👤 **주 용도** - 인물, 패션, 여행, 저조도
- ✨ **특징** - Vision Film Technology

**추천 시나리오:**

- ISO 200 ~ 800
- 조리개 ≤ f/5.6 (얕은 심도 또는 저조도)
- 주광 또는 실내

**왜 Portra 160이 아닌 400?**

- ISO 400이 더 범용적 (2배 빠름)
- PGI 37 vs 28: 차이 미미 (여전히 세계 최고급)
- 저조도 대응력 우수

</details>

---

### 4️⃣ **Kodak Vision3 500T** (네거티브, ISO 500)

<details>
<summary><b>📊 상세 정보 보기</b></summary>

```yaml
이름: Kodak Vision3 500T (5219)
제조사: Kodak
타입: Cine Negative (ECN-2)
ISO: 500 (Tungsten 3200K)
ISO: 320 (Daylight with 85 filter)
```

**특성:**

- 🎨 **색온도 3200K** - 유일한 텅스텐 필름
- 🎬 **주 용도** - 영화, 저조도, 실내 촬영
- ✨ **특징** - Extended highlight latitude (+2 stops)

**추천 시나리오:**

- ISO ≥ 400
- 색온도 ≤ 4000K (텅스텐 / 실내 조명)
- WB: Tungsten / Incandescent

**CineStill 800T 대체 이유:**

- Vision3 500T가 원본 필름
- CineStill = Vision3 리믹스 (remjet 제거판)
- ISO 500도 충분히 저조도 커버

</details>

---

### 5️⃣ **Kodak T-Max 100** (흑백, ISO 100)

<details>
<summary><b>📊 상세 정보 보기</b></summary>

```yaml
이름: Kodak Professional T-Max 100
제조사: Kodak
타입: B&W Negative (T-MAX Developer)
ISO: 100 (Push +3 stop까지)
그레인: PGI < 25 (4×6인치에서 거의 인지 불가)
```

**특성:**

- 🔍 **그레인 10/10** - World's finest grain B&W
- 📊 **해상력 200 lines/mm** - 극한 디테일
- 🎨 **주 용도** - 흑백 예술, 확대 인화, 스캔
- ✨ **특징** - T-GRAIN Emulsion

**추천 시나리오:**

- 흑백 모드 또는 Monochrome Picture Style
- ISO ≤ 200
- 고해상력 요구 (확대 인화, 세밀한 디테일)

</details>

---

## 🛠️ 기술 스택

### **프론트엔드**

```
Next.js 14+          # React SSR, 이미지 최적화
React 18+            # 컴포넌트 기반 UI
Tailwind CSS 3+      # 유틸리티 클래스 스타일링
Zustand 4+           # 경량 상태 관리
Axios 1+             # HTTP 클라이언트
react-dropzone 14+   # Drag & Drop 업로드
```

### **백엔드**

```
Flask 3+             # Python 웹 프레임워크
Pillow 10+           # 이미지 처리
colour-science 0.4+  # 과학적 색공간 변환
NumPy 1.24+          # 고속 배열 연산
SciPy 1.11+          # 보간, 곡선 피팅
exifread             # EXIF 메타데이터 파싱
SQLAlchemy 2+        # ORM
Celery + Redis       # 비동기 작업
```

### **데이터베이스**

```
SQLite 3+            # 개발 환경
PostgreSQL 15+       # 프로덕션 환경
```

### **배포 & 인프라**

```
Docker               # 컨테이너화
GCP Cloud Run        # Serverless 배포 (4GB RAM, 2 vCPU)
GCP Cloud Storage    # 이미지 임시 저장
Cloudflare           # CDN
Sentry               # 에러 추적
```

---

## 📁 프로젝트 구조

```
C:\대학프로그래밍폴더\Filmrecipe\
│
├── frontend/                    # Next.js 프론트엔드
│   ├── app/
│   │   ├── page.tsx            # 메인 페이지
│   │   ├── upload/             # 업로드 페이지
│   │   └── result/             # 결과 페이지
│   ├── components/
│   │   ├── ImageUploader.tsx   # 드래그&드롭 업로드
│   │   ├── FilmPreview.tsx     # 필름 미리보기
│   │   └── DownloadButton.tsx  # 다운로드 버튼
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
│   │   │   ├── exif_extractor.py    # EXIF 추출 로직
│   │   │   ├── film_matcher.py      # 필름 매칭 알고리즘
│   │   │   └── image_processor.py   # 이미지 처리 파이프라인
│   │   ├── models/
│   │   │   ├── film.py         # Film 모델
│   │   │   └── recipe.py       # FilmRecipe 모델
│   │   └── utils/
│   │       ├── lut_loader.py   # 3D LUT 로더
│   │       ├── grain_generator.py  # 그레인 생성
│   │       └── tone_curve.py   # 톤 커브 적용
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
│   ├── pdfs/mvp/               # MVP 5개 필름 PDF
│   ├── luts/                   # 3D LUT 파일 (.cube)
│   ├── grain_overlays/         # 그레인 텍스처 PNG
│   └── curves/                 # 톤 커브 JSON
│
├── docs/
│   ├── SRS.md                  # 요구사항 명세서
│   ├── API.md                  # API 문서
│   ├── DEPLOYMENT.md           # 배포 가이드
│   └── ROADMAP.md              # 개발 로드맵
│
├── tests/
│   ├── test_exif.py
│   ├── test_matcher.py
│   └── test_processor.py
│
├── config/
│   └── films.yaml              # 필름 설정
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md                   # 이 문서
```

---

## 🚀 개발 계획 (상세)

> **목표:** 3일 단위로 배포 가능한 기능 완성  
> **전략:** 백엔드 → 프론트엔드 → 통합 순서

### **개발 규모 산정 기준**

| 규모          | 설명                   | 예상 시간 |
| ------------- | ---------------------- | --------- |
| **🟢 Small**  | 단일 기능, 의존성 없음 | 2~4시간   |
| **🟡 Medium** | 복합 기능, 약간의 통합 | 4~8시간   |
| **🔴 Large**  | 핵심 기능, 많은 통합   | 8~12시간  |

---

## 📅 **Day 1: 프로젝트 기반 구축** (8시간)

### **목표:** 개발 환경 세팅 + DB 스키마 완성

| 시간              | 작업                          | 규모 | 산출물                             |
| ----------------- | ----------------------------- | ---- | ---------------------------------- |
| **09:00 - 10:30** | 프로젝트 디렉토리 구조 생성   | 🟢   | 전체 폴더 구조                     |
| **10:30 - 12:00** | 가상환경 + 패키지 설치        | 🟢   | `requirements.txt`, `package.json` |
| **13:00 - 15:00** | DB 스키마 작성 및 초기 데이터 | 🟡   | `schema.sql`, SQLite DB 생성       |
| **15:00 - 17:00** | Flask 앱 기본 구조 + 라우팅   | 🟡   | `/api/films` GET 테스트 성공       |
| **17:00 - 18:00** | Git 설정 + 첫 커밋            | 🟢   | GitHub 레포지토리                  |

### **체크리스트**

```bash
✅ 프로젝트 디렉토리 생성
✅ Python 가상환경 (venv) 생성
✅ Flask 설치 (pip install Flask SQLAlchemy)
✅ database/schema.sql 작성
✅ SQLite DB 생성 (filmrecipe.db)
✅ films 테이블 5개 데이터 INSERT
✅ film_recipes 테이블 5개 레시피 INSERT
✅ Flask 앱 실행 확인 (localhost:5000)
✅ GET /api/films 테스트 성공
✅ Git 초기화 + .gitignore 설정
```

### **Day 1 종료 시점 상태**

```
✅ 백엔드 서버 실행 가능
✅ DB에 MVP 5개 필름 데이터 존재
✅ GET /api/films API 동작
❌ EXIF 추출 기능 (Day 2)
❌ 필름 매칭 알고리즘 (Day 2)
❌ 이미지 처리 (Day 3)
❌ 프론트엔드 (Day 3)
```

---

## 📅 **Day 2: 핵심 로직 구현** (10시간)

### **목표:** EXIF 추출 + 필름 매칭 알고리즘 완성

| 시간              | 작업                    | 규모 | 산출물                            |
| ----------------- | ----------------------- | ---- | --------------------------------- |
| **09:00 - 11:00** | EXIF 추출 서비스 구현   | 🟡   | `exif_extractor.py` 완성          |
| **11:00 - 13:00** | 필름 매칭 알고리즘 구현 | 🔴   | `film_matcher.py` 완성            |
| **14:00 - 16:00** | POST /api/upload 구현   | 🟡   | 이미지 업로드 + EXIF 추출         |
| **16:00 - 18:00** | POST /api/match 구현    | 🟡   | 필름 5개 추천 API                 |
| **18:00 - 19:00** | 단위 테스트 작성        | 🟢   | `test_exif.py`, `test_matcher.py` |

### **체크리스트**

```bash
✅ exifread 라이브러리 설치
✅ EXIF 추출 함수 구현
   - ISO, 셔터 속도, 조리개, WB, 색온도
✅ 필름 매칭 알고리즘 구현
   - calculate_iso_score()
   - calculate_wb_score()
   - calculate_aperture_score()
   - calculate_shutter_score()
✅ POST /api/upload 구현
   - 이미지 파일 수신
   - EXIF 추출
   - 임시 저장 (data/temp/)
✅ POST /api/match 구현
   - 5개 필름 점수 계산
   - 정렬 후 JSON 반환
✅ Postman으로 API 테스트
✅ 단위 테스트 작성
```

### **Day 2 종료 시점 상태**

```
✅ 이미지 업로드 API 동작
✅ EXIF 자동 추출
✅ 필름 5개 추천 (점수 포함)
❌ 이미지 처리 파이프라인 (Day 3)
❌ LUT 적용 (Day 3)
❌ 프론트엔드 (Day 3)
```

---

## 📅 \*\*Day 3: 이미지 처리 + 프론트엔드 (12시간)

### **목표:** 필름 시뮬레이션 적용 + 기본 UI 완성

| 시간              | 작업                        | 규모 | 산출물                    |
| ----------------- | --------------------------- | ---- | ------------------------- |
| **09:00 - 12:00** | 이미지 처리 파이프라인 구현 | 🔴   | `image_processor.py` 완성 |
| **13:00 - 15:00** | LUT 로더 + 적용 함수        | 🟡   | `lut_loader.py` 완성      |
| **15:00 - 17:00** | 그레인 오버레이 구현        | 🟡   | `grain_generator.py` 완성 |
| **17:00 - 19:00** | Next.js 프론트엔드 기본 UI  | 🟡   | 업로드 페이지 완성        |
| **19:00 - 21:00** | 통합 테스트 + 버그 수정     | 🟡   | E2E 테스트 성공           |

### **체크리스트**

```bash
✅ Pillow, colour-science 설치
✅ apply_film_simulation() 함수 구현
   - 색공간 변환 (RGB → Linear RGB)
   - 3D LUT 적용
   - 톤 커브 적용
   - 그레인 오버레이
✅ 간단한 LUT 파일 준비 (테스트용)
✅ 그레인 텍스처 PNG 생성 (Photoshop/GIMP)
✅ POST /api/process 구현
   - 5개 필름 버전 생성
   - 임시 폴더 저장
   - URL 반환
✅ Next.js 프로젝트 생성
✅ 이미지 업로드 컴포넌트 (react-dropzone)
✅ 필름 선택 UI
✅ 미리보기 표시
✅ 다운로드 버튼
✅ E2E 테스트 (업로드 → 처리 → 다운로드)
```

### **Day 3 종료 시점 상태**

```
✅ 전체 파이프라인 동작
✅ 이미지 업로드 가능
✅ 필름 5개 적용 가능
✅ 다운로드 가능
✅ 기본 UI 완성
❌ LUT 데이터 정교화 (추후)
❌ 톤 커브 정밀 조정 (추후)
❌ 배포 (추후)
```

---

## 🎯 **MVP 완성 체크리스트 (Day 1 완료)**

```bash
✅ 백엔드 서버 실행 (Flask)
✅ DB에 5개 필름 데이터 존재 (13개 아님!)
✅ GET /api/films API 동작
✅ GET /api/films/{id} API 동작
✅ 파라미터 검증 + 에러 처리
✅ JSON property (tone_curve, spectral_dye 등)
✅ 코드 리뷰 완료 및 버그 수정
⏳ 이미지 업로드 (Day 2)
⏳ EXIF 자동 추출 (Day 2)
⏳ 필름 5개 자동 추천 (Day 2)
⏳ 필름 시뮬레이션 적용 (Day 3)
⏳ 프론트엔드 (Day 3)
```

---

## 📅 **Day 4-7: 개선 및 배포** (선택 사항)

### **Day 4: 데이터 정교화** (8시간)

```
- PDF 데이터 수동 추출 (WebPlotDigitizer)
- Characteristic Curves → JSON 변환
- Spectral Dye Density → JSON 변환
- 정확한 LUT 파일 생성 (DaVinci Resolve)
```

### **Day 5: UI/UX 개선** (8시간)

```
- Tailwind CSS 스타일링 강화
- 로딩 애니메이션 추가
- 에러 처리 개선
- 반응형 디자인
```

### **Day 6: 테스트 & 최적화** (8시간)

```
- 단위 테스트 커버리지 80% 이상
- 성능 최적화 (이미지 압축)
- 메모리 사용량 최적화
- 보안 점검
```

### **Day 7: 배포** (8시간)

```
- Docker 이미지 빌드
- GCP Cloud Run 배포
- 환경 변수 설정
- 도메인 연결
- 모니터링 설정 (Sentry)
```

---

## 📦 설치 및 실행

### **1️⃣ 사전 요구사항**

```bash
# 필수 소프트웨어
- Python 3.11+
- Node.js 18+
- Git

# 권장 소프트웨어
- Docker Desktop (배포용)
- VS Code (개발 환경)
```

### **2️⃣ 저장소 클론**

```bash
git clone https://github.com/your-username/filmrecipe.git
cd filmrecipe
```

### **3️⃣ 백엔드 설정**

```bash
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 수정

# DB 초기화
python -c "from app import db; db.create_all()"

# 서버 실행
python run.py
```

**백엔드 실행 확인:**

```
http://localhost:5000/api/films
```

### **4️⃣ 프론트엔드 설정**

```bash
cd frontend

# 패키지 설치
npm install

# 환경 변수 설정
cp .env.local.example .env.local
# .env.local 파일 수정

# 개발 서버 실행
npm run dev
```

**프론트엔드 실행 확인:**

```
http://localhost:3000
```

### **5️⃣ Docker로 실행 (선택)**

```bash
# 전체 스택 실행
docker-compose up -d

# 확인
docker ps
```

---

## 📖 API 문서

### **기본 URL**

```
개발: http://localhost:5000/api
프로덕션: https://filmrecipe-api.run.app/api
```

### **엔드포인트 목록**

#### **1. GET /films**

**설명:** 필름 목록 조회

**Query Parameters:**

```
tier: mvp|core|extended|all (default: mvp)
type: color|bw|all (default: all)
```

**응답 예시:**

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
      "recipes": [
        {
          "id": 1,
          "recipe_name": "Standard E-6",
          "iso_range": "25-100"
        }
      ]
    }
  ]
}
```

#### **2. POST /upload**

**설명:** 이미지 업로드 및 EXIF 추출

**Request:**

```
Content-Type: multipart/form-data
Body: images=[File]
```

**응답 예시:**

```json
{
  "job_id": "abc123",
  "images": [
    {
      "filename": "IMG_0001.jpg",
      "exif": {
        "iso": 200,
        "shutter_speed": 0.008,
        "aperture": 5.6,
        "white_balance": "Auto"
      },
      "matched_films": [
        {
          "film_id": 2,
          "film_name": "Fujichrome Provia 100F",
          "score": 85
        }
      ]
    }
  ]
}
```

#### **3. POST /process**

**설명:** 필름 시뮬레이션 적용

**Request:**

```json
{
  "job_id": "abc123",
  "film_ids": [1, 2, 3, 4, 5],
  "options": {
    "apply_grain": true,
    "grain_strength": 0.5
  }
}
```

**응답 예시:**

```json
{
  "job_id": "abc123",
  "status": "completed",
  "results": [
    {
      "film_id": 1,
      "film_name": "Fujichrome Velvia 50",
      "output_url": "/download/abc123/IMG_0001_velvia50.jpg"
    }
  ],
  "zip_url": "/download/abc123/all_films.zip"
}
```

**상세 API 문서:** [docs/API.md](docs/API.md)

---

## 🗺️ 로드맵

### **✅ Phase 1: MVP (현재)**

- [x] 5개 필름 (Velvia 50, Provia 100F, Portra 400, Vision3 500T, T-Max 100)
- [x] EXIF 기반 자동 매칭
- [x] 기본 필름 시뮬레이션 (LUT + 그레인)
- [x] 웹 UI (업로드 / 다운로드)

### **🚧 Phase 2: Core Films (예정)**

- [ ] 8개 필름 추가 (총 13개)
  - Ektachrome E100
  - Gold 200
  - UltraMax 400
  - Ektar 100
  - Portra 160
  - ProImage 100
  - T-Max 400
  - Rollei RPX 100
- [ ] 배치 처리 (여러 이미지 동시)
- [ ] RAW 파일 지원 (CR2, NEF)

### **🔮 Phase 3: Extended (향후)**

- [ ] 7개 필름 추가 (총 20개)
- [ ] 사용자 계정 (로그인, 히스토리)
- [ ] 커스텀 레시피 (사용자 정의)
- [ ] 푸시/풀 현상 시뮬레이션
- [ ] 모바일 앱 (iOS/Android)

---

## 🤝 기여 가이드

### **기여 방법**

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### **코드 스타일**

```python
# Python (PEP 8)
- 들여쓰기: 4 spaces
- 줄 길이: 120자 이하
- 함수명: snake_case
- 클래스명: PascalCase
```

```typescript
// TypeScript (Airbnb Style)
- 들여쓰기: 2 spaces
- 세미콜론: 사용
- 함수명: camelCase
- 컴포넌트명: PascalCase
```

### **테스트**

```bash
# 백엔드 테스트!
cd backend
pytest

# 프론트엔드 테스트!


cd frontend
npm test
```
[filmrecipe1](https://github.com/user-attachments/assets/cb2300fc-8f7c-4606-a0a6-6abca368e970)
[filmrecipe2](https://github.com/user-attachments/assets/a18a1973-cd71-4429-b49d-e85df18d3193)

