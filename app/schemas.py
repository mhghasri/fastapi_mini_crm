'''
schemas
'''

'''
╭──────────────────────────────────────────────╮
│                 Import Modules               │
╰──────────────────────────────────────────────╯
'''

from pydantic.networks import EmailStr
from pydantic import BaseModel, Field
from datetime import datetime

'''
╭──────────────────────────────────────────────╮
│                 Customer Schemas             │
╰──────────────────────────────────────────────╯
'''

class BaseCustomerSchema(BaseModel):

    name: str
    email: EmailStr

    class Config:
        '''
        mean read from sqlalchemy orm not from a dict
        '''
        from_attributes = True
    

class GetCustomerSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True

class PostCustomerSchema(BaseCustomerSchema):
    pass

class UpdateCustomerSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

'''
╭──────────────────────────────────────────────╮
│                  Order Schemas               │
╰──────────────────────────────────────────────╯
'''
from pydantic import field_serializer, field_validator
from pydantic_core import PydanticCustomError

class PostOrderSchema(BaseModel):
    title: str
    description: str
    price: float
    customer_id: int

    @field_validator("price")
    def validate_price(cls, value: float):
        if value < 0:
            raise PydanticCustomError(
                "قیمت منفی",
                "قیمت نباید منفی باشد",
                {"value" : value}
            )
        
        return value
    
    @field_validator("title")
    def validate_title(cls, value: str):
        if len(value) > 50:
            raise PydanticCustomError(
                "تعداد کارکتر تایتل بیش از حد",
                "تایتل باید از 50 کارکتر کمتر باشید",
                {"value" : value}
            )
        
        return value



class GetOrderSchema(BaseModel):
    id: int
    title: str
    description: str
    price: float
    created_at: datetime
    updated_at: datetime

    customer: GetCustomerSchema

    @field_serializer("price")
    def rounded_price(self, value):
        return round(value, 2)
    
class PutOrderSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    customer_id: int | None = None

    @field_validator("price")
    def validate_price(cls, value: float):
        if value is not None and value < 0:
            raise PydanticCustomError(
                "قیمت منفی",
                "قیمت نباید منفی باشد",
                {"value" : value}
            )
        
        return value
    
    @field_validator("title")
    def validate_title(cls, value: str):
        if value is not None and len(value) > 50:
            raise PydanticCustomError(
                "تعداد کارکتر تایتل بیش از حد",
                "تایتل باید از 50 کارکتر کمتر باشید",
                {"value" : value}
            )
        
        return value

from pydantic import computed_field, model_serializer
class GetCustomerOrderSchema(GetCustomerSchema):
    orders: list[GetOrderSchema] = []

    # @computed_field               # یک فیلد که نداریم رو بهمون میده   
    # @property
    # def order_count(self) -> int:
    #     return len(self.order)

    @model_serializer
    def serializer(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "order_count": len(self.orders),
            "orders": self.orders,
        }