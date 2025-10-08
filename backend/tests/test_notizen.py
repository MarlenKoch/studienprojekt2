import pytest
from fastapi.testclient import TestClient


class TestNotizenAPI:
    """Tests für die Notizen-API Endpunkte"""

    def test_create_notiz(self, client: TestClient, sample_notiz_data):
        """Test: Notiz erstellen"""
        response = client.post("/api/notizen/", json=sample_notiz_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titel"] == sample_notiz_data["titel"]
        assert data["labels"] == sample_notiz_data["labels"]
        assert data["reihenfolgeKiAntworten"] == sample_notiz_data["reihenfolgeKiAntworten"]
        assert "id" in data

    def test_get_all_notizen_empty(self, client: TestClient):
        """Test: Alle Notizen abrufen (leer)"""
        response = client.get("/api/notizen/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_notizen_with_data(self, client: TestClient, sample_notiz_data):
        """Test: Alle Notizen abrufen (mit Daten)"""
        # Erst eine Notiz erstellen
        create_response = client.post("/api/notizen/", json=sample_notiz_data)
        assert create_response.status_code == 200

        # Dann alle Notizen abrufen
        response = client.get("/api/notizen/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titel"] == sample_notiz_data["titel"]

    def test_get_notiz_by_id(self, client: TestClient, sample_notiz_data):
        """Test: Einzelne Notiz abrufen"""
        # Erst eine Notiz erstellen
        create_response = client.post("/api/notizen/", json=sample_notiz_data)
        created_notiz = create_response.json()
        notiz_id = created_notiz["id"]

        # Dann die Notiz abrufen
        response = client.get(f"/api/notizen/{notiz_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == notiz_id
        assert data["titel"] == sample_notiz_data["titel"]

    def test_get_notiz_not_found(self, client: TestClient):
        """Test: Nicht existierende Notiz abrufen"""
        response = client.get("/api/notizen/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_update_notiz(self, client: TestClient, sample_notiz_data):
        """Test: Notiz aktualisieren"""
        # Erst eine Notiz erstellen
        create_response = client.post("/api/notizen/", json=sample_notiz_data)
        created_notiz = create_response.json()
        notiz_id = created_notiz["id"]

        # Dann die Notiz aktualisieren
        update_data = {
            "titel": "Aktualisierter Notiz Titel",
            "labels": {
                "fach": "Informatik",
                "schwierigkeit": "schwer"
            }
        }
        response = client.put(f"/api/notizen/{notiz_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titel"] == update_data["titel"]
        assert data["labels"] == update_data["labels"]

    def test_update_notiz_not_found(self, client: TestClient):
        """Test: Nicht existierende Notiz aktualisieren"""
        update_data = {"titel": "Neuer Titel"}
        response = client.put("/api/notizen/999", json=update_data)
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_delete_notiz(self, client: TestClient, sample_notiz_data):
        """Test: Notiz löschen"""
        # Erst eine Notiz erstellen
        create_response = client.post("/api/notizen/", json=sample_notiz_data)
        created_notiz = create_response.json()
        notiz_id = created_notiz["id"]

        # Dann die Notiz löschen
        response = client.delete(f"/api/notizen/{notiz_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == notiz_id

        # Überprüfen, dass die Notiz wirklich gelöscht wurde
        get_response = client.get(f"/api/notizen/{notiz_id}")
        assert get_response.status_code == 404

    def test_delete_notiz_not_found(self, client: TestClient):
        """Test: Nicht existierende Notiz löschen"""
        response = client.delete("/api/notizen/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_create_notiz_minimal_data(self, client: TestClient):
        """Test: Notiz mit minimalen Daten erstellen"""
        minimal_data = {
            "titel": "Minimal Notiz",
            "labels": {"fach": "Test"}
        }
        response = client.post("/api/notizen/", json=minimal_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titel"] == minimal_data["titel"]
        assert data["labels"] == minimal_data["labels"]
        assert data["reihenfolgeKiAntworten"] == []

    def test_create_notiz_complex_labels(self, client: TestClient):
        """Test: Notiz mit komplexen Labels erstellen"""
        complex_data = {
            "titel": "Komplexe Notiz",
            "labels": {
                "fach": "Informatik",
                "schwierigkeit": "schwer",
                "thema": "Algorithmen",
                "tags": ["Sortierung", "Suche", "Komplexität"],
                "semester": 3,
                "credits": 6,
                "wichtig": True,
                "deadline": "2024-12-15"
            },
            "reihenfolgeKiAntworten": [3, 1, 4, 2]
        }
        response = client.post("/api/notizen/", json=complex_data)
        assert response.status_code == 200
        data = response.json()
        assert data["labels"] == complex_data["labels"]
        assert data["reihenfolgeKiAntworten"] == complex_data["reihenfolgeKiAntworten"]

    def test_get_dateien_fuer_notiz_empty(self, client: TestClient, sample_notiz_data):
        """Test: Dateien für Notiz abrufen (leer)"""
        # Erst eine Notiz erstellen
        create_response = client.post("/api/notizen/", json=sample_notiz_data)
        created_notiz = create_response.json()
        notiz_id = created_notiz["id"]

        # Dateien für die Notiz abrufen
        response = client.get(f"/api/notizen/{notiz_id}/dateien")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_kiantworten_fuer_notiz_empty(self, client: TestClient, sample_notiz_data):
        """Test: KI-Antworten für Notiz abrufen (leer)"""
        # Erst eine Notiz erstellen
        create_response = client.post("/api/notizen/", json=sample_notiz_data)
        created_notiz = create_response.json()
        notiz_id = created_notiz["id"]

        # KI-Antworten für die Notiz abrufen
        response = client.get(f"/api/notizen/{notiz_id}/kiantworten")
        assert response.status_code == 200
        assert response.json() == []

    def test_link_datei_zu_notiz(self, client: TestClient, sample_notiz_data, sample_datei_data):
        """Test: Datei mit Notiz verknüpfen"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]

        # Dann eine Datei erstellen
        datei_response = client.post("/api/dateien/", json=sample_datei_data)
        datei_id = datei_response.json()["id"]

        # Datei mit Notiz verknüpfen
        response = client.post(f"/api/notizen/{notiz_id}/dateien/{datei_id}")
        assert response.status_code == 200
        assert "erfolgreich" in response.json()["message"]

        # Überprüfen, dass die Verknüpfung existiert
        dateien_response = client.get(f"/api/notizen/{notiz_id}/dateien")
        assert dateien_response.status_code == 200
        dateien = dateien_response.json()
        assert len(dateien) == 1
        assert dateien[0]["id"] == datei_id

    def test_unlink_datei_von_notiz(self, client: TestClient, sample_notiz_data, sample_datei_data):
        """Test: Datei von Notiz trennen"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]

        # Dann eine Datei erstellen
        datei_response = client.post("/api/dateien/", json=sample_datei_data)
        datei_id = datei_response.json()["id"]

        # Datei mit Notiz verknüpfen
        link_response = client.post(f"/api/notizen/{notiz_id}/dateien/{datei_id}")
        assert link_response.status_code == 200

        # Datei von Notiz trennen
        response = client.delete(f"/api/notizen/{notiz_id}/dateien/{datei_id}")
        assert response.status_code == 200
        assert "erfolgreich" in response.json()["message"]

        # Überprüfen, dass die Verknüpfung entfernt wurde
        dateien_response = client.get(f"/api/notizen/{notiz_id}/dateien")
        assert dateien_response.status_code == 200
        assert dateien_response.json() == []

    def test_link_nonexistent_datei_to_notiz(self, client: TestClient, sample_notiz_data):
        """Test: Nicht existierende Datei mit Notiz verknüpfen"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]

        # Versuchen, nicht existierende Datei zu verknüpfen
        response = client.post(f"/api/notizen/{notiz_id}/dateien/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_link_datei_to_nonexistent_notiz(self, client: TestClient, sample_datei_data):
        """Test: Datei mit nicht existierender Notiz verknüpfen"""
        # Erst eine Datei erstellen
        datei_response = client.post("/api/dateien/", json=sample_datei_data)
        datei_id = datei_response.json()["id"]

        # Versuchen, mit nicht existierender Notiz zu verknüpfen
        response = client.post(f"/api/notizen/999/dateien/{datei_id}")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]
