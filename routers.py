from fastapi import APIRouter

import models
from database import engine

router = APIRouter()
models.Base.metadata.create_all(bind=engine)


class MerchandiseBase(BaseModel):
    name: str
    category_id: int
    price: int
    stock: int


db_dependency = Annotated[Session, Depends(get_db)]
