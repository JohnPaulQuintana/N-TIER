from fastapi import APIRouter, Depends
from utils.dependencies import get_current_user, require_role

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
def get_users():
    return {"message": "Get users"}


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user),
):
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "project_id": current_user.project_id,
        "project_slug": current_user.project_slug,
        "role": current_user.role,
    }


@router.get("/admin-test")
def admin_test(
    current_user=Depends(require_role("admin")),
):
    return {
        "message": "You have admin access",
        "user_id": current_user.user_id,
        "project": current_user.project_slug,
        "role": current_user.role,
        "debug": current_user
    }
