from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from routers import vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_posts = [{"title": "xxx title1", "content": "xxx content1", "id": 1}, {"title": "xxx title2", "content": "xxx content2", "id": 2}]

# def find_post(id):
#     for post in my_posts:
#         if post['id'] == id:
#             return post

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)): 
#     posts = db.query(models.Post).all()

#     return {"data": posts}



