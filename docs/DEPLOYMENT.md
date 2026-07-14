# VibeMap 배포 가이드

> Netlify (프론트엔드) + Render (백엔드) 배포 전체 가이드

---

## 📊 배포 환경 개요

| 구성 | 서비스 | URL | 설명 |
|------|--------|-----|------|
| 프론트엔드 | Netlify | https://vibemap.netlify.app | 정적 사이트 호스팅 |
| 백엔드 | Render | https://vibemap-backend.onrender.com | 서버 호스팅 |
| 데이터베이스 | SQLite | Render 서버 내 | 파일 기반 DB |

---

## 🚀 배포 전 체크리스트

### 배포 전 필수 작업
- [ ] 모든 코드 테스트 완료
- [ ] 환경 변수 설정 완료 (`.env.example` 작성)
- [ ] Git에 민감정보 커밋 안 됨 확인
- [ ] `.gitignore`에 `.env` 포함 확인
- [ ] 모든 커밋 로컬에서 테스트 완료
- [ ] 배포 브랜치 최신화
- [ ] 문서 최신화 (README, docs/)

### 코드 품질 검사
```bash
# 백엔드
cd chatbot
black app/  # 포맷팅
flake8 app/ # 린팅

# 프론트엔드
cd ../frontend
npm run lint  # ESLint
npm run build # 빌드 테스트
```

---

## 1️⃣ 백엔드 배포 (Render)

### 사전 준비

#### 1단계: 저장소 준비
```bash
# 저장소에 backend 폴더 있는지 확인
git status

# requirements.txt 최신화
pip freeze > chatbot/requirements.txt

# 커밋 및 푸시
git add chatbot/
git commit -m "chore: requirements.txt 업데이트"
git push origin main
```

