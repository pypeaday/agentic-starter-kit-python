# FastAPI + HTMX Starter Kit

A modern web application starter kit that combines the power of FastAPI with the simplicity of HTMX. This project provides a solid foundation for building web applications with Python, featuring built-in authentication, SQLite database integration, and interactive UI components.

## Features

- **FastAPI Backend**: High-performance, easy-to-use web framework
- **HTMX Integration**: Modern, browser-native interactivity without complex JavaScript
- **SQLite Database**: Simple, file-based database with SQLAlchemy ORM
- **User Authentication**: Built-in email/password authentication with JWT tokens
- **Admin Interface**: Ready-to-use admin dashboard
- **Theme Support**: Dark/light theme switching with customizable colors
- **Interactive UI Components**: Pre-built HTMX-powered components (todo list, infinite scroll, etc.)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fastapi-htmx-starter.git
cd fastapi-htmx-starter
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure it:
```bash
cp .env.example .env
```

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` to see your application running.

## Environment Variables

Configure these variables in your `.env` file:

- `DATABASE_URL`: SQLite database URL (default: sqlite:///./data/app.db)
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `ADMIN_EMAIL`: Default admin user email
- `ADMIN_PASSWORD`: Default admin user password
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `ENVIRONMENT`: Development or production mode

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI application setup
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── auth.py             # Authentication logic
├── htmx.py            # HTMX utility functions
├── static/
│   └── css/
│       └── theme.css   # Theme styles
└── templates/
    ├── base.html       # Base template
    ├── index.html      # Home page
    ├── login.html      # Login page
    ├── register.html   # Registration page
    └── admin/
        └── dashboard.html  # Admin dashboard
```

## Authentication

The starter kit includes a complete authentication system:

- User registration with email/password
- JWT token-based authentication
- Remember me functionality
- Role-based authorization (user/admin)
- Automatic admin user creation

## HTMX Features

Demonstrates various HTMX capabilities:

- Dynamic content loading
- Form submissions without page reloads
- Infinite scroll
- Active search
- Toast notifications
- Theme switching

## Development

### Adding New Routes

1. Create a new route file in the `app` directory
2. Define your routes using FastAPI's router
3. Include the router in `main.py`

Example:
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/my-route")
def my_route():
    return {"message": "Hello"}
```

### Database Migrations

The project uses SQLAlchemy for database management. To make changes to the database schema:

1. Modify the models in `models.py`
2. The changes will be automatically applied on next startup

### Theme Customization

1. Add new themes in `app/themes.py`
2. Update theme CSS variables in `static/css/theme.css`
3. Use theme classes in your templates

## Production Deployment

Before deploying to production:

1. Set a secure `JWT_SECRET_KEY`
2. Change default admin credentials
3. Set `ENVIRONMENT=production`
4. Configure proper CORS settings
5. Enable HTTPS
6. Set appropriate cookie security flags

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
