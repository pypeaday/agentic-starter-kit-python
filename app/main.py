from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from . import (
    models,
    database,
    themes,
    auth,
    auth_routes,
    admin_routes,
    todo_routes,
    roles,
    jinja_filters,
)

app = FastAPI(title="FastAPI HTMX Starter")
templates = Jinja2Templates(directory="app/templates")

# Register custom Jinja2 filters
jinja_filters.register_filters(templates)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add middleware to extract token from cookies
@app.middleware("http")
async def cookie_to_authorization(request: Request, call_next):
    # Extract token from cookie
    token = request.cookies.get("access_token")

    # Check if we have a token and no authorization header already exists
    has_auth_header = False
    for k, v in request.scope.get("headers", []):
        if k.decode().lower() == "authorization":
            has_auth_header = True
            break

    # Create a modified scope with the authorization header if token exists and no auth header
    if token and not has_auth_header:
        # Get the original headers as a list of tuples
        headers = list(request.scope.get("headers", []))

        # Add the authorization header
        auth_value = f"Bearer {token}"
        headers.append((b"authorization", auth_value.encode()))

        # Update the scope headers
        request.scope["headers"] = headers

    # Process the request and get the response
    response = await call_next(request)
    return response


# Include auth routes
app.include_router(auth_routes.router)

# Include admin routes
app.include_router(admin_routes.router)

# Include todo routes
app.include_router(todo_routes.router)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Default theme
DEFAULT_THEME = "gruvbox-dark"


def get_current_theme(request: Request) -> tuple[themes.ThemeColors, str]:
    """Get the current theme colors based on cookie or default"""
    theme_name = request.cookies.get("theme", DEFAULT_THEME)
    theme = themes.get_theme(theme_name)
    if not theme:
        theme = themes.get_theme(DEFAULT_THEME)
        theme_name = DEFAULT_THEME
    return theme, theme_name


def set_theme_cookie(response: HTMLResponse, theme_name: str) -> None:
    """Set theme cookie with standard parameters"""
    response.set_cookie(
        key="theme",
        value=theme_name,
        max_age=31536000,  # 1 year
        httponly=False,  # Allow JavaScript to read the cookie
        samesite="lax",
        secure=False,  # Allow non-HTTPS for local development
    )


# API Models
class ThemeColors(BaseModel):
    bg: str
    bg1: str
    bg2: str
    fg: str
    fg1: str
    accent: str
    accent_hover: str
    success: str
    error: str


# Create tables if they don't exist
from sqlalchemy import inspect

# Check if tables exist before creating them
inspector = inspect(database.engine)
existing_tables = inspector.get_table_names()

# Database should be created by alembic migrations
# Initialize database with admin user and default roles
print("Initializing database...")
with database.SessionLocal() as db:
    try:
        # Create admin user if it doesn't exist
        admin = auth.ensure_admin_exists(db)
        print(f"Admin user confirmed: {admin.email}")

        # Create default roles if they don't exist
        roles.ensure_default_roles_exist(db)
        print("Default roles confirmed")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise


@app.get("/")
def home(request: Request, db: Session = Depends(database.get_db)):
    # Get current user from token cookie if available
    access_token = request.cookies.get("access_token")
    current_user = None
    todos = []

    if access_token:
        # Token is stored without Bearer prefix
        try:
            current_user = auth.get_optional_current_user_sync(access_token, db)
            if current_user:
                # Get user's todos if authenticated
                todos = (
                    db.query(models.Todo)
                    .filter(models.Todo.user_id == current_user.id)
                    .order_by(models.Todo.created_at.desc())
                    .all()
                )
        except Exception as e:
            # Invalid token, ignore and proceed as anonymous user
            print(f"Authentication error: {e}")
            pass

    theme, current_theme = get_current_theme(request)
    response = templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "theme": theme,
            "current_theme": current_theme,
            "user": current_user,
            "todos": todos,
        },
    )
    response.set_cookie(
        key="theme",
        value=current_theme,
        max_age=31536000,  # 1 year
        httponly=False,  # Allow JavaScript to read the cookie
        samesite="lax",
        secure=False,  # Allow non-HTTPS for local development
    )
    return response


@app.get("/settings")
def settings_page(request: Request):
    theme, current_theme = get_current_theme(request)
    # Create a dict of theme names and their colors
    theme_previews = {name: colors for name, colors in themes.THEMES.items()}
    # Sort themes alphabetically for consistent display
    theme_previews = dict(sorted(theme_previews.items()))

    response = templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "theme_previews": theme_previews,
            "current_theme": current_theme,
            "theme": theme,
        },
    )
    set_theme_cookie(response, current_theme)
    return response


@app.post("/settings/theme")
def update_theme(request: Request, theme_name: str = Form(...)):
    if theme_name not in themes.THEMES:
        raise HTTPException(status_code=400, detail="Invalid theme")

    # Update the HTML data-theme attribute via HTMX response
    response = HTMLResponse("", status_code=200)
    set_theme_cookie(response, theme_name)
    response.headers["HX-Trigger"] = "themeChanged"
    return response


# JSON API endpoints
@app.get("/api/theme/{theme_name}", response_model=ThemeColors)
def get_theme_colors(theme_name: str):
    theme = themes.get_theme(theme_name)
    if not theme:
        raise HTTPException(status_code=404, detail=f"Theme '{theme_name}' not found")
    return theme
