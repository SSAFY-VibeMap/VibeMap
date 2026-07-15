from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.post import service as post_service
from app.post.schemas import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
    DeleteRequest,
    PostCreate,
    PostDetail,
    PostListResponse,
    PostSummary,
    PostUpdate,
)

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("", response_model=PostListResponse)
def list_posts(
    keyword: str | None = None,
    region: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PostListResponse:
    return post_service.list_posts(db, keyword=keyword, region=region, page=page, limit=limit)


@router.get("/{post_id}", response_model=PostDetail)
def get_post(post_id: int, db: Session = Depends(get_db)) -> PostDetail:
    return post_service.get_post_detail(db, post_id)


@router.post("", response_model=PostSummary, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)) -> PostSummary:
    return post_service.create_post(db, payload)


@router.put("/{post_id}", response_model=PostSummary)
def update_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)) -> PostSummary:
    return post_service.update_post(db, post_id, payload)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, payload: DeleteRequest, db: Session = Depends(get_db)) -> Response:
    post_service.delete_post(db, post_id, payload.password)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
) -> CommentResponse:
    return post_service.create_comment(db, post_id, payload)


@router.put("/{post_id}/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    post_id: int,
    comment_id: int,
    payload: CommentUpdate,
    db: Session = Depends(get_db),
) -> CommentResponse:
    return post_service.update_comment(db, post_id, comment_id, payload)


@router.delete("/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    post_id: int,
    comment_id: int,
    payload: DeleteRequest,
    db: Session = Depends(get_db),
) -> Response:
    post_service.delete_comment(db, post_id, comment_id, payload.password)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
