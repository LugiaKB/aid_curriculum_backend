"""
Base model with common fields
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime
from app.database.connection import Base


class BaseModel(Base):
    """
    Base model class with common fields
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
