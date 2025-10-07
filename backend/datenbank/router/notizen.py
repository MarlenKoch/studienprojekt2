from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datenbank import get_db
from crud import (
    create_notiz,
    get_notiz,
    get_notizen,
    update_notiz,
    delete_notiz,
)
from pydanticModelle import NotizCreate, NotizResponse, NotizUpdate

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
