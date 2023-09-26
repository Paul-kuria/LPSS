from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from psycopg2.errors import UniqueViolation
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/members", tags=["Member"])

"""create member account"""


@router.post("/create", response_model=schemas.MemberLog)
async def create_record(
    send_info: schemas.MemberLog,
    db: Session = Depends(get_db),
):
    new_registration = models.MemberLog(**send_info.model_dump())
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    return new_registration


"""Retrieve one account"""


@router.get("/{vehicle_plate}", response_model=schemas.MemberLog)
async def get_one_record(vehicle_plate: str, db: Session = Depends(get_db)):
    post = (
        db.query(models.MemberLog)
        .filter(models.MemberLog.vehicle_plate == vehicle_plate)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"member with vehicle: {vehicle_plate} was not found.",
        )
    return post


"""Update one account"""


@router.put("/{vehicle_plate}", response_model=schemas.MemberLog)
def update_record(
    vehicle_plate: str, updated_post: schemas.MemberLog, db: Session = Depends(get_db)
):
    update_query = db.query(models.MemberLog).filter(
        models.MemberLog.vehicle_plate == vehicle_plate
    )
    upd_record = update_query.first()

    if upd_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"member with vehicle: {vehicle_plate} does not exist",
        )
    update_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    returned_data = update_query.first()
    if returned_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plate has been updated"
        )
    return update_query.first()


"""Delete one account"""


@router.delete("/{vehicle_plate}")
def delete_record(vehicle_plate: str, db: Session = Depends(get_db)):
    delete_query = db.query(models.MemberLog).filter(
        models.MemberLog.vehicle_plate == vehicle_plate
    )
    entry = delete_query.first()

    if entry == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="member with vehicle: {vehicle_plate} does not exist",
        )

    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


"""Retrieve all accounts"""


@router.get("/all/", response_model=List[schemas.MemberLog])
def get_all_records(db: Session = Depends(get_db)):
    records = db.query(models.MemberLog).all()
    return records


"""Bulk Create Accounts"""


@router.post("/upload", response_model=List[schemas.MemberLog])
async def upload_multiple_records(
    upload_records_list: List[schemas.MemberLog], db: Session = Depends(get_db)
):
    all_records = []
    batch_size = 100

    # Load the records in as List of model objects to be updated
    for row in upload_records_list:
        row = row.model_dump()
        post = models.MemberLog(**row)
        all_records.append(post)

    # Handle transactions
    try:
        for i in range(0, len(upload_records_list), batch_size):
            batch = all_records[i : i + batch_size]
            try:
                db.bulk_save_objects(batch)
                db.commit()
            except UniqueViolation:
                db.rollback()
        return all_records
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while uploading records",
        )
