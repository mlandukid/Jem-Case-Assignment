from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Announcement(BaseModel):
    message: str
    send_time: Optional[datetime] = None
