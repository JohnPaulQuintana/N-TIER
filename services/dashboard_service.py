# services/dashboard_service.py

from sqlalchemy.orm import Session

from repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, db: Session):
        self.repository = DashboardRepository(db)

    def get_stats(self, project_id: int) -> dict:
        return self.repository.get_stats(
            project_id=project_id,
        )
