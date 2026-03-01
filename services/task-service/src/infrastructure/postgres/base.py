from sqlalchemy.orm import DeclarativeBase
from infrastructure.postgres.database import metadata


class Base(DeclarativeBase):
    metadata = metadata