from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from core.permission import require_roles
from models.inventory_model import Inventory
from models.product_model import Product

router = APIRouter(prefix="/inventory", tags=["Inventory"], dependencies=[Depends(get_current_user)])

@router.post("/stock-in/{product_id}", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def stock_in(product_id: int, quantity: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()

    if not inventory:
        inventory = Inventory(product_id=product_id, quantity=quantity)
        db.add(inventory)
    else:
        inventory.quantity += quantity
    db.commit()
    return {"Info": "Stock Added"}

@router.post("/stock-out/{product_id}", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def stock_out(product_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Product not found in inventory")
    if inventory.quantity < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    inventory.quantity -= quantity
    db.commit()
    return {"Info": "Stock Removed"}

@router.get("/report")
def inventory_report(db: Session = Depends(get_db)):
    return db.query(Inventory).all()