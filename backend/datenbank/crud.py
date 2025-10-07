from sqlalchemy.orm import Session
from classModelsForDB import Datei, Notiz, KiAntwort, QuizSession, QuizFrage
from dbSchemas import (
    DateiCreate, DateiUpdate,
    NotizCreate, NotizUpdate,
    KiAntwortCreate, KiAntwortUpdate,
    QuizSessionCreate, QuizSessionUpdate,
    QuizFrageCreate, QuizFrageUpdate,
)

# CRUD für Dateien
def get_dateien(db: Session):
    return db.query(Datei).all()


def get_datei(db: Session, dateiId: int):
    return db.query(Datei).filter(Datei.id == dateiId).first()


def create_datei(db: Session, datei_data: DateiCreate):
    db_datei = Datei(**datei_data.dict(exclude_unset=True))
    db.add(db_datei)
    db.commit()
    db.refresh(db_datei)
    return db_datei


def update_datei(db: Session, dateiId: int, datei_data: DateiUpdate):
    datei = get_datei(db, dateiId)
    if not datei:
        return None
    update_fields = datei_data.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(datei, key, value)
    db.commit()
    db.refresh(datei)
    return datei


def delete_datei(db: Session, dateiId: int):
    datei = get_datei(db, dateiId)
    if datei:
        db.delete(datei)
        db.commit()
        return datei
    return None


# CRUD für Notizen
def get_notizen(db: Session):
    return db.query(Notiz).all()


def get_notiz(db: Session, notizId: int):
    return db.query(Notiz).filter(Notiz.id == notizId).first()


def create_notiz(db: Session, notiz_data: NotizCreate):
    db_notiz = Notiz(**notiz_data.dict(exclude_unset=True))
    db.add(db_notiz)
    db.commit()
    db.refresh(db_notiz)
    return db_notiz


def update_notiz(db: Session, notizId: int, notiz_data: NotizUpdate):
    notiz = get_notiz(db, notizId)
    if not notiz:
        return None
    update_fields = notiz_data.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(notiz, key, value)
    db.commit()
    db.refresh(notiz)
    return notiz


def delete_notiz(db: Session, notizId: int):
    notiz = get_notiz(db, notizId)
    if notiz:
        db.delete(notiz)
        db.commit()
        return notiz
    return None


# CRUD für Ki-Antworten
def get_kiantworten(db: Session):
    return db.query(KiAntwort).all()


def get_kiantwort(db: Session, kiantwortId: int):
    return db.query(KiAntwort).filter(KiAntwort.id == kiantwortId).first()


def create_kiantwort(db: Session, kiantwort_data: KiAntwortCreate):
    db_kia = KiAntwort(**kiantwort_data.dict(exclude_unset=True))
    db.add(db_kia)
    db.commit()
    db.refresh(db_kia)
    return db_kia


def update_kiantwort(db: Session, kiantwortId: int, kiantwort_data: KiAntwortUpdate):
    kia = get_kiantwort(db, kiantwortId)
    if not kia:
        return None
    update_fields = kiantwort_data.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(kia, key, value)
    db.commit()
    db.refresh(kia)
    return kia


def delete_kiantwort(db: Session, kiantwortId: int):
    kia = get_kiantwort(db, kiantwortId)
    if kia:
        db.delete(kia)
        db.commit()
        return kia
    return None


# CRUD für Quiz-Sessions
def get_quiz_sessions(db: Session):
    return db.query(QuizSession).all()


def get_quiz_session(db: Session, quizSessionId: int):
    return db.query(QuizSession).filter(QuizSession.id == quizSessionId).first()


def create_quiz_session(db: Session, qs_data: QuizSessionCreate):
    db_qs = QuizSession(**qs_data.dict(exclude_unset=True))
    db.add(db_qs)
    db.commit()
    db.refresh(db_qs)
    return db_qs


def update_quiz_session(db: Session, quizSessionId: int, qs_data: QuizSessionUpdate):
    qs = get_quiz_session(db, quizSessionId)
    if not qs:
        return None
    update_fields = qs_data.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(qs, key, value)
    db.commit()
    db.refresh(qs)
    return qs


def delete_quiz_session(db: Session, quizSessionId: int):
    qs = get_quiz_session(db, quizSessionId)
    if qs:
        db.delete(qs)
        db.commit()
        return qs
    return None


# CRUD für Quiz-Fragen
def get_quiz_fragen(db: Session):
    return db.query(QuizFrage).all()


def get_quiz_frage(db: Session, quizFrageId: int):
    return db.query(QuizFrage).filter(QuizFrage.id == quizFrageId).first()


def create_quiz_frage(db: Session, frage_data: QuizFrageCreate):
    db_frage = QuizFrage(**frage_data.dict(exclude_unset=True))
    db.add(db_frage)
    db.commit()
    db.refresh(db_frage)
    return db_frage


def update_quiz_frage(db: Session, quizFrageId: int, frage_data: QuizFrageUpdate):
    frage = get_quiz_frage(db, quizFrageId)
    if not frage:
        return None
    update_fields = frage_data.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(frage, key, value)
    db.commit()
    db.refresh(frage)
    return frage


def delete_quiz_frage(db: Session, quizFrageId: int):
    frage = get_quiz_frage(db, quizFrageId)
    if frage:
        db.delete(frage)
        db.commit()
        return frage
    return None


# Besondere Anfragen / Relationen

# Notiz <-> Datei (Many-to-Many)
def get_dateien_fuer_notiz(db: Session, notizId: int):
    notiz = get_notiz(db, notizId)
    return notiz.dateien if notiz else []


def get_notizen_fuer_datei(db: Session, dateiId: int):
    datei = get_datei(db, dateiId)
    return datei.notizen if datei else []


def link_datei_zu_notiz(db: Session, notizId: int, dateiId: int):
    notiz = get_notiz(db, notizId)
    datei = get_datei(db, dateiId)
    if not notiz or not datei:
        return None
    if datei not in notiz.dateien:
        notiz.dateien.append(datei)
        db.commit()
        db.refresh(notiz)
    return notiz


def unlink_datei_von_notiz(db: Session, notizId: int, dateiId: int):
    notiz = get_notiz(db, notizId)
    datei = get_datei(db, dateiId)
    if not notiz or not datei:
        return None
    if datei in notiz.dateien:
        notiz.dateien.remove(datei)
        db.commit()
        db.refresh(notiz)
    return notiz


# Ki-Antworten zu einer Notiz
def get_kiantworten_fuer_notiz(db: Session, notizId: int):
    notiz = get_notiz(db, notizId)
    return notiz.antworten if notiz else []


# Quiz-Fragen zu einer Quiz-Session
def get_quiz_fragen_fuer_session(db: Session, quizSessionId: int):
    qs = get_quiz_session(db, quizSessionId)
    return qs.fragen if qs else []
