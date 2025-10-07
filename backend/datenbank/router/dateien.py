from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..datenbank import get_db
from ..crud import (
    create_datei,
    get_datei,
    get_dateien,
    update_datei,
    delete_datei,
    get_notizen_fuer_datei,
    get_quiz_sessions_fuer_datei,
)
from ..pydanticModelle import DateiCreate, DateiResponse, DateiUpdate, NotizResponse, QuizSessionResponse


router = APIRouter()

@router.post("/", response_model=DateiResponse)
def create_datei_endpoint(payload: DateiCreate, db: Session = Depends(get_db)):
    return create_datei(db, payload)

@router.get("/", response_model=list[DateiResponse])
def get_dateien_endpoint(db: Session = Depends(get_db)):
    return get_dateien(db)

@router.get("/{datei_id}", response_model=DateiResponse)
def get_datei_endpoint(datei_id: int, db: Session = Depends(get_db)):
    datei = get_datei(db, datei_id)
    if not datei:
        raise HTTPException(status_code=404, detail="Datei nicht gefunden")
    return datei

@router.put("/{datei_id}", response_model=DateiResponse)
def update_datei_endpoint(datei_id: int, payload: DateiUpdate, db: Session = Depends(get_db)):
    updated = update_datei(db, datei_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Datei nicht gefunden")
    return updated

@router.delete("/{datei_id}", response_model=DateiResponse)
def delete_datei_endpoint(datei_id: int, db: Session = Depends(get_db)):
    deleted = delete_datei(db, datei_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Datei nicht gefunden")
    return deleted

@router.get("/{datei_id}/notizen", response_model=list[NotizResponse])
def get_notizen_fuer_datei_endpoint(datei_id: int, db: Session = Depends(get_db)):
    return get_notizen_fuer_datei(db, datei_id)

@router.get("/{datei_id}/quiz-sessions", response_model=list[QuizSessionResponse])
def get_quiz_sessions_fuer_datei_endpoint(datei_id: int, db: Session = Depends(get_db)):
    return get_quiz_sessions_fuer_datei(db, datei_id)
