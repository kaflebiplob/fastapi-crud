from pydantic import BaseModel
class Products(BaseModel):
    id:int
    name:str
    description:str=None
    price:float
    quantity:int
    
    