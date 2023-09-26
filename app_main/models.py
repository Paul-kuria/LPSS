import uuid

from sqlalchemy import TIMESTAMP, UUID, VARCHAR, Boolean, Column, Integer, String, null
from sqlalchemy.sql.expression import text

from .database import Base


class MemberLog(Base):
    __tablename__ = "member_registry"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)  # UUID column
    name = Column(String, nullable=False)
    vehicle_type = Column(VARCHAR(50), nullable=False)
    vehicle_color = Column(VARCHAR(30), nullable=False)
    vehicle_plate = Column(VARCHAR(30), unique=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class logEntrance(Base):
    __tablename__ = "entrance_log"

    id = Column(Integer, nullable=False, primary_key=True)
    vehicle_plate = Column(VARCHAR(50), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    entry_status = Column(Boolean, server_default="TRUE", nullable=False)
    # owner_name = Column(String, ForeignKey("member_registry.name", ondelete="CASCADE"), nullable=False)


class VisitLog(Base):
    __tablename__ = "visitors_registry"

    id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    vehicle_type = Column(VARCHAR(50), nullable=False)
    vehicle_color = Column(VARCHAR(30), nullable=False)
    vehicle_plate = Column(VARCHAR(30), primary_key=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    # host = Column(Integer, ForeignKey("member_registry.id", ondelete="CASCADE"), nullable=False)
