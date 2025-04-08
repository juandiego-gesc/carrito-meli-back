from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from src.main.bd.models.cart_models import CartItem
from src.main.controller.dto.cart_dto import NewCartItemDTO, CartItemDTO
from src.logging_config import LOGGING_CONFIG 

logger = logging.getLogger(__name__)

class CartLogic:
    def __init__(self, db: Session):
        self.db = db

    def create_cart_item(self, cart_item: NewCartItemDTO, user_id: int):
        logger.info("Adding new cart item")
        try:
            # Check if the item already exists for the user
            existing_item = self.db.query(CartItem).filter(
                CartItem.user_id == user_id,
                CartItem.product_id == cart_item.product_id,
                CartItem.del_flag == False
            ).first()
            if existing_item:
            # Update the quantity if the product is already in the cart
                existing_item.quantity += cart_item.quantity
                self.db.commit()
                self.db.refresh(existing_item)
                logger.debug(f"Updated cart item with id {existing_item.id}: new quantity {existing_item.quantity}")
                return existing_item
            else:
            # Create a new cart item if it does not exist
                new_item = CartItem(
                    user_id=user_id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity
                )
                self.db.add(new_item)
                self.db.commit()
                self.db.refresh(new_item)
                logger.debug(f"Created new cart item with id {new_item.id}")
                return new_item
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError while creating cart item: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while creating cart item: {e}")
            raise

    def update_cart_item(self, cart_item: CartItemDTO):
        logger.info(f"Updating cart item with id {cart_item.id}")
        try:
            db_cart_item = self.get_cart_item_by_id(cart_item.id)
            if db_cart_item:
                if cart_item.quantity <= 0:
                    self.soft_delete_cart_item(cart_item.id)
                    return None
                else:        
                    db_cart_item.quantity = cart_item.quantity
                    self.db.commit()
                    self.db.refresh(db_cart_item)
                    logger.debug(f"Updated cart item with id {db_cart_item.id}")
            return db_cart_item
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError while updating cart item: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while updating cart item: {e}")
            raise

    def soft_delete_cart_item(self, cart_item_id: int):
        logger.info(f"Soft deleting cart item with id {cart_item_id}")
        try:
            db_cart_item = self.get_cart_item_by_id(cart_item_id)
            if db_cart_item:
                db_cart_item.del_flag = True
                self.db.commit()
                logger.debug(f"Soft deleted cart item with id {cart_item_id}")
            return db_cart_item
        except Exception as e:
            logger.error(f"Error soft deleting cart item: {e}")
            raise

    def hard_delete_cart_item(self, cart_item_id: int):
        logger.info(f"Hard deleting cart item with id {cart_item_id}")
        try:
            db_cart_item = self.get_cart_item_by_id(cart_item_id)
            if db_cart_item:
                self.db.delete(db_cart_item)
                self.db.commit()
                logger.debug(f"Hard deleted cart item with id {cart_item_id}")
            return db_cart_item
        except Exception as e:
            logger.error(f"Error hard deleting cart item: {e}")
            raise

    def get_cart_items_by_user(self, user_id: int):
        logger.info(f"Getting cart items for user {user_id}")
        try:
            cart_items = self.db.query(CartItem).filter(
                CartItem.user_id == user_id, CartItem.del_flag == False
            ).all()
            logger.debug(f"Got {len(cart_items)} cart items for user {user_id}")
            return cart_items
        except Exception as e:
            logger.error(f"Error getting cart items by user: {e}")
            raise

    def get_cart_item_by_id(self, cart_item_id: int):
        logger.info(f"Getting cart item by id {cart_item_id}")
        try:
            cart_item = self.db.query(CartItem).filter(
                CartItem.id == cart_item_id, CartItem.del_flag == False
            ).first()
            if not cart_item:
                raise Exception(f"Cart item with id {cart_item_id} not found")
            return cart_item
        except Exception as e:
            logger.error(f"Error getting cart item by id: {e}")
            raise

