from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from src.main.bd.config.database import SessionLocal, engine
from src.main.bd.models.cart_models import Base, CartItem, User
from src.main.auth import get_current_user
from src.main.logic.cart_logic import CartLogic
from src.main.controller.dto.cart_dto import NewCartItemDTO, CartItemDTO
from sqlalchemy.orm import Session

cart_route = APIRouter()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]

@cart_route.post("/create", status_code=status.HTTP_201_CREATED)
async def add_cart_item(cart_item: NewCartItemDTO, db: db_dependency, user_data: user_dependency):
    if not user_data:
        raise HTTPException(status_code=401, detail="User not authenticated")
    print(user_data)
    
    logic = CartLogic(db)
    try:
        return logic.create_cart_item(cart_item, user_data["user_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@cart_route.put("/update", status_code=status.HTTP_200_OK)
async def update_cart_item(cart_item: CartItemDTO, db: db_dependency, user_data: user_dependency):
    if not user_data:
        raise HTTPException(status_code=401, detail="User not authenticated")
    logic = CartLogic(db)
    try:
        updated_item = logic.update_cart_item(cart_item)
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@cart_route.delete("/delete/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(cart_item_id: int, db: db_dependency, user_data: user_dependency,mode: str = "soft"):
    if not user_data:
        raise HTTPException(status_code=401, detail="User not authenticated")
    logic = CartLogic(db)
    try:
        if mode == "hard":
            logic.hard_delete_cart_item(cart_item_id)
        else:
            logic.soft_delete_cart_item(cart_item_id)
        return {"detail": f"Cart item {cart_item_id} deleted ({mode})"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@cart_route.get("/", status_code=status.HTTP_200_OK)
async def get_cart_items_by_user(db: db_dependency, user_data: user_dependency):
    if not user_data:
        raise HTTPException(status_code=401, detail="User not authenticated")
    logic = CartLogic(db)
    try:
        return logic.get_cart_items_by_user(user_data["user_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))