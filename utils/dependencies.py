from fastapi import Depends, HTTPException
from typing import Callable
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from configs.settings import settings
from database.connection import get_db
from repositories.project_repository import ProjectRepository
from repositories.user_project_repository import UserProjectRepository
from repositories.user_repository import UserRepository
from schemas.auth import AuthContext

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please provide a valid access token.",
        )
    
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed. The provided access token is invalid or has expired.",
        )

    user_id = payload.get("sub")
    project_id = payload.get("project_id")
    role = payload.get("role")

    if not user_id or not project_id or not role:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed. The access token contains an invalid payload.",
        )

    try:
        user_id = int(user_id)
        project_id = int(project_id)

    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed. The access token contains invalid user or project information.",
        )

    user_repository = UserRepository(db)
    project_repository = ProjectRepository(db)
    user_project_repository = UserProjectRepository(db)

    user = user_repository.get_by_id(user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed. The user account is inactive or does not exist.",
        )

    project = project_repository.get_by_id(project_id)

    if not project:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed. The associated project is inactive or does not exist.",
        )

    membership = user_project_repository.get_membership(
        user_id=user.id,
        project_id=project.id,
    )

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied. You do not have permission to access this project.",
        )

    return AuthContext(
        user_id=user.id,
        full_name=user.full_name,
        email=user.email,
        project_id=project.id,
        project_slug=project.slug,
        role=role,
    )


def require_role(*allowed_roles: str) -> Callable:
    def role_checker(
        current_user=Depends(get_current_user),
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Access denied. You do not have the required permissions to perform this action.",
            )

        return current_user

    return role_checker
