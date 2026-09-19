# api/routes/dashboard.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.dashboard import (
    DashboardStatsData,
    DashboardStatsResponse,
)
from services.dashboard_service import DashboardService
from utils.dependencies import require_role


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    service = DashboardService(db=db)

    try:
        stats = service.get_stats(
            project_id=current_user.project_id,
        )

        return DashboardStatsResponse(
            status=True,
            message="Dashboard statistics retrieved successfully.",
            data=DashboardStatsData(
                total_vehicles=stats["total_vehicles"],
                service_records=stats["service_records"],
                scheduled=stats["scheduled"],
                appointments=stats["appointments"],
            ),
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve dashboard statistics.",
        )