from models import OrderItems, Orders, Carts
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
from schema import OrderSummary



router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/confirm/{cart_id}")
def submit_order(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Carts).filter(Carts.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart Not Found")
    if not cart.cart_cartitems:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cart Items not Available")
    
    new_order = Orders(
        uid = cart.uid,
        status = "Pending",
        created_at = datetime.utcnow()
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart.cart_cartitems:
        order_items = OrderItems(
            order_id = new_order.id,
            product_id = item.product_id,
            quantity = item.quantity,
            price_at_order = item.price_in_cart
        )
        db.add(order_items)

    db.commit()

    total = sum(i.quantity * i.price_at_order for i in new_order.orders_orderitems)

    return {
        "order_id": new_order.id,
        "user_id": new_order.uid,
        "status": new_order.status,
        "created_at": new_order.created_at,
        "items": [
            {
                "product_id": i.product_id,
                "quantity": i.quantity,
                "price_at_order": i.price_at_order
            } for i in new_order.orders_orderitems
        ],
        "total": total
    }


@router.get("/confirm/{order_id}/summary")
def order_summary(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Orders).filter(Orders.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Not Found")
    if not order.orders_orderitems:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order is Empty")
    
    total_items = sum(item.quantity for item in order.orders_orderitems)
    total_price = sum(item.quantity*item.price_at_order for item in order.orders_orderitems)

    return OrderSummary(
        order_id=order.id,
        user_id=order.uid,
        created_at=datetime.utcnow(),
        total_items=total_items,
        total_price=total_price,
        payment_status="Not Confirmed"
    )
    


