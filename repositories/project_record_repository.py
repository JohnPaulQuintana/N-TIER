from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.project_record import ProjectRecord


class ProjectRecordRepository:

    def __init__(self, db: Session):
        self.db = db

    #  add new services
    def add_service(
        self,
        project_id: int,
        record_id: int,
        service: dict,
    ) -> ProjectRecord:
        try:
            statement = select(ProjectRecord).where(
                ProjectRecord.id == record_id,
                ProjectRecord.project_id == project_id,
            )

            record = self.db.execute(statement).scalar_one_or_none()

            if record is None:
                raise ValueError("Vehicle record not found.")

            data = dict(record.data)

            services = list(data.get("services", []))

            services.append(service)

            data["services"] = services

            record.data = data

            self.db.commit()
            self.db.refresh(record)

            return record

        except SQLAlchemyError:
            self.db.rollback()
            raise

    # Check exisiting records of platenumber
    def exists_by_plate_number(
        self,
        project_id: int,
        plate_number: str,
    ) -> bool:
        statement = select(ProjectRecord.id).where(
            ProjectRecord.project_id == project_id,
            ProjectRecord.data["plateNumber"].as_string() == plate_number,
        )

        return self.db.execute(statement).scalar_one_or_none() is not None

    # Register new vehicle records
    def create(
        self,
        project_id: int,
        data: dict,
    ) -> ProjectRecord:
        try:
            record = ProjectRecord(
                project_id=project_id,
                data=data,
            )

            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)

            return record

        except SQLAlchemyError:
            self.db.rollback()
            raise

    #  get only today records
    def get_today(
        self,
        project_id: int,
        page: int,
        page_size: int,
    ) -> tuple[list[ProjectRecord], int]:
        today = datetime.now().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        tomorrow = today + timedelta(days=1)

        base_filter = (
            ProjectRecord.project_id == project_id,
            ProjectRecord.created_at >= today,
            ProjectRecord.created_at < tomorrow,
        )

        count_statement = select(func.count(ProjectRecord.id)).where(*base_filter)

        total = self.db.execute(count_statement).scalar_one()

        offset = (page - 1) * page_size

        statement = (
            select(ProjectRecord)
            .where(*base_filter)
            .order_by(ProjectRecord.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )

        records = list(self.db.execute(statement).scalars().all())

        return records, total

    # Get all records
    def get_all(
        self,
        project_id: int,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> tuple[list[ProjectRecord], int]:

        filters = [
            ProjectRecord.project_id == project_id,
        ]

        if search and search.strip():
            filters.append(
                ProjectRecord.data["plateNumber"]
                .as_string()
                .ilike(f"%{search.strip()}%")
            )

        count_statement = select(func.count(ProjectRecord.id)).where(*filters)

        total = self.db.execute(count_statement).scalar_one()

        offset = (page - 1) * page_size

        statement = (
            select(ProjectRecord)
            .where(*filters)
            .order_by(ProjectRecord.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )

        records = list(self.db.execute(statement).scalars().all())

        return records, total

    # Update vehicle records
    def update(
        self,
        project_id: int,
        record_id: int,
        data: dict,
    ) -> ProjectRecord:
        try:
            statement = select(ProjectRecord).where(
                ProjectRecord.id == record_id,
                ProjectRecord.project_id == project_id,
            )

            record = self.db.execute(statement).scalar_one_or_none()

            if record is None:
                raise ValueError("Vehicle record not found.")

            record.data = data

            self.db.commit()
            self.db.refresh(record)

            return record

        except SQLAlchemyError:
            self.db.rollback()
            raise
