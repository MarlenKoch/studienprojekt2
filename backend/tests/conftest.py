import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from datenbank.datenbank import get_db
from datenbank.modelle import Base

# Test-Datenbank (In-Memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override der Datenbank-Dependency für Tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """Erstellt eine frische Test-Datenbank für jeden Test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Test-Client mit Override der Datenbank-Dependency"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_datei_data():
    """Beispiel-Daten für Datei-Tests"""
    return {
        "titel": "Test Mathematik Vorlesung",
        "pfad": "/test/mathe_vorlesung.pdf",
        "dateiart": "PDF",
        "dozent": "Prof. Dr. Test",
        "semester": "WS 2024/25",
        "modul": "Mathematik I"
    }


@pytest.fixture
def sample_notiz_data():
    """Beispiel-Daten für Notiz-Tests"""
    return {
        "titel": "Test Notiz",
        "labels": {
            "fach": "Mathematik",
            "schwierigkeit": "mittel",
            "thema": "Lineare Algebra"
        },
        "reihenfolgeKiAntworten": [1, 2, 3]
    }


@pytest.fixture
def sample_kiantwort_data():
    """Beispiel-Daten für KI-Antwort-Tests"""
    return {
        "inhalt": "Test KI-Antwort Inhalt",
        "kommentar": "Test Kommentar",
        "typ": "Definition",
        "notiz_id": 1
    }


@pytest.fixture
def sample_quiz_session_data():
    """Beispiel-Daten für Quiz-Session-Tests"""
    return {
        "titel": "Test Quiz Session"
    }


@pytest.fixture
def sample_quiz_frage_data():
    """Beispiel-Daten für Quiz-Frage-Tests"""
    return {
        "frage": "Was ist eine Test-Frage?",
        "Antwort": "Eine Frage zum Testen",
        "Erklaerung": "Dies ist eine Erklärung für Test-Zwecke",
        "quiz_session_id": 1
    }
