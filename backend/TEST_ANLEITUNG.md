# 🧪 Test-Anleitung - Lernassistent API

## Schnellstart

### 1. Vorbereitung
```bash
cd backend
source .venv/bin/activate  # Linux/macOS
# oder
.venv\Scripts\activate     # Windows

# Test-Abhängigkeiten installieren
pip install pytest pytest-asyncio httpx
```

### 2. Alle Tests ausführen
```bash
python -m pytest tests/
```

### 3. Tests mit detaillierter Ausgabe
```bash
pytest -v
```

## 📋 Test-Kommandos

### Grundlegende Kommandos
```bash
# Alle Tests ausführen
pytest

# Nur bestimmte Test-Datei
pytest tests/test_dateien.py

# Nur bestimmte Test-Klasse
pytest tests/test_dateien.py::TestDateienAPI

# Nur bestimmten Test
pytest tests/test_dateien.py::TestDateienAPI::test_create_datei

# Tests mit Live-Output
pytest -s

# Tests stoppen beim ersten Fehler
pytest -x
```

### Coverage-Reports
```bash
# Mit Coverage-Report
pytest --cov=.

# HTML Coverage-Report
pytest --cov=. --cov-report=html
# Dann öffnen: htmlcov/index.html
```

## 🎯 Test-Kategorien

### Unit Tests (einzelne API-Endpunkte)
```bash
pytest tests/test_dateien.py        # Dateien-API
pytest tests/test_notizen.py        # Notizen-API
pytest tests/test_kiantworten.py    # KI-Antworten-API
pytest tests/test_quiz_sessions.py  # Quiz-Sessions-API
pytest tests/test_quiz_fragen.py    # Quiz-Fragen-API
```

### Integrationstests (komplette Workflows)
```bash
pytest tests/test_integration.py
```

## 📊 Was wird getestet?

### ✅ Alle CRUD-Operationen
- **Create**: POST-Endpunkte
- **Read**: GET-Endpunkte (alle & einzelne)
- **Update**: PUT-Endpunkte
- **Delete**: DELETE-Endpunkte

### ✅ Alle Relationen
- **Dateien ↔ Notizen** (Many-to-Many)
- **Dateien ↔ Quiz-Sessions** (Many-to-Many)
- **Notizen → KI-Antworten** (One-to-Many)
- **Quiz-Sessions → Quiz-Fragen** (One-to-Many)

### ✅ Fehlerbehandlung
- 404 Fehler (nicht gefunden)
- 422 Fehler (Validierung)
- Foreign Key Constraints
- Edge Cases

### ✅ Integrationstests
- Vollständige Workflows
- Cascade Delete
- Datenkonsistenz
- Komplexe Verknüpfungen

## 🔍 Beispiel-Testlauf

```bash
$ pytest -v

========================= test session starts =========================
platform darwin -- Python 3.11.0
collected 89 items

tests/test_dateien.py::TestDateienAPI::test_create_datei PASSED     [  1%]
tests/test_dateien.py::TestDateienAPI::test_get_all_dateien_empty PASSED [  2%]
tests/test_dateien.py::TestDateienAPI::test_get_datei_by_id PASSED  [  3%]
...
tests/test_integration.py::TestIntegration::test_complete_workflow PASSED [98%]
tests/test_integration.py::TestIntegration::test_cascade_delete_behavior PASSED [99%]
tests/test_integration.py::TestIntegration::test_api_health_endpoints PASSED [100%]

========================= 89 passed in 12.34s =========================
```

## 🚨 Troubleshooting

### Problem: Tests schlagen fehl
```bash
# Detaillierte Fehlermeldungen anzeigen
pytest -v -s

# Nur fehlgeschlagene Tests erneut ausführen
pytest --lf
```

### Problem: Import-Fehler
```bash
# Sicherstellen, dass virtuelle Umgebung aktiviert ist
source .venv/bin/activate

# Abhängigkeiten neu installieren
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx
```

### Problem: Datenbank-Fehler
Die Tests verwenden eine In-Memory SQLite-Datenbank, die automatisch für jeden Test erstellt wird. Bei Problemen:

```bash
# Tests einzeln ausführen
pytest tests/test_dateien.py::TestDateienAPI::test_create_datei -v -s
```

## 📈 Test-Statistiken

Nach einem vollständigen Testlauf sollten Sie sehen:

- **85 Tests** insgesamt
- **100% Pass-Rate** (alle Tests bestehen)
- **~95%+ Code Coverage**
- **Laufzeit**: ~1 Sekunde

## 🎉 Erfolgreich getestet!

Wenn alle Tests grün sind (PASSED), funktioniert die API korrekt:

✅ Alle CRUD-Operationen funktionieren  
✅ Alle Relationen sind korrekt implementiert  
✅ Fehlerbehandlung ist robust  
✅ Integrationstests bestehen  
✅ API ist produktionsbereit  

## 📚 Weitere Informationen

Für detaillierte Informationen siehe: `tests/README.md`

---

**Tipp**: Führen Sie die Tests regelmäßig aus, besonders nach Änderungen an der API!
