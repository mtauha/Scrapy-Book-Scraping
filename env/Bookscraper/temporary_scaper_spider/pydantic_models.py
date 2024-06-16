from pydantic import BaseModel

class BookModel(BaseModel):
    url:str
    title: str
    product_type: str
    price_excl_tax: float
    price_incl_tax: float
    tax: float
    availability: int
    num_reviews: int
    stars: int
    category: str
    description: str

    class Config:
        from_attributes = True


class Book(BaseModel):
    id:int
    url:str
    title: str
    product_type: str
    price_excl_tax: float
    price_incl_tax: float
    tax: float
    availability: int
    num_reviews: int
    stars: int
    category: str
    description: str

    class Config:
        from_attributes = True