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

class PostCustomerSchema(BaseCustomerSchema):
    pass

class UpdateCustomerSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None