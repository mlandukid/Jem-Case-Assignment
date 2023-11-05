from datetime import datetime
import uuid

class Database:
    # Initialization method for the Database class.
    def __init__(self):
        self.announcements = []  # A list to store scheduled announcements.
        self.sent_announcements = set()  # A set to keep track of sent announcements IDs.

    # Method to add a new announcement to the schedule.
    def add_announcement(self, announcement):
        self.announcements.append(announcement)  # Add the new announcement to the list.

    # Method to retrieve announcements that are due to be sent.
    def get_due_announcements(self, current_time):
        # Filter announcements that are due to be sent at or before the current time.
        due_announcements = [a for a in self.announcements if a['announcement'].send_time <= current_time]
        # Keep only the announcements that are scheduled for a future time.
        self.announcements = [a for a in self.announcements if a['announcement'].send_time > current_time]
        return due_announcements  # Return the list of due announcements.

    # Method to mark an announcement as sent.
    def mark_as_sent(self, announcement_id):
        self.sent_announcements.add(announcement_id)  # Add the announcement ID to the sent set.

    # Method to check if an announcement has been sent.
    def has_been_sent(self, announcement_id):
        # Check if the announcement ID is in the sent announcements set.
        return announcement_id in self.sent_announcements

# Create an instance of the 'Database' class to be used as an in-memory 'database'.
db = Database()
