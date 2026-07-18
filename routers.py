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


@router.get("/merchandise", status_code=status.HTTP_200_OK)
async def get_merchandises(db: db_dependency):
    merchs = db.query(models.Merchandise).all()
    return merchs


@router.get("/merchandise/{id}", status_code=status.HTTP_200_OK)
async def get_merchandise(id: int, db: db_dependency):
    merch = db.query(models.Merchandise).filter(models.Merchandise.id == id).first()

    if merch is None:
        raise HTTPException(status_code=404, detail="Merchandise not found")

    return merch


@router.get("/merchandise/search/", status_code=status.HTTP_200_OK)
async def get_merchandise_by_search(db: db_dependency, name: str = Query(default=None),
                                    category: int = Query(default=None)):
    m = models.Merchandise

    merchs = db.query(m).filter(
        or_(
            m.name.like(f"%{name}%"),
            m.category_id == category,
        )
    ).all()

    return merchs


@router.delete("/merchandise/{id}", status_code=status.HTTP_200_OK)
async def delete_merchandise(id: int, db: db_dependency):
    merch = db.query(models.Merchandise).filter(models.Merchandise.id == id).first()

    if merch is None:
        raise HTTPException(status_code=404, detail="Merchandise not found")

    db.delete(merch)
    db.commit()

    return {"message": "Merchandise deleted"}
