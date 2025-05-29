# FGA Demo App

A FastAPI-based demo application integrating [OpenFGA](https://openfga.dev/) for fine-grained authorization.  
This app demonstrates user, group, and patient profile management with OpenFGA-backed access control.

## Features

- User and group creation
- Patient profile creation and group assignment
- Relationship and permission management via OpenFGA
- REST API endpoints for setup and permission checks

## Requirements

- Python 3.8+
- [OpenFGA](https://openfga.dev/) instance (cloud or local)
- [pip](https://pip.pypa.io/)
- (Recommended) [python-dotenv](https://pypi.org/project/python-dotenv/) for environment variable management

## Useful Links

- [OpenFGA Playground (Sandbox)](https://play.fga.dev/sandbox)
- [OpenFGA API Documentation](https://openfga.dev/api/)

## Setup

1. **Clone the repository**

    ```sh
    git clone <your-repo-url>
    cd fga_demo_app
    ```

2. **Install dependencies**

    ```sh
    pip install -r requirements.txt
    ```

    If `requirements.txt` is missing, install manually:

    ```sh
    pip install fastapi uvicorn openfga-sdk httpx python-dotenv
    ```

3. **Configure environment variables**

    Create a `.env` file in the project root:

    ```
    OPENFGA_API_SCHEME=http
    OPENFGA_API_HOST=<your-fga-host>:<port>
    OPENFGA_STORE_ID=<your-fga-store-id>
    AUTHORIZATION_MODEL_ID=<your-fga-model-id>
    ```

4. **Run the application**

    ```sh
    uvicorn fga_demo_app.main:app --reload
    ```

    The API will be available at `http://localhost:8000`.

## API Endpoints

### `GET /setup`

Initializes demo data:
- Creates users (Alice, Bob, Chris)
- Creates groups (Viewer, Editor)
- Assigns users to groups
- Creates a patient profile and sets up FGA relationships

**Response:**
```json
{
  "patient_profile_id": "...",
  "users": {
    "alice": "...",
    "bob": "...",
    "chris": "..."
  }
}
```

### `GET /check/{user_id}/{action}/{profile_id}`

Checks if a user has a specific permission on a patient profile.

**Example:**
```
GET /check/18e04c81-2a2a-4e20-b070-97793d90c858/view/27492fd3-933f-4dfd-b31b-c1bd1b181907
```

**Response:**
```json
{
  "user": "Alice (Patient)",
  "action": "view",
  "object": "Alice (Patient)",
  "allowed": true
}
```

### `GET /hello`

Health check endpoint.

**Response:**
```json
{"message": "Hello, world!"}
```

## Project Structure

```
fga_demo_app/
├── fga_demo_app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── fga_client.py
│   └── ...
├── data_store.json
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Notes

- The app uses a local `data_store.json` for mock user/group/profile data.
- All FGA configuration is loaded from `.env`.
- Make sure your OpenFGA instance and model are set up before running the app.

## License

MIT License

