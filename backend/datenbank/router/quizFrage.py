from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..datenbank import get_db
from ..crud import (
    create_quiz_frage,
    get_quiz_frage,
    get_quiz_fragen,
    update_quiz_frage,
    delete_quiz_frage,
)
from ..pydanticModelle import QuizFrageCreate, QuizFrageResponse, QuizFrageUpdate

router = APIRouter()


@router.post("/", response_model=QuizFrageResponse)
def create_quiz_frage_endpoint(payload: QuizFrageCreate, db: Session = Depends(get_db)):
    return create_quiz_frage(db, payload)


@router.get("/", response_model=list[QuizFrageResponse])
def get_quiz_fragen_endpoint(db: Session = Depends(get_db)):
    return get_quiz_fragen(db)


@router.get("/{quiz_frage_id}", response_model=QuizFrageResponse)
def get_quiz_frage_endpoint(quiz_frage_id: int, db: Session = Depends(get_db)):
    quiz_frage = get_quiz_frage(db, quiz_frage_id)
    if not quiz_frage:
        raise HTTPException(status_code=404, detail="Quiz-Frage nicht gefunden")
    return quiz_frage


@router.put("/{quiz_frage_id}", response_model=QuizFrageResponse)
def update_quiz_frage_endpoint(
    quiz_frage_id: int, payload: QuizFrageUpdate, db: Session = Depends(get_db)
):
    updated = update_quiz_frage(db, quiz_frage_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Quiz-Frage nicht gefunden")
    return updated


@router.delete("/{quiz_frage_id}", response_model=QuizFrageResponse)
def delete_quiz_frage_endpoint(quiz_frage_id: int, db: Session = Depends(get_db)):
    deleted = delete_quiz_frage(db, quiz_frage_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Quiz-Frage nicht gefunden")
    return deleted
