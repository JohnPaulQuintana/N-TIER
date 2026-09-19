from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.auth import UserCreate, UserLogin
from services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        user = service.register_user(user_data)

        return {
            "message": "Registration successful",
            "user_id": user.id,
            "email": user.email,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post("/refresh")
def refresh(
    request: Request,
    db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get(
        "refresh_token",
    )

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token not found.",
        )

    service = AuthService(db)

    try:
        access_token = service.refresh_access_token(
            refresh_token,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error),
        )


@router.post("/login")
def login(
    login_data: UserLogin,
    response: Response,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        result = service.login_user(login_data)

        # Store the refresh token in a secure browser cookie.
        # The frontend JavaScript cannot access this cookie because httponly=True.
        # The browser will automatically send it when calling /auth/refresh.
        # secure=True means the cookie is only sent over HTTPS.
        # samesite="lax" helps protect against cross-site request forgery.
        # max_age keeps the refresh token cookie for 30 days.
        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 30,
        )

        return {
            "message": "Login successful",
            "access_token": result["access_token"],
            "token_type": "bearer",
            "user_id": result["user"].id,
            "email": result["user"].email,
            "project": {
                "id": result["project"].id,
                "name": result["project"].name,
                "slug": result["project"].slug,
            },
            "role": {
                "id": result["role"].id,
                "name": result["role"].name,
                "slug": result["role"].slug,
            },
        }

    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return {
        "message": "Logout successful",
    }
