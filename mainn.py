from fastapi import FastAPI
from models import Base
from database import engine
from routers import post, user, auth, vote
from config import settings

Base.metadata.create_all(bind=engine)


app = FastAPI()





#purpose of router object is to split of all our path operataion to diff files and then just call them.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
def root():
    pass



    





    