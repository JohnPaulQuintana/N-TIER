from sqlalchemy.orm import Session

from repositories.project_repository import ProjectRepository
from repositories.role_repository import RoleRepository
from repositories.user_project_repository import UserProjectRepository
from repositories.user_repository import UserRepository
from schemas.auth import UserCreate, UserLogin
from utils.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)


class AuthService:

    def __init__(self, db: Session):
        self.db = db

        self.user_repository = UserRepository(db)
        self.project_repository = ProjectRepository(db)
        self.role_repository = RoleRepository(db)
        self.user_project_repository = UserProjectRepository(db)

    def login_user(
        self,
        login_data: UserLogin,
    ):
        user = self.user_repository.get_by_email(
            login_data.email,
        )

        if not user:
            raise ValueError(
                "Invalid email or password",
            )

        if not user.is_active:
            raise PermissionError(
                "User account is inactive",
            )

        if not verify_password(
            login_data.password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid email or password",
            )

        project = self.project_repository.get_by_slug(
            login_data.project_slug,
        )

        if not project:
            raise ValueError(
                "Project not found or inactive",
            )

        membership = self.user_project_repository.get_membership(
            user_id=user.id,
            project_id=project.id,
        )

        if not membership:
            raise PermissionError(
                "User does not have access to this project",
            )

        role = self.role_repository.get_by_id(
            membership.role_id,
        )

        if not role:
            raise ValueError(
                "User role not found",
            )

        access_token = create_access_token(
            user_id=user.id,
            project_id=project.id,
            role=role.slug,
        )

        refresh_token = create_refresh_token(
            user_id=user.id,
            project_id=project.id,
            role=role.slug,
        )

        return {
            "user": user,
            "project": project,
            "membership": membership,
            "role": role,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def refresh_access_token(
        self,
        refresh_token: str,
    ):
        try:
            payload = decode_refresh_token(
                refresh_token,
            )

            user_id = payload.get("sub")
            project_id = payload.get("project_id")
            role = payload.get("role")

            if not user_id or not project_id or not role:
                raise ValueError(
                    "Invalid refresh token.",
                )

            user = self.user_repository.get_by_id(
                int(user_id),
            )

            if not user:
                raise ValueError(
                    "User not found.",
                )

            if not user.is_active:
                raise PermissionError(
                    "User account is inactive.",
                )

            access_token = create_access_token(
                user_id=int(user_id),
                project_id=int(project_id),
                role=role,
            )

            return access_token

        except Exception as error:
            raise ValueError(
                "Invalid or expired refresh token.",
            ) from error

    def register_user(
        self,
        user_data: UserCreate,
    ):
        try:
            # 1. Find the requested project
            project = self.project_repository.get_by_slug(
                user_data.project_slug,
            )

            if not project:
                raise ValueError(
                    "Project not found or inactive",
                )

            # 2. Find the global user role
            user_role = self.role_repository.get_by_slug(
                "user",
            )

            if not user_role:
                raise ValueError(
                    "Default user role not found",
                )

            # 3. Find existing central account
            user = self.user_repository.get_by_email(
                user_data.email,
            )

            # 4. Create account if it doesn't exist
            if not user:
                password_hash = hash_password(
                    user_data.password,
                )

                user = self.user_repository.create(
                    full_name=user_data.full_name,
                    email=user_data.email,
                    password_hash=password_hash,
                )

            # 5. Check whether this user already belongs
            #    to this project
            existing_membership = self.user_project_repository.get_membership(
                user_id=user.id,
                project_id=project.id,
            )

            if existing_membership:
                raise ValueError(
                    "User is already registered for this project",
                )

            # 6. Connect user to project
            membership = self.user_project_repository.create(
                user_id=user.id,
                project_id=project.id,
                role_id=user_role.id,
            )

            # 7. Commit everything together
            self.db.commit()

            self.db.refresh(user)
            self.db.refresh(membership)

            return user
        except:
            self.db.rollback()
            raise

    def check_project_access(
        self,
        user_id: int,
        project_slug: str,
    ):
        project = self.project_repository.get_by_slug(
            project_slug,
        )

        if not project:
            raise ValueError(
                "Project not found or inactive",
            )

        membership = self.user_project_repository.get_membership(
            user_id=user_id,
            project_id=project.id,
        )

        if not membership:
            raise PermissionError(
                "User does not have access to this project",
            )

        return membership
