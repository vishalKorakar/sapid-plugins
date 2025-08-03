from pydantic import BaseModel

class ItemUpdate(BaseModel):
    id: str
    name: str
    price: int
