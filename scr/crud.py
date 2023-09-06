from sqlalchemy.orm import Session

from . import models, schemas


def get_object_by_key(db: Session, key: int):
    return db.query(models.Object).filter(models.Object.key == key).first()


def create_object(db: Session, object: schemas.ObjectCreate):
    db_object = models.Object(key=object.key, Expires=object.Expires)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object