from typing import List
from pydantic import BaseModel
from datetime import date, datetime


class User(BaseModel):
    username: str = ""
    password: str = ""
    name: str = ""
    role: str = ""
    DOB: datetime = datetime.today()
    phone: int = 1111111111
    
