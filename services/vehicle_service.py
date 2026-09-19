from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from repositories.project_record_repository import ProjectRecordRepository
from models.project_record import ProjectRecord
from schemas.vehicle import (
    ServiceCreate,
    VehicleCreate,
)
from uuid import uuid4


class VehicleService:

    def __init__(self, db: Session):
        self.repository = ProjectRecordRepository(db)

    def get_today(
        self,
        project_id: int,
        page: int,
        page_size: int,
    ):
        return self.repository.get_today(
            project_id=project_id,
            page=page,
            page_size=page_size,
        )

    def get_all(
        self,
        project_id: int,
        page: int,
        page_size: int,
        search: str | None = None,
    ):
        return self.repository.get_all(
            project_id=project_id,
            page=page,
            page_size=page_size,
            search=search,
        )

    def create(
        self,
        project_id: int,
        vehicle: VehicleCreate,
    ):
        # Business validation
        if not vehicle.plateNumber:
            raise ValueError("Plate number is required.")

        if not vehicle.make:
            raise ValueError("Vehicle make is required.")

        if not vehicle.model:
            raise ValueError("Vehicle model is required.")

        if not vehicle.ownerName:
            raise ValueError("Owner name is required.")

        plate_number = vehicle.plateNumber.strip()
        if self.repository.exists_by_plate_number(
            project_id=project_id,
            plate_number=plate_number,
        ):
            raise ValueError(
                f"Vehicle with plate number '{plate_number}' already exists."
            )

        return self.repository.create(
            project_id=project_id,
            data=vehicle.model_dump(),
        )

    def create_service(
        self,
        project_id: int,
        record_id: int,
        service: ServiceCreate,
    ):
        service_data = {
            "id": str(uuid4()),
            **service.model_dump(),
        }

        return self.repository.add_service(
            project_id=project_id,
            record_id=record_id,
            service=service_data,
        )

    def update(
        self,
        project_id: int,
        record_id: int,
        vehicle: VehicleCreate,
    ):
        if not vehicle.plateNumber:
            raise ValueError("Plate number is required.")

        if not vehicle.make:
            raise ValueError("Vehicle make is required.")

        if not vehicle.model:
            raise ValueError("Vehicle model is required.")

        if not vehicle.ownerName:
            raise ValueError("Vehicle owner name is required.")

        plate_number = vehicle.plateNumber.strip()

        statement = select(ProjectRecord.id).where(
            ProjectRecord.project_id == project_id,
            ProjectRecord.data["plateNumber"].as_string() == plate_number,
            ProjectRecord.id != record_id,
        )

        existing_id = self.repository.db.execute(statement).scalar_one_or_none()

        if existing_id is not None:
            raise ValueError(
                f"Vehicle with plate number '{plate_number}' already exists."
            )

        return self.repository.update(
            project_id=project_id,
            record_id=record_id,
            data=vehicle.model_dump(),
        )
