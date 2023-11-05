from fastapi.testclient import TestClient
from app.main import app
from app.models import Announcement
from app.scheduler import send_due_announcements
from app.database import db
from datetime import datetime, timedelta
import pytest
import asyncio

client = TestClient(app)

@pytest.mark.asyncio
async def test_announcement_scheduling():
    # Arrange
    announcement = Announcement(message="Test announcement")
    # Act
    response = client.post("/announcements/", content=announcement.json())
    # Assert
    assert response.status_code == 200
    assert len(db.announcements) == 1

@pytest.mark.asyncio
async def test_announcement_sending():
    # Arrange
    send_time = datetime.now() + timedelta(seconds=10)
    announcement = Announcement(message="Test announcement", send_time=send_time)
    # Act
    response = client.post("/announcements/", content=announcement.json())
    announcement_id = response.json()['id']
    await asyncio.sleep(15)  # Wait for the time to send the announcement
    send_due_announcements()
    # Assert
    assert db.has_been_sent(announcement_id)

@pytest.mark.asyncio
async def test_no_duplicate_sending():
    # Arrange
    announcement = Announcement(message="Test announcement", send_time=datetime.now())
    # Act
    response = client.post("/announcements/", content=announcement.json())
    announcement_id = response.json()['id']
    send_due_announcements()  # First sending attempt
    send_due_announcements()  # Second sending attempt
    # Assert
    sent_count = sum(1 for ann in db.sent_announcements if ann == announcement_id)
    assert sent_count == 1

# Run the pytest main function if this file is executed as the main program
if __name__ == "__main__":
    pytest.main()
