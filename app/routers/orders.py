from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database, schemas, models, crud

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    return crud.create_order_transactionally(db, order)

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(order_id: int, status_update: schemas.OrderUpdateStatus, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == models.OrderStatus.CANCELLED and status_update.status == models.OrderStatus.SHIPPED:
        raise HTTPException(status_code=400, detail="Cannot ship a cancelled order")
        
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    return order

