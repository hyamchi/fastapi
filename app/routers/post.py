from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from app import oauth2
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])



@router.get("/", response_model=List[schemas.PostOut])

def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #results = cursor.execute(""" select * from posts """)
    ##posts = cursor.fetchall()
    #column_names = [column[0] for column in cursor.description]
    #posts = [dict(zip(column_names, row)) for row in results]
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).order_by(models.Post.id).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id, models.Post.title, models.Post.content, models.Post.published, models.Post.created_at, models.Post.owner_id).filter(models.Post.title.contains(search)).order_by(models.Post.id).limit(limit).offset(skip).all()
    print(posts)
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""insert into posts (title, content, published) values (?, ?, ?)""", (post.title, post.content, post.published))
    # cursor.commit()

    print (current_user)

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # result = cursor.execute("""select * from posts where id = ?""", (id))
    # column_names = [column[0] for column in cursor.description]
    # post = [dict(zip(column_names, row)) for row in result]

    print (current_user)

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id, models.Post.title, models.Post.content, models.Post.published, models.Post.created_at, models.Post.owner_id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with {id} was not found")
        
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""delete from posts where id = ?""", (id))

    # if cursor.rowcount == 0:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"post with {id} was not found")

    # cursor.commit()

    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to perform requested action")

    db.delete(post)
    db.commit()

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""update posts set title = ?, content = ?, published = ? where id = ?""", (post.title, post.content, post.published, id))

    # if cursor.rowcount == 0:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"post with id {id} was not found")

    # cursor.commit()

    # return {"data": "updated was successful"}
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()

    if old_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} was not found")
    
    if old_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()