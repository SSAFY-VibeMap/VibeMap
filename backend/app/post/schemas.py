from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class DeleteRequest(BaseModel):
    password: str = Field(..., min_length=1, max_length=255)


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1, max_length=255)


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1, max_length=255)


class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1, max_length=255)
    content_id: str | None = Field(None, max_length=100)
    meet_at: datetime | None = None


class PostUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1, max_length=255)
    content_id: str | None = Field(None, max_length=100)
    meet_at: datetime | None = None


class PostSummary(BaseModel):
    id: int
    title: str
    content: str
    content_id: str | None = None
    content_title: str | None = None
    content_start_date: str | None = None
    content_end_date: str | None = None
    meet_at: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class PostDetail(PostSummary):
    comments: list[CommentResponse] = []


class PostListResponse(BaseModel):
    data: list[PostSummary]
    total_page: int
    page: int
    limit: int
