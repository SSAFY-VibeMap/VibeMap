# VibeMap API 명세서

> FastAPI 기반 REST API 상세 문서

---

## 📊 데이터베이스 스키마

### SQLite 테이블 구조

#### `posts` 테이블 - 게시글
```sql
CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  password VARCHAR(255) NOT NULL,  -- 평문 저장 (교육용)
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  region VARCHAR(50) DEFAULT 'seoul'
);
```

**칼럼 설명**
| 칼럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | 게시글 고유 ID (자동증가) |
| title | VARCHAR(255) | 게시글 제목 |
| content | TEXT | 게시글 내용 |
| password | VARCHAR(255) | 수정/삭제 비밀번호 (평문) |
| created_at | DATETIME | 작성 일시 |
| updated_at | DATETIME | 수정 일시 |
| region | VARCHAR(50) | 지역 (기본값: seoul) |

---

#### `comments` 테이블 - 댓글
```sql
CREATE TABLE comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER NOT NULL,
  content TEXT NOT NULL,
  password VARCHAR(255) NOT NULL,  -- 평문 저장 (교육용)
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);
```

**칼럼 설명**
| 칼럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | 댓글 고유 ID (자동증가) |
| post_id | INTEGER | 게시글 ID (외래키) |
| content | TEXT | 댓글 내용 |
| password | VARCHAR(255) | 수정/삭제 비밀번호 (평문) |
| created_at | DATETIME | 작성 일시 |
| updated_at | DATETIME | 수정 일시 |

---

#### `events` 테이블 - 행사/축제
```sql
CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  date_start DATETIME NOT NULL,
  date_end DATETIME NOT NULL,
  location VARCHAR(255),
  latitude FLOAT,
  longitude FLOAT,
  category VARCHAR(50),  -- '축제', '전시', '공연' 등
  region VARCHAR(50) DEFAULT 'seoul',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**칼럼 설명**
| 칼럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | 행사 고유 ID (자동증가) |
| title | VARCHAR(255) | 행사명 |
| description | TEXT | 행사 설명 |
| date_start | DATETIME | 시작 일시 |
| date_end | DATETIME | 종료 일시 |
| location | VARCHAR(255) | 장소 |
| latitude | FLOAT | 위도 |
| longitude | FLOAT | 경도 |
| category | VARCHAR(50) | 카테고리 (축제, 전시, 공연 등) |
| region | VARCHAR(50) | 지역 (기본값: seoul) |
| created_at | DATETIME | 생성 일시 |

---

## 📚 API 엔드포인트

### Base URL
```
개발: http://localhost:8000
배포: https://vibemap-backend.onrender.com
```

---

## 1️⃣ 게시글 API (`/api/posts`)

### 1-1. 게시글 목록 조회
```
GET /api/posts
```

**Query Parameters**
| 매개변수 | 타입 | 필수 | 설명 |
|---------|------|:----:|------|
| page | int | ❌ | 페이지 번호 (기본값: 1) |
| limit | int | ❌ | 페이지당 개수 (기본값: 10) |
| region | str | ❌ | 지역 필터 (기본값: seoul) |

**Response (200 OK)**
```json
{
  "data": [
    {
      "id": 1,
      "title": "강남역 근처 맛있는 한식당",
      "content": "최근에 방문한 음식점이...",
      "region": "seoul",
      "created_at": "2026-07-14T10:30:00",
      "updated_at": "2026-07-14T10:30:00"
    },
    {
      "id": 2,
      "title": "강남역 근처 맛있는 한식당 2",
      "content": "정말 좋은 음식점입니다...",
      "region": "seoul",
      "created_at": "2026-07-14T11:00:00",
      "updated_at": "2026-07-14T11:00:00"
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 10
}
```

**cURL 예시**
```bash
curl "http://localhost:8000/api/posts?page=1&limit=10&region=seoul"
```

---

### 1-2. 게시글 상세 조회
```
GET /api/posts/{id}
```

**Path Parameters**
| 매개변수 | 타입 | 설명 |
|---------|------|------|
| id | int | 게시글 ID |

**Response (200 OK)**
```json
{
  "id": 1,
  "title": "강남역 근처 맛있는 한식당",
  "content": "최근에 방문한 음식점이...",
  "region": "seoul",
  "created_at": "2026-07-14T10:30:00",
  "updated_at": "2026-07-14T10:30:00",
  "comments": [
    {
      "id": 1,
      "content": "좋은 정보 감사합니다!",
      "created_at": "2026-07-14T11:00:00",
      "updated_at": "2026-07-14T11:00:00"
    }
  ]
}
```

**Response (404 Not Found)**
```json
{
  "detail": "Post not found"
}
```

**cURL 예시**
```bash
curl "http://localhost:8000/api/posts/1"
```

---

### 1-3. 게시글 작성
```
POST /api/posts
```

**Request Body**
```json
{
  "title": "강남역 근처 맛있는 한식당",
  "content": "최근에 방문한 음식점이...",
  "password": "1234",
  "region": "seoul"
}
```

**Request Schema (Pydantic)**
| 필드 | 타입 | 필수 | 설명 |
|------|------|:----:|------|
| title | str | ✅ | 제목 (1-255자) |
| content | str | ✅ | 내용 |
| password | str | ✅ | 수정/삭제 비밀번호 |
| region | str | ❌ | 지역 (기본값: seoul) |

**Response (201 Created)**
```json
{
  "id": 1,
  "title": "강남역 근처 맛있는 한식당",
  "content": "최근에 방문한 음식점이...",
  "region": "seoul",
  "created_at": "2026-07-14T10:30:00"
}
```

**cURL 예시**
```bash
curl -X POST "http://localhost:8000/api/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "강남역 근처 맛있는 한식당",
    "content": "최근에 방문한 음식점이...",
    "password": "1234",
    "region": "seoul"
  }'
```

---

### 1-4. 게시글 수정
```
PUT /api/posts/{id}
```

**Path Parameters**
| 매개변수 | 타입 | 설명 |
|---------|------|------|
| id | int | 게시글 ID |

**Request Body**
```json
{
  "title": "강남역 근처 맛있는 한식당 (수정)",
  "content": "방문 후 감상...",
  "password": "1234"
}
```

**Response (200 OK)**
```json
{
  "id": 1,
  "title": "강남역 근처 맛있는 한식당 (수정)",
  "content": "방문 후 감상...",
  "updated_at": "2026-07-14T12:00:00"
}
```

**Response (401 Unauthorized) - 비밀번호 불일치**
```json
{
  "detail": "Invalid password"
}
```

**Response (404 Not Found)**
```json
{
  "detail": "Post not found"
}
```

**cURL 예시**
```bash
curl -X PUT "http://localhost:8000/api/posts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "강남역 근처 맛있는 한식당 (수정)",
    "content": "방문 후 감상...",
    "password": "1234"
  }'
