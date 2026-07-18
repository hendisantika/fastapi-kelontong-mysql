from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

import models
from database import engine, get_db

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


@router.put("/merchandise/{id}", status_code=status.HTTP_200_OK)
async def update_merchandise(id: int, merchandise: MerchandiseBase, db: db_dependency):
    m = models.Merchandise

    merch = db.query(m).filter(m.id == id).first()

    if merch is None:
        raise HTTPException(status_code=404, detail="Merchandise not found")

    db_merch = m(**merchandise.dict())
    db.query(m).filter(m.id == id).update({
        m.name: db_merch.name,
        m.category_id: db_merch.category_id,
        m.price: db_merch.price,
        m.stock: db_merch.stock
    }, synchronize_session=False)
    db.commit()

    return {"message": "Merchandise updated"}
