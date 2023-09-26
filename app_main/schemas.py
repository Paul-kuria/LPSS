import uuid
from turtle import st
from typing import Optional

from pydantic import BaseModel


class MemberLog(BaseModel):
    # id: uuid.UUID
    name: str
    vehicle_type: str
    vehicle_color: str
    vehicle_plate: str

    class Config:
        from_attributes = True


class VisitorLog(BaseModel):
    id: int
    name: str
    vehicle_type: str
    vehicle_color: str
    vehicle_plate: str

    class Config:
        from_attributes = True


class EntranceLogs(BaseModel):
    id: int
    vehicle_plate: str
    entry_status: bool

    class Config:
        from_attributes = True


class MemberUpdate(BaseModel):
    name: str
    vehicle_type: str
    vehicle_color: str
