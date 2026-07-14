# VibeMap API 명세서

> FastAPI 기반 REST API 상세 문서

---

## 📊 데이터 구조

### 1) 축제 데이터

축제 정보는 DB에 저장하지 않고 JSON 파일을 직접 읽어 사용합니다.

- `프로젝트자료/data/서울/서울_축제공연행사.json`
- `프로젝트자료/data/부산/부산_축제공연행사.json`
- `프로젝트자료/data/광주_전라권/광주_전라권_축제공연행사.json`
- `프로젝트자료/data/대전_충청권/대전_충청권_축제공연행사.json`
- `프로젝트자료/data/구미_경북권/구미_경북권_축제공연행사.json`

축제 API는 위 JSON 원본을 읽어서 응답합니다.

### 2) SQLite 테이블 구조

#### `posts` 테이블 - 게시물

게시물은 사용자가 익명으로 작성할 수 있습니다.

```sql
CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  password VARCHAR(255) NOT NULL,
  region VARCHAR(50) DEFAULT 'seoul',
  content_id VARCHAR(100),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**칼럼 설명**

| 칼럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | 게시물 고유 ID |
| title | VARCHAR(255) | 게시물 제목 |
| content | TEXT | 게시물 내용 |
| password | VARCHAR(255) | 수정/삭제 비밀번호 |
| region | VARCHAR(50) | 지역 코드 |
| content_id | VARCHAR(100) | 연결된 축제 JSON 원본 ID |
| created_at | DATETIME | 작성 일시 |
| updated_at | DATETIME | 수정 일시 |

---

#### `comments` 테이블 - 댓글

```sql
CREATE TABLE comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER NOT NULL,
  content TEXT NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);