#### 2단계: Render 계정 생성
1. [Render](https://render.com) 접속
2. GitHub 계정으로 로그인
3. 계정 설정 완료

---

### 배포 설정

#### 1단계: 새 Web Service 생성
1. Render 대시보드 → "New +" → "Web Service"
2. GitHub 저장소 선택
3. "VibeMap" 또는 원하는 이름 입력

#### 2단계: 배포 명령 설정
```
Environment: Python 3.11
Region: Singapore (또는 가장 가까운 지역)

Build Command:
pip install -r chatbot/requirements.txt

Start Command:
cd chatbot && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### 3단계: 환경 변수 설정
Render 대시보드 → "Environment" → "Add Secret File" 또는 "Add Environment Variable"

```
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
NAVER_MAP_API_KEY=...
DATABASE_URL=sqlite:///./vibemap.db
FRONTEND_URL=https://vibemap.netlify.app
API_SECRET_KEY=your-production-secret-key
LOG_LEVEL=INFO
```

#### 4단계: 배포 시작
- "Create Web Service" 클릭
- 배포 프로세스 시작 (약 5-10분)
- 배포 완료 후 URL 생성
- 예: `https://vibemap-backend.onrender.com`

---

### 배포 후 확인

#### 헬스 체크
```bash
# API 문서 접근
curl https://vibemap-backend.onrender.com/docs

# API 엔드포인트 테스트
curl https://vibemap-backend.onrender.com/api/posts
curl https://vibemap-backend.onrender.com/api/events
```

#### 로그 확인
Render 대시보드 → "Logs" 탭에서 실시간 로그 확인

#### 문제 발생 시
```bash
# 1. 환경 변수 재확인
# 대시보드에서 모든 환경 변수 값 검증

# 2. 재배포
# 대시보드 → "Manual Deploy" → "Deploy latest commit"

# 3. 로그 확인
# 에러 메시지를 로그에서 찾아 해결
```

---

## 2️⃣ 프론트엔드 배포 (Netlify)

### 사전 준비

#### 1단계: 빌드 테스트
```bash
cd frontend

# 의존성 설치
npm install

# 프로덕션 빌드 테스트
npm run build

# dist/ 폴더 생성 확인
ls -la dist/
```

#### 2단계: 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# 백엔드 URL 업데이트
VITE_API_BASE_URL=https://vibemap-backend.onrender.com
VITE_NAVER_MAP_API_KEY=...
```

#### 3단계: 저장소에 커밋
```bash
# 프론트엔드 폴더만 커밋 (dist/ 제외)
git add frontend/
git commit -m "chore: frontend .env.example 업데이트"
git push origin main
```

---

### 배포 설정

#### 1단계: Netlify 계정 생성
1. [Netlify](https://netlify.com) 접속
2. GitHub 계정으로 로그인

#### 2단계: 프로젝트 연결
1. "Add new site" → "Import an existing project"
2. GitHub 저장소 선택
3. "VibeMap" 또는 "vibemap-frontend" 선택

#### 3단계: 빌드 설정
```
Team: Personal

Owner: 본인

Repository branch: main

Build settings:
  Base directory: frontend
  Build command: npm run build
  Publish directory: frontend/dist
```

#### 4단계: 환경 변수 설정
"Site settings" → "Build & deploy" → "Environment"

```
VITE_API_BASE_URL=https://vibemap-backend.onrender.com
VITE_NAVER_MAP_API_KEY=...
VITE_ENV=production
```

#### 5단계: 배포
- "Deploy site" 클릭
- 배포 프로세스 시작 (약 1-3분)
- 배포 완료 후 URL 생성
- 예: `https://vibemap.netlify.app`

---

### 배포 후 확인

#### 프론트엔드 접속
```bash
# 브라우저에서 접속
https://vibemap.netlify.app

# 주요 기능 테스트
1. 홈페이지 로드
2. 게시판 페이지 이동
3. 게시글 목록 조회
4. 채팅 버튼 클릭
5. 지도 페이지 이동
```

#### 빌드 로그 확인
Netlify 대시보드 → "Deploys" → 최근 배포 → "Deploy log"

#### 문제 발생 시
```bash
# 1. 환경 변수 재확인
# Netlify 대시보드에서 모든 변수 값 검증

# 2. 빌드 스크립트 확인
# package.json의 build 명령 검증

# 3. 로컬에서 재 테스트
npm run build
npm run preview

# 4. 재배포
# Netlify 대시보드 → "Trigger new build" → "Deploy site"
```

---

## 3️⃣ 전체 연동 테스트

### 배포 후 통합 테스트

#### Step 1: 백엔드 API 확인
```bash
# API 문서 접근
https://vibemap-backend.onrender.com/docs

# Swagger UI에서 각 엔드포인트 테스트:
- GET /api/posts
- POST /api/posts
- GET /api/events
- POST /api/chat
```

#### Step 2: 프론트엔드-백엔드 통신 확인
```bash
# 프론트엔드 접속
https://vibemap.netlify.app

# 브라우저 개발자 도구 → Network 탭에서 확인:
1. API 요청 성공 여부
2. CORS 에러 없음
3. 응답 데이터 정상
```

#### Step 3: 주요 기능 테스트

**게시판 테스트**
- [ ] 게시글 목록 조회
- [ ] 게시글 작성
- [ ] 게시글 수정 (비밀번호 검증)
- [ ] 게시글 삭제
- [ ] 댓글 작성/수정/삭제

**챗봇 테스트**
- [ ] 채팅창 열기
- [ ] 메시지 전송
- [ ] AI 응답 수신
- [ ] 대화 이력 표시

**지도 테스트**
- [ ] 지도 로드
- [ ] 행사 핀 표시
- [ ] 핀 클릭 시 상세정보 표시

---

## 🔄 지속적 배포 (CI/CD) 설정

### Render - 자동 배포
```
Render은 기본적으로 GitHub push를 감지하여 자동 배포됨
- main 브랜치 push → 자동 배포 트리거
- 배포 상태: Render 대시보드의 "Events" 탭에서 확인
```

### Netlify - 자동 배포
```
Netlify도 기본적으로 GitHub push를 감지하여 자동 배포됨
- frontend/ 폴더 변경 감지 → 자동 빌드 및 배포
- 배포 상태: Netlify 대시보드의 "Deploys" 탭에서 확인
```

### GitHub Actions 활용 (고급)
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd chatbot
          pip install -r requirements.txt
          pytest
```

---

## 📋 배포 체크리스트

### 배포 전
- [ ] 모든 테스트 통과
- [ ] 코드 품질 검사 완료
- [ ] `.env.example` 작성
- [ ] README 최신화
- [ ] API 문서 최신화
- [ ] Git에 민감정보 없음 확인

### 백엔드 배포 후
- [ ] Render URL 생성 확인
- [ ] 환경 변수 모두 설정 확인
- [ ] API 엔드포인트 응답 확인
- [ ] Swagger UI 접근 가능 확인
- [ ] DB 연결 확인

### 프론트엔드 배포 후
- [ ] Netlify URL 생성 확인
- [ ] 환경 변수 모두 설정 확인
- [ ] 사이트 로드 확인
- [ ] 주요 페이지 접근 가능 확인
- [ ] API 통신 성공 확인

### 통합 테스트
- [ ] 게시판 CRUD 동작
- [ ] 챗봇 API 응답
- [ ] 지도 표시
- [ ] 모바일 반응형
- [ ] CORS 설정 정상

### 최종 확인
- [ ] 배포 URL 문서에 기록
- [ ] 팀원에게 배포 완료 공유
- [ ] 모니터링 설정 (선택사항)
- [ ] 자동 배포 규칙 확인

---

## 🔗 배포 URL 저장

배포 완료 후 다음 정보를 기록하세요:

```markdown
## VibeMap 배포 정보

### 프론트엔드 (Netlify)
- URL: https://vibemap.netlify.app
- 저장소: https://github.com/your-org/vibemap/tree/main/frontend
- 배포 브랜치: main

### 백엔드 (Render)
- URL: https://vibemap-backend.onrender.com
- API 문서: https://vibemap-backend.onrender.com/docs
- 저장소: https://github.com/your-org/vibemap/tree/main/chatbot
- 배포 브랜치: main

### 환경 설정
- Netlify 환경 변수: [설정됨]
- Render 환경 변수: [설정됨]

### 배포 담당자
- 프론트엔드: [담당자 이름]
- 백엔드: [담당자 이름]
```

---

## 🆘 배포 문제 해결

### "Build failed" 에러
```bash
# 1. 로컬에서 빌드 테스트
npm run build (frontend)
pip install -r requirements.txt (backend)

# 2. 의존성 문제 확인
# requirements.txt, package.json 버전 확인

# 3. 재배포
# Render/Netlify 대시보드에서 "Redeploy"
```

### "CORS error" 발생
```bash
# 1. FRONTEND_URL 확인
echo $FRONTEND_URL  # Render

# 2. VITE_API_BASE_URL 확인
# Netlify 환경 변수에서 확인

# 3. 백엔드 CORS 설정 확인
# app/main.py의 CORSMiddleware 설정

# 4. 재배포
```

### "API connection failed"
```bash
# 1. 백엔드 헬스 체크
curl https://vibemap-backend.onrender.com/docs

# 2. 환경 변수 확인
# 모든 API 키 정확성 검증

# 3. 로그 확인
# Render 대시보드의 Logs 탭

# 4. 재시작
# Render 대시보드 → "Manual Restart"
```

### "Database error"
```bash
# 1. DATABASE_URL 확인
# Render에서 정확한 경로 설정

# 2. DB 초기화
# Render에 SSH 접속 후 DB 재생성

# 3. 마이그레이션 실행
# 필요 시 스키마 재구성
```

---

## 📞 모니터링 및 유지보수

### Render 모니터링
- 대시보드: https://dashboard.render.com
- 로그 확인: Logs 탭
- 환경 변수 수정: Environment 탭
- 재배포: Manual Deploy

### Netlify 모니터링
- 대시보드: https://app.netlify.com
- 빌드 로그: Deploys 탭
- 환경 변수 수정: Site settings
- 재배포: Trigger new build

### 성능 모니터링 (선택사항)
- Render: Analytics 탭
- Netlify: Analytics 탭
- 외부: Sentry, New Relic 등

---

## 📝 배포 문서

배포 완료 후 README 또는 DEPLOYMENT.md에 다음을 기록하세요:

```markdown
## 배포된 서비스

- **프론트엔드**: https://vibemap.netlify.app
- **백엔드 API**: https://vibemap-backend.onrender.com
- **API 문서**: https://vibemap-backend.onrender.com/docs

## 배포 일시
- 2026-07-16 15:30 UTC

## 배포자
- 이름: [배포 담당자]
```
