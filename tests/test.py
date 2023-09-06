import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.main import app, get_db

from scr import crud, schemas

client = TestClient(app)

SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///./sql_app_test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.mark.unit
def test_create_object(db: Session = Depends(get_db)):
    object = schemas.ObjectCreate(key=42, Expires=datetime.now())
    db_object = crud.create_object(db=db, object=object)

    assert db_object.key == object.key
    assert db_object.Expires == object.Expires


@pytest.mark.unit
def test_get_object_by_key(db: Session = Depends(get_db)):
    object = schemas.ObjectCreate(key=42, Expires=datetime.now())
    db_object = crud.create_object(db=db, object=object)

    get_object = crud.get_object_by_key(db=db, key=object.key)

    assert get_object.key == object.key
    assert get_object.Expires == object.Expires
