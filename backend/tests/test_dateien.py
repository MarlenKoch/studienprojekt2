import pytest
from fastapi.testclient import TestClient


class TestDateienAPI:
    """Tests für die Dateien-API Endpunkte"""

    def test_create_datei(self, client: TestClient, sample_datei_data):
        """Test: Datei erstellen"""
        response = client.post("/api/dateien/", json=sample_datei_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titel"] == sample_datei_data["titel"]
        assert data["pfad"] == sample_datei_data["pfad"]
        assert data["dateiart"] == sample_datei_data["dateiart"]
        assert data["dozent"] == sample_datei_data["dozent"]
        assert data["semester"] == sample_datei_data["semester"]
        assert data["modul"] == sample_datei_data["modul"]
        assert "id" in data

    def test_get_all_dateien_empty(self, client: TestClient):
        """Test: Alle Dateien abrufen (leer)"""
        response = client.get("/api/dateien/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_dateien_with_data(self, client: TestClient, sample_datei_data):
        """Test: Alle Dateien abrufen (mit Daten)"""
        # Erst eine Datei erstellen
        create_response = client.post("/api/dateien/", json=sample_datei_data)
        assert create_response.status_code == 200

        # Dann alle Dateien abrufen
        response = client.get("/api/dateien/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titel"] == sample_datei_data["titel"]

    def test_get_datei_by_id(self, client: TestClient, sample_datei_data):
        """Test: Einzelne Datei abrufen"""
        # Erst eine Datei erstellen
        create_response = client.post("/api/dateien/", json=sample_datei_data)
        created_datei = create_response.json()
        datei_id = created_datei["id"]

        # Dann die Datei abrufen
        response = client.get(f"/api/dateien/{datei_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == datei_id
        assert data["titel"] == sample_datei_data["titel"]

    def test_get_datei_not_found(self, client: TestClient):
        """Test: Nicht existierende Datei abrufen"""
        response = client.get("/api/dateien/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_update_datei(self, client: TestClient, sample_datei_data):
        """Test: Datei aktualisieren"""
        # Erst eine Datei erstellen
        create_response = client.post("/api/dateien/", json=sample_datei_data)
        created_datei = create_response.json()
        datei_id = created_datei["id"]

        # Dann die Datei aktualisieren
        update_data = {
            "titel": "Aktualisierter Titel",
            "dozent": "Prof. Dr. Neu"
        }
        response = client.put(f"/api/dateien/{datei_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titel"] == update_data["titel"]
        assert data["dozent"] == update_data["dozent"]
        # Andere Felder sollten unverändert bleiben
        assert data["pfad"] == sample_datei_data["pfad"]

    def test_update_datei_not_found(self, client: TestClient):
        """Test: Nicht existierende Datei aktualisieren"""
        update_data = {"titel": "Neuer Titel"}
        response = client.put("/api/dateien/999", json=update_data)
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_delete_datei(self, client: TestClient, sample_datei_data):
        """Test: Datei löschen"""
        # Erst eine Datei erstellen
        create_response = client.post("/api/dateien/", json=sample_datei_data)
        created_datei = create_response.json()
        datei_id = created_datei["id"]

        # Dann die Datei löschen
        response = client.delete(f"/api/dateien/{datei_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == datei_id

        # Überprüfen, dass die Datei wirklich gelöscht wurde
        get_response = client.get(f"/api/dateien/{datei_id}")
        assert get_response.status_code == 404

    def test_delete_datei_not_found(self, client: TestClient):
        """Test: Nicht existierende Datei löschen"""
        response = client.delete("/api/dateien/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_create_datei_minimal_data(self, client: TestClient):
        """Test: Datei mit minimalen Daten erstellen"""
        minimal_data = {
            "titel": "Minimal Datei",
            "pfad": "/minimal/path.pdf"
        }
        response = client.post("/api/dateien/", json=minimal_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titel"] == minimal_data["titel"]
        assert data["pfad"] == minimal_data["pfad"]
        assert data["dateiart"] is None
        assert data["dozent"] is None

    def test_create_datei_with_empty_strings(self, client: TestClient):
        """Test: Datei mit leeren Strings erstellen (wird akzeptiert)"""
        empty_data = {
            "titel": "",  # Leerer Titel wird akzeptiert
            "pfad": ""    # Leerer Pfad wird akzeptiert
        }
        response = client.post("/api/dateien/", json=empty_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titel"] == ""
        assert data["pfad"] == ""
        assert "id" in data

    def test_get_notizen_fuer_datei_empty(self, client: TestClient, sample_datei_data):
        """Test: Notizen für Datei abrufen (leer)"""
        # Erst eine Datei erstellen
        create_response = client.post("/api/dateien/", json=sample_datei_data)
        created_datei = create_response.json()
        datei_id = created_datei["id"]

        # Notizen für die Datei abrufen
        response = client.get(f"/api/dateien/{datei_id}/notizen")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_quiz_sessions_fuer_datei_empty(self, client: TestClient, sample_datei_data):
        """Test: Quiz-Sessions für Datei abrufen (leer)"""
        # Erst eine Datei erstellen
        create_response = client.post("/api/dateien/", json=sample_datei_data)
        created_datei = create_response.json()
        datei_id = created_datei["id"]

        # Quiz-Sessions für die Datei abrufen
        response = client.get(f"/api/dateien/{datei_id}/quiz-sessions")
        assert response.status_code == 200
        assert response.json() == []
