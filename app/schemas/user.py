from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    street: str
    house_number: str
    zip: str
    city: str
    business_phone: str
    personal_phone: str
