import pytest
from fastapi.testclient import TestClient


class TestQuizFragenAPI:
    """Tests für die Quiz-Fragen-API Endpunkte"""

    def test_create_quiz_frage(self, client: TestClient, sample_quiz_session_data, sample_quiz_frage_data):
        """Test: Quiz-Frage erstellen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]
        
        # Quiz-Frage-Daten mit korrekter session_id
        frage_data = sample_quiz_frage_data.copy()
        frage_data["quiz_session_id"] = session_id

        response = client.post("/api/quiz-fragen/", json=frage_data)
        assert response.status_code == 200
        data = response.json()
        assert data["frage"] == frage_data["frage"]
        assert data["Antwort"] == frage_data["Antwort"]
        assert data["Erklaerung"] == frage_data["Erklaerung"]
        assert data["quiz_session_id"] == session_id
        assert "id" in data

    def test_get_all_quiz_fragen_empty(self, client: TestClient):
        """Test: Alle Quiz-Fragen abrufen (leer)"""
        response = client.get("/api/quiz-fragen/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_quiz_fragen_with_data(self, client: TestClient, sample_quiz_session_data, sample_quiz_frage_data):
        """Test: Alle Quiz-Fragen abrufen (mit Daten)"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]
        
        # Quiz-Frage erstellen
        frage_data = sample_quiz_frage_data.copy()
        frage_data["quiz_session_id"] = session_id
        create_response = client.post("/api/quiz-fragen/", json=frage_data)
        assert create_response.status_code == 200

        # Dann alle Quiz-Fragen abrufen
        response = client.get("/api/quiz-fragen/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["frage"] == frage_data["frage"]

    def test_get_quiz_frage_by_id(self, client: TestClient, sample_quiz_session_data, sample_quiz_frage_data):
        """Test: Einzelne Quiz-Frage abrufen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]
        
        # Quiz-Frage erstellen
        frage_data = sample_quiz_frage_data.copy()
        frage_data["quiz_session_id"] = session_id
        create_response = client.post("/api/quiz-fragen/", json=frage_data)
        created_frage = create_response.json()
        frage_id = created_frage["id"]

        # Dann die Quiz-Frage abrufen
        response = client.get(f"/api/quiz-fragen/{frage_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == frage_id
        assert data["frage"] == frage_data["frage"]

    def test_get_quiz_frage_not_found(self, client: TestClient):
        """Test: Nicht existierende Quiz-Frage abrufen"""
        response = client.get("/api/quiz-fragen/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_update_quiz_frage(self, client: TestClient, sample_quiz_session_data, sample_quiz_frage_data):
        """Test: Quiz-Frage aktualisieren"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]
        
        # Quiz-Frage erstellen
        frage_data = sample_quiz_frage_data.copy()
        frage_data["quiz_session_id"] = session_id
        create_response = client.post("/api/quiz-fragen/", json=frage_data)
        created_frage = create_response.json()
        frage_id = created_frage["id"]

        # Dann die Quiz-Frage aktualisieren
        update_data = {
            "frage": "Was ist eine aktualisierte Test-Frage?",
            "Antwort": "Eine aktualisierte Antwort"
        }
        response = client.put(f"/api/quiz-fragen/{frage_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["frage"] == update_data["frage"]
        assert data["Antwort"] == update_data["Antwort"]
        # Andere Felder sollten unverändert bleiben
        assert data["Erklaerung"] == frage_data["Erklaerung"]

    def test_update_quiz_frage_not_found(self, client: TestClient):
        """Test: Nicht existierende Quiz-Frage aktualisieren"""
        update_data = {"frage": "Neue Frage?"}
        response = client.put("/api/quiz-fragen/999", json=update_data)
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_delete_quiz_frage(self, client: TestClient, sample_quiz_session_data, sample_quiz_frage_data):
        """Test: Quiz-Frage löschen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]
        
        # Quiz-Frage erstellen
        frage_data = sample_quiz_frage_data.copy()
        frage_data["quiz_session_id"] = session_id
        create_response = client.post("/api/quiz-fragen/", json=frage_data)
        created_frage = create_response.json()
        frage_id = created_frage["id"]

        # Dann die Quiz-Frage löschen
        response = client.delete(f"/api/quiz-fragen/{frage_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == frage_id

        # Überprüfen, dass die Quiz-Frage wirklich gelöscht wurde
        get_response = client.get(f"/api/quiz-fragen/{frage_id}")
        assert get_response.status_code == 404

    def test_delete_quiz_frage_not_found(self, client: TestClient):
        """Test: Nicht existierende Quiz-Frage löschen"""
        response = client.delete("/api/quiz-fragen/999")
        assert response.status_code == 404
        assert "nicht gefunden" in response.json()["detail"]

    def test_create_quiz_frage_with_nonexistent_session(self, client: TestClient):
        """Test: Quiz-Frage mit nicht existierender Quiz-Session erstellen (wird akzeptiert)"""
        frage_data = {
            "frage": "Test Frage?",
            "Antwort": "Test Antwort",
            "Erklaerung": "Test Erklärung",
            "quiz_session_id": 999
        }
        response = client.post("/api/quiz-fragen/", json=frage_data)
        # Die API akzeptiert derzeit auch nicht existierende quiz_session_ids
        assert response.status_code == 200
        data = response.json()
        assert data["frage"] == frage_data["frage"]
        assert data["Antwort"] == frage_data["Antwort"]
        assert data["Erklaerung"] == frage_data["Erklaerung"]
        assert data["quiz_session_id"] == 999
        assert "id" in data

    def test_create_multiple_fragen_for_session(self, client: TestClient, sample_quiz_session_data):
        """Test: Mehrere Fragen für eine Quiz-Session erstellen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]

        fragen_data = [
            {
                "frage": "Was ist Python?",
                "Antwort": "Eine Programmiersprache",
                "Erklaerung": "Python ist eine interpretierte, objektorientierte Programmiersprache",
                "quiz_session_id": session_id
            },
            {
                "frage": "Was ist eine Liste in Python?",
                "Antwort": "Eine geordnete Sammlung von Elementen",
                "Erklaerung": "Listen sind veränderbare Sequenzen in Python",
                "quiz_session_id": session_id
            },
            {
                "frage": "Was ist ein Dictionary?",
                "Antwort": "Eine Sammlung von Schlüssel-Wert-Paaren",
                "Erklaerung": "Dictionaries sind ungeordnete, veränderbare Sammlungen",
                "quiz_session_id": session_id
            }
        ]

        created_ids = []
        for frage_data in fragen_data:
            response = client.post("/api/quiz-fragen/", json=frage_data)
            assert response.status_code == 200
            created_ids.append(response.json()["id"])

        # Überprüfen, dass alle Fragen erstellt wurden
        all_fragen_response = client.get("/api/quiz-fragen/")
        assert all_fragen_response.status_code == 200
        all_fragen = all_fragen_response.json()
        assert len(all_fragen) == 3

        # Überprüfen, dass alle Fragen zur richtigen Quiz-Session gehören
        for frage in all_fragen:
            assert frage["quiz_session_id"] == session_id

    def test_update_quiz_frage_change_session(self, client: TestClient, sample_quiz_session_data, sample_quiz_frage_data):
        """Test: Quiz-Frage zu anderer Quiz-Session verschieben"""
        # Erste Quiz-Session erstellen
        session1_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session1_id = session1_response.json()["id"]
        
        # Zweite Quiz-Session erstellen
        session2_data = sample_quiz_session_data.copy()
        session2_data["titel"] = "Zweite Quiz-Session"
        session2_response = client.post("/api/quiz-sessions/", json=session2_data)
        session2_id = session2_response.json()["id"]
        
        # Quiz-Frage für erste Session erstellen
        frage_data = sample_quiz_frage_data.copy()
        frage_data["quiz_session_id"] = session1_id
        create_response = client.post("/api/quiz-fragen/", json=frage_data)
        frage_id = create_response.json()["id"]

        # Quiz-Frage zur zweiten Session verschieben
        update_data = {"quiz_session_id": session2_id}
        response = client.put(f"/api/quiz-fragen/{frage_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["quiz_session_id"] == session2_id

        # Überprüfen über die Session-Endpunkte
        session2_fragen = client.get(f"/api/quiz-sessions/{session2_id}/fragen")
        assert len(session2_fragen.json()) == 1
        
        session1_fragen = client.get(f"/api/quiz-sessions/{session1_id}/fragen")
        assert len(session1_fragen.json()) == 0

    def test_create_quiz_frage_with_long_content(self, client: TestClient, sample_quiz_session_data):
        """Test: Quiz-Frage mit langem Inhalt erstellen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]
        
        long_content_data = {
            "frage": "Was ist die Zeitkomplexität des Quicksort-Algorithmus und wie funktioniert er im Detail?",
            "Antwort": "O(n log n) im Durchschnitt, O(n²) im schlechtesten Fall",
            "Erklaerung": """Quicksort ist ein Divide-and-Conquer-Algorithmus, der folgendermaßen funktioniert:
            
1. Wähle ein Pivot-Element aus dem Array
2. Partitioniere das Array so, dass alle Elemente kleiner als das Pivot links stehen und alle größeren rechts
3. Wende Quicksort rekursiv auf die beiden Teilarrays an

Die durchschnittliche Zeitkomplexität beträgt O(n log n), da das Array in jedem Schritt etwa halbiert wird.
Im schlechtesten Fall (bereits sortiertes Array mit schlechter Pivot-Wahl) beträgt die Komplexität O(n²).
Die Raumkomplexität beträgt O(log n) für den Rekursionsstack im Durchschnitt.""",
            "quiz_session_id": session_id
        }
        
        response = client.post("/api/quiz-fragen/", json=long_content_data)
        assert response.status_code == 200
        data = response.json()
        assert data["frage"] == long_content_data["frage"]
        assert data["Antwort"] == long_content_data["Antwort"]
        assert data["Erklaerung"] == long_content_data["Erklaerung"]

    def test_create_quiz_frage_minimal_data(self, client: TestClient, sample_quiz_session_data):
        """Test: Quiz-Frage mit minimalen Daten erstellen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]
        
        minimal_data = {
            "frage": "Minimal Frage?",
            "Antwort": "Minimal Antwort",
            "Erklaerung": "Minimal Erklärung",
            "quiz_session_id": session_id
        }
        response = client.post("/api/quiz-fragen/", json=minimal_data)
        assert response.status_code == 200
        data = response.json()
        assert data["frage"] == minimal_data["frage"]
        assert data["Antwort"] == minimal_data["Antwort"]
        assert data["Erklaerung"] == minimal_data["Erklaerung"]

    def test_create_quiz_frage_missing_required_fields(self, client: TestClient, sample_quiz_session_data):
        """Test: Quiz-Frage mit fehlenden Pflichtfeldern erstellen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]
        
        # Test mit fehlendem 'frage' Feld
        incomplete_data = {
            "Antwort": "Test Antwort",
            "Erklaerung": "Test Erklärung",
            "quiz_session_id": session_id
        }
        response = client.post("/api/quiz-fragen/", json=incomplete_data)
        assert response.status_code == 422  # Validation Error

        # Test mit fehlendem 'Antwort' Feld
        incomplete_data2 = {
            "frage": "Test Frage?",
            "Erklaerung": "Test Erklärung",
            "quiz_session_id": session_id
        }
        response2 = client.post("/api/quiz-fragen/", json=incomplete_data2)
        assert response2.status_code == 422  # Validation Error

    def test_quiz_frage_with_special_characters(self, client: TestClient, sample_quiz_session_data):
        """Test: Quiz-Frage mit Sonderzeichen erstellen"""
        # Erst eine Quiz-Session erstellen
        session_response = client.post("/api/quiz-sessions/", json=sample_quiz_session_data)
        session_id = session_response.json()["id"]
        
        special_chars_data = {
            "frage": "Was bedeutet das Symbol ∑ in der Mathematik? Und wie berechnet man ∫x²dx?",
            "Antwort": "∑ ist das Summensymbol, ∫x²dx = x³/3 + C",
            "Erklaerung": "Das Sigma-Symbol (∑) steht für Summation. Das Integral ∫x²dx wird mit der Potenzregel berechnet: ∫xⁿdx = xⁿ⁺¹/(n+1) + C",
            "quiz_session_id": session_id
        }
        
        response = client.post("/api/quiz-fragen/", json=special_chars_data)
        assert response.status_code == 200
        data = response.json()
        assert data["frage"] == special_chars_data["frage"]
        assert data["Antwort"] == special_chars_data["Antwort"]
        assert "∑" in data["frage"]
        assert "∫" in data["frage"]
