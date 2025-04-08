from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from src.main.bd.models.cart_models import Product
from src.main.controller.dto.product_dto import NewProductDTO, ProductDTO

logger = logging.getLogger(__name__)

class ProductLogic:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: NewProductDTO):
        logger.info("Creating a new product")
        try:
            db_product = Product(
                name=product.name,
                price=product.price,
                image_url=product.image_url,
                description=product.description
            )
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            logger.debug(f"Created product with id {db_product.id}")
            return db_product
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError while creating product: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while creating product: {e}")
            raise

    def update_product(self, product: ProductDTO):
        logger.info(f"Updating product with id {product.id}")
        try:
            db_product = self.get_product_by_id(product.id)
            if db_product:
                db_product.name = product.name
                db_product.price = product.price
                db_product.image_url = product.image_url
                db_product.description = product.description
                self.db.commit()
                self.db.refresh(db_product)
                logger.debug(f"Updated product id {db_product.id}")
            return db_product
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError while updating product: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while updating product: {e}")
            raise

    def soft_delete_product(self, product_id: int):
        logger.info(f"Soft deleting product with id {product_id}")
        try:
            db_product = self.get_product_by_id(product_id)
            if db_product:
                db_product.del_flag = True
                self.db.commit()
                logger.debug(f"Soft deleted product with id {product_id}")
            return db_product
        except Exception as e:
            logger.error(f"Error soft deleting product: {e}")
            raise

    def hard_delete_product(self, product_id: int):
        logger.info(f"Hard deleting product with id {product_id}")
        try:
            db_product = self.get_product_by_id(product_id)
            if db_product:
                self.db.delete(db_product)
                self.db.commit()
                logger.debug(f"Hard deleted product with id {product_id}")
            return db_product
        except Exception as e:
            logger.error(f"Error hard deleting product: {e}")
            raise

    def get_all_products(self):
        logger.info("Getting all products")
        try:
            products = self.db.query(Product).filter(Product.del_flag == False).all()
            logger.debug(f"Got {len(products)} products")
            return products
        except Exception as e:
            logger.error(f"Error getting all products: {e}")
            raise

    def get_product_by_id(self, product_id: int):
        logger.info(f"Getting product by id {product_id}")
        try:
            product = self.db.query(Product).filter(Product.id == product_id, Product.del_flag == False).first()
            if not product:
                raise Exception(f"Product with id {product_id} not found")
            return product
        except Exception as e:
            logger.error(f"Error getting product by id: {e}")
            raise