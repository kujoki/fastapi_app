import json

import prometheus_client
import redis
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response
from prometheus_client import Counter, Histogram
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

_INF = float("inf")


def save_cache(key, value):
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    value_str = json.dumps(value.to_json())
    redis_client.set(key, value_str)


def load_cache():
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    cache = {}
    for key in redis_client.keys():
        value = redis_client.get(key)
        value = json.loads(value)
        cache[key] = value
    return cache


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/objects/", response_model=schemas.Object)
def create_object(object: schemas.ObjectCreate, db: Session = Depends(get_db)):
    db_object = crud.get_object_by_key(db, key=object.key)
    if db_object:
        raise HTTPException(
            status_code=400, detail="Объект с таким ключом уже существует"
        )
    # Кэшевое
    key = "object-%s" % object.key
    save_cache(key, object)
    return crud.create_object(db=db, object=object)


@app.get("/objects/{key}", response_model=schemas.Object)
def get_object_by_key(key: int, db: Session = Depends(get_db)):
    db_object = crud.get_object_by_key(db, key=key)
    if db_object is None:
        raise HTTPException(status_code=404, detail="Объект не найден")
    return db_object


router = APIRouter()


@router.get("/liveness/")
def liveness():
    return "OK"


@router.get("/readiness/")
def readiness():
    return "OK"


@app.get("/metrics/")
def requests_count():
    graphs = {}
    graphs["c"] = Counter(
        f"python_request_operations_total_by_user",
        "The total number of processed requests for user",
    )
    graphs["h"] = Histogram(
        f"python_request_duration_seconds_by_user",
        "Histogram for the duration in seconds for user.",
        buckets=(1, 2, 5, 6, 10, _INF),
    )
    res = []
    for k, v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(str(res), media_type="text/plain")


app.include_router(router)

if __name__ == "__main__":
    load_cache()
