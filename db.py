from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session
from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

#rds_connectionstring= "postgresql://admin1:kMW(o-12K525@database-1.cwha0ue2atiq.us-east-1.rds.amazonaws.com:5432/postgres"
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(rds_connectionstring, echo=True)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]   
