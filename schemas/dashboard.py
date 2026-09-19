from pydantic import BaseModel


class DashboardStatsData(BaseModel):
    total_vehicles: int
    service_records: int
    scheduled: int
    appointments: int


class DashboardStatsResponse(BaseModel):
    status: bool
    message: str
    data: DashboardStatsData