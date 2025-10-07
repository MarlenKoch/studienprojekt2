from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


# Datei
class DateiCreate(BaseModel):
    titel: str
    pfad: str
    dateiart: Optional[str] = None
    dozent: Optional[str] = None
    semester: Optional[str] = None
    modul: Optional[str] = None


class DateiUpdate(BaseModel):
    titel: Optional[str] = None
    pfad: Optional[str] = None
    dateiart: Optional[str] = None
    dozent: Optional[str] = None
    semester: Optional[str] = None
    modul: Optional[str] = None


class DateiResponse(BaseModel):
    id: int
    titel: str
    pfad: str
    dateiart: Optional[str] = None
    dozent: Optional[str] = None
    semester: Optional[str] = None
    modul: Optional[str] = None

    class Config:
        orm_mode = True


# Notiz
class NotizCreate(BaseModel):
    titel: str
    labels: Dict[str, Any]
    reihenfolgeKiAntworten: List[Any] = Field(default_factory=list)


class NotizUpdate(BaseModel):
    titel: Optional[str] = None
    labels: Optional[Dict[str, Any]] = None
    reihenfolgeKiAntworten: Optional[List[Any]] = None


class NotizResponse(BaseModel):
    id: int
    titel: str
    labels: Dict[str, Any]
    reihenfolgeKiAntworten: List[Any] = Field(default_factory=list)

    class Config:
        orm_mode = True


# KiAntwort
class KiAntwortCreate(BaseModel):
    inhalt: Optional[str] = None
    kommentar: Optional[str] = None
    typ: Optional[str] = None
    notiz_id: int


class KiAntwortUpdate(BaseModel):
    inhalt: Optional[str] = None
    kommentar: Optional[str] = None
    typ: Optional[str] = None
    notiz_id: Optional[int] = None


class KiAntwortResponse(BaseModel):
    id: int
    inhalt: Optional[str] = None
    kommentar: Optional[str] = None
    typ: Optional[str] = None
    notiz_id: int

    class Config:
        orm_mode = True


# QuizSession
class QuizSessionCreate(BaseModel):
    titel: str


class QuizSessionUpdate(BaseModel):
    titel: Optional[str] = None


class QuizSessionResponse(BaseModel):
    id: int
    titel: str

    class Config:
        orm_mode = True


# QuizFrage
class QuizFrageCreate(BaseModel):
    frage: str
    Antwort: str
    Erklaerung: str
    quiz_session_id: int


class QuizFrageUpdate(BaseModel):
    frage: Optional[str] = None
    Antwort: Optional[str] = None
    Erklaerung: Optional[str] = None
    quiz_session_id: Optional[int] = None


class QuizFrageResponse(BaseModel):
    id: int
    frage: str
    Antwort: str
    Erklaerung: str
    quiz_session_id: int

    class Config:
        orm_mode = True