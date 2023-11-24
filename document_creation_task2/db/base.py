from sqlalchemy.orm import DeclarativeBase

from document_creation_task2.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
