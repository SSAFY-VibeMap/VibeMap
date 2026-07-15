from __future__ import annotations

from math import ceil

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from backend.app.post.models import Comment, Post
from backend.app.post.schemas import (
    CommentCreate,
    CommentUpdate,
    PostCreate,
    PostListResponse,
    PostSummary,
    PostUpdate,
)


def verify_password(saved_password: str, request_password: str) -> None:
    if saved_password != request_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")


def get_post_or_404(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


def get_comment_or_404(db: Session, post_id: int, comment_id: int) -> Comment:
    comment = db.get(Comment, comment_id)
    if comment is None or comment.post_id != post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


def list_posts(
    db: Session,
    keyword: str | None = None,
    region: str | None = None,
    page: int = 1,
    limit: int = 10,
) -> PostListResponse:
    page = max(page, 1)
    limit = min(max(limit, 1), 100)

    query = select(Post)
    count_query = select(Post)

    filters = []
    if keyword:
        pattern = f"%{keyword}%"
        filters.append(or_(Post.title.ilike(pattern), Post.content.ilike(pattern)))
    if region:
        filters.append(Post.region == region)

    for condition in filters:
        query = query.where(condition)
        count_query = count_query.where(condition)

    total = len(db.scalars(count_query).all())
    posts = db.scalars(query.order_by(Post.created_at.desc()).offset((page - 1) * limit).limit(limit)).all()
    total_page = ceil(total / limit) if total else 0

    return PostListResponse(
        data=[PostSummary.model_validate(post) for post in posts],
        total_page=total_page,
        page=page,
        limit=limit,
    )


def get_post_detail(db: Session, post_id: int) -> Post:
    post = db.scalars(select(Post).options(selectinload(Post.comments)).where(Post.id == post_id)).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


def create_post(db: Session, payload: PostCreate) -> Post:
    post = Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(db: Session, post_id: int, payload: PostUpdate) -> Post:
    post = get_post_or_404(db, post_id)
    verify_password(post.password, payload.password)

    update_data = payload.model_dump(exclude={"password"})
    for field, value in update_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int, password: str) -> None:
    post = get_post_or_404(db, post_id)
    verify_password(post.password, password)
    db.delete(post)
    db.commit()


def create_comment(db: Session, post_id: int, payload: CommentCreate) -> Comment:
    get_post_or_404(db, post_id)
    comment = Comment(post_id=post_id, **payload.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def update_comment(db: Session, post_id: int, comment_id: int, payload: CommentUpdate) -> Comment:
    comment = get_comment_or_404(db, post_id, comment_id)
    verify_password(comment.password, payload.password)
    comment.content = payload.content
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, post_id: int, comment_id: int, password: str) -> None:
    comment = get_comment_or_404(db, post_id, comment_id)
    verify_password(comment.password, password)
    db.delete(comment)
    db.commit()
