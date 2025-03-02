from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import markdown

from backend.app.db.database import get_db
from backend.app.models.post import Post as PostModel
from backend.app.schemas.post import Post, PostCreate, PostUpdate

router = APIRouter()

@router.get("/", response_model=List[Post])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(PostModel).order_by(PostModel.created_at.desc()).offset(skip).limit(limit).all()
    return posts

@router.get("/{slug}", response_model=Post)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.slug == slug).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(PostModel).filter(PostModel.slug == post.slug).first()
    if db_post:
        raise HTTPException(status_code=400, detail="Slug already exists")
    
    new_post = PostModel(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{post_id}", response_model=Post)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_data = post_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    return None

@router.get("/{slug}/html", response_model=dict)
def get_post_html(slug: str, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.slug == slug).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    html_content = markdown.markdown(post.content)
    return {
        "title": post.title,
        "html_content": html_content,
        "created_at": post.created_at
    }