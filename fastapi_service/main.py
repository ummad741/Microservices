from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from pydantic import BaseModel
from passlib.context import CryptContext
import os

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("PG_PORT")

# Replace 'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}' with your database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(metadata=MetaData())

# Define your 'admins' table


class Admins(Base):
    __tablename__ = "Admins_admins"
    id = Column(Integer, primary_key=True, index=True)
    admins = Column(String, index=True)
    name = Column(String)
    age = Column(Integer)
    surname = Column(String)
    phone = Column(String)
    password = Column(String)
    gender = Column(String)




# factory code

# Create the table in the database
Base.metadata.create_all(bind=engine)

# Password hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminResponse(BaseModel):
    id: int
    admins: str
    name: str
    age: int
    surname: str
    phone: str
    password: str
    gender: str


class AdminCreate(BaseModel):
    admins: str
    name: str
    age: int
    surname: str
    phone: str
    password: str
    gender: str


app = FastAPI()

# Dependency to get the database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI routes
@app.get("/admins/{admin_id}", response_model=AdminResponse)
def read_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admins).filter(Admins.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


@app.post("/admins/", response_model=AdminResponse)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    admin_db = Admins(**admin.dict())
    db.add(admin_db)
    db.commit()
    db.refresh(admin_db)
    return admin_db
