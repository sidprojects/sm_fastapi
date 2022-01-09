from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import schemas, models, oath2


router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

'''
Managing posts code starts here
'''
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user = Depends(oath2.get_current_user), 
              limit:int = 10, skip:int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    # Add .filter(models.Post.owner_id == current_user.id) in the query to limit post visibility
    # to their own users.
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts_query = db.query(models.Post, func.count(models.Vote.post_id).label("num_votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    
    results = posts_query.all()
    
    return results

@router.get("/{id}", response_model=schemas.PostOut)
def get_one_post(id: int, response:Response, db: Session = Depends(get_db),
                 current_user = Depends(oath2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("num_votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"requested post with id {id} was not found")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db),
                 current_user = Depends(oath2.get_current_user)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()    
    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user = Depends(oath2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # del_post = cursor.fetchone()
    
    del_query = db.query(models.Post).filter(models.Post.id == id)
    del_post = del_query.first()
    
    if del_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} is not found")
        
    if del_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform required action")

    # conn.commit()
    del_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post:schemas.CreatePost, db: Session = Depends(get_db),
                current_user = Depends(oath2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    
    update_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = update_query.first()
    
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} is not found")
    
    if update_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform required action")
    
    update_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return update_query.first()
    
