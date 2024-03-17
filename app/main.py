from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from . import models
from .database import engine

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
