from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from configs.settings import settings
from api.users import router as users_router
from api.vehicle import router as vehicle_router
from api.auth import router as auth_router
from api.health import router as health_router
from api.dashboard import router as dashboard_router
from errors.handlers import validation_exception_handler

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aca-services.netlify.app",
        # "http://localhost:5173",
        # "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(vehicle_router)
app.include_router(dashboard_router)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)
