from src.main.bd.models.cart_models import User
from src.main.controller.dto.user_dto import UserDTO, NewUserDTO, UserLoginDTO
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from src.logging_config import LOGGING_CONFIG  # Import the logging configuration
from src.main.auth import create_access_token, verify_password, get_password_hash, Token
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class UserLogic:
    def __init__(self, db: Session):
        self.db = db
        self.key = Fernet.generate_key()

    def login(self, login:UserLoginDTO):
        user = self.get_user_by_username(login.username)
        
        if not user or not verify_password(login.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        logger.info(f"User {user.username} logged in successfully")
        return create_access_token(user.username, user.id)

    def create_user(self, user: NewUserDTO):
        logger.info("Creating a new user")
        hashed_password = get_password_hash(user.password)
        try:
            db_user = User(
                username=user.username,
                name=user.name,
                email=user.email,
                hashed_password=hashed_password
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            logger.debug(f"Created user with id {db_user.id}")
            return self.login(UserLoginDTO(username=user.username, password=user.password))
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while creating a user: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while creating a user: {e}")
            raise

    def update_user(self, user: UserDTO):
        logger.info(f"Updating user with id {user.id}")
        try:
            db_user = self.get_user_by_id(user.id)
            if db_user:
                db_user.username = user.username
                db_user.name = user.name
                db_user.email = user.email
                db_user.hashed_password = user.hashed_password
                self.db.commit()
                self.db.refresh(db_user)
                logger.debug(f"Updated user with id {db_user.id}")
            return db_user
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while updating a user: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while updating a user: {e}")
            raise

    def delete_user(self, user_id: str):
        logger.info(f"Deleting user with id {user_id}")
        try:
            db_user = self.get_user_by_id(user_id)
            if db_user:
                self.db.delete(db_user)
                self.db.commit()
                logger.debug(f"Deleted user with id {db_user.id}")
            return db_user
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while deleting a user: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while deleting a user: {e}")
            raise

    def get_all_users(self):
        logger.info("Getting all users")
        try:
            users = self.db.query(User).all()
            logger.debug(f"Got {len(users)} users")
            return users
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while getting all users: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while getting all users: {e}")
            raise

    def get_user_by_id(self, user_id: str):
        logger.info(f"Getting user by id {user_id}")
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                logger.debug(f"Got user with username {user.username}, {user.name}, {user.email}")
            else:
                logger.debug(f"User with id {user_id} not found")
                raise Exception(f"User with id {user_id} not found")
            return user
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while getting a user by id: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while getting a user by id: {e}")
            raise

    def get_user_by_email(self, email: str):
        logger.info(f"Getting user by email {email}")
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if user:
                logger.debug(f"Got user {user.username}, {user.name}, {user.id}")
            else:
                logger.debug(f"User with email {email} not found")
                raise Exception(f"User with email {email} not found")
            return user
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while getting a user by email {email}: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while getting a user by email {email}: {e}")
            raise

    def get_user_by_username(self, username: str):
        logger.info(f"Getting user by username {username}")
        try:
            user = self.db.query(User).filter(User.username == username, User.del_flag == False).first()
            if user:
                logger.debug(f"Got user with id {user.id}, {user.name} {user.email}")
            else:
                logger.debug(f"User with username {username} not found")
                raise Exception(f"User with username {username} not found")
            return user
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while getting a user by username {username}: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while getting a user by username {username}: {e}")
            raise
