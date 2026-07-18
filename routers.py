from fastapi import APIRouter

import models
from database import engine

router = APIRouter()
models.Base.metadata.create_all(bind=engine)
