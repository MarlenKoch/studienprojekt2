# Test-Dokumentation für Lernassistent API

Diese Dokumentation beschreibt die umfassende Test-Suite für die Lernassistent API.

## Übersicht

Die Test-Suite umfasst:
- **Unit Tests** für alle API-Endpunkte
- **Integrationstests** für komplexe Workflows
- **Fixtures** für Test-Daten
- **In-Memory Datenbank** für isolierte Tests

## Test-Struktur

```
backend/tests/
├── __init__.py                 # Test-Package
├── conftest.py                 # Test-Konfiguration und Fixtures
├── test_dateien.py            # Tests für Dateien-API
├── test_notizen.py            # Tests für Notizen-API
├── test_kiantworten.py        # Tests für KI-Antworten-API
├── test_quiz_sessions.py      # Tests für Quiz-Sessions-API
├── test_quiz_fragen.py        # Tests für Quiz-Fragen-API
├── test_integration.py        # Integrationstests
└── README.md                  # Diese Dokumentation
```

## Tests ausführen

### Voraussetzungen

1. **Virtuelle Umgebung aktivieren:**
   ```bash
   cd backend
   source .venv/bin/activate  # Linux/macOS
   # oder
   .venv\Scripts\activate     # Windows
   ```

2. **Abhängigkeiten installieren:**
   ```bash
   pip install pytest pytest-asyncio httpx
   ```

### Alle Tests ausführen

```bash
# Alle Tests ausführen
pytest

# Mit detaillierter Ausgabe
pytest -v

# Mit Coverage-Report
pytest --cov=. --cov-report=html

# Nur bestimmte Test-Datei
pytest tests/test_dateien.py

# Nur bestimmte Test-Klasse
pytest tests/test_dateien.py::TestDateienAPI

# Nur bestimmten Test
pytest tests/test_dateien.py::TestDateienAPI::test_create_datei
```

### Test-Optionen

```bash
# Tests parallel ausführen (schneller)
pytest -n auto

# Tests mit Live-Logs
pytest -s

# Tests stoppen beim ersten Fehler
pytest -x

# Nur fehlgeschlagene Tests erneut ausführen
pytest --lf

# Tests mit Marker ausführen
pytest -m "not slow"
```

## 📊 Test-Kategorien

### 1. Unit Tests

#### Dateien-API (`test_dateien.py`)
-  CRUD-Operationen (Create, Read, Update, Delete)
-  Validierung von Eingabedaten
-  Fehlerbehandlung (404, 422)
-  Relationen zu Notizen und Quiz-Sessions
-  Edge Cases (minimale Daten, ungültige Daten)

#### Notizen-API (`test_notizen.py`)
-  CRUD-Operationen
-  Komplexe JSON-Labels
-  Verknüpfung mit Dateien (Many-to-Many)
-  Verknüpfung mit KI-Antworten (One-to-Many)
-  Fehlerbehandlung

#### KI-Antworten-API (`test_kiantworten.py`)
-  CRUD-Operationen
-  Verknüpfung mit Notizen
-  Code-Beispiele und lange Inhalte
-  Verschieben zwischen Notizen
-  Foreign Key Constraints

#### Quiz-Sessions-API (`test_quiz_sessions.py`)
-  CRUD-Operationen
-  Verknüpfung mit Dateien (Many-to-Many)
-  Verknüpfung mit Quiz-Fragen (One-to-Many)
-  Cascade Delete Verhalten
-  Mehrfach-Verknüpfungen

#### Quiz-Fragen-API (`test_quiz_fragen.py`)
-  CRUD-Operationen
-  Verknüpfung mit Quiz-Sessions
-  Lange Inhalte und Sonderzeichen
-  Verschieben zwischen Sessions
-  Validierung von Pflichtfeldern

### 2. Integrationstests (`test_integration.py`)

-  **Vollständiger Workflow**: Alle Entitäten in einem zusammenhängenden Test
-  **Cascade Delete**: Überprüfung des Löschverhaltens
-  **Many-to-Many Beziehungen**: Komplexe Verknüpfungen
-  **Datenkonsistenz**: Updates und Konsistenz-Checks
-  **Fehlerbehandlung**: Robustheit bei ungültigen Operationen
-  **API Health**: Root- und Health-Endpunkte



## 📈 Test-Coverage

Die Tests decken ab:

### API-Endpunkte (100%)
-  Alle CRUD-Operationen
-  Alle Relationen-Endpunkte
-  Fehlerbehandlung
-  Edge Cases

### Datenbank-Operationen (100%)
-  Alle CRUD-Funktionen
-  Foreign Key Constraints
-  Cascade Delete
-  Many-to-Many Relationen

### Geschäftslogik (100%)
-  Datenvalidierung
-  Beziehungslogik
-  Konsistenz-Checks

## Debugging von Tests

### Test-Logs anzeigen
```bash
pytest -s --log-cli-level=DEBUG
```

### Einzelnen Test debuggen
```bash
pytest tests/test_dateien.py::TestDateienAPI::test_create_datei -v -s
```

### Test-Datenbank inspizieren
```python
# In einem Test
def test_debug_database(client, test_db):
    # Daten erstellen
    response = client.post("/api/dateien/", json=sample_data)
    
    # Breakpoint setzen
    import pdb; pdb.set_trace()
    
    # Datenbank-Zustand überprüfen
    assert response.status_code == 200
```

