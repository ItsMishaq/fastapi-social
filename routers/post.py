from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models, schemas
from typing import List, Optional
import oauth2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#path function decorator for showing existing posts
# {{URL}}/posts?limit=4&skip=2&search=deen%20mn   this shows the specs used in url as limit, search and skip parameters
@router.get("/", response_model=List[schemas.PostOut])  #response_model="List[schemas.Post]" List is added coz we are returning multiple posts instead of one.
def get_posts(db: Session= Depends(get_db), limit: int = 10, skip: int = 0, search: Optional [str] = ""):
    # posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    # print(posts)
    return  posts

#path function decorator for adding new posts to existing dictionary
@router.post("/", status_code=201, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published)VALUES(%s, %s, %s) RETURNING* """,(post.title, post.content, post.published))
   
    # print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    


#path function for single post retrievel
@router.get("/{id}", response_model=schemas.PostOut) 
def get_post(id: int, db: Session= Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts WHERE id= %s""",(str(id)))
    # Post = cursor.fetchone()
    # post=db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # print(post)

    if not post:
        status_code=status.HTTP_404_NOT_FOUND
        return{"Message": f"post with {id} was not found"}
    # print(post)
    return post



#deleting a post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING* """,(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return {'message':'post has been successfully deleted'}
    

#Updating a post
@router.put("/{id}", status_code=202, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING* """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id== id)
    post = post_query.first()
  
    if post ==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
              detail=f"the post with {id} is not available")
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()

    return post_query.first()

    