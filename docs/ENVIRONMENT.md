# VibeMap 환경 변수 설정 가이드

> 개발, 스테이징, 배포 환경별 환경 변수 설정

---

## 📝 개발 환경 설정 (Local)

### 백엔드 `.env.example`
```env
# ===== FastAPI 설정 =====
API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=dev-secret-key-change-in-production

# ===== 데이터베이스 =====
DATABASE_URL=sqlite:///./vibemap.db

# ===== OpenAI API =====
OPENAI_API_KEY=sk-...your-openai-key...
OPENAI_MODEL=gpt-4o-mini

# ===== 카카오 지도 API =====
KAKAO_MAP_API_KEY=...your-kakao-map-key...

# ===== CORS 설정 =====
FRONTEND_URL=http://localhost:5173

# ===== 로깅 =====
LOG_LEVEL=DEBUG
```

### 프론트엔드 `.env.example`
```env
# ===== API 설정 =====
VITE_API_BASE_URL=http://localhost:8000

# ===== 카카오 지도 =====
VITE_KAKAO_MAP_API_KEY=...your-kakao-map-key...

# ===== 환경 =====
VITE_ENV=development
```

---

## 🔧 환경 변수 설정 단계별 가이드

### Step 1: `.env.example` 파일 복사

**백엔드**
```bash
cd chatbot
cp .env.example .env
```

**프론트엔드**
```bash
cd frontend
cp .env.example .env
```

---

### Step 2: API 키 등록

