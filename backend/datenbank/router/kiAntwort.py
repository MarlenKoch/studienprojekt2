from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..datenbank import get_db
from ..crud import (
    create_kiantwort,
    get_kiantwort,
    get_kiantworten,
    update_kiantwort,
    delete_kiantwort,
    get_kiantworten_fuer_notiz,
)
from ..pydanticModelle import KiAntwortCreate, KiAntwortResponse, KiAntwortUpdate

router = APIRouter()


@router.post("/", response_model=KiAntwortResponse)
def create_kiantwort_endpoint(payload: KiAntwortCreate, db: Session = Depends(get_db)):
    return create_kiantwort(db, payload)


@router.get("/", response_model=list[KiAntwortResponse])
def get_kiantworten_endpoint(db: Session = Depends(get_db)):
    return get_kiantworten(db)


@router.get("/{kiantwort_id}", response_model=KiAntwortResponse)
def get_kiantwort_endpoint(kiantwort_id: int, db: Session = Depends(get_db)):
    kiantwort = get_kiantwort(db, kiantwort_id)
    if not kiantwort:
        raise HTTPException(status_code=404, detail="KI-Antwort nicht gefunden")
    return kiantwort


@router.put("/{kiantwort_id}", response_model=KiAntwortResponse)
def update_kiantwort_endpoint(
    kiantwort_id: int, payload: KiAntwortUpdate, db: Session = Depends(get_db)
):
    updated = update_kiantwort(db, kiantwort_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="KI-Antwort nicht gefunden")
    return updated


@router.delete("/{kiantwort_id}", response_model=KiAntwortResponse)
def delete_kiantwort_endpoint(kiantwort_id: int, db: Session = Depends(get_db)):
    deleted = delete_kiantwort(db, kiantwort_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="KI-Antwort nicht gefunden")
    return deleted


@router.get("/notiz/{notiz_id}", response_model=list[KiAntwortResponse])
def get_kiantworten_fuer_notiz_endpoint(notiz_id: int, db: Session = Depends(get_db)):
    return get_kiantworten_fuer_notiz(db, notiz_id)
