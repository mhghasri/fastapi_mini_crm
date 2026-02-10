'''
customer routers
'''

'''
╭──────────────────────────────────────────────╮
│                  Import Modules              │
╰──────────────────────────────────────────────╯
'''

from app.schemas import GetCustomerSchema, UpdateCustomerSchema, BaseCustomerSchema, PostCustomerSchema, GetCustomerOrderSchema
from fastapi import Depends, Path, status, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models import Customer
from app.database import get_db
from typing import List
from main import app

'''
╭──────────────────────────────────────────────╮
│                  get customers               │
╰──────────────────────────────────────────────╯
'''

@app.get("/customers", response_model=List[GetCustomerSchema], status_code=status.HTTP_200_OK)
def get_customers(q: str | None = Query(default=None, deprecated=True, alias="search", description="this is search data if you want."), db:Session = Depends(get_db)):
    if q is not None:
        query = db.query(Customer).filter(or_(Customer.name.ilike(f"%{q}%"), Customer.email.ilike(f"%{q}%")))
        return query
    query = db.query(Customer).all()
    try:
        return query
    
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error has eccourd")

'''
╭──────────────────────────────────────────────╮
│                retrieve customers            │
╰──────────────────────────────────────────────╯
'''

@app.get("/customers/{customer_id}", response_model=GetCustomerOrderSchema, status_code=status.HTTP_200_OK)
def retrieve_customer(customer_id: int, db: Session = Depends(get_db)):
    query = db.query(Customer).options(joinedload(Customer.orders)).filter_by(id=customer_id).one_or_none()

    if query:
        return query

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="مشتری با این آیدی پیدانشد!")

'''
╭──────────────────────────────────────────────╮
│                  post customers              │
╰──────────────────────────────────────────────╯
'''

@app.post("/customers", response_model=GetCustomerSchema, status_code=status.HTTP_201_CREATED)
def post_customers(data: PostCustomerSchema, db:Session = Depends(get_db)):
    new_customer = Customer(**data.model_dump())

    try:
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

        return new_customer

    except IntegrityError as e:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Customer with this email already exists.")
    
'''
╭──────────────────────────────────────────────╮
│                 update customers             │
╰──────────────────────────────────────────────╯
'''

@app.put("/customers/{customer_id}", response_model=GetCustomerSchema, status_code=status.HTTP_200_OK)
def update_customer_detail(request: UpdateCustomerSchema, customer_id: int = Path(..., title="customer id", description="put id for update customer data"), db: Session = Depends(get_db)):
    customer = db.query(Customer).filter_by(id=customer_id).one_or_none()

    update_date = request.model_dump(exclude_unset=True)        # exclude_unset -> ignore null data

    if customer:
        for k, v in update_date.items():
            setattr(customer, k, v)

        db.commit()
        db.refresh(customer)
        return customer

    else:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="customer not found!")

'''
╭──────────────────────────────────────────────╮
│                 delete customers             │
╰──────────────────────────────────────────────╯
'''

@app.delete("/customers/{customer_id}", response_model=GetCustomerSchema, status_code=status.HTTP_202_ACCEPTED)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter_by(id=customer_id).one_or_none()

    if customer:
        db.delete(customer)
        db.commit()

        return customer
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"customer with id: {customer_id} not found for delete!")