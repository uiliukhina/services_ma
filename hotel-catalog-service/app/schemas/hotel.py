from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.base_schema import Base


class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    city = Column(String, nullable=False)
    description = Column(String, nullable=False)