```

**칼럼 설명**

| 칼럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | 댓글 고유 ID |
| post_id | INTEGER | 게시물 ID |
| content | TEXT | 댓글 내용 |
| password | VARCHAR(255) | 수정/삭제 비밀번호 |
| created_at | DATETIME | 작성 일시 |
| updated_at | DATETIME | 수정 일시 |

---

## 📌 스키마 참고

- 축제 데이터는 JSON 파일을 직접 읽어 응답합니다.
- `posts` 는 익명 작성 방식입니다. 작성자 정보는 저장하지 않습니다.
- 비밀번호는 게시물과 댓글의 수정/삭제용으로만 사용합니다.
- `content_id` 는 축제 JSON 원본과 게시물을 연결할 때 사용하는 선택 필드입니다.

---

## 📚 API 엔드포인트

### Base URL

```
개발: http://localhost:8000
배포: https://vibemap-backend.onrender.com
```

---

## 1️⃣ 축제 API (`/api/events`)

축제 API는 DB가 아니라 JSON 원본에서 직접 읽습니다.

### 1-1. 축제 목록 조회

```
GET /api/events
```

**Query Parameters**

| 매개변수 | 타입 | 필수 | 설명 |
|---------|------|:----:|------|
| keyword | str | ❌ | 행사명/장소명 검색어 |
| latitude | float | 필수 | 경도/위도 |
| longitude | float | 필수 | 경도/위도 |
| page | int | ❌ | 페이지 번호 |
| limit | int | ❌ | 페이지당 개수 |

**Response (200 OK)**

```json
{
  "data": [
    {
      "id": "125678",
      "title": "한강 불꽃축제",
      "image_url": "https://example.com/festival.jpg",
      "venue_name": "여의도 한강공원",
      "venue_address": "서울 영등포구 여의동로 330",
      "latitude": 37.5281,
      "longitude": 126.9346
    }
  ],
  "total_page": 8,
  "page": 1,
  "limit": 10
}
```

**cURL 예시**

```bash
curl "http://localhost:8000/api/events?region=seoul&category=축제&page=1"
```

---

### 1-2. 축제 상세 조회

```
GET /api/events/{id}
```

**Path Parameters**

| 매개변수 | 타입 | 설명 |
|---------|------|------|
| id | string | 축제 원본 ID |

**Response (200 OK)**

```json
{
  "id": "125678",
  "title": "한강 불꽃축제",
  "image_url": "https://example.com/festival.jpg",
  "venue_name": "여의도 한강공원",
  "venue_address": "서울 영등포구 여의동로 330",
  "latitude": 37.5281,
  "longitude": 126.9346
}
```

**Response (404 Not Found)**

```json
{
  "detail": "Event not found"
}
```

---

## 2️⃣ 게시물 API (`/api/posts`)

게시물은 사용자 익명 작성이 가능합니다.

### 2-1. 게시물 목록 조회

```
GET /api/posts
```

**Query Parameters**

| 매개변수 | 타입 | 필수 | 설명 |
|---------|------|:----:|------|
| keyword | str | ❌ | 제목/내용 검색어 |
| latitude | ✅ | 필수 | 경도/위도 |
| longitude | ✅ | 필수 | 경도/위도 |
| page | int | ❌ | 페이지 번호 |
| limit | int | ❌ | 페이지당 개수 |

**Response (200 OK)**

```json
{
  "data": [
    {
      "id": 1,
      "title": "불꽃축제 같이 볼 사람 모집",
      "content": "여의도에서 함께 볼 분 구합니다.",
      "content_id": "125678",
      "meet_at": "2026-07-14T10:30:00",
      "created_at": "2026-07-14T10:30:00",
      "updated_at": "2026-07-14T10:30:00"
    }
  ],
  "total_page": 5,
  "page": 1,
  "limit": 10
}
```

---

### 2-2. 게시물 상세 조회

```
GET /api/posts/{id}
```

**Response (200 OK)**

```json
{
  "id": 1,
  "title": "불꽃축제 같이 볼 사람 모집",
  "content": "여의도에서 함께 볼 분 구합니다.",
  "content_id": "125678",
  "meet_at": "2026-07-14T10:30:00",
  "created_at": "2026-07-14T10:30:00",
  "updated_at": "2026-07-14T10:30:00",
  "comments": [
    {
      "id": 1,
      "content": "저도 참여하고 싶어요!",
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

---

### 2-3. 게시물 작성

```
POST /api/posts
```

**Request Body**

```json
{
  "title": "불꽃축제 같이 볼 사람 모집",
  "content": "여의도에서 함께 볼 분 구합니다.",
  "password": "1234",
  "content_id": "125678",
  "meet_at": "2026-07-14T10:30:00"
}
```

**Request Schema (Pydantic)**

| 필드 | 타입 | 필수 | 설명 |
|------|------|:----:|------|
| title | str | ✅ | 제목 |
| content | str | ✅ | 내용 |
| password | str | ✅ | 수정/삭제 비밀번호 |
| content_id | str | ❌ | 축제 원본 연결 ID |
| meet_at | str | ✅ | 만남 일정 |

**Response (201 Created)**

```json
{
  "title": "불꽃축제 같이 볼 사람 모집",
  "content": "여의도에서 함께 볼 분 구합니다.",
  "password": "1234",
  "content_id": "125678",
  "meet_at": "2026-07-14T10:30:00"
}
```

---

### 2-4. 게시물 수정

```
PUT /api/posts/{id}
```

**Request Body**

```json
{
  "title": "불꽃축제 같이 볼 사람 모집 (수정)",
  "content": "인원 1명 추가 모집합니다.",
  "password": "1234",
  "meet_at": "2026-07-14T10:30:00"
}
```

**Response (200 OK)**

```json
{
  "id": 1,
  "title": "불꽃축제 같이 볼 사람 모집 (수정)",
  "content": "인원 1명 추가 모집합니다.",
  "updated_at": "2026-07-14T12:00:00",
  "meet_at": "2026-07-14T10:30:00"
}
```

**Response (401 Unauthorized)**

```json
{
  "detail": "Invalid password"
}
```

---

### 2-5. 게시물 삭제

```
DELETE /api/posts/{id}
```

**Request Body**

```json
{
  "password": "1234"
}
```

**Response (204 No Content)**

응답 본문 없음

---

## 3️⃣ 댓글 API (`/api/posts/{post_id}/comments`)

### 3-1. 댓글 작성

```
POST /api/posts/{post_id}/comments
```

**Request Body**

```json
{
  "content": "저도 참여하고 싶어요!",
  "password": "5678"
}
```

**Response (201 Created)**

```json
{
  "id": 1,
  "post_id": 1,
  "content": "저도 참여하고 싶어요!",
  "created_at": "2026-07-14T11:00:00"
}
```

---

### 3-2. 댓글 수정

```
PUT /api/posts/{post_id}/comments/{comment_id}
```

**Request Body**

```json
{
  "content": "참여 가능해요!",
  "password": "5678"
}
```

**Response (200 OK)**

```json
{
  "id": 1,
  "post_id": 1,
  "content": "참여 가능해요!",
  "updated_at": "2026-07-14T11:30:00"
}
```

---

### 3-3. 댓글 삭제

```
DELETE /api/posts/{post_id}/comments/{comment_id}
```

**Request Body**

```json
{
  "password": "5678"
}
```

**Response (204 No Content)**

응답 본문 없음

---

## 4️⃣ 챗봇 API (`/api/chat`)

### 4-1. 챗봇 메시지 처리

```
POST /api/chat
```

**Request Body**

```json
{
  "message": "강남역 근처 불꽃축제 알려줘"
}
```

**Response (200 OK)**

```json
{
  "id": "SADJ123",
  "reply": "강남역 근처의 축제와 관련 게시물을 확인해볼게요."
}
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

## 📱 API 클라이언트 예시

```javascript
// services/apiClient.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = {
  get: async (url, options = {}) => fetch(`${API_BASE_URL}${url}`, { ...options }),
  post: async (url, data, options = {}) => fetch(`${API_BASE_URL}${url}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    body: JSON.stringify(data),
    ...options
  }),
  put: async (url, data, options = {}) => fetch(`${API_BASE_URL}${url}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    body: JSON.stringify(data),
    ...options
  }),
  delete: async (url, options = {}) => fetch(`${API_BASE_URL}${url}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    ...options
  })
};

export default apiClient;
```

```javascript
// services/eventService.js
import apiClient from './apiClient';

export const eventService = {
  getEvents: (page = 1, limit = 10, region = 'seoul', category = '') =>
    apiClient.get('/api/events', {
      params: { page, limit, region, category }
    }),

  getEvent: (id) =>
    apiClient.get(`/api/events/${id}`),

  getEventMarkers: (region = 'seoul', type = 'all') =>
    apiClient.get('/api/events/map', {
      params: { region, type }
    })
};
```

```javascript
// services/postService.js
import apiClient from './apiClient';

export const postService = {
  getPosts: (page = 1, limit = 10, region = 'seoul') =>
    apiClient.get('/api/posts', {
      params: { page, limit, region }
    }),

  getPost: (id) =>
    apiClient.get(`/api/posts/${id}`),

  createPost: (data) =>
    apiClient.post('/api/posts', data),

  updatePost: (id, data) =>
    apiClient.put(`/api/posts/${id}`, data),

  deletePost: (id, password) =>
    apiClient.delete(`/api/posts/${id}`, {
      data: { password }
    })
};
```

```javascript
// services/commentService.js
import apiClient from './apiClient';

export const commentService = {
  createComment: (postId, data) =>
    apiClient.post(`/api/posts/${postId}/comments`, data),

  updateComment: (postId, commentId, data) =>
    apiClient.put(`/api/posts/${postId}/comments/${commentId}`, data),

  deleteComment: (postId, commentId, password) =>
    apiClient.delete(`/api/posts/${postId}/comments/${commentId}`, {
      data: { password }
    })
};
```

```javascript
// services/chatService.js
import apiClient from './apiClient';

export const chatService = {
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
1. FastAPI 공식 문서
2. Swagger UI에서 직접 테스트
3. GitHub Issues에 문의
