import pytest
from fastapi.testclient import TestClient


class TestQuizSessionsAPI:
    """Tests für die Quiz-Sessions-API Endpunkte"""

    def test_create_quiz_session(self, client: TestClient, sample_quiz_session_data):
        """Test: Quiz-Session erstellen"""
        response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titel"] == sample_quiz_session_data["titel"]
        assert "id" in data

    def test_get_all_quiz_sessions_empty(self, client: TestClient):
        """Test: Alle Quiz-Sessions abrufen (leer)"""
        response = client.get("/api/quiz-sessions/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_quiz_sessions_with_data(self, client: TestClient, sample_quiz_session_data):
        """Test: Alle Quiz-Sessions abrufen (mit Daten)"""
        # Erst eine Quiz-Session erstellen
        create_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        assert create_response.status_code == 200

        # Dann alle Quiz-Sessions abrufen
        response = client.get("/api/quiz-sessions/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titel"] == sample_quiz_session_data["titel"]

    def test_get_quiz_session_by_id(self, client: TestClient, sample_quiz_session_data):
        """Test: Einzelne Quiz-Session abrufen"""
        # Erst eine Quiz-Session erstellen
        create_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        created_session = create_response.json()
        session_id = created_session["id"]

        # Dann die Quiz-Session abrufen
        response = client.get(f"/api/quiz-sessions/{session_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == session_id
        assert data["titel"] == sample_quiz_session_data["titel"]

    def test_get_quiz_session_not_found(self, client: TestClient):
        """Test: Nicht existierende Quiz-Session abrufen"""
        response = client.get("/api/quiz-sessions/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_update_quiz_session(self, client: TestClient, sample_quiz_session_data):
        """Test: Quiz-Session aktualisieren"""
        # Erst eine Quiz-Session erstellen
        create_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        created_session = create_response.json()
        session_id = created_session["id"]

        # Dann die Quiz-Session aktualisieren
        update_data = {
            "titel": "Aktualisierte Quiz-Session"
        }
        response = client.put(f"/api/quiz-sessions/{session_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titel"] == update_data["titel"]

    def test_update_quiz_session_not_found(self, client: TestClient):
        """Test: Nicht existierende Quiz-Session aktualisieren"""
        update_data = {"titel": "Neuer Titel"}
        response = client.put("/api/quiz-sessions/999", json=update_data)
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_delete_quiz_session(self, client: TestClient, sample_quiz_session_data):
        """Test: Quiz-Session löschen"""
        # Erst eine Quiz-Session erstellen
        create_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        created_session = create_response.json()
        session_id = created_session["id"]

        # Dann die Quiz-Session löschen
        response = client.delete(f"/api/quiz-sessions/{session_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == session_id

        # Überprüfen, dass die Quiz-Session wirklich gelöscht wurde
        get_response = client.get(f"/api/quiz-sessions/{session_id}")
        assert get_response.status_code == 404

    def test_delete_quiz_session_not_found(self, client: TestClient):
        """Test: Nicht existierende Quiz-Session löschen"""
        response = client.delete("/api/quiz-sessions/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_get_fragen_fuer_quiz_session_empty(self, client: TestClient, sample_quiz_session_data):
        """Test: Fragen für Quiz-Session abrufen (leer)"""
        # Erst eine Quiz-Session erstellen
        create_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        created_session = create_response.json()
        session_id = created_session["id"]

        # Fragen für die Quiz-Session abrufen
        response = client.get(f"/api/quiz-sessions/{session_id}/fragen")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_dateien_fuer_quiz_session_empty(self, client: TestClient, sample_quiz_session_data):
        """Test: Dateien für Quiz-Session abrufen (leer)"""
        # Erst eine Quiz-Session erstellen
        create_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        created_session = create_response.json()
        session_id = created_session["id"]

        # Dateien für die Quiz-Session abrufen
        response = client.get(f"/api/quiz-sessions/{session_id}/dateien")
        assert response.status_code == 200
        assert response.json() == []

    def test_link_datei_zu_quiz_session(self, client: TestClient, sample_quiz_session_data, sample_datei_data):
        """Test: Datei mit Quiz-Session verknüpfen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]

        # Dann eine Datei erstellen
        datei_response = client.post("/api/dateien/", json=sample_datei_data)
        datei_id = datei_response.json()["id"]

        # Datei mit Quiz-Session verknüpfen
        response = client.post(f"/api/quiz-sessions/{session_id}/dateien/{datei_id}")
        assert response.status_code == 200
        assert "erfolgreich" in response.json()["message"]

        # Überprüfen, dass die Verknüpfung existiert
        dateien_response = client.get(f"/api/quiz-sessions/{session_id}/dateien")
        assert dateien_response.status_code == 200
        dateien = dateien_response.json()
        assert len(dateien) == 1
        assert dateien[0]["id"] == datei_id

    def test_unlink_datei_von_quiz_session(self, client: TestClient, sample_quiz_session_data, sample_datei_data):
        """Test: Datei von Quiz-Session trennen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]

        # Dann eine Datei erstellen
        datei_response = client.post("/api/dateien/", json=sample_datei_data)
        datei_id = datei_response.json()["id"]

        # Datei mit Quiz-Session verknüpfen
        link_response = client.post(f"/api/quiz-sessions/{session_id}/dateien/{datei_id}")
        assert link_response.status_code == 200

        # Datei von Quiz-Session trennen
        response = client.delete(f"/api/quiz-sessions/{session_id}/dateien/{datei_id}")
        assert response.status_code == 200
        assert "erfolgreich" in response.json()["message"]

        # Überprüfen, dass die Verknüpfung entfernt wurde
        dateien_response = client.get(f"/api/quiz-sessions/{session_id}/dateien")
        assert dateien_response.status_code == 200
        assert dateien_response.json() == []

    def test_link_nonexistent_datei_to_quiz_session(self, client: TestClient, sample_quiz_session_data):
        """Test: Nicht existierende Datei mit Quiz-Session verknüpfen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]

        # Versuchen, nicht existierende Datei zu verknüpfen
        response = client.post(f"/api/quiz-sessions/{session_id}/dateien/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_link_datei_to_nonexistent_quiz_session(self, client: TestClient, sample_datei_data):
        """Test: Datei mit nicht existierender Quiz-Session verknüpfen"""
        # Erst eine Datei erstellen
        datei_response = client.post("/api/dateien/", json=sample_datei_data)
        datei_id = datei_response.json()["id"]

        # Versuchen, mit nicht existierender Quiz-Session zu verknüpfen
        response = client.post(f"/api/quiz-sessions/999/dateien/{datei_id}")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_get_fragen_fuer_quiz_session_with_data(self, client: TestClient, sample_quiz_session_data, sample_quiz_frage_data):
        """Test: Fragen für Quiz-Session abrufen (mit Daten)"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]

        # Mehrere Fragen für diese Quiz-Session erstellen
        for i in range(3):
            frage_data = sample_quiz_frage_data.copy()
            frage_data["quiz_session_id"] = session_id
            frage_data["frage"] = f"Test Frage {i+1}?"
            create_response = client.post("/api/quiz-fragen/", json=frage_data)
            assert create_response.status_code == 200

        # Fragen für die Quiz-Session abrufen
        response = client.get(f"/api/quiz-sessions/{session_id}/fragen")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Überprüfen, dass alle Fragen zur richtigen Quiz-Session gehören
        for frage in data:
            assert frage["quiz_session_id"] == session_id

    def test_multiple_dateien_link_to_quiz_session(self, client: TestClient, sample_quiz_session_data, sample_datei_data):
        """Test: Mehrere Dateien mit Quiz-Session verknüpfen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]

        datei_ids = []
        # Mehrere Dateien erstellen und verknüpfen
        for i in range(3):
            datei_data = sample_datei_data.copy()
            datei_data["titel"] = f"Test Datei {i+1}"
            datei_response = client.post("/api/dateien/", json=datei_data)
            datei_id = datei_response.json()["id"]
            datei_ids.append(datei_id)

            # Datei mit Quiz-Session verknüpfen
            link_response = client.post(f"/api/quiz-sessions/{session_id}/dateien/{datei_id}")
            assert link_response.status_code == 200

        # Alle verknüpften Dateien abrufen
        dateien_response = client.get(f"/api/quiz-sessions/{session_id}/dateien")
        assert dateien_response.status_code == 200
        dateien = dateien_response.json()
        assert len(dateien) == 3
        
        # Überprüfen, dass alle Dateien verknüpft sind
        returned_ids = [datei["id"] for datei in dateien]
        for datei_id in datei_ids:
            assert datei_id in returned_ids

    def test_quiz_session_cascade_delete_fragen(self, client: TestClient, sample_quiz_session_data, sample_quiz_frage_data):
        """Test: Beim Löschen einer Quiz-Session werden auch die Fragen gelöscht (Cascade)"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]

        # Eine Frage für diese Quiz-Session erstellen
        frage_data = sample_quiz_frage_data.copy()
        frage_data["quiz_session_id"] = session_id
        frage_response = client.post("/api/quiz-fragen/", json=frage_data)
        frage_id = frage_response.json()["id"]

        # Quiz-Session löschen
        delete_response = client.delete(f"/api/quiz-sessions/{session_id}")
        assert delete_response.status_code == 200

        # Überprüfen, dass die Frage auch gelöscht wurde
        frage_get_response = client.get(f"/api/quiz-fragen/{frage_id}")
        assert frage_get_response.status_code == 404
