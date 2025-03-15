from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from . import models, database, auth, schemas
from .database import get_db


# Create a dependency that will check for admin role
def admin_dependency(
    token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)
):
    user = auth.get_current_user_sync(token, db)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Admin role required.",
        )
    return user


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    current_user: models.User = Depends(admin_dependency),
    db: Session = Depends(get_db),
):
    """Admin dashboard showing system statistics and management options."""
    # Get user count
    user_count = db.query(models.User).count()

    # Get recent users
    recent_users = (
        db.query(models.User).order_by(models.User.created_at.desc()).limit(5).all()
    )

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "current_user": current_user,
            "user": current_user,  # Add this for the base template
            "user_count": user_count,
            "recent_users": recent_users,
        },
    )


@router.get("/users", response_class=HTMLResponse)
async def list_users(
    request: Request,
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db),
):
    """List all users in the system."""
    users = db.query(models.User).all()
    return templates.TemplateResponse(
        "admin/users.html",
        {
            "request": request,
            "current_user": current_user,
            "user": current_user,  # Add this for the base template
            "users": users,
        },
    )


@router.post("/users/{user_id}/toggle-role")
async def toggle_user_role(
    user_id: int,
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Toggle a user's role between 'user' and 'admin'."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Don't allow admins to demote themselves
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot change your own role")

    # Toggle role
    user.role = "admin" if user.role == "user" else "user"
    db.commit()

    return {"success": True, "role": user.role}


@router.post("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Toggle a user's active status."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Don't allow admins to deactivate themselves
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")

    # Toggle active status
    user.is_active = not user.is_active
    db.commit()

    return {"success": True, "is_active": user.is_active}
