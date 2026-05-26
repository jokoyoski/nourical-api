# Nourical

A Flask web application built with best practices.

## Features

- Modular project structure
- Environment configuration
- Poetry dependency management
- Template system with Jinja2
- Static file management (CSS, JS, images)
- Development server with debug mode
- PostgreSQL database integration
- Swagger API documentation
- User authentication with OTP verification
- Password hashing with bcrypt
- Firebase Cloud Messaging (FCM) for push notifications

## Installation

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Edit `.env` and set your `SECRET_KEY` and `DATABASE_URL`

## Running the Application

Start the development server:
```bash
poetry run python app.py
```

Or activate the virtual environment first:
```bash
poetry shell
python app.py
```

The application will be available at `http://127.0.0.1:5001`

## Project Structure

```
nourical/
├── app.py                      # Main application file
├── config.py                  # Configuration settings
├── models.py                  # Database models (User, OTP, UserDevice, etc.)
├── auth_routes.py             # Authentication API endpoints
├── device_routes.py           # Device token management endpoints
├── goals_routes.py            # Goals API endpoints
├── preferences_routes.py      # Preferences API endpoints
├── pyproject.toml             # Poetry configuration and dependencies
├── .env.example               # Example environment variables
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
├── services/                 # Business logic
│   ├── auth_service.py
│   ├── firebase_service.py   # FCM push notification service
│   └── goals_service.py
├── repositories/             # Data access layer
│   ├── user_repository.py
│   ├── user_device_repository.py
│   └── onboarding_repository.py
├── templates/                # HTML templates
│   ├── index.html
│   └── about.html
└── static/                   # Static files
    └── css/
        └── style.css
```

## API Documentation

Swagger UI is available at `http://127.0.0.1:5001/docs/`

### Authentication Endpoints

#### 1. Register User
- **POST** `/api/auth/register`
- Creates a new user account and sends a 6-digit OTP to their email
- Body: `{ "full_name": "John Doe", "email": "john@example.com", "password": "securepassword123" }`
- Returns user ID and OTP (in development mode)

#### 2. Verify OTP
- **POST** `/api/auth/verify-otp`
- Verifies the OTP and activates the user account
- Body: `{ "email": "john@example.com", "otp": "123456" }`
- OTP expires after 10 minutes

#### 3. Login
- **POST** `/api/auth/login`
- Logs in a verified user
- Body: `{ "email": "john@example.com", "password": "securepassword123" }`
- User must be verified with OTP before logging in

## Database Tables

### Users
- id (primary key)
- full_name
- email (unique)
- password_hash (bcrypt)
- is_verified (boolean)
- created_at (timestamp)

### OTPs
- id (primary key)
- user_id (foreign key)
- code (6-digit)
- is_used (boolean)
- expires_at (timestamp)
- created_at (timestamp)

### User Devices
- id (primary key)
- user_id (foreign key)
- device_token (FCM token)
- platform (ios, android, or web)
- created_at (timestamp)
- updated_at (timestamp)

## Firebase Cloud Messaging (FCM) Setup

### 1. Firebase Configuration

1. Create a Firebase project at https://console.firebase.google.com/
2. Download the service account key JSON file
3. Place the JSON file in the project root (or any location)
4. Set the `FIREBASE_CREDENTIALS_PATH` in your `.env` file:
   ```
   FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
   ```

### 2. Device Token Endpoints

#### Register Device Token
- **POST** `/api/device`
- Requires Bearer token authentication
- Body: `{ "device_token": "fcm-token-from-client", "platform": "android" }`
- Platform options: `ios`, `android`, `web`

#### Get User Devices
- **GET** `/api/device`
- Requires Bearer token authentication
- Returns list of all registered devices for the user

#### Delete Device Token
- **DELETE** `/api/device/<device_id>`
- Requires Bearer token authentication
- Deletes a specific device token

### 3. Sending Notifications

Use the `firebase_service.py` to send notifications:

```python
from services.firebase_service import send_push_notification, send_multicast_notification

# Send to single device
send_push_notification(
    device_token="user-fcm-token",
    title="Meal Reminder",
    body="It's time for your meal!",
    data={"meal_type": "lunch"}
)

# Send to multiple devices
send_multicast_notification(
    device_tokens=["token1", "token2"],
    title="Daily Summary",
    body="Your nutrition summary is ready"
)
```

## Development

The application runs in debug mode by default. Changes to Python files will automatically restart the server.

## License

MIT License
# nourical-api
