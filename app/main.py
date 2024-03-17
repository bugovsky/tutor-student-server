from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from . import models
from .database import engine
from .routers import user, auth

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)

