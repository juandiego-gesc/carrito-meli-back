from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.main.controller.user_controller import user_route
from src.main.controller.user_controller import auth_route
from src.main.controller.cart_controller import cart_route
from src.main.controller.product_controller import product_route





app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_route, prefix="/users", tags=["users"])
app.include_router(cart_route, prefix="/cart", tags=["cart"])
app.include_router(product_route, prefix="/products", tags=["products"])
app.include_router(auth_route, prefix="/auth", tags=["auth"])
@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the E-commerce API!"}


