import pytest
from fastapi.testclient import TestClient


class TestKiAntwortenAPI:
    """Tests für die KI-Antworten-API Endpunkte"""

    def test_create_kiantwort(self, client: TestClient, sample_notiz_data, sample_kiantwort_data):
        """Test: KI-Antwort erstellen"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]
        
        # KI-Antwort-Daten mit korrekter notiz_id
        kiantwort_data = sample_kiantwort_data.copy()
        kiantwort_data["notiz_id"] = notiz_id

        response = client.post("/api/kiantworten/", json=kiantwort_data)
        assert response.status_code == 200
        data = response.json()
        assert data["inhalt"] == kiantwort_data["inhalt"]
        assert data["kommentar"] == kiantwort_data["kommentar"]
        assert data["typ"] == kiantwort_data["typ"]
        assert data["notiz_id"] == notiz_id
        assert "id" in data

    def test_get_all_kiantworten_empty(self, client: TestClient):
        """Test: Alle KI-Antworten abrufen (leer)"""
        response = client.get("/api/kiantworten/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_kiantworten_with_data(self, client: TestClient, sample_notiz_data, sample_kiantwort_data):
        """Test: Alle KI-Antworten abrufen (mit Daten)"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]
        
        # KI-Antwort erstellen
        kiantwort_data = sample_kiantwort_data.copy()
        kiantwort_data["notiz_id"] = notiz_id
        create_response = client.post("/api/kiantworten/", json=kiantwort_data)
        assert create_response.status_code == 200

        # Dann alle KI-Antworten abrufen
        response = client.get("/api/kiantworten/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["inhalt"] == kiantwort_data["inhalt"]

    def test_get_kiantwort_by_id(self, client: TestClient, sample_notiz_data, sample_kiantwort_data):
        """Test: Einzelne KI-Antwort abrufen"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]
        
        # KI-Antwort erstellen
        kiantwort_data = sample_kiantwort_data.copy()
        kiantwort_data["notiz_id"] = notiz_id
        create_response = client.post("/api/kiantworten/", json=kiantwort_data)
        created_kiantwort = create_response.json()
        kiantwort_id = created_kiantwort["id"]

        # Dann die KI-Antwort abrufen
        response = client.get(f"/api/kiantworten/{kiantwort_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == kiantwort_id
        assert data["inhalt"] == kiantwort_data["inhalt"]

    def test_get_kiantwort_not_found(self, client: TestClient):
        """Test: Nicht existierende KI-Antwort abrufen"""
        response = client.get("/api/kiantworten/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_update_kiantwort(self, client: TestClient, sample_notiz_data, sample_kiantwort_data):
        """Test: KI-Antwort aktualisieren"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]
        
        # KI-Antwort erstellen
        kiantwort_data = sample_kiantwort_data.copy()
        kiantwort_data["notiz_id"] = notiz_id
        create_response = client.post("/api/kiantworten/", json=kiantwort_data)
        created_kiantwort = create_response.json()
        kiantwort_id = created_kiantwort["id"]

        # Dann die KI-Antwort aktualisieren
        update_data = {
            "inhalt": "Aktualisierter KI-Antwort Inhalt",
            "typ": "Beispiel"
        }
        response = client.put(f"/api/kiantworten/{kiantwort_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["inhalt"] == update_data["inhalt"]
        assert data["typ"] == update_data["typ"]
        # Andere Felder sollten unverändert bleiben
        assert data["kommentar"] == kiantwort_data["kommentar"]

    def test_update_kiantwort_not_found(self, client: TestClient):
        """Test: Nicht existierende KI-Antwort aktualisieren"""
        update_data = {"inhalt": "Neuer Inhalt"}
        response = client.put("/api/kiantworten/999", json=update_data)
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_delete_kiantwort(self, client: TestClient, sample_notiz_data, sample_kiantwort_data):
        """Test: KI-Antwort löschen"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]
        
        # KI-Antwort erstellen
        kiantwort_data = sample_kiantwort_data.copy()
        kiantwort_data["notiz_id"] = notiz_id
        create_response = client.post("/api/kiantworten/", json=kiantwort_data)
        created_kiantwort = create_response.json()
        kiantwort_id = created_kiantwort["id"]

        # Dann die KI-Antwort löschen
        response = client.delete(f"/api/kiantworten/{kiantwort_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == kiantwort_id

        # Überprüfen, dass die KI-Antwort wirklich gelöscht wurde
        get_response = client.get(f"/api/kiantworten/{kiantwort_id}")
        assert get_response.status_code == 404

    def test_delete_kiantwort_not_found(self, client: TestClient):
        """Test: Nicht existierende KI-Antwort löschen"""
        response = client.delete("/api/kiantworten/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_create_kiantwort_minimal_data(self, client: TestClient, sample_notiz_data):
        """Test: KI-Antwort mit minimalen Daten erstellen"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]
        
        minimal_data = {
            "notiz_id": notiz_id
        }
        response = client.post("/api/kiantworten/", json=minimal_data)
        assert response.status_code == 200
        data = response.json()
        assert data["notiz_id"] == notiz_id
        assert data["inhalt"] is None
        assert data["kommentar"] is None
        assert data["typ"] is None

    def test_create_kiantwort_with_code(self, client: TestClient, sample_notiz_data):
        """Test: KI-Antwort mit Code-Beispiel erstellen"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]
        
        code_data = {
            "inhalt": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
            "kommentar": "Implementierung des Quicksort-Algorithmus in Python",
            "typ": "Code-Beispiel",
            "notiz_id": notiz_id
        }
        response = client.post("/api/kiantworten/", json=code_data)
        assert response.status_code == 200
        data = response.json()
        assert data["inhalt"] == code_data["inhalt"]
        assert data["typ"] == code_data["typ"]

    def test_get_kiantworten_fuer_notiz(self, client: TestClient, sample_notiz_data, sample_kiantwort_data):
        """Test: KI-Antworten für eine bestimmte Notiz abrufen"""
        # Erst eine Notiz erstellen
        notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz_id = notiz_response.json()["id"]
        
        # Mehrere KI-Antworten für diese Notiz erstellen
        for i in range(3):
            kiantwort_data = sample_kiantwort_data.copy()
            kiantwort_data["notiz_id"] = notiz_id
            kiantwort_data["inhalt"] = f"KI-Antwort {i+1}"
            create_response = client.post("/api/kiantworten/", json=kiantwort_data)
            assert create_response.status_code == 200

        # KI-Antworten für die Notiz abrufen
        response = client.get(f"/api/kiantworten/notiz/{notiz_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Überprüfen, dass alle KI-Antworten zur richtigen Notiz gehören
        for kiantwort in data:
            assert kiantwort["notiz_id"] == notiz_id

    def test_get_kiantworten_fuer_nonexistent_notiz(self, client: TestClient):
        """Test: KI-Antworten für nicht existierende Notiz abrufen"""
        response = client.get("/api/kiantworten/notiz/999")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_kiantwort_with_nonexistent_notiz(self, client: TestClient):
        """Test: KI-Antwort mit nicht existierender Notiz erstellen (wird akzeptiert)"""
        kiantwort_data = {
            "inhalt": "Test Inhalt",
            "notiz_id": 999
        }
        response = client.post("/api/kiantworten/", json=kiantwort_data)
        # Die API akzeptiert derzeit auch nicht existierende notiz_ids
        assert response.status_code == 200
        data = response.json()
        assert data["inhalt"] == kiantwort_data["inhalt"]
        assert data["notiz_id"] == 999
        assert "id" in data

    def test_update_kiantwort_change_notiz(self, client: TestClient, sample_notiz_data, sample_kiantwort_data):
        """Test: KI-Antwort zu anderer Notiz verschieben"""
        # Erste Notiz erstellen
        notiz1_response = client.post("/api/notizen/", json=sample_notiz_data)
        notiz1_id = notiz1_response.json()["id"]
        
        # Zweite Notiz erstellen
        notiz2_data = sample_notiz_data.copy()
        notiz2_data["titel"] = "Zweite Notiz"
        notiz2_response = client.post("/api/notizen/", json=notiz2_data)
        notiz2_id = notiz2_response.json()["id"]
        
        # KI-Antwort für erste Notiz erstellen
        kiantwort_data = sample_kiantwort_data.copy()
        kiantwort_data["notiz_id"] = notiz1_id
        create_response = client.post("/api/kiantworten/", json=kiantwort_data)
        kiantwort_id = create_response.json()["id"]

        # KI-Antwort zur zweiten Notiz verschieben
        update_data = {"notiz_id": notiz2_id}
        response = client.put(f"/api/kiantworten/{kiantwort_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["notiz_id"] == notiz2_id

        # Überprüfen, dass die KI-Antwort jetzt zur zweiten Notiz gehört
        notiz2_kiantworten = client.get(f"/api/kiantworten/notiz/{notiz2_id}")
        assert len(notiz2_kiantworten.json()) == 1
        
        notiz1_kiantworten = client.get(f"/api/kiantworten/notiz/{notiz1_id}")
        assert len(notiz1_kiantworten.json()) == 0
