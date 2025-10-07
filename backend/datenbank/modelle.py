from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from .datenbank import Base

# Zuordnungstabelle Notiz/Datei
notiz_datei = Table( "notiz_datei", Base.metadata, Column("notiz_id", ForeignKey("notizen.id"), primary_key=True), Column("datei_id", ForeignKey("dateien.id"), primary_key=True), )

datei_quizsession = Table( "datei_quizsession", Base.metadata, Column("datei_id", ForeignKey("dateien.id"), primary_key=True), Column("quiz_session_id", ForeignKey("quizSessions.id"), primary_key=True), )


    
# Speichern von Dateien
class Datei(Base):
    __tablename__="dateien"
    
    id = Column(Integer, primary_key=True, index=True)
    titel = Column(String, index=True, nullable=False)
    pfad = Column(String, index=True,nullable=False)
    dateiart = Column(String, index=True, nullable=True)
    dozent = Column(String, index=True, nullable=True)
    semester = Column(String, index=True, nullable=True)
    modul = Column(String, index=True, nullable=True)
    
    quiz_sessions = relationship("QuizSession", secondary=datei_quizsession, back_populates="dateien")
    notizen = relationship("Notiz", secondary=notiz_datei, back_populates="dateien")

    
# Speichern von Notizen
class Notiz(Base):
    __tablename__="notizen"
    
    id = Column(Integer, primary_key=True, index=True)
    titel = Column(String, index=True, nullable=False)
    labels = Column(JSON, nullable=False, nullable=False)
    reihenfolgeKiAntworten = Column(JSON, nullable=False, default=list)

    kiAntworten = relationship("KiAntwort", back_populates="notiz", cascade="all, delete-orphan")
    dateien = relationship("Datei", secondary=notiz_datei, back_populates="notizen")


# Speichern von KI-Antworten
class KiAntwort(Base):
    __tablename__="kiAntworten"
    
    id = Column(Integer, primary_key=True, index=True)
    inhalt = Column(String, index=True, nullable=True)
    kommentar = Column(String, index=True, nullable=True)
    typ = Column(String, index=True, nullable=True)

    notiz_id = Column(Integer, ForeignKey("notizen.id"), nullable=False, index=True)
    notiz = relationship("Notiz", back_populates="kiAntworten")
    
    
 # Speichern von Quiz-Sessions
class QuizSession(Base):
    __tablename__="quizSessions"
    
    id = Column(Integer, primary_key=True, index=True)
    titel = Column(String, index=True, nullable=False)

    fragen = relationship("QuizFrage", back_populates="quiz_session", cascade="all, delete-orphan")
    dateien = relationship("Datei", secondary=datei_quizsession, back_populates="quiz_sessions")


    
# Speichern von Quiz-Fragen
class QuizFrage(Base):
    __tablename__="quizFragen"
    
    id = Column(Integer, primary_key=True, index=True)
    frage = Column(String, index=True, nullable=False)
    Antwort = Column(String, index=True, nullable=False)
    Erklaerung = Column(String, index=True, nullable=False)

    quiz_session_id = Column(Integer, ForeignKey("quizSessions.id"), nullable=False, index=True)
    quiz_session = relationship("QuizSession", back_populates="fragen")
    
    



