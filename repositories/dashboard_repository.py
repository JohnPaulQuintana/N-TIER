# repositories/dashboard_repository.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.project_record import ProjectRecord


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_stats(self, project_id: int) -> dict:
        statement = select(ProjectRecord).where(ProjectRecord.project_id == project_id)

        records = self.db.execute(statement).scalars().all()

        total_vehicles = len(records)

        service_records = sum(
            len(record.data.get("services", [])) for record in records
        )

        return {
            "total_vehicles": total_vehicles,
            "service_records": service_records,
            "scheduled": 0,
            "appointments": 0,
        }