#### OpenAI API 키 획득
1. [OpenAI Platform](https://platform.openai.com) 접속
2. 로그인 및 API 키 생성
3. 백엔드 `.env` 파일에 등록

```env
OPENAI_API_KEY=sk-proj-...
```

#### Kakao Map API 키 획득
1. [Kakao Developers](https://developers.kakao.com) 접속
2. 애플리케이션 등록
3. Maps API 활성화
4. 프론트/백엔드 `.env` 파일에 등록

**백엔드**
```env
KAKAO_MAP_API_KEY=...
```

**프론트엔드**
```env
VITE_KAKAO_MAP_API_KEY=...
```

---

### Step 3: 데이터베이스 설정 검증

```bash
cd chatbot

# 가상환경 활성화 후
python -c "from backend.app.database import engine; from backend.app.models import *; engine.create_all()"
```

---

## 🚀 배포 환경 설정

### Render (백엔드)

#### 환경 변수 설정 방법
1. Render 대시보드 → 서비스 선택
2. "Environment" 탭 → "Add Environment Variable"
3. 다음 변수들 추가

```
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
NAVER_MAP_API_KEY=...
DATABASE_URL=sqlite:///./vibemap.db
FRONTEND_URL=https://vibemap.netlify.app
API_SECRET_KEY=prod-secret-key-change-this
LOG_LEVEL=INFO
```

#### 주의사항
- 모든 민감정보는 반드시 환경 변수로 등록
- `DATABASE_URL` 경로는 Render 권한 있는 경로 사용
- `FRONTEND_URL`은 실제 배포 도메인으로 설정
- 개발 환경과 다른 강력한 `API_SECRET_KEY` 사용

---

### Netlify (프론트엔드)

#### 환경 변수 설정 방법
1. Netlify 대시보드 → Site settings
2. "Build & deploy" → "Environment"
3. "Edit variables" → 변수 추가

```
VITE_API_BASE_URL=https://vibemap-backend.onrender.com
VITE_KAKAO_MAP_API_KEY=...
VITE_ENV=production
```

#### 주의사항
- `VITE_API_BASE_URL`은 배포된 백엔드 URL 사용
- Vite 변수는 반드시 `VITE_` 접두사 사용
- 프론트엔드에서 노출되는 변수만 등록

---

## 🔒 보안 규칙

### ✅ 필수 따라야 할 규칙
1. ✅ `.env` 파일은 절대 Git에 올리지 않기
   ```bash
   # .gitignore에 추가
   .env
   .env.local
   *.env
   ```

2. ✅ `.env.example`로 필요한 변수 명시
   ```bash
   # 실제 값은 저장 안 함
   OPENAI_API_KEY=sk-...your-key...
   ```

3. ✅ 모든 API 키, DB 정보는 환경 변수로 관리
   ```python
   # ❌ 잘못된 예
   OPENAI_API_KEY = "sk-..."
   
   # ✅ 올바른 예
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   ```

4. ✅ 배포 전 환경 변수 누출 검사
   ```bash
   # 소스 코드에서 민감정보 검색
   git grep -i "sk-proj"
   git grep -i "api.key"
   ```

5. ✅ 개발/배포 환경 변수 분리
   - 개발: `http://localhost:8000`
   - 배포: `https://vibemap-backend.onrender.com`

---

## 📋 환경 변수 체크리스트

### 개발 환경 (.env 로컬 파일)
- [ ] `DATABASE_URL` 설정 (SQLite)
- [ ] `OPENAI_API_KEY` 설정
- [ ] `KAKAO_MAP_API_KEY` 설정
- [ ] `FRONTEND_URL` 설정 (로컬: http://localhost:5173)
- [ ] `API_SECRET_KEY` 설정
- [ ] `.gitignore`에 `.env` 포함 확인

### 배포 환경 (Render/Netlify)
- [ ] **Render**: 모든 환경 변수 설정 완료
- [ ] **Netlify**: 모든 환경 변수 설정 완료
- [ ] 환경 변수 값 정확성 검증
- [ ] `.env` 파일 저장소 누출 없음 확인

---

## 🧪 환경 변수 검증

### 백엔드 검증

```bash
cd chatbot

# 1. .env 파일 로드 확인
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('API KEY:', os.getenv('OPENAI_API_KEY')[:10]+'***')"

# 2. DB 연결 확인
python -c "from backend.app.database import engine; engine.connect(); print('DB Connected')"

# 3. API 서버 시작
uvicorn app.main:app --reload
```

### 프론트엔드 검증

```bash
cd frontend

# 1. 환경 변수 확인
npm run dev

# 2. 브라우저 개발자 도구 → Console 확인
# import.meta.env.VITE_API_BASE_URL 확인
```

---

## 🔄 환경 변수 업데이트

### 로컬 개발 중
```bash
# .env 파일 수정 후 서버 재시작
# (핫 리로드되지 않으므로 수동 재시작 필요)
```

### 배포된 환경
```bash
# 1. Render/Netlify 대시보드에서 환경 변수 수정
# 2. 자동으로 재배포 트리거됨
# 3. 배포 완료 후 변경사항 확인
```

---

## ⚠️ 일반적인 실수

### 실수 1: 민감정보 하드코딩
```python
# ❌ 잘못된 예
OPENAI_API_KEY = "sk-proj-abc123..."  # Git에 올라감!

# ✅ 올바른 예
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

### 실수 2: `.env` 파일을 Git에 올림
```bash
# ❌ 잘못된 예
git add .env  # 절대 금지!

# ✅ 올바른 예
git add .env.example  # 템플릿만 올림
```

### 실수 3: 프론트엔드에서 민감정보 노출
```javascript
// ❌ 잘못된 예 - 클라이언트에 노출됨
const OPENAI_KEY = import.meta.env.VITE_OPENAI_API_KEY;

// ✅ 올바른 예 - 백엔드에서만 사용
// 백엔드 .env에만 저장
```

### 실수 4: 배포 환경의 환경 변수 누락
```bash
# ❌ 배포 후 API 오류 발생
# → 환경 변수가 설정되지 않음

# ✅ 배포 전 체크리스트 확인
# → Render/Netlify 대시보드에서 모든 변수 확인
```

---

## 📞 문제 해결

### "OPENAI_API_KEY not found" 에러
```bash
# 1. .env 파일이 있는지 확인
ls -la chatbot/.env

# 2. 환경 변수 로드 코드 확인
# dotenv import 및 load_dotenv() 호출 확인

# 3. API 키 값 확인
cat chatbot/.env | grep OPENAI
```

### "Database connection failed" 에러
```bash
# 1. DATABASE_URL 확인
echo $DATABASE_URL

# 2. SQLite 파일 경로 확인
ls -la database/

# 3. 권한 확인
chmod 755 database/
```

### 배포 후 API 호출 실패
```bash
# 1. CORS 설정 확인
# FRONTEND_URL이 정확히 설정되었는가?

# 2. 환경 변수 반영 확인
# Render/Netlify에서 환경 변수 업데이트 후 재배포?

# 3. API 엔드포인트 확인
curl https://vibemap-backend.onrender.com/docs
```
