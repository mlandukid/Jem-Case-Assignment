from fastapi import FastAPI
from .models import Announcement
from .database import db
from .scheduler import send_due_announcements
import uuid

app = FastAPI()

@app.post("/announcements/")
async def create_announcement(announcement: Announcement):
    if announcement.send_time is None:
        announcement.send_time = datetime.now()
    announcement_id = str(uuid.uuid4())
    db.add_announcement({"id": announcement_id, "announcement": announcement})
    return {"id": announcement_id, "message": "Announcement scheduled"}
