from app.main import app
from app.models import Announcement
from app.scheduler import send_due_announcements
from app.database import db
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import asyncio

# Setup test client for FastAPI application
client = TestClient(app)

# Test announcement scheduling functionality
async def test_announcement_scheduling():
    # Arrange
    announcement = Announcement(message="Test announcement")
    # Act
    response = client.post("/announcements/", json=announcement.dict())
    # Assert
    assert response.status_code == 200
    assert len(db.announcements) == 1

# Test that announcements are sent at the correct time
async def test_announcement_sending():
    # Arrange
    send_time = datetime.now() + timedelta(seconds=10)
    announcement = Announcement(message="Test announcement", send_time=send_time)
    # Act
    response = client.post("/announcements/", json=announcement.dict())
    announcement_id = response.json()['id']
    await asyncio.sleep(15)  # Wait for the time to send the announcement
    send_due_announcements()
    # Assert
    assert db.has_been_sent(announcement_id)

# Test that announcements are not sent more than once
async def test_no_duplicate_sending():
    # Arrange
    announcement = Announcement(message="Test announcement", send_time=datetime.now())
    # Act
    response = client.post("/announcements/", json=announcement.dict())
    announcement_id = response.json()['id']
    send_due_announcements()  # First sending attempt
    send_due_announcements()  # Second sending attempt
    # Assert
    sent_count = sum(1 for ann in db.sent_announcements if ann == announcement_id)
    assert sent_count == 1

# Run all async tests
async def run_tests():
    await asyncio.gather(
        test_announcement_scheduling(),
        test_announcement_sending(),
        test_no_duplicate_sending()
    )

# Entry point for testing when this script is executed
if __name__ == "__main__":
    asyncio.run(run_tests())