```

---

### 1-5. 게시글 삭제
```
DELETE /api/posts/{id}
```

**Path Parameters**
| 매개변수 | 타입 | 설명 |
|---------|------|------|
| id | int | 게시글 ID |

**Request Body**
```json
{
  "password": "1234"
}
```

**Response (204 No Content)**
```
(응답 본문 없음)
```

**Response (401 Unauthorized) - 비밀번호 불일치**
```json
{
  "detail": "Invalid password"
}
```

**Response (404 Not Found)**
```json
{
  "detail": "Post not found"
}
```

**cURL 예시**
```bash
curl -X DELETE "http://localhost:8000/api/posts/1" \
  -H "Content-Type: application/json" \
  -d '{"password": "1234"}'
```

---

## 2️⃣ 댓글 API (`/api/posts/{post_id}/comments`)

### 2-1. 댓글 작성
```
POST /api/posts/{post_id}/comments
```

**Path Parameters**
| 매개변수 | 타입 | 설명 |
|---------|------|------|
| post_id | int | 게시글 ID |

**Request Body**
```json
{
  "content": "좋은 정보 감사합니다!",
  "password": "5678"
}
```

**Response (201 Created)**
```json
{
  "id": 1,
  "post_id": 1,
  "content": "좋은 정보 감사합니다!",
  "created_at": "2026-07-14T11:00:00"
}
```

**cURL 예시**
```bash
curl -X POST "http://localhost:8000/api/posts/1/comments" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "좋은 정보 감사합니다!",
    "password": "5678"
  }'
