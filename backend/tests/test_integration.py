import pytest
from fastapi.testclient import TestClient


class TestIntegration:
    """Integrationstests für die gesamte API"""

    def test_complete_workflow(self, client: TestClient):
        """Test: Vollständiger Workflow mit allen Entitäten"""
        
        # 1. Datei erstellen
        datei_data = {
            "titel": "Integration Test Datei",
            "pfad": "/test/integration.pdf",
            "dateiart": "PDF",
            "dozent": "Prof. Integration",
            "semester": "WS 2024/25",
            "modul": "Integration Testing"
        }
        datei_response = client.post("/api/dateien/", json=datei_data)
        assert datei_response.status_code == 200
        datei_id = datei_response.json()["id"]

        # 2. Notiz erstellen
        notiz_data = {
            "titel": "Integration Test Notiz",
            "labels": {
                "fach": "Testing",
                "schwierigkeit": "mittel",
                "thema": "Integration"
            },
            "reihenfolgeKiAntworten": []
        }
        notiz_response = client.post("/api/notizen/", json=notiz_data)
        assert notiz_response.status_code == 200
        notiz_id = notiz_response.json()["id"]

        # 3. Datei mit Notiz verknüpfen
        link_response = client.post(f"/api/notizen/{notiz_id}/dateien/{datei_id}")
        assert link_response.status_code == 200

        # 4. KI-Antwort erstellen
        kiantwort_data = {
            "inhalt": "Integration Testing ist wichtig für die Qualitätssicherung",
            "kommentar": "Grundlegende Erklärung",
            "typ": "Definition",
            "notiz_id": notiz_id
        }
        kiantwort_response = client.post("/api/kiantworten/", json=kiantwort_data)
        assert kiantwort_response.status_code == 200
        kiantwort_id = kiantwort_response.json()["id"]

        # 5. Quiz-Session erstellen
        quiz_session_data = {
            "titel": "Integration Test Quiz"
        }
        session_response = client.post("/api/quiz-sessions/", json=quiz_session_data)
        assert session_response.status_code == 200
        session_id = session_response.json()["id"]

        # 6. Datei mit Quiz-Session verknüpfen
        session_link_response = client.post(f"/api/quiz-sessions/{session_id}/dateien/{datei_id}")
        assert session_link_response.status_code == 200

        # 7. Quiz-Frage erstellen
        quiz_frage_data = {
            "frage": "Was ist Integration Testing?",
            "Antwort": "Testing der Zusammenarbeit zwischen Komponenten",
            "Erklaerung": "Integration Testing überprüft die Schnittstellen zwischen verschiedenen Modulen",
            "quiz_session_id": session_id
        }
        frage_response = client.post("/api/quiz-fragen/", json=quiz_frage_data)
        assert frage_response.status_code == 200
        frage_id = frage_response.json()["id"]

        # 8. Verknüpfungen überprüfen
        # Notiz sollte die Datei enthalten
        notiz_dateien = client.get(f"/api/notizen/{notiz_id}/dateien")
        assert len(notiz_dateien.json()) == 1
        assert notiz_dateien.json()[0]["id"] == datei_id

        # Notiz sollte die KI-Antwort enthalten
        notiz_kiantworten = client.get(f"/api/notizen/{notiz_id}/kiantworten")
        assert len(notiz_kiantworten.json()) == 1
        assert notiz_kiantworten.json()[0]["id"] == kiantwort_id

        # Quiz-Session sollte die Datei enthalten
        session_dateien = client.get(f"/api/quiz-sessions/{session_id}/dateien")
        assert len(session_dateien.json()) == 1
        assert session_dateien.json()[0]["id"] == datei_id

        # Quiz-Session sollte die Frage enthalten
        session_fragen = client.get(f"/api/quiz-sessions/{session_id}/fragen")
        assert len(session_fragen.json()) == 1
        assert session_fragen.json()[0]["id"] == frage_id

        # 9. Datei sollte in beiden Relationen erscheinen
        datei_notizen = client.get(f"/api/dateien/{datei_id}/notizen")
        assert len(datei_notizen.json()) == 1
        assert datei_notizen.json()[0]["id"] == notiz_id

        datei_sessions = client.get(f"/api/dateien/{datei_id}/quiz-sessions")
        assert len(datei_sessions.json()) == 1
        assert datei_sessions.json()[0]["id"] == session_id

    def test_cascade_delete_behavior(self, client: TestClient):
        """Test: Cascade-Delete Verhalten"""
        
        # Notiz mit KI-Antworten erstellen
        notiz_data = {
            "titel": "Cascade Test Notiz",
            "labels": {"test": "cascade"}
        }
        notiz_response = client.post("/api/notizen/", json=notiz_data)
        notiz_id = notiz_response.json()["id"]

        # Mehrere KI-Antworten erstellen
        kiantwort_ids = []
        for i in range(3):
            kiantwort_data = {
                "inhalt": f"KI-Antwort {i+1}",
                "notiz_id": notiz_id
            }
            response = client.post("/api/kiantworten/", json=kiantwort_data)
            kiantwort_ids.append(response.json()["id"])

        # Quiz-Session mit Fragen erstellen
        session_data = {"titel": "Cascade Test Session"}
        session_response = client.post("/api/quiz-sessions/", json=session_data)
        session_id = session_response.json()["id"]

        frage_ids = []
        for i in range(2):
            frage_data = {
                "frage": f"Frage {i+1}?",
                "Antwort": f"Antwort {i+1}",
                "Erklaerung": f"Erklärung {i+1}",
                "quiz_session_id": session_id
            }
            response = client.post("/api/quiz-fragen/", json=frage_data)
            frage_ids.append(response.json()["id"])

        # Notiz löschen - sollte KI-Antworten mit löschen
        delete_notiz_response = client.delete(f"/api/notizen/{notiz_id}")
        assert delete_notiz_response.status_code == 200

        # KI-Antworten sollten gelöscht sein
        for kiantwort_id in kiantwort_ids:
            response = client.get(f"/api/kiantworten/{kiantwort_id}")
            assert response.status_code == 404

        # Quiz-Session löschen - sollte Fragen mit löschen
        delete_session_response = client.delete(f"/api/quiz-sessions/{session_id}")
        assert delete_session_response.status_code == 200

        # Fragen sollten gelöscht sein
        for frage_id in frage_ids:
            response = client.get(f"/api/quiz-fragen/{frage_id}")
            assert response.status_code == 404

    def test_many_to_many_relationships(self, client: TestClient):
        """Test: Many-to-Many Beziehungen zwischen Dateien, Notizen und Quiz-Sessions"""
        
        # Mehrere Dateien erstellen
        datei_ids = []
        for i in range(3):
            datei_data = {
                "titel": f"Datei {i+1}",
                "pfad": f"/test/datei_{i+1}.pdf"
            }
            response = client.post("/api/dateien/", json=datei_data)
            datei_ids.append(response.json()["id"])

        # Mehrere Notizen erstellen
        notiz_ids = []
        for i in range(2):
            notiz_data = {
                "titel": f"Notiz {i+1}",
                "labels": {"nummer": i+1}
            }
            response = client.post("/api/notizen/", json=notiz_data)
            notiz_ids.append(response.json()["id"])

        # Mehrere Quiz-Sessions erstellen
        session_ids = []
        for i in range(2):
            session_data = {"titel": f"Session {i+1}"}
            response = client.post("/api/quiz-sessions/", json=session_data)
            session_ids.append(response.json()["id"])

        # Komplexe Verknüpfungen erstellen
        # Datei 1 mit Notiz 1 und 2
        client.post(f"/api/notizen/{notiz_ids[0]}/dateien/{datei_ids[0]}")
        client.post(f"/api/notizen/{notiz_ids[1]}/dateien/{datei_ids[0]}")

        # Datei 2 mit Notiz 1
        client.post(f"/api/notizen/{notiz_ids[0]}/dateien/{datei_ids[1]}")

        # Datei 1 und 2 mit Session 1
        client.post(f"/api/quiz-sessions/{session_ids[0]}/dateien/{datei_ids[0]}")
        client.post(f"/api/quiz-sessions/{session_ids[0]}/dateien/{datei_ids[1]}")

        # Datei 3 mit Session 2
        client.post(f"/api/quiz-sessions/{session_ids[1]}/dateien/{datei_ids[2]}")

        # Verknüpfungen überprüfen
        # Datei 1 sollte in 2 Notizen und 1 Session sein
        datei1_notizen = client.get(f"/api/dateien/{datei_ids[0]}/notizen")
        assert len(datei1_notizen.json()) == 2

        datei1_sessions = client.get(f"/api/dateien/{datei_ids[0]}/quiz-sessions")
        assert len(datei1_sessions.json()) == 1

        # Notiz 1 sollte 2 Dateien haben
        notiz1_dateien = client.get(f"/api/notizen/{notiz_ids[0]}/dateien")
        assert len(notiz1_dateien.json()) == 2

        # Session 1 sollte 2 Dateien haben
        session1_dateien = client.get(f"/api/quiz-sessions/{session_ids[0]}/dateien")
        assert len(session1_dateien.json()) == 2

    def test_data_consistency_after_updates(self, client: TestClient):
        """Test: Datenkonsistenz nach Updates"""
        
        # Grunddaten erstellen
        datei_response = client.post("/api/dateien/", json={
            "titel": "Original Datei",
            "pfad": "/original.pdf"
        })
        datei_id = datei_response.json()["id"]

        notiz_response = client.post("/api/notizen/", json={
            "titel": "Original Notiz",
            "labels": {"status": "original"}
        })
        notiz_id = notiz_response.json()["id"]

        # KI-Antwort erstellen
        kiantwort_response = client.post("/api/kiantworten/", json={
            "inhalt": "Original Inhalt",
            "notiz_id": notiz_id
        })
        kiantwort_id = kiantwort_response.json()["id"]

        # Verknüpfung erstellen
        client.post(f"/api/notizen/{notiz_id}/dateien/{datei_id}")

        # Updates durchführen
        client.put(f"/api/dateien/{datei_id}", json={
            "titel": "Aktualisierte Datei"
        })

        client.put(f"/api/notizen/{notiz_id}", json={
            "titel": "Aktualisierte Notiz",
            "labels": {"status": "updated"}
        })

        client.put(f"/api/kiantworten/{kiantwort_id}", json={
            "inhalt": "Aktualisierter Inhalt"
        })

        # Konsistenz überprüfen
        # Verknüpfungen sollten noch bestehen
        notiz_dateien = client.get(f"/api/notizen/{notiz_id}/dateien")
        assert len(notiz_dateien.json()) == 1
        assert notiz_dateien.json()[0]["titel"] == "Aktualisierte Datei"

        notiz_kiantworten = client.get(f"/api/notizen/{notiz_id}/kiantworten")
        assert len(notiz_kiantworten.json()) == 1
        assert notiz_kiantworten.json()[0]["inhalt"] == "Aktualisierter Inhalt"

        # Einzelne Entitäten sollten aktualisiert sein
        datei_check = client.get(f"/api/dateien/{datei_id}")
        assert datei_check.json()["titel"] == "Aktualisierte Datei"

        notiz_check = client.get(f"/api/notizen/{notiz_id}")
        assert notiz_check.json()["titel"] == "Aktualisierte Notiz"
        assert notiz_check.json()["labels"]["status"] == "updated"

    def test_error_handling_in_workflows(self, client: TestClient):
        """Test: Fehlerbehandlung in komplexen Workflows"""
        
        # KI-Antwort mit nicht existierender Notiz wird akzeptiert
        kiantwort_with_invalid_notiz = {
            "inhalt": "Test",
            "notiz_id": 999
        }
        response = client.post("/api/kiantworten/", json=kiantwort_with_invalid_notiz)
        assert response.status_code == 200  # API akzeptiert nicht existierende notiz_ids

        # Quiz-Frage mit nicht existierender Session wird akzeptiert
        frage_with_invalid_session = {
            "frage": "Test?",
            "Antwort": "Test",
            "Erklaerung": "Test",
            "quiz_session_id": 999
        }
        response = client.post("/api/quiz-fragen/", json=frage_with_invalid_session)
        assert response.status_code == 200  # API akzeptiert nicht existierende quiz_session_ids

        # Versuche, nicht existierende Entitäten zu verknüpfen
        response = client.post("/api/notizen/999/dateien/999")
        assert response.status_code == 404

        response = client.post("/api/quiz-sessions/999/dateien/999")
        assert response.status_code == 404

        # Versuche, nicht existierende Entitäten zu aktualisieren
        response = client.put("/api/dateien/999", json={"titel": "Test"})
        assert response.status_code == 404

        response = client.put("/api/notizen/999", json={"titel": "Test"})
        assert response.status_code == 404

        # Versuche, nicht existierende Entitäten zu löschen
        response = client.delete("/api/dateien/999")
        assert response.status_code == 404

        response = client.delete("/api/notizen/999")
        assert response.status_code == 404

    def test_api_health_endpoints(self, client: TestClient):
        """Test: API Health und Root Endpunkte"""
        
        # Root Endpunkt
        response = client.get("/")
        assert response.status_code == 200
        assert "Lernassistent API" in response.json()["message"]

        # Health Check
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
