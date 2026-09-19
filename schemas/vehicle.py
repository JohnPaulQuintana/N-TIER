from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class Part(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    price: int | None = Field(default=None, ge=0)


class VehicleService(BaseModel):
    id: str = Field(min_length=1)
    serviceDate: str = Field(min_length=1)
    technician: str | None = None
    servicePerformed: str | None = None
    parts: list[Part] = Field(min_length=1)

class ServiceCreateData(BaseModel):
    vehicle_id: int
    service_id: str


class ServiceCreateResponse(BaseModel):
    status: bool
    message: str
    data: ServiceCreateData | None = None
    
class VehicleCreate(BaseModel):
    plateNumber: str = Field(
        min_length=1,
        max_length=20,
    )

    year: str | None = None

    make: str = Field(
        min_length=1,
        max_length=100,
    )

    model: str = Field(
        min_length=1,
        max_length=150,
    )

    ownerName: str = Field(
        min_length=1,
        max_length=150,
    )

    contactNumber: str = Field(
        min_length=11,
        max_length=11,
        pattern=r"^\d{11}$",
    )

    address: str = Field(
        min_length=1,
    )

    services: list[VehicleService] = Field(
        default_factory=list,
    )

    @field_validator(
        "plateNumber",
        "make",
        "model",
        "ownerName",
        "contactNumber",
        "address",
        "year",
        mode="before",
    )
    @classmethod
    def strip_strings(cls, value):
        if isinstance(value, str):
            return value.strip()

        return value


class ServiceCreate(BaseModel):
    serviceDate: str = Field(
        min_length=1,
    )

    technician: str | None = None

    servicePerformed: str | None = None

    parts: list[Part] = Field(
        min_length=1,
    )

    @field_validator(
        "serviceDate",
        "technician",
        "servicePerformed",
        mode="before",
    )
    @classmethod
    def strip_strings(cls, value):
        if isinstance(value, str):
            return value.strip()

        return value


class VehicleCreateData(BaseModel):
    id: int


class VehicleCreateResponse(BaseModel):
    status: bool
    message: str
    data: VehicleCreateData | None = None


# Get Today Inserted Data | Get All
class VehicleTodayData(BaseModel):
    id: int
    data: dict
    created_at: datetime
    updated_at: datetime


class VehicleTodayResponse(BaseModel):
    status: bool
    message: str
    data: list[VehicleTodayData]
    page: int
    page_size: int
    total: int
    total_pages: int


# Update Records
class VehicleUpdateData(BaseModel):
    id: int


class VehicleUpdateResponse(BaseModel):
    status: bool
    message: str
    data: VehicleUpdateData | None = None