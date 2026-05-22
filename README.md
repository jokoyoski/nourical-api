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
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── models.py             # Database models (User, OTP)
├── auth_routes.py        # Authentication API endpoints
├── pyproject.toml        # Poetry configuration and dependencies
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
├── templates/           # HTML templates
│   ├── index.html
│   └── about.html
└── static/              # Static files
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

## Development

The application runs in debug mode by default. Changes to Python files will automatically restart the server.

## License

MIT License
# nourical-api
