from collections.abc import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from configs.settings import settings


engine = create_engine(
    settings.database_url,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session

# Test connection to database if connected
# python -m database.connection
# with engine.connect() as connection:
#     result = connection.execute(text("SELECT 1"))
#     print(result.scalar())