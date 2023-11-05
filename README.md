# JEM Senior Software Engineer Technical Assessment

This API allows employers to send announcements to their employees via a WhatsApp chatbot. It supports sending announcements immediately or scheduling them for a future time.

## Technical Assessment Overview

The goal of this assessment is to address a specific issue with duplicate messages being sent and to propose a new architecture to solve this problem.

### Identified Issues

- **Duplicate Announcements**: Some employees receive the same announcements more than once. This could be due to:

  1. **Race Conditions**: Concurrent execution of the scheduler could result in sending duplicate messages if proper locking mechanisms aren't in place.
  2. **Idempotency Not Maintained**: If the system does not correctly mark announcements as sent, retries could cause duplicates.

### Proposed Architecture

To address these issues, the following architecture is proposed:

- **Database Transactions**: Ensure that operations on the database are atomic to prevent race conditions.
- **Idempotency Key**: Implement an idempotency key in the announcement creation process to prevent sending duplicates.
- **Status Tracking**: Each announcement should have a status that is updated when it is sent, to prevent re-sending.

## Quick Proof of Concept

The provided PoC simulates the Employer Web Portal with an API that such a portal would call. It does not connect to the WhatsApp Cloud API.

### Running the Project

To run this project on your local machine, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/mlandukid/Jem-Case-Assignment.git
```

2. Navigate to the project directory:

```bash
cd Jem-Case-Assignment
```

3. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate

```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Start the FastAPI application:

```bash
uvicorn app.main:app --reload

```
### Interacting with the API

Once the FastAPI application is running, you can interact with the API using the following endpoints:

#### Create an Announcement

To create a new announcement:

```http
POST /announcements/
```

Payload:
```json
{
    "message": "Your announcement message here",
    "send_time": "Optional: The scheduled time to send the announcement (ISO 8601 format)"
}
```

Example using `curl`:
```bash
curl -X POST "http://127.0.0.1:8000/announcements/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{"message":"Our end of year party is on Saturday evening!","send_time":"2023-12-31T19:00:00Z"}"
```

#### Retrieve All Announcements

To retrieve all scheduled announcements:

```http
GET /announcements/
```

Example using `curl`:
```bash
curl -X GET "http://127.0.0.1:8000/announcements/" -H  "accept: application/json"
```

### API Documentation

For full API documentation, visit the `/docs` or `/redoc` endpoints while the application is running:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

These pages provide interactive documentation and the ability to test the API endpoints directly from the browser.


### Stopping the Application

To stop the FastAPI application, press `CTRL+C` in the terminal where it is running.

## Testing

To run the tests for this project, you need to have `pytest` and `pytest-asyncio` installed in your virtual environment. If you have not installed them yet, you can do so by running:

```bash
pip install pytest pytest-asyncio
```

Once you have the necessary packages installed, you can run the tests using the following command:

```bash
pytest
```

This will execute all the test cases defined in the `tests/` directory and provide a report on which tests passed or failed.


## FAQs

**Q: What if I get a `404 Not Found` when accessing the root URL?**

**A:** The root URL (e.g., `http://127.0.0.1:8000/`) does not have an associated endpoint. Use `/docs` or `/redoc` for API documentation, or use the specific endpoints to interact with the API.

**Q: How do I know if the announcements are being sent?**

**A:** Since this is a PoC and not connected to the WhatsApp Cloud API, sending announcements is simulated. You can check the console logs for confirmation of "sending" actions or implement logging within the scheduler to verify operations.


## Conclusion

This PoC demonstrates a potential solution to the issue of duplicate announcements being sent. By following the steps outlined in this README, you can set up, interact, and test the application.