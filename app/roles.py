from datetime import datetime
import json
from sqlalchemy.orm import Session
from . import models

DEFAULT_ROLES = {
    "admin": {
        "description": "Full system access",
        "permissions": {
            "view_users": True,
            "manage_users": True,
            "view_roles": True,
            "manage_roles": True,
            "view_system": True,
            "manage_system": True,
        },
    },
    "user": {
        "description": "Standard user access",
        "permissions": {
            "view_users": False,
            "manage_users": False,
            "view_roles": False,
            "manage_roles": False,
            "view_system": False,
            "manage_system": False,
        },
    },
    "moderator": {
        "description": "User management access",
        "permissions": {
            "view_users": True,
            "manage_users": True,
            "view_roles": True,
            "manage_roles": False,
            "view_system": True,
            "manage_system": False,
        },
    },
}


def ensure_default_roles_exist(db: Session):
    """Ensure default roles exist in the database."""
    for role_name, role_data in DEFAULT_ROLES.items():
        role = db.query(models.Role).filter(models.Role.name == role_name).first()
        if not role:
            role = models.Role(
                name=role_name,
                description=role_data["description"],
                permissions=json.dumps(role_data["permissions"]),
                created_at=datetime.utcnow(),
            )
            db.add(role)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Error ensuring default roles exist: {e}")


def has_permission(user: models.User, permission: str) -> bool:
    """Check if a user has a specific permission."""
    if not user or not user.role_info:
        return False

    try:
        permissions = json.loads(user.role_info.permissions)
        return permissions.get(permission, False)
    except (json.JSONDecodeError, AttributeError):
        return False


def requires_permission(permission: str):
    """Decorator to check if a user has a specific permission."""
    from fastapi import HTTPException, Depends
    from .auth import get_current_active_user
    from .database import get_db

    def decorator(func):
        async def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")
            if not user:
                # If current_user is not in kwargs, try to get it
                db = kwargs.get("db") or next(get_db())
                user = await get_current_active_user(db=db)

            if not has_permission(user, permission):
                raise HTTPException(
                    status_code=403, detail=f"Permission denied: {permission} required"
                )
            return await func(*args, **kwargs)

        # Copy metadata from original function
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator
