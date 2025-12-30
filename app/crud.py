from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas

def create_order_transactionally(db: Session, order_data: schemas.OrderCreate):
    try:
        new_order = models.Order(status=models.OrderStatus.PENDING)
        db.add(new_order)
        db.flush()

        for item in order_data.items:
            product = db.query(models.Product).filter(models.Product.id == item.product_id).with_for_update().first()

            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            
            if product.stock_quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")

            product.stock_quantity -= item.quantity

            order_item = models.OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity_ordered=item.quantity,
                price_at_order=product.price
            )
            db.add(order_item)

        db.commit()
        db.refresh(new_order)
        return new_order

    except Exception as e:
        db.rollback()
        raise e
    
