from fastapi import FastAPI
from datetime import datetime
import uuid
from .models import Announcement
from .database import db
from .scheduler import send_due_announcements

app = FastAPI()

@app.post("/announcements/")
async def create_announcement(announcement: Announcement):
    # Set the announcement send time to now if not provided
    if announcement.send_time is None:
        announcement.send_time = datetime.now()
    # Generate a unique ID for the new announcement
    announcement_id = str(uuid.uuid4())
    # Add the announcement to the database
    db.add_announcement({"id": announcement_id, "announcement": announcement})
    # Return a response indicating the announcement has been scheduled
    return {"id": announcement_id, "message": "Announcement scheduled"}

@app.get("/")
async def read_root():
    return {"Hello": "Welcome to the Announcement API"}