```

---

### 2-2. 댓글 수정
```
PUT /api/posts/{post_id}/comments/{comment_id}
```

**Path Parameters**
| 매개변수 | 타입 | 설명 |
|---------|------|------|
| post_id | int | 게시글 ID |
| comment_id | int | 댓글 ID |

**Request Body**
```json
{
  "content": "정말 좋은 정보네요!",
  "password": "5678"
}
```

**Response (200 OK)**
```json
{
  "id": 1,
  "post_id": 1,
  "content": "정말 좋은 정보네요!",
  "updated_at": "2026-07-14T11:30:00"
}
```

**cURL 예시**
```bash
curl -X PUT "http://localhost:8000/api/posts/1/comments/1" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "정말 좋은 정보네요!",
    "password": "5678"
  }'
```

---

### 2-3. 댓글 삭제
```
DELETE /api/posts/{post_id}/comments/{comment_id}
```

**Path Parameters**
| 매개변수 | 타입 | 설명 |
|---------|------|------|
| post_id | int | 게시글 ID |
| comment_id | int | 댓글 ID |

**Request Body**
```json
{
  "password": "5678"
}
```

**Response (204 No Content)**
```
(응답 본문 없음)
```

**cURL 예시**
```bash
curl -X DELETE "http://localhost:8000/api/posts/1/comments/1" \
  -H "Content-Type: application/json" \
  -d '{"password": "5678"}'
```

---

## 3️⃣ 행사 API (`/api/events`)

### 3-1. 행사 목록 조회
```
GET /api/events
```

**Query Parameters**
| 매개변수 | 타입 | 필수 | 설명 |
|---------|------|:----:|------|
| region | str | ❌ | 지역 필터 (기본값: seoul) |
| category | str | ❌ | 카테고리 필터 (축제, 전시, 공연 등) |
| page | int | ❌ | 페이지 번호 (기본값: 1) |
| limit | int | ❌ | 페이지당 개수 (기본값: 10) |

**Response (200 OK)**
```json
{
  "data": [
    {
      "id": 1,
      "title": "강남 음식 축제",
      "description": "지역 음식 문화를 체험할 수 있는 축제입니다.",
      "date_start": "2026-07-20T10:00:00",
      "date_end": "2026-07-22T18:00:00",
      "location": "강남역 광장",
      "latitude": 37.4979,
      "longitude": 127.0276,
      "category": "축제",
      "region": "seoul"
    },
    {
      "id": 2,
      "title": "서울 현대 미술 전시",
      "description": "현대 미술 작가들의 작품 전시",
      "date_start": "2026-07-15T09:00:00",
      "date_end": "2026-08-31T18:00:00",
      "location": "서울 시립미술관",
      "latitude": 37.5505,
      "longitude": 126.9212,
      "category": "전시",
      "region": "seoul"
    }
  ],
  "total": 5,
  "page": 1,
  "limit": 10
}
```

**cURL 예시**
```bash
curl "http://localhost:8000/api/events?region=seoul&category=축제&page=1"
```

---

### 3-2. 행사 상세 조회
```
GET /api/events/{id}
```

**Path Parameters**
| 매개변수 | 타입 | 설명 |
|---------|------|------|
| id | int | 행사 ID |

**Response (200 OK)**
```json
{
  "id": 1,
  "title": "강남 음식 축제",
  "description": "지역 음식 문화를 체험할 수 있는 축제입니다.",
  "date_start": "2026-07-20T10:00:00",
  "date_end": "2026-07-22T18:00:00",
  "location": "강남역 광장",
  "latitude": 37.4979,
  "longitude": 127.0276,
  "category": "축제",
  "region": "seoul"
}
```

**Response (404 Not Found)**
```json
{
  "detail": "Event not found"
}
```

**cURL 예시**
```bash
curl "http://localhost:8000/api/events/1"
```

---

## 4️⃣ 챗봇 API ⭐ (`/api/chat`) - 핵심 기능

### 챗봇 메시지 처리
```
POST /api/chat
```

**Request Body**
```json
{
  "message": "강남역 근처 한식당 추천해줘",
  "region": "강남"
}
```

**Request Schema (Pydantic)**
| 필드 | 타입 | 필수 | 설명 |
|------|------|:----:|------|
| message | str | ✅ | 사용자 질문/요청 |
| region | str | ❌ | 지역 정보 |

**Response (200 OK)**
```json
{
  "reply": "강남역 근처의 추천 한식당을 소개합니다. 최근 게시글에서 가장 인기 있는 음식점들은 다음과 같습니다...",
  "intent": "restaurant_recommendation",
  "data": {
    "restaurants": [
      {
        "name": "음식점 A",
        "address": "서울시 강남구 강남대로 98길 10",
        "rating": 4.5,
        "reviews": 24
      },
      {
        "name": "음식점 B",
        "address": "서울시 강남구 테헤란로 10",
        "rating": 4.3,
        "reviews": 18
      }
    ]
  }
}
```

**Intent 분류 (의도 인식)**
| Intent | 설명 | 예시 |
|--------|------|------|
| `restaurant_recommendation` | 음식점 추천 | "강남역 근처 한식당 추천해줘" |
| `event_search` | 축제/행사 검색 | "7월 행사가 뭐가 있어?" |
| `tourist_info` | 관광지 정보 | "강남의 관광지는?" |
| `community_search` | 커뮤니티 게시글 검색 | "맛있는 음식점에 대한 글 찾아줘" |
| `general` | 일반 질문 | "강남에 대해 알려줘" |

**응답 로직**
1. OpenAI API 또는 규칙 기반으로 사용자 의도 분류
2. 의도별로 DB 검색 수행 (게시글, 행사, 음식점 데이터)
3. 자연스러운 문장으로 응답 생성 + 관련 데이터 반환

**Response (400 Bad Request) - 잘못된 입력**
```json
{
  "detail": "Message field is required"
}
```

**cURL 예시**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "강남역 근처 한식당 추천해줘",
    "region": "강남"
  }'
```

