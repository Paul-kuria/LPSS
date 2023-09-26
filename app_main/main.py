from fastapi import FastAPI

from . import models
from .database import engine, get_db
from .routers import tenants, visitors

"""Instance"""
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(tenants.router)


@app.get("/")
def root():
    return {"message": "ANPR Project"}
