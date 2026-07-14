# VibeMap 프로젝트 설정 및 구조

> 프로젝트 구조, 데이터 모델, 팀 역할, RFP 요구사항 정보

---

## 📦 프로젝트 구조

```
VibeMap/
├── backend/                      # FastAPI 백엔드
│   ├── app/
│   │   ├── api/
│   │   │   ├── posts.py         # 게시글 라우터
│   │   │   ├── comments.py      # 댓글 라우터
│   │   │   ├── events.py        # 행사 라우터
│   │   │   └── chat.py          # 챗봇 라우터 (/api/chat)
│   │   ├── models/
│   │   │   ├── post.py          # Post 모델 (SQLAlchemy)
│   │   │   ├── comment.py       # Comment 모델
│   │   │   # Note: Event 데이터는 DB가 아니라 프로젝트자료/data/*.json 파일에서 읽어 사용합니다.
│   │   ├── schemas/
│   │   │   ├── post.py          # Post Pydantic 스키마
│   │   │   ├── comment.py       # Comment 스키마
│   │   │   └── chat.py          # Chat 요청/응답 스키마
│   │   ├── services/
│   │   │   ├── post_service.py  # 게시글 비즈니스 로직
│   │   │   ├── chat_service.py  # 챗봇 비즈니스 로직
│   │   │   └── openai_service.py# OpenAI 통합
│   │   ├── database.py          # SQLAlchemy 설정
│   │   └── main.py              # FastAPI 애플리케이션
│   ├── .env                      # 환경 변수 (Git 제외)
│   ├── .env.example              # 환경 변수 템플릿
│   ├── .gitignore                # Git 무시 파일
│   ├── requirements.txt           # Python 의존성
│   └── README.md                 # 백엔드 문서
│
├── frontend/                     # Vue.js 프론트엔드
│   ├── src/
│   │   ├── components/
│   │   │   ├── BoardList.vue     # 게시판 목록
│   │   │   ├── PostDetail.vue    # 게시글 상세
│   │   │   ├── PostForm.vue      # 게시글 작성/수정
│   │   │   ├── ChatBox.vue       # 채팅 UI (플로팅)
│   │   │   ├── MapView.vue       # Kakao 지도
│   │   │   └── EventPanel.vue    # 축제 정보 패널
│   │   ├── services/
│   │   │   ├── apiClient.js      # fetch 설정
│   │   │   ├── postService.js    # 게시글 API
│   │   │   └── chatService.js    # 챗봇 API
│   │   ├── views/
│   │   │   ├── Home.vue          # 홈 페이지
│   │   │   ├── Board.vue         # 게시판 페이지
│   │   │   └── Events.vue        # 행사 페이지
│   │   ├── App.vue               # 루트 컴포넌트
│   │   └── main.js               # 진입점
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── docs/
│   ├── .AGENTS.md                # 코드 컨벤션, Git 전략
│   ├── API_SPECIFICATION.md      # API 명세, DB 스키마
│   ├── PROJECT_SETUP.md          # 프로젝트 구조, 팀 역할
│   ├── ENVIRONMENT.md            # 환경 변수 설정
│   └── DEPLOYMENT.md             # 배포 가이드
│
├── README.md                     # 프로젝트 개요
└── .gitignore
```

---

## 🏗️ 기술 상세 정보

### 백엔드 (FastAPI)
| 항목 | 기술 | 버전 | 용도 |
|------|------|------|------|
| Framework | FastAPI | 0.104.0 | REST API 서버 |
| Server | Uvicorn | 0.24.0 | ASGI 서버 |
| Database | SQLite | - | 영속 데이터 저장 |
| ORM | SQLAlchemy | 2.0.23 | 데이터 모델링 |
| Validation | Pydantic | 2.4.0 | 요청/응답 검증 |
| AI/NLP | OpenAI | 1.3.0 | 챗봇 기능 |
| Env Management | python-dotenv | 1.0.0 | 환경 변수 관리 |
| Hosting | Render | - | 백엔드 호스팅 |

