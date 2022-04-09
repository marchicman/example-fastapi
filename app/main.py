from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# con alembic non serve che sia sqlalchemy a creare le tabelle
# alembic revision --autogenerate -m "creazione iniziale tabelle"
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_posts = [
#     {"title": "Foo", "content": "There comes my hero", "id": 1},
#     {"title": "Red", "content": "It's my aeroplane", "id": 2}
# ]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_post_index(id):
#     for i,p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
    
@app.get("/")
def root():
    return {"message": "Hello World"}



