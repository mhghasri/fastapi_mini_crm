from app.schemas import GetOrderSchema, PutOrderSchema, PostOrderSchema
from fastapi import Depends, Path, status, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models import Order, Customer
from app.database import get_db
from typing import List
from main import app

'''
╭──────────────────────────────────────────────╮
│                    get orders                │
╰──────────────────────────────────────────────╯
'''

@app.get("/orders", response_model=List[GetOrderSchema], status_code=status.HTTP_200_OK)
def get_order(db: Session=Depends(get_db)):
    query = db.query(Order).options(joinedload(Order.customer)).all()

    return query

@app.post("/orders", response_model=GetOrderSchema, status_code=status.HTTP_201_CREATED)
def post_order(data: PostOrderSchema, db: Session =Depends(get_db)):
    customer = db.query(Customer).filter_by(id=data.customer_id).one_or_none()

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "code" : "مشتری پیدا نشد",
            "message" : "یک کاستومر با این آیدی یافت نشد دوباره تلاش کنید.",
            "customer_id" : data.customer_id
        })
    
    order = Order(**data.model_dump())

    db.add(order)
    db.commit()
    db.refresh(order)

    return order

@app.put("/orders/{order_id}", response_model=GetOrderSchema, status_code=status.HTTP_200_OK)
def put_order(data: PutOrderSchema, order_id: int = Path(..., title="order_id", description="plead enter order id for change data."), db: Session = Depends(get_db)):
    order = db.query(Order).filter_by(id=order_id).one_or_none()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found order id with this id: {order_id}")
    
    if data.customer_id is not None:
        customer = db.query(Customer).filter_by(id=data.customer_id).one_or_none()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found new custom with id: {data.customer_id}")
        
    update_data = data.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(order, k, v)

    db.commit()
    db.refresh(order)

    return order