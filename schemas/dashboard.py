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


# ============================================================
# INCOME PART
# ============================================================

class DashboardIncomePart(BaseModel):
    id: str | None = None
    name: str
    quantity: float
    price: float
    total: float


# ============================================================
# INCOME RECORD
# ============================================================

class DashboardIncomeRecord(BaseModel):
    vehicle: str
    plate_number: str
    owner_name: str
    service_id: str | None = None
    service_performed: str
    service_income: float
    parts: list[DashboardIncomePart]


# ============================================================
# DAILY ANALYTICS
# ============================================================

class DashboardDailyAnalytics(BaseModel):
    date: str
    income: float
    expenses: float
    balance: float
    income_records: list[DashboardIncomeRecord]


# ============================================================
# FINANCIAL ANALYTICS
# ============================================================

class DashboardFinancialAnalytics(BaseModel):
    month: str
    income: float
    expenses: float
    balance: float
    daily: list[DashboardDailyAnalytics]


# ============================================================
# DASHBOARD DATA
# ============================================================

class DashboardAnalyticsData(BaseModel):
    total_vehicles: int
    service_records: int
    financial: DashboardFinancialAnalytics


# ============================================================
# RESPONSE
# ============================================================

class DashboardAnalyticsResponse(BaseModel):
    status: bool
    message: str
    data: DashboardAnalyticsData