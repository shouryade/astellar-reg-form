from typing import Optional
from fastapi import Form
from pydantic import BaseModel


class UserRegForm(BaseModel):
        TeamName: Optional[str] = Form(...)
        Player1Name: Optional[str] = Form(...)
        Player2Name: Optional[str] = Form(...)
        Player3Name: Optional[str] = Form(...)
        email1: Optional[str] = Form(...)
        email2: Optional[str] = Form(...)
        email3: Optional[str] = Form(...)
        phone: Optional[int] = Form(...)

        class Config:
                orm_mode=True