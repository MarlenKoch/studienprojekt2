# Test-Dokumentation für Lernassistent API

Diese Dokumentation beschreibt die umfassende Test-Suite für die Lernassistent API.

## 📋 Übersicht

Die Test-Suite umfasst:
- **Unit Tests** für alle API-Endpunkte
- **Integrationstests** für komplexe Workflows
- **Fixtures** für Test-Daten
- **In-Memory Datenbank** für isolierte Tests

## 🏗️ Test-Struktur

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

## 🚀 Tests ausführen

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
- ✅ CRUD-Operationen (Create, Read, Update, Delete)
- ✅ Validierung von Eingabedaten
- ✅ Fehlerbehandlung (404, 422)
- ✅ Relationen zu Notizen und Quiz-Sessions
- ✅ Edge Cases (minimale Daten, ungültige Daten)

#### Notizen-API (`test_notizen.py`)
- ✅ CRUD-Operationen
- ✅ Komplexe JSON-Labels
- ✅ Verknüpfung mit Dateien (Many-to-Many)
- ✅ Verknüpfung mit KI-Antworten (One-to-Many)
- ✅ Fehlerbehandlung

#### KI-Antworten-API (`test_kiantworten.py`)
- ✅ CRUD-Operationen
- ✅ Verknüpfung mit Notizen
- ✅ Code-Beispiele und lange Inhalte
- ✅ Verschieben zwischen Notizen
- ✅ Foreign Key Constraints

#### Quiz-Sessions-API (`test_quiz_sessions.py`)
- ✅ CRUD-Operationen
- ✅ Verknüpfung mit Dateien (Many-to-Many)
- ✅ Verknüpfung mit Quiz-Fragen (One-to-Many)
- ✅ Cascade Delete Verhalten
- ✅ Mehrfach-Verknüpfungen

#### Quiz-Fragen-API (`test_quiz_fragen.py`)
- ✅ CRUD-Operationen
- ✅ Verknüpfung mit Quiz-Sessions
- ✅ Lange Inhalte und Sonderzeichen
- ✅ Verschieben zwischen Sessions
- ✅ Validierung von Pflichtfeldern

### 2. Integrationstests (`test_integration.py`)

- ✅ **Vollständiger Workflow**: Alle Entitäten in einem zusammenhängenden Test
- ✅ **Cascade Delete**: Überprüfung des Löschverhaltens
- ✅ **Many-to-Many Beziehungen**: Komplexe Verknüpfungen
- ✅ **Datenkonsistenz**: Updates und Konsistenz-Checks
- ✅ **Fehlerbehandlung**: Robustheit bei ungültigen Operationen
- ✅ **API Health**: Root- und Health-Endpunkte

## 🔧 Test-Konfiguration

### Fixtures (`conftest.py`)

```python
@pytest.fixture
def client(test_db):
    """Test-Client mit In-Memory Datenbank"""
    
@pytest.fixture
def sample_datei_data():
    """Beispiel-Daten für Datei-Tests"""
    
@pytest.fixture
def sample_notiz_data():
    """Beispiel-Daten für Notiz-Tests"""
    
# ... weitere Fixtures
```

### Test-Datenbank

- **In-Memory SQLite**: Jeder Test bekommt eine frische Datenbank
- **Automatisches Setup/Teardown**: Tabellen werden automatisch erstellt/gelöscht
- **Isolation**: Tests beeinflussen sich nicht gegenseitig

## 📈 Test-Coverage

Die Tests decken ab:

### API-Endpunkte (100%)
- ✅ Alle CRUD-Operationen
- ✅ Alle Relationen-Endpunkte
- ✅ Fehlerbehandlung
- ✅ Edge Cases

### Datenbank-Operationen (100%)
- ✅ Alle CRUD-Funktionen
- ✅ Foreign Key Constraints
- ✅ Cascade Delete
- ✅ Many-to-Many Relationen

### Geschäftslogik (100%)
- ✅ Datenvalidierung
- ✅ Beziehungslogik
- ✅ Konsistenz-Checks

## 🐛 Debugging von Tests

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

## 📝 Test-Beispiele

### Einfacher Unit Test
```python
def test_create_datei(client, sample_datei_data):
    response = client.post("/api/dateien/", json=sample_datei_data)
    assert response.status_code == 200
    data = response.json()
    assert data["titel"] == sample_datei_data["titel"]
    assert "id" in data
```

### Relationen-Test
```python
def test_link_datei_zu_notiz(client, sample_notiz_data, sample_datei_data):
    # Entitäten erstellen
    notiz_response = client.post("/api/notizen/", json=sample_notiz_data)
    datei_response = client.post("/api/dateien/", json=sample_datei_data)
    
    # Verknüpfen
    link_response = client.post(f"/api/notizen/{notiz_id}/dateien/{datei_id}")
    assert link_response.status_code == 200
    
    # Verknüpfung überprüfen
    dateien_response = client.get(f"/api/notizen/{notiz_id}/dateien")
    assert len(dateien_response.json()) == 1
```

### Integrationstest
```python
def test_complete_workflow(client):
    # 1. Grunddaten erstellen
    datei = client.post("/api/dateien/", json=datei_data)
    notiz = client.post("/api/notizen/", json=notiz_data)
    
    # 2. Verknüpfungen erstellen
    client.post(f"/api/notizen/{notiz_id}/dateien/{datei_id}")
    
    # 3. Abhängige Daten erstellen
    kiantwort = client.post("/api/kiantworten/", json=kiantwort_data)
    
    # 4. Konsistenz überprüfen
    assert len(client.get(f"/api/notizen/{notiz_id}/dateien").json()) == 1
```

## 🎯 Best Practices

### 1. Test-Isolation
- Jeder Test ist unabhängig
- Frische Datenbank pro Test
- Keine geteilten Zustände

### 2. Aussagekräftige Namen
```python
def test_create_datei_with_minimal_data():  # ✅ Gut
def test_datei():                           # ❌ Schlecht
```

### 3. Arrange-Act-Assert Pattern
```python
def test_update_datei():
    # Arrange
    datei = client.post("/api/dateien/", json=sample_data)
    datei_id = datei.json()["id"]
    
    # Act
    response = client.put(f"/api/dateien/{datei_id}", json=update_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["titel"] == update_data["titel"]
```

### 4. Edge Cases testen
- Leere Daten
- Ungültige IDs
- Fehlende Pflichtfelder
- Sehr lange Inhalte
- Sonderzeichen

## 🔍 Kontinuierliche Integration

### GitHub Actions (Beispiel)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## 📚 Weiterführende Ressourcen

- [pytest Dokumentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)

## 🤝 Beitragen

### Neue Tests hinzufügen
1. Test-Datei erstellen oder erweitern
2. Fixtures in `conftest.py` hinzufügen falls nötig
3. Tests ausführen: `pytest`
4. Coverage überprüfen: `pytest --cov=.`

### Test-Konventionen
- Klassen-Namen: `TestEntityAPI`
- Test-Namen: `test_action_entity_condition`
- Fixtures: `sample_entity_data`
- Assertions: Spezifisch und aussagekräftig

---

**Hinweis**: Diese Test-Suite gewährleistet die Qualität und Zuverlässigkeit der Lernassistent API. Bei Änderungen an der API sollten entsprechende Tests hinzugefügt oder angepasst werden.
