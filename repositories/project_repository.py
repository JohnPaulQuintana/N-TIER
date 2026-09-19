from sqlalchemy import select
from sqlalchemy.orm import Session

from models.project import Project


class ProjectRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        project_id: int,
    ) -> Project | None:
        statement = select(Project).where(
            Project.id == project_id,
            Project.is_active.is_(True),
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> Project | None:
        statement = select(Project).where(
            Project.slug == slug,
            Project.is_active.is_(True),
        )

        return self.db.scalar(statement)