### 프론트엔드 (Vue.js)
| 항목 | 기술 | 용도 |
|------|------|------|
| Framework | Vue.js 3 | UI 프레임워크 |
| Build Tool | Vite | 빠른 번들링 |
| Router | Vue Router | 페이지 네비게이션 |
| HTTP Client | fetch | API 통신 |
| Styling | CSS3 | UI 스타일 |
| Map API | Kakao Map | 지도 기능 |
| Hosting | Netlify | 프론트엔드 호스팅 |

---

## 📋 데이터 모델 (상세)

### Post 테이블
게시글 정보를 저장하는 핵심 테이블

| 칼럼 | 타입 | 설명 | 제약조건 |
|------|------|------|---------|
| id | INTEGER | 게시글 ID | PK, AUTO_INCREMENT |
| title | VARCHAR(255) | 게시글 제목 | NOT NULL |
| content | TEXT | 게시글 내용 | NOT NULL |
| password | VARCHAR(255) | 수정/삭제 비밀번호 | NOT NULL, 평문 저장 |
| region | VARCHAR(50) | 지역 분류 | DEFAULT='seoul' |
| created_at | DATETIME | 작성 일시 | DEFAULT=NOW() |
| updated_at | DATETIME | 수정 일시 | DEFAULT=NOW() |

### Comment 테이블
댓글 정보를 저장하는 테이블

| 칼럼 | 타입 | 설명 | 제약조건 |
|------|------|------|---------|
| id | INTEGER | 댓글 ID | PK, AUTO_INCREMENT |
| post_id | INTEGER | 게시글 ID | FK (Post.id) |
| content | TEXT | 댓글 내용 | NOT NULL |
| password | VARCHAR(255) | 수정/삭제 비밀번호 | NOT NULL, 평문 저장 |
| created_at | DATETIME | 작성 일시 | DEFAULT=NOW() |
| updated_at | DATETIME | 수정 일시 | DEFAULT=NOW() |

### Event 데이터 소스
행사/축제 데이터는 DB에 저장하지 않고 프로젝트 내 JSON 원본 파일을 직접 읽어 응답합니다.

- 파일 위치 예시:
	- `프로젝트자료/data/서울/서울_축제공연행사.json`
	- `프로젝트자료/data/부산/부산_축제공연행사.json`

참고: 이벤트 관련 필터링/검색은 이 JSON 원본을 기반으로 구현합니다. 필요 시 별도 마이그레이션 스크립트를 통해 DB로 이전할 수 있습니다.

---

## 👥 팀 구성 및 역할 분담

### 프로젝트 일정 (Day 1 ~ Day 3)

#### **Day 1 (2026-07-14) - 기획 및 설계**

| No | 작업명 | 담당 | 소요시간 | 상태 |
|:--:|--------|------|:-------:|:----:|
| 1 | **기획**: 착수 및 범위 확정, 화면 흐름, API/DB 초안 | 전원 | 1일 | 진행중 |
| 2 | **설계**: 백엔드 기본 골격 (FastAPI, SQLite, SQLAlchemy, .env) | BE 2명 | 1일 | 예정 |

---

#### **Day 2 (2026-07-15) - 본격 개발**

