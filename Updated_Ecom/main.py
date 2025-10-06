from fastapi import FastAPI, Depends, HTTPException
from database import create_table
from typing import Annotated
from Authentication import get_current_user
from routers import Users, Products, Carts, Orders
from fastapi.security import OAuth2PasswordBearer

create_table()

app = FastAPI()

user_depend = Annotated[dict, Depends(get_current_user)]

app.include_router(Users.router)
app.include_router(Products.router)
app.include_router(Carts.router)
app.include_router(Orders.router)


@app.get("/")
def welcome():
    return {"Message": "Welcome to my Update ECOMMERCE"}

# @app.get("/me")
# def user(user: user_depend):
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication Failed")
#     return {"User": user}