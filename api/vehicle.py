from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query
from utils.dependencies import get_current_user, require_role
from schemas.vehicle import (
    VehicleCreate,
    VehicleCreateData,
    VehicleCreateResponse,
    VehicleTodayData,
    VehicleTodayResponse,
    VehicleUpdateResponse,
    VehicleUpdateData,
    ServiceCreate,
    ServiceCreateData,
    ServiceCreateResponse,
)
from services.vehicle_service import VehicleService
from database.connection import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicle"],
)


@router.get(
    "/all",
    response_model=VehicleTodayResponse,
)
def get_all(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    service = VehicleService(db=db)

    try:
        project_id = current_user.project_id

        records, total = service.get_all(
            project_id=project_id,
            page=page,
            page_size=page_size,
            search=search,
        )

        total_pages = ceil(total / page_size) if total > 0 else 0

        return VehicleTodayResponse(
            status=True,
            message="Vehicles retrieved successfully.",
            data=[
                VehicleTodayData(
                    id=record.id,
                    data=record.data,
                    created_at=record.created_at,
                    updated_at=record.updated_at,
                )
                for record in records
            ],
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve vehicles.",
        )


@router.get(
    "/today",
    response_model=VehicleTodayResponse,
)
def get_today(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    service = VehicleService(db=db)

    try:
        project_id = current_user.project_id

        records, total = service.get_today(
            project_id=project_id,
            page=page,
            page_size=page_size,
        )

        total_pages = ceil(total / page_size) if total > 0 else 0

        return VehicleTodayResponse(
            status=True,
            message="Today's vehicles retrieved successfully.",
            data=[
                VehicleTodayData(
                    id=record.id,
                    data=record.data,
                    created_at=record.created_at,
                    updated_at=record.updated_at,
                )
                for record in records
            ],
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve today's vehicles.",
        )


@router.post(
    "/insert",
    response_model=VehicleCreateResponse,
)
def create(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    service = VehicleService(db=db)

    try:
        project_id = current_user.project_id

        vehicle_record = service.create(
            project_id=project_id,
            vehicle=vehicle,
        )

        return VehicleCreateResponse(
            status=True,
            message="Vehicle created successfully.",
            data=VehicleCreateData(
                id=vehicle_record.id,
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Failed to save vehicle record.",
        )


@router.post(
    "/{record_id}/services",
    response_model=ServiceCreateResponse,
)
def create_service(
    record_id: int,
    service: ServiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    vehicle_service = VehicleService(db=db)

    try:
        project_id = current_user.project_id

        record = vehicle_service.create_service(
            project_id=project_id,
            record_id=record_id,
            service=service,
        )

        service_id = record.data["services"][-1]["id"]

        return ServiceCreateResponse(
            status=True,
            message="Service added successfully.",
            data=ServiceCreateData(
                vehicle_id=record.id,
                service_id=service_id,
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Failed to add service.",
        )


@router.put(
    "/{record_id}",
    response_model=VehicleUpdateResponse,
)
def update(
    record_id: int,
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    service = VehicleService(db=db)

    try:
        project_id = current_user.project_id

        vehicle_record = service.update(
            project_id=project_id,
            record_id=record_id,
            vehicle=vehicle,
        )

        return VehicleUpdateResponse(
            status=True,
            message="Vehicle updated successfully.",
            data=VehicleUpdateData(
                id=vehicle_record.id,
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Failed to update vehicle record.",
        )
