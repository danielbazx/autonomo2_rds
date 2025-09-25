from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session
from sqlmodel import create_engine

rds_connectionstring= "postgresql://admin1:tY2u2)S8ErCS@database-2.cwha0ue2atiq.us-east-1.rds.amazonaws.com:5432/postgres"
engine = create_engine(rds_connectionstring, echo=True)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]   
