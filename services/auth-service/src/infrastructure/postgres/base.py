from infrastructure.postgres.database import metadata
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    metadata = metadata
