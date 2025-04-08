from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from src.main.bd.config.database import SessionLocal, engine
from src.main.bd.models.cart_models import Base, Product
from src.main.logic.product_logic import ProductLogic
from src.main.controller.dto.product_dto import NewProductDTO, ProductDTO
from sqlalchemy.orm import Session

product_route = APIRouter()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@product_route.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(product: NewProductDTO, db: db_dependency):
    logic = ProductLogic(db)
    try:
        return logic.create_product(product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@product_route.put("/update", status_code=status.HTTP_200_OK)
async def update_product(product: ProductDTO, db: db_dependency):
    logic = ProductLogic(db)
    try:
        updated_product = logic.update_product(product)
        return updated_product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@product_route.delete("/delete/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: db_dependency, mode: str = "soft"):
    logic = ProductLogic(db)
    try:
        if mode == "hard":
            logic.hard_delete_product(product_id)
        else:
            logic.soft_delete_product(product_id)
        return {"detail": f"Product {product_id} deleted ({mode})"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@product_route.get("/all", status_code=status.HTTP_200_OK)
async def get_all_products(db: db_dependency):
    logic = ProductLogic(db)
    try:
        return logic.get_all_products()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@product_route.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: db_dependency):
    logic = ProductLogic(db)
    try:
        return logic.get_product_by_id(product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))