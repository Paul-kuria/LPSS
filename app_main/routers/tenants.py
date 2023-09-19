from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session 
from typing import List 
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from pydantic import ValidationError
from .. import models, schemas
from ..database import get_db 


router = APIRouter(prefix="/members", tags=["Member"])

'''create member account'''
@router.post("/", response_model=schemas.MemberLog)
async def create_record(
    send_info: schemas.MemberLog,
    db: Session = Depends(get_db),
    ):

    new_registration = models.MemberLog(
        **send_info.model_dump()
    )
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    return new_registration

'''Retrieve one account'''
@router.get("/{vehicle_plate}", response_model=schemas.MemberLog)
async def get_one_record(
    vehicle_plate: str,
    db: Session = Depends(get_db)
):
    post = db.query(models.MemberLog).filter(models.MemberLog.vehicle_plate == vehicle_plate).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"member with vehicle: {vehicle_plate} was not found."
        )
    return post 

'''Update one account'''
@router.put("/{vehicle_plate}", response_model=schemas.MemberLog)
def update_record(
    vehicle_plate: str,
    updated_post: schemas.MemberLog,
    db: Session = Depends(get_db)
):
    update_query = db.query(models.MemberLog).filter(models.MemberLog.vehicle_plate == vehicle_plate)
    upd_record = update_query.first()

    if upd_record == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"member with vehicle: {vehicle_plate} does not exist",
        )
    update_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return update_query.first()

'''Delete one account'''
@router.delete("/{vehicle_plate}")
def delete_record(
    vehicle_plate: str,
    db: Session = Depends(get_db)
):
    delete_query = db.query(models.MemberLog).filter(models.MemberLog.vehicle_plate == vehicle_plate)
    entry = delete_query.first()

    if entry == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='member with vehicle: {vehicle_plate} does not exist',
        )
    
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


'''Retrieve all accounts'''
@router.get("/", response_model=List[schemas.MemberLog])
def get_all_records(db: Session = Depends(get_db)):
    records = db.query(models.MemberLog).all()
    return records