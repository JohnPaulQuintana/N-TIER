from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user_project import UserProject


class UserProjectRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_membership(
        self,
        user_id: int,
        project_id: int,
    ) -> UserProject | None:
        statement = select(UserProject).where(
            UserProject.user_id == user_id,
            UserProject.project_id == project_id,
            UserProject.is_active.is_(True),
        )

        return self.db.scalar(statement)

    def create(
        self,
        user_id: int,
        project_id: int,
        role_id: int,
    ) -> UserProject:
        membership = UserProject(
            user_id=user_id,
            project_id=project_id,
            role_id=role_id,
        )

        self.db.add(membership)

        return membership
