from fastapi import APIRouter, Depends, status
from typing import Annotated
from src.main.bd.config.database import SessionLocal, engine
from src.main.bd.models.cart_models import Base, User
from src.main.logic.user_logic import UserLogic
from src.main.controller.dto.user_dto import UserDTO, NewUserDTO, UserLoginDTO
from src.main.auth import Token, get_current_user
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

key = Fernet.generate_key()
user_route = APIRouter()
auth_route = APIRouter()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]

@user_route.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
@auth_route.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = UserLoginDTO(username=form_data.username, password=form_data.password)
    print(user)
    logic = UserLogic(db)
    try:
        return logic.login(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_route.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: NewUserDTO, db: db_dependency):
    logic = UserLogic(db)
    try:
        return logic.create_user(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_route.put("/update", status_code=status.HTTP_200_OK)
async def update_user(user: UserDTO, db: db_dependency, user_data: user_dependency):
    if user_data.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this user")
    logic = UserLogic(db)
    try:
        updated_user = logic.update_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_user


@user_route.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: db_dependency, user_data: user_dependency):
    if user_data.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this user")
    logic = UserLogic(db)
    try:
        deleted_user = logic.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "User deleted"}


@user_route.get("/get/all", status_code=status.HTTP_200_OK)
async def show_users(db: db_dependency):
    logic = UserLogic(db)
    try:
        return logic.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_route.get("/get/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: str, db: db_dependency):
    logic = UserLogic(db)
    try:
        user = logic.get_user_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user


@user_route.get("/get/username/{username}", status_code=status.HTTP_200_OK)
async def get_user_by_username(username: str, db: db_dependency):
    logic = UserLogic(db)
    try:
        user = logic.get_user_by_username(username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user
