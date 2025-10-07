from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..datenbank import get_db
from ..crud import (
    create_notiz,
    get_notiz,
    get_notizen,
    update_notiz,
    delete_notiz,
    get_dateien_fuer_notiz,
    get_kiantworten_fuer_notiz,
    link_datei_zu_notiz,
    unlink_datei_von_notiz,
)
from ..pydanticModelle import NotizCreate, NotizResponse, NotizUpdate, DateiResponse, KiAntwortResponse

router = APIRouter()


@router.post("/", response_model=NotizResponse)
def create_notiz_endpoint(payload: NotizCreate, db: Session = Depends(get_db)):
    return create_notiz(db, payload)


@router.get("/", response_model=list[NotizResponse])
def get_notizen_endpoint(db: Session = Depends(get_db)):
    return get_notizen(db)


@router.get("/{notiz_id}", response_model=NotizResponse)
def get_notiz_endpoint(notiz_id: int, db: Session = Depends(get_db)):
    notiz = get_notiz(db, notiz_id)
    if not notiz:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")
    return notiz


@router.put("/{notiz_id}", response_model=NotizResponse)
def update_notiz_endpoint(
    notiz_id: int, payload: NotizUpdate, db: Session = Depends(get_db)
):
    updated = update_notiz(db, notiz_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")
    return updated


@router.delete("/{notiz_id}", response_model=NotizResponse)
def delete_notiz_endpoint(notiz_id: int, db: Session = Depends(get_db)):
    deleted = delete_notiz(db, notiz_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")
    return deleted

@router.get("/{notiz_id}/dateien", response_model=list[DateiResponse])
def get_dateien_fuer_notiz_endpoint(notiz_id: int, db: Session = Depends(get_db)):
    return get_dateien_fuer_notiz(db, notiz_id)

@router.get("/{notiz_id}/kiantworten", response_model=list[KiAntwortResponse])
def get_kiantworten_fuer_notiz_endpoint(notiz_id: int, db: Session = Depends(get_db)):
    return get_kiantworten_fuer_notiz(db, notiz_id)

@router.post("/{notiz_id}/dateien/{datei_id}")
def link_datei_zu_notiz_endpoint(
    notiz_id: int, datei_id: int, db: Session = Depends(get_db)
):
    result = link_datei_zu_notiz(db, notiz_id, datei_id)
    if not result:
        raise HTTPException(status_code=404, detail="Notiz oder Datei nicht gefunden")
    return {"message": "Datei erfolgreich mit Notiz verknüpft"}

@router.delete("/{notiz_id}/dateien/{datei_id}")
def unlink_datei_von_notiz_endpoint(
    notiz_id: int, datei_id: int, db: Session = Depends(get_db)
):
    result = unlink_datei_von_notiz(db, notiz_id, datei_id)
    if not result:
        raise HTTPException(status_code=404, detail="Notiz oder Datei nicht gefunden")
    return {"message": "Datei erfolgreich von Notiz getrennt"}
