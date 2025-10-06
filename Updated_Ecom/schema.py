from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
import re




# User Registration and Login
class Create_User(BaseModel):
    username: str
    user_email: EmailStr
    user_password: str

    @field_validator("user_password")
    def check_password(cls, value: str) -> str:
        if len(value) < 8 or len(value) > 20:
            raise ValueError("Password must be in between 8 to 20 charactere")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain Capital letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain small letter")
        if not re.search(r"[\d]",value):
            raise ValueError("Password must contain a digit")
        if not re.search(r"[!@#$%^&*()]", value):
            raise ValueError("Password must contain any speical character")
        return value    

class User_Out(BaseModel):
    id: int
    username: str
    user_email: EmailStr
    user_phone: str
    user_address: str

    class Config:
        orm_mode = True

class User_login(BaseModel):
    user_email: EmailStr
    user_password: str

#Product Add and Edit
class Create_Product(BaseModel):
    product_name: str
    producta_description: str
    product_price: int
    product_stock: int

class Product_Out(Create_Product):
    id: int

    class Config:
        orm_mode = True

#Add to Cart
class CartItemsInput(BaseModel):
    product_id: int
    quantity: int

class Create_Cart(BaseModel):
    user_id: int
    items: list[CartItemsInput]

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 0,
                "items": [
                    {"product_id": 0, "quantity": 0},
                    {"product_id": 0, "quantity": 0}
                ]
            }
        }

class CartItems_Out(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_in_cart: int

    class Config:
        orm_mode = True


class Cart_Out(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    items: list[CartItems_Out] = []
    cart_total: int

    class Config:
        orm_mode = True

#Order Summary
class OrderSummary(BaseModel):
    order_id: int
    user_id: int
    created_at: datetime
    total_items: int
    total_price: int
    payment_status: str

    class Config:
        orm_mode = True