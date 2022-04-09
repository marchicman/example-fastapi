from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from starlette.responses import Response

from sqlalchemy import func
from app import oauth2
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts"
)

@router.get('/', response_model=List[schemas.PostOut])
#@router.get('/')
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit : int = 10, skip : int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts) models.Post.owner_id == current_user.id, 
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # .all()
    # per SQLAlchemy i join sono  INNER
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # senza .all() stampo la query che fa
   # print(results)

    return results

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(payload: dict = Body(...)):
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # return {"new_post": f"title {payload['title']} content: {payload['content']}"}
    # return {"data": post_dict}
    # cursor.execute(""" INSERT INTO posts (title, content, published) 
    #                    VALUES(%s, %s, %s) RETURNING * """, 
    #                    (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # ** fa l'unpack del dictionary creato dal metodo .dict() e crea una situazione come la riga sopra
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # per recuperare il campo id

    return new_post


@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # post = find_post(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    print(current_user)
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
   
    return post

@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # index = find_post_index(id)
    # if deleted_post == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # my_posts.pop(index)
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, upd_post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                     (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # index = find_post_index(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
   
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    # my_posts.pop(index)

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    post_query.update(upd_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()