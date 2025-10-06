from fastapi import Depends, APIRouter, HTTPException
from models import Carts, Products, CartItems
from schema import Create_Cart, Cart_Out
from database import get_db
from sqlalchemy.orm import Session
import datetime
from Authentication import admin_only

get_db()

router = APIRouter(prefix="/carts", tags=["Carts"])

@router.post("/", response_model=Cart_Out)
def create_cart(cart: Create_Cart, db: Session = Depends(get_db)):
    new_cart = Carts(uid = cart.user_id, created_at=datetime.datetime.now(datetime.UTC))
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    
    Cart_Items = []
    for item in cart.items:
        product = db.query(Products).filter(Products.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product Not Found")
        if product.product_stock < item.quantity:
            raise HTTPException(status_code=400, detail="Product is not in Stock")
        
        cart_item = CartItems(
            cart_id = new_cart.id,
            product_id = item.product_id,
            quantity = item.quantity,
            price_in_cart = product.product_price            
        )
        db.add(cart_item)
        Cart_Items.append(cart_item)
    db.commit()

    new_cart.cart_cartitems = Cart_Items
    total = sum(i.quantity * i.price_in_cart for i in Cart_Items)

    return Cart_Out.model_validate(
        {
            "id": new_cart.id,
            "user_id": new_cart.uid,
            "created_at": new_cart.created_at,
            "items": new_cart.cart_cartitems,
            "cart_total": total,
        },
        from_attributes=True
    )


@router.get("/{cart_id}", response_model=Cart_Out)
def view_cart(cart_id: int, db: Session = Depends(get_db)):
    existing_cart = db.query(Carts).filter(Carts.id == cart_id).first()
    if not existing_cart:
        raise HTTPException(status_code=404, detail="Cart Not Found")
    total = sum(i.quantity + i.price_in_cart for i in existing_cart.cart_cartitems)

    return Cart_Out.model_validate(
        {
            "id": existing_cart.id,
            "user_id": existing_cart.uid,
            "created_at": existing_cart.created_at,
            "items": existing_cart.cart_cartitems,
            "cart_total": total,
        },
        from_attributes=True
    )
    
@router.put("/{cart_id}", response_model=Cart_Out)
def update_cart(cart_id: int, updated_cart: Create_Cart, db: Session = Depends(get_db)):
    existing_cart = db.query(Carts).filter(Carts.id == cart_id).first()
    if not existing_cart:
        raise HTTPException(status_code=404, detail="Cart Not Found")
    db.query(CartItems).filter(CartItems.cart_id == existing_cart.id).delete()

    new_items = []
    for item in updated_cart.items:
        product = db.query(Products).filter(Products.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.product_stock < item.quantity:
            raise HTTPException(status_code=400, detail="Product not in Stock")
        
        cart_item = CartItems(
            cart_id= existing_cart.id,
            product_id= item.product_id,
            quantity= item.quantity,
            price_in_cart = product.product_price
        )
        db.add(cart_item)
        new_items.append(cart_item)
    db.commit()

    existing_cart.cart_cartitems = new_items
    total = sum(i.quantity * i.price_in_cart for i in new_items)
    
    return Cart_Out.model_validate(
        {
            "id": existing_cart.id,
            "user_id": existing_cart.uid,
            "created_at": existing_cart.created_at,
            "items": existing_cart.cart_cartitems,
            "cart_total": total,
        },
        from_attributes=True
    )


@router.delete("/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Carts).filter(Carts.id == cart_id).delete()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart Not Found")
    db.delete(cart)
    db.commit()
    return {"message": f"Your {cart_id} has been deleted"}
    
