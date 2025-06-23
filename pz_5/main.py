from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel



class CadetBase(BaseModel):
    name: str
    rank: str


class CadetCreate(CadetBase):
    pass


class Cadet(CadetBase):
    id: int

    class Config:
        orm_mode = True



SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class DBCadet(Base):
    __tablename__ = "cadets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rank = Column(String)


Base.metadata.create_all(bind=engine)

app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cadets/", response_model=Cadet)
def create_cadet(cadet: CadetCreate, db: Session = Depends(get_db)):
    db_cadet = DBCadet(**cadet.dict())
    db.add(db_cadet)
    db.commit()
    db.refresh(db_cadet)
    return db_cadet


@app.get("/cadets/", response_model=List[Cadet])
def read_cadets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cadets = db.query(DBCadet).offset(skip).limit(limit).all()
    return cadets


@app.get("/cadets/{cadet_id}", response_model=Cadet)
def read_cadet(cadet_id: int, db: Session = Depends(get_db)):
    cadet = db.query(DBCadet).filter(DBCadet.id == cadet_id).first()
    if cadet is None:
        raise HTTPException(status_code=404, detail="Курсант не найден")
    return cadet


@app.put("/cadets/{cadet_id}", response_model=Cadet)
def update_cadet(cadet_id: int, cadet: CadetCreate, db: Session = Depends(get_db)):
    db_cadet = db.query(DBCadet).filter(DBCadet.id == cadet_id).first()
    if db_cadet is None:
        raise HTTPException(status_code=404, detail="Курсант не найден")
    for var, value in vars(cadet).items():
        setattr(db_cadet, var, value) if value else None
    db.add(db_cadet)
    db.commit()
    db.refresh(db_cadet)
    return db_cadet


@app.delete("/cadets/{cadet_id}")
def delete_cadet(cadet_id: int, db: Session = Depends(get_db)):
    db_cadet = db.query(DBCadet).filter(DBCadet.id == cadet_id).first()
    if db_cadet is None:
        raise HTTPException(status_code=404, detail="Курсант не найден")
    db.delete(db_cadet)
    db.commit()
    return {"message": "Курсант удален"}