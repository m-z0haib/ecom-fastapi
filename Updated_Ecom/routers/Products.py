from fastapi import Depends, APIRouter, HTTPException, Query
from models import Products
from schema import Create_Product, Product_Out
from database import get_db
from sqlalchemy.orm import Session
from Authentication import admin_only

get_db()

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[Product_Out])
def view_all_products(db: Session = Depends(get_db)):
    return db.query(Products).all()


@router.get("/search")
def search_product(q: str = Query(description="Search for the product"), db: Session = Depends(get_db)):
    if not q:
        return {"message":"Search product in singlular form"}
    products = db.query(Products).filter(Products.product_name.ilike(f"%{q}%")).all()
    if not products:
        return {"message": f"No Product Found for '{q}': Try another singular one"}
    return {"result": products}    




@router.post("/add_product", response_model=Product_Out, dependencies=[Depends(admin_only)])
def add_product(new_product: Create_Product, db: Session = Depends(get_db)):
    existing_product = db.query(Products).filter(Products.product_name == new_product.product_name).first()
    if existing_product:
        raise HTTPException(status_code=404, detail="Product Already Exists")
    new_product = Products(product_name = new_product.product_name, producta_description = new_product.producta_description,
                            product_price = new_product.product_price, product_stock = new_product.product_stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{product_id}", response_model=Product_Out)
def add_product(product_id: int,  new_product: Create_Product, db: Session = Depends(get_db)):
    existing_product = db.query(Products).filter(Products.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    existing_product.product_name = new_product.product_name
    existing_product.producta_description = new_product.product_description
    existing_product.product_price = new_product.product_price
    existing_product.product_stock = new_product.product_stock
    db.commit()
    db.refresh(existing_product)
    return existing_product

@router.delete("/{product_id}", response_model=Product_Out)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    existing_product = db.query(Products).filter(Products.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(existing_product)
    db.commit()
    return {"message": "Product has been deleted"}

