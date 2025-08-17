from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI(
    title="Order Service",
    root_path="/api/orders",      # 👈 Critical
    docs_url="/docs",             # Not prefixed
    openapi_url="/openapi.json"   # Not prefixed
)

models.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Order service is live!"}

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(
        customer_name=order.customer_name,
        items=",".join(order.items),  # ✅ Convert list to comma-separated string
        total_price=order.total_price,
        order_date=order.order_date
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # ✅ Convert items string back to list for response
    return schemas.Order(
        id=db_order.id,
        customer_name=db_order.customer_name,
        items=db_order.items.split(","),  # 🔁 back to list
        total_price=db_order.total_price,
        order_date=db_order.order_date
    )

@app.get("/orders/", response_model=list[schemas.Order])
def list_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, new_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in new_data.dict().items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted"}