| No | 작업명 | 담당 | 소요시간 | 상태 |
|:--:|--------|------|:-------:|:----:|
| 3 | 커뮤니티 게시글 모델/CRUD API, 비밀번호 검증 | 백광훈 (BE) | 2일 | 예정 |
| 4 | 서울 행사 데이터 모델, 조회 API, 검색 보조 로직 | 신예지 (BE) | 2일 | 예정 |
| 5 | 챗봇 API 설계 및 /api/chat 구현 | 백광훈 (BE) | 2일 | 예정 |
| 6 | Kakao Map 연동용 데이터 정리, 핀용 응답 포맷 | 신예지 (BE) | 2일 | 예정 |
| 7 | Vue 프로젝트 초기화, 라우팅, 공통 레이아웃 | 윤종근 (FE) | 1일 | 예정 |
| 8 | 게시판 목록/상세/작성/수정 UI | 윤종근 (FE) | 1일 | 예정 |
| 9 | 채팅 UI, 대화 히스토리, 플로팅 버튼 | 윤종근 (FE) | 2일 | 예정 |
| 10 | Kakao Map 화면, 행사 핀 표시, 모바일 대응 | 윤종근 (FE) | 2일 | 예정 |
| 11 | 축제 모집 화면 또는 모집 패널 | 윤종근 (FE) | 2일 | 예정 |

---

#### **Day 3 (2026-07-16) - 배포 및 완성**

| No | 작업명 | 담당 | 소요시간 | 상태 |
|:--:|--------|------|:-------:|:----:|
| 12 | **배포**: 배포, URL 검증, 문서화 | 전원 | 1일 | 예정 |
| 13 | **발표준비**: PPT 제작, 발표 준비 | 전원 | 1일 | 예정 |

---

### 👨‍💻 팀원 역할 상세

#### **백광훈** (백엔드 개발자)
**담당 업무**
- ✅ Post/Comment 데이터 모델 설계 (SQLAlchemy)
- ✅ 게시글 CRUD API 구현
- ✅ 댓글 CRUD API 구현
- ✅ 비밀번호 검증 로직 (평문 저장)
- ✅ **챗봇 API 설계 및 구현** (`POST /api/chat`)
- ✅ OpenAI API 통합

#### **신예지** (백엔드 개발자)
**담당 업무**
- ✅ Event 데이터 모델 설계
- ✅ 행사 조회 API 구현
- ✅ 검색 보조 로직 (챗봇용)
- ✅ Kakao Map 연동용 데이터 정리
- ✅ CORS 설정 및 배포 환경 준비

#### **윤종근** (프론트엔드 개발자)
**담당 업무**
- ✅ Vue.js 프로젝트 초기화
- ✅ 라우팅 및 공통 레이아웃
- ✅ 게시판 UI (목록/상세/작성/수정)
- ✅ 채팅 UI + 플로팅 버튼
- ✅ 지도 화면 + 행사 표시
- ✅ 모바일 반응형 처리

---

## 🔴 Must 요구사항 (필수)

### 커뮤니티 게시판
- [ ] 1개 권역 게시판 CRUD API
- [ ] 게시글 목록/상세/작성/수정/삭제
- [ ] 댓글 CRUD
- [ ] SQLite DB 영속 저장
- [ ] Vue 컴포넌트 구현

### 챗봇
- [ ] `POST /api/chat` 엔드포인트 구현
- [ ] JSON 요청/응답 처리
- [ ] OpenAI API 또는 규칙 기반 응답

### 채팅 UI
- [ ] 대화 히스토리 유지
- [ ] 모바일 반응형 디자인
- [ ] 플로팅 버튼/팝업

### 배포
- [ ] 프론트엔드: Netlify 배포
- [ ] 백엔드: Render 배포
- [ ] 배포 URL 검증 및 문서화

---

## 🔵 Constraint (제약사항)

### 익명 커뮤니티
- 회원가입/로그인 없음
- 사용자 인증/권한 체계 제외
- 비회원 기반 최소 권한 구조

### 비밀번호 기반 관리
- 게시글 작성 시 비밀번호 설정
- 비밀번호 일치 여부로만 권한 판단
- ⚠️ 평문 저장 (교육용 예외)

### 환경 변수 관리
- `.env` 파일 사용 (Git 제외)
- API 키, DB 경로 환경 변수화
- 소스 코드에 민감정보 미포함

### DB 영속 저장
- SQLite 파일 저장소 필수
- 데이터 조회 API 필수
