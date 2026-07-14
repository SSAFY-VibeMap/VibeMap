# 🗺️ VibeMap - 지역 기반 음식 정보 커뮤니티

> 익명 커뮤니티와 AI 챗봇으로 지역의 맛있는 음식점을 발견하세요

## 📋 프로젝트 소개

**VibeMap**은 회원가입 없이 누구나 참여할 수 있는 익명 기반 지역 정보 커뮤니티입니다. 
사용자들은 지역별 게시판에서 음식점 정보를 공유하고, AI 챗봇을 통해 맞춤형 추천을 받을 수 있습니다.

### 🎯 핵심 특징
- **익명 커뮤니티**: 회원가입 없이 비밀번호 기반으로 관리
- **AI 챗봇**: OpenAI를 활용한 자연스러운 추천과 정보 제공
- **지역 맞춤형**: 사용자 위치 기반 정보 제공
- **모바일 최적화**: 모든 디바이스에서 쾌적한 사용 경험

---

## 🎯 주요 기능

### 커뮤니티 게시판
- **익명 기반**: 회원가입 없이 비밀번호로 게시글 관리
- **CRUD 기능**: 게시글, 댓글 작성/수정/삭제
- **지역별 분류**: 지역 기반 게시판 운영

### AI 챗봇
- **자연어 처리**: 사용자 의도 자동 분류
- **정보 검색**: 음식점, 축제, 관광지 정보 제공
- **추천 기능**: OpenAI 기반 지역별 음식점 추천

### 지도 연동
- **위치 표시**: 음식점, 축제 위치를 지도에 표시
- **상세 정보**: 위치 클릭 시 상세 정보 확인
- **검색 기능**: 지역별, 카테고리별 검색

---

## ⚙️ 기술 스택

### 백엔드
- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **AI**: OpenAI API
- **Hosting**: Render

### 프론트엔드
- **Framework**: Vue.js
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Map**: Naver Map API
- **Hosting**: Netlify

---

## 🚀 빠른 시작

### 사전 요구사항
- Python 3.8+
- Node.js 14+
- Git

### 백엔드 실행

```bash
cd chatbot

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에서 필요한 값 수정

# 서버 실행
uvicorn app.main:app --reload
```

### 프론트엔드 실행

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env

# 개발 서버 실행
npm run dev
```

---

## 📚 개발 문서

상세한 개발 정보는 `docs/` 폴더를 참고하세요.

| 문서 | 내용 |
|------|------|
| [`.AGENTS.md`](docs/.AGENTS.md) | 코드 컨벤션, Git 전략, 코드 리뷰 |
| [`API_SPECIFICATION.md`](docs/API_SPECIFICATION.md) | API 명세, 데이터 스키마 |
| [`PROJECT_SETUP.md`](docs/PROJECT_SETUP.md) | 프로젝트 구조, 팀 역할, RFP 요구사항 |
| [`ENVIRONMENT.md`](docs/ENVIRONMENT.md) | 환경 변수 설정 가이드 |
| [`DEPLOYMENT.md`](docs/DEPLOYMENT.md) | 배포 가이드 (Netlify, Render) |

---

## 📞 문의

문제가 발생하면 GitHub Issues를 통해 보고해주세요.

## 📄 라이선스

MIT License
