from typing import Optional
from pydantic import BaseModel,Field
 
class UserRegForm(BaseModel):
        TeamName: Optional[str] = None
        Player1Name: Optional[str] = None
        Player2Name: Optional[str] = None
        Player3Name: Optional[str] = None
        email1: Optional[str] = None
        email2: Optional[str] = None
        email3: Optional[str] = None
        phone: Optional[int] = None