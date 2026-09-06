from fastapi import FastAPI

from . import models
from .database import Base, engine
from .routers import course, intro, user

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(intro.router)
app.include_router(course.router)
app.include_router(user.router)
