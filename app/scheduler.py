from .database import db  # Import the 'db' instance from the 'database' module within the same package.
from datetime import datetime  # Import the datetime class for working with dates and times.

# Define a function that sends due announcements.
def send_due_announcements():
    current_time = datetime.now()  # Get the current time.
    # Retrieve the list of announcements that are due to be sent at the current time.
    due_announcements = db.get_due_announcements(current_time)
    
    # Iterate over each due announcement.
    for announcement in due_announcements:
        # Check if the announcement has not already been sent.
        if not db.has_been_sent(announcement['id']):
            # Mark the announcement as sent in the database.
            db.mark_as_sent(announcement['id'])
            # Print a confirmation that the announcement has been sent.
            print(f"Sent announcement: {announcement['id']}")
