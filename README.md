# Lernassistent

## Projektübersicht

Ziel des Projekts ist es, einen fortschrittlichen KI-basierten Lernassistenten zu entwickeln, der Studierende und Schüler in ihren Lernprozessen unterstützt. Das System ermöglicht verschiedene Lernarten und hilft dabei, diese wissenschaftlich fundiert effizienter zu gestalten. Der Lernassistent bietet Funktionen zur Verwaltung von Dateien, Notizen, KI-generierten Antworten und interaktiven Quiz-Sessions. Das Projekt entsteht im Rahmen der Studienprojekte der Hochschule für Wirtschaft und Recht Berlin.

## Technologien

Für das Projekt werden folgende Technologien verwendet:

### Frontend
- **React**: Für die Entwicklung der Benutzeroberfläche, um interaktive und reaktive Elemente zu gestalten.
- **TypeScript**: Eingesetzt für stark typisierten, fehlerfreien Code sowohl beim Entwickeln von neuen Komponenten als auch bei der Wartung und Weiterentwicklung der Anwendung.

### Backend
- **Python FastAPI**: Zur Entwicklung des Backends, das schnelle und effiziente API-Endpoints bereitstellt.
- **SQLite Datenbank**: Verwendet zur Speicherung von Daten, um einfache und schnelle Datenbankinteraktionen zu gewährleisten.
- **SQLAlchemy**: Eingesetzt als ORM (Object-Relational Mapper), um die Datenbankverwaltung und Komplexitätsreduktion bei SQL-Abfragen zu unterstützen.
- **Pydantic**: Für Datenvalidierung und Serialisierung der API-Modelle.

### AI Integration
- **KI-Modelle**: Integration verschiedener KI-Modelle zur Generierung von Lerninhalten, Antworten und personalisierten Lernempfehlungen.

## Setup und Installation

### Voraussetzungen

- Node.js für das Frontend
- Python 3.11+ für das Backend
- Git für die Versionskontrolle

### Installation

1. **Repository klonen**
   ```bash
   git clone https://github.com/MarlenKoch/studienprojekt2.git
   cd studienprojekt2
   ```

2. **Backend (Python FastAPI)**
   - Navigieren Sie in das Verzeichnis des Backend-Projekts:
     ```bash
     cd backend
     ```
   - Erstellen Sie eine virtuelle Umgebung:
     ```bash
     python -m venv .venv
     ```
   - Aktivieren Sie die virtuelle Umgebung:
     - Auf Mac/Linux:
       ```bash
       source .venv/bin/activate
       ```
     - Auf Windows:
       ```bash
       .venv\Scripts\activate
       ```
   - Installieren Sie die erforderlichen Python-Pakete:
     ```bash
     pip install -r requirements.txt
     ```

3. **Frontend (React TypeScript)**
   - Navigieren Sie in das Verzeichnis des Frontend-Projekts:
     ```bash
     cd frontend
     ```
   - Führen Sie den folgenden Befehl aus, um die Abhängigkeiten zu installieren:
     ```bash
     npm install
     ```

## Verwendung

### Starten des Backend-Servers

Innerhalb des Backend-Projektverzeichnisses (mit aktivierter virtueller Umgebung):
```bash
uvicorn main:app --reload --port 8001
```

Die API ist dann verfügbar unter:
- **API**: http://localhost:8001
- **Swagger Dokumentation**: http://localhost:8001/docs
- **ReDoc Dokumentation**: http://localhost:8001/redoc

### Starten des Frontend-Servers

Innerhalb des Frontend-Projektverzeichnisses:
```bash
npm start
```

### Testen der Anwendung

Sobald beide Server laufen, öffnen Sie Ihren bevorzugten Webbrowser und navigieren Sie zur URL:
```
http://localhost:3000
```

## API-Funktionen

Der Lernassistent bietet folgende Hauptfunktionen:

### 📁 Dateiverwaltung
- Upload und Verwaltung von Lernmaterialien (PDFs, Dokumente)
- Kategorisierung nach Fach, Dozent, Semester und Modul
- Verknüpfung mit Notizen und Quiz-Sessions

### 📝 Notizensystem
- Erstellung und Verwaltung von strukturierten Notizen
- Flexible Label-Systeme für Kategorisierung
- Verknüpfung mit Dateien und KI-generierten Inhalten

### 🤖 KI-Antworten
- Generierung von KI-basierten Lerninhalten
- Verschiedene Antworttypen (Definitionen, Beispiele, Code)
- Kommentierung und Bewertung von KI-Antworten

### 🎯 Quiz-System
- Erstellung interaktiver Quiz-Sessions
- Fragen mit Antworten und Erklärungen
- Verknüpfung mit Lernmaterialien

## Tests

Das Projekt verfügt über eine umfassende Test-Suite:

### Tests ausführen
```bash
cd backend
source .venv/bin/activate  # Linux/macOS
python -m pytest tests/ -v
```

## Projektstruktur

```
studienprojekt2/
├── backend/                    # FastAPI Backend
│   ├── datenbank/             # Datenbankmodelle und CRUD
│   │   ├── modelle.py         # SQLAlchemy Modelle
│   │   ├── pydanticModelle.py # Pydantic Schemas
│   │   ├── crud.py            # CRUD Operationen
│   │   └── router/            # API Router
│   ├── tests/                 # Test-Suite
│   ├── main.py               # FastAPI Anwendung
│   └── requirements.txt      # Python Dependencies
├── frontend/                  # React Frontend
└── README.md                 # Projektdokumentation
```

