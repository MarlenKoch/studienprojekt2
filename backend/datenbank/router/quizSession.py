from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..datenbank import get_db
from ..crud import (
    create_quiz_session,
    get_quiz_session,
    get_quiz_sessions,
    update_quiz_session,
    delete_quiz_session,
    get_quiz_fragen_fuer_session,
    get_dateien_fuer_quiz_session,
    link_datei_zu_quiz_session,
    unlink_datei_von_quiz_session,
)
from ..pydanticModelle import QuizSessionCreate, QuizSessionResponse, QuizSessionUpdate, QuizFrageResponse, DateiResponse

router = APIRouter()


@router.post("/", response_model=QuizSessionResponse)
def create_quiz_session_endpoint(payload: QuizSessionCreate, db: Session = Depends(get_db)):
    return create_quiz_session(db, payload)


@router.get("/", response_model=list[QuizSessionResponse])
def get_quiz_sessions_endpoint(db: Session = Depends(get_db)):
    return get_quiz_sessions(db)


@router.get("/{quiz_session_id}", response_model=QuizSessionResponse)
def get_quiz_session_endpoint(quiz_session_id: int, db: Session = Depends(get_db)):
    quiz_session = get_quiz_session(db, quiz_session_id)
    if not quiz_session:
        raise HTTPException(status_code=404, detail="Quiz-Session nicht gefunden")
    return quiz_session


@router.put("/{quiz_session_id}", response_model=QuizSessionResponse)
def update_quiz_session_endpoint(
    quiz_session_id: int, payload: QuizSessionUpdate, db: Session = Depends(get_db)
):
    updated = update_quiz_session(db, quiz_session_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Quiz-Session nicht gefunden")
    return updated


@router.delete("/{quiz_session_id}", response_model=QuizSessionResponse)
def delete_quiz_session_endpoint(quiz_session_id: int, db: Session = Depends(get_db)):
    deleted = delete_quiz_session(db, quiz_session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Quiz-Session nicht gefunden")
    return deleted


@router.get("/{quiz_session_id}/fragen", response_model=list[QuizFrageResponse])
def get_quiz_fragen_fuer_session_endpoint(quiz_session_id: int, db: Session = Depends(get_db)):
    return get_quiz_fragen_fuer_session(db, quiz_session_id)


@router.get("/{quiz_session_id}/dateien", response_model=list[DateiResponse])
def get_dateien_fuer_quiz_session_endpoint(quiz_session_id: int, db: Session = Depends(get_db)):
    return get_dateien_fuer_quiz_session(db, quiz_session_id)


@router.post("/{quiz_session_id}/dateien/{datei_id}")
def link_datei_zu_quiz_session_endpoint(
    quiz_session_id: int, datei_id: int, db: Session = Depends(get_db)
):
    result = link_datei_zu_quiz_session(db, quiz_session_id, datei_id)
    if not result:
        raise HTTPException(status_code=404, detail="Quiz-Session oder Datei nicht gefunden")
    return {"message": "Datei erfolgreich mit Quiz-Session verknüpft"}


@router.delete("/{quiz_session_id}/dateien/{datei_id}")
def unlink_datei_von_quiz_session_endpoint(
    quiz_session_id: int, datei_id: int, db: Session = Depends(get_db)
):
    result = unlink_datei_von_quiz_session(db, quiz_session_id, datei_id)
    if not result:
        raise HTTPException(status_code=404, detail="Quiz-Session oder Datei nicht gefunden")
    return {"message": "Datei erfolgreich von Quiz-Session getrennt"}
