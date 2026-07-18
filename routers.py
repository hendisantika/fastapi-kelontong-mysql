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


@router.post("/merchandises", status_code=status.HTTP_201_CREATED)
async def create_merchandise(merchandise: MerchandiseBase, db: db_dependency):
    db_merch = models.Merchandise(**merchandise.dict())
    db.add(db_merch)
    db.commit()

    return {"message": "New data created"}
