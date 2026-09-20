from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.dashboard import DashboardAnalyticsData, DashboardAnalyticsResponse
from services.dashboard_service import DashboardService
from utils.dependencies import require_role

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/analytics",
    response_model=DashboardAnalyticsResponse,
)
def get_dashboard_analytics(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    """
    Get dashboard financial analytics for the selected month.
    """

    service = DashboardService(db=db)

    try:
        stats = service.get_analytics(
            project_id=current_user.project_id,
            year=year,
            month=month,
        )

        data = DashboardAnalyticsData(
            total_vehicles=stats["total_vehicles"],
            service_records=stats["service_records"],
            financial=stats["financial"],
        )

        return DashboardAnalyticsResponse(
            status=True,
            message="Dashboard analytics retrieved successfully.",
            data=data,
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve dashboard analytics.",
        )