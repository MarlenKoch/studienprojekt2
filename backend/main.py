from fastapi import FastAPI
from datenbank.datenbank import engine
from datenbank.modelle import Base
from datenbank.router import dateien, notizen, kiAntwort, quizSession, quizFrage

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lernassistent API",
    description="API für den Lernassistenten mit Dateien, Notizen, KI-Antworten, Quiz-Sessions und Quiz-Fragen",
    version="1.0.0"
)

# Include routers
app.include_router(dateien.router, prefix="/api/dateien", tags=["Dateien"])
app.include_router(notizen.router, prefix="/api/notizen", tags=["Notizen"])
app.include_router(kiAntwort.router, prefix="/api/kiantworten", tags=["KI-Antworten"])
app.include_router(quizSession.router, prefix="/api/quiz-sessions", tags=["Quiz-Sessions"])
app.include_router(quizFrage.router, prefix="/api/quiz-fragen", tags=["Quiz-Fragen"])

@app.get("/")
async def root():
    return {"message": "Lernassistent API - Alle Endpunkte verfügbar"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API läuft erfolgreich"}
