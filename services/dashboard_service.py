# services/dashboard_service.py

from sqlalchemy.orm import Session

from repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, db: Session):
        self.repository = DashboardRepository(db)

    def get_analytics(
        self,
        project_id: int,
        year: int,
        month: int,
    ) -> dict:
        """
        Get dashboard analytics for a project.
        """

        return self.repository.get_analytics(
            project_id=project_id,
            year=year,
            month=month,
        )