---

## 📋 HTTP 상태 코드

| 상태 코드 | 설명 | 사용 예시 |
|----------|------|----------|
| 200 | OK | 조회, 수정 성공 |
| 201 | Created | 생성 성공 |
| 204 | No Content | 삭제 성공 |
| 400 | Bad Request | 잘못된 요청 형식 |
| 401 | Unauthorized | 비밀번호 불일치 |
| 404 | Not Found | 리소스 없음 |
| 500 | Internal Server Error | 서버 오류 |

---

## 🧪 API 테스트

### Swagger UI (자동 생성)
```
개발: http://localhost:8000/docs
배포: https://vibemap-backend.onrender.com/docs
```

FastAPI에서 자동으로 생성되는 Swagger UI에서 모든 API를 테스트할 수 있습니다.

### ReDoc (API 문서)
```
개발: http://localhost:8000/redoc
배포: https://vibemap-backend.onrender.com/redoc
```

---

## 🔄 CORS 설정

프론트엔드와 백엔드가 다른 도메인에서 실행될 때 CORS 설정이 필요합니다.

**FastAPI 예시**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # 개발
        "https://vibemap.netlify.app"  # 배포
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🚨 에러 처리

### 일반 에러 응답 형식
```json
{
  "detail": "에러 메시지"
}
```

### 유효성 검사 에러 (422)
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 📱 API 클라이언트 예시 (Vue.js)

```javascript
// services/apiClient.js
import axios from 'axios';

const API_BASE_URL = process.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default apiClient;
```

```javascript
// services/postService.js
import apiClient from './apiClient';

export const postService = {
  // 게시글 목록
  getPosts: (page = 1, limit = 10, region = 'seoul') =>
    apiClient.get('/api/posts', {
      params: { page, limit, region }
    }),

  // 게시글 상세
  getPost: (id) =>
    apiClient.get(`/api/posts/${id}`),

  // 게시글 작성
  createPost: (data) =>
    apiClient.post('/api/posts', data),

  // 게시글 수정
  updatePost: (id, data) =>
    apiClient.put(`/api/posts/${id}`, data),

  // 게시글 삭제
  deletePost: (id, password) =>
    apiClient.delete(`/api/posts/${id}`, {
      data: { password }
    })
};
```

```javascript
// services/chatService.js
import apiClient from './apiClient';

export const chatService = {
  // 챗봇 메시지
  sendMessage: (message, region) =>
    apiClient.post('/api/chat', {
      message,
      region
    })
};
```

---

## 📞 API 지원

API 사용 중 문제가 발생하면:
1. [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
2. Swagger UI에서 "Try it out" 버튼으로 직접 테스트
3. GitHub Issues에 문의
