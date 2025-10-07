# API Test Bodies für Swagger

Diese Datei enthält alle JSON Request Bodies zum Testen der API-Endpunkte mit Swagger UI.

## Dateien API (`/api/dateien`)

### POST `/api/dateien/` - Datei erstellen
```json
{
  "titel": "Mathematik Vorlesung 1",
  "pfad": "/uploads/mathe_vorlesung_1.pdf",
  "dateiart": "PDF",
  "dozent": "Prof. Dr. Schmidt",
  "semester": "WS 2024/25",
  "modul": "Mathematik I"
}
```

### PUT `/api/dateien/{datei_id}` - Datei aktualisieren
```json
{
  "titel": "Mathematik Vorlesung 1 - Überarbeitet",
  "dozent": "Prof. Dr. Schmidt-Müller",
  "semester": "WS 2024/25"
}
```

## Notizen API (`/api/notizen`)

### POST `/api/notizen/` - Notiz erstellen
```json
{
  "titel": "Wichtige Mathematik-Konzepte",
  "labels": {
    "fach": "Mathematik",
    "schwierigkeit": "mittel",
    "thema": "Lineare Algebra",
    "tags": ["Vektoren", "Matrizen", "Determinanten"]
  },
  "reihenfolgeKiAntworten": [1, 3, 2]
}
```

### PUT `/api/notizen/{notiz_id}` - Notiz aktualisieren
```json
{
  "titel": "Erweiterte Mathematik-Konzepte",
  "labels": {
    "fach": "Mathematik",
    "schwierigkeit": "schwer",
    "thema": "Lineare Algebra",
    "tags": ["Vektoren", "Matrizen", "Determinanten", "Eigenwerte"]
  }
}
```

## KI-Antworten API (`/api/kiantworten`)

### POST `/api/kiantworten/` - KI-Antwort erstellen
```json
{
  "inhalt": "Eine Matrix ist eine rechteckige Anordnung von Zahlen, Symbolen oder Ausdrücken in Zeilen und Spalten. Matrizen werden in der linearen Algebra verwendet, um lineare Transformationen darzustellen und Systeme linearer Gleichungen zu lösen.",
  "kommentar": "Grundlegende Definition von Matrizen",
  "typ": "Definition",
  "notiz_id": 1
}
```

### PUT `/api/kiantworten/{kiantwort_id}` - KI-Antwort aktualisieren
```json
{
  "inhalt": "Eine Matrix ist eine rechteckige Anordnung von Zahlen, Symbolen oder Ausdrücken in Zeilen und Spalten. Matrizen werden in der linearen Algebra verwendet, um lineare Transformationen darzustellen und Systeme linearer Gleichungen zu lösen. Beispiel: Eine 2x3-Matrix hat 2 Zeilen und 3 Spalten.",
  "kommentar": "Erweiterte Definition mit Beispiel",
  "typ": "Definition mit Beispiel"
}
```

## Quiz-Sessions API (`/api/quiz-sessions`)

### POST `/api/quiz-sessions/` - Quiz-Session erstellen
```json
{
  "titel": "Mathematik Quiz - Lineare Algebra"
}
```

### PUT `/api/quiz-sessions/{quiz_session_id}` - Quiz-Session aktualisieren
```json
{
  "titel": "Mathematik Quiz - Erweiterte Lineare Algebra"
}
```

## Quiz-Fragen API (`/api/quiz-fragen`)

### POST `/api/quiz-fragen/` - Quiz-Frage erstellen
```json
{
  "frage": "Was ist eine Matrix?",
  "Antwort": "Eine rechteckige Anordnung von Zahlen in Zeilen und Spalten",
  "Erklaerung": "Matrizen sind fundamentale Objekte in der linearen Algebra. Sie bestehen aus Elementen, die in einem rechteckigen Schema angeordnet sind. Eine m×n-Matrix hat m Zeilen und n Spalten.",
  "quiz_session_id": 1
}
```

### PUT `/api/quiz-fragen/{quiz_frage_id}` - Quiz-Frage aktualisieren
```json
{
  "frage": "Was ist eine Matrix und wie wird sie notiert?",
  "Antwort": "Eine rechteckige Anordnung von Zahlen in Zeilen und Spalten, notiert als A = [aij]",
  "Erklaerung": "Matrizen sind fundamentale Objekte in der linearen Algebra. Sie bestehen aus Elementen aij, die in einem rechteckigen Schema angeordnet sind, wobei i die Zeile und j die Spalte bezeichnet."
}
```

## Weitere Beispiele für komplexere Daten

### Notiz mit komplexeren Labels
```json
{
  "titel": "Algorithmen und Datenstrukturen",
  "labels": {
    "fach": "Informatik",
    "schwierigkeit": "schwer",
    "thema": "Algorithmen",
    "tags": ["Sortierung", "Suche", "Komplexität"],
    "semester": "3",
    "credits": 6,
    "wichtig": true,
    "deadline": "2024-12-15"
  },
  "reihenfolgeKiAntworten": []
}
```

### KI-Antwort für Programmierung
```json
{
  "inhalt": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
  "kommentar": "Implementierung des Quicksort-Algorithmus in Python",
  "typ": "Code-Beispiel",
  "notiz_id": 2
}
```

### Quiz-Frage für Programmierung
```json
{
  "frage": "Was ist die durchschnittliche Zeitkomplexität des Quicksort-Algorithmus?",
  "Antwort": "O(n log n)",
  "Erklaerung": "Quicksort hat im Durchschnitt eine Zeitkomplexität von O(n log n). Im schlechtesten Fall (bereits sortierte Liste) kann sie jedoch O(n²) betragen. Die beste Zeitkomplexität ist ebenfalls O(n log n).",
  "quiz_session_id": 2
}
```

## Relationen testen

### Datei mit Notiz verknüpfen
- **POST** `/api/notizen/{notiz_id}/dateien/{datei_id}`
- Kein Body erforderlich

### Datei von Notiz trennen
- **DELETE** `/api/notizen/{notiz_id}/dateien/{datei_id}`
- Kein Body erforderlich

### Datei mit Quiz-Session verknüpfen
- **POST** `/api/quiz-sessions/{quiz_session_id}/dateien/{datei_id}`
- Kein Body erforderlich

### Datei von Quiz-Session trennen
- **DELETE** `/api/quiz-sessions/{quiz_session_id}/dateien/{datei_id}`
- Kein Body erforderlich

## Test-Reihenfolge Empfehlung

1. **Dateien erstellen** (POST `/api/dateien/`)
2. **Notizen erstellen** (POST `/api/notizen/`)
3. **Quiz-Sessions erstellen** (POST `/api/quiz-sessions/`)
4. **KI-Antworten erstellen** (POST `/api/kiantworten/`)
5. **Quiz-Fragen erstellen** (POST `/api/quiz-fragen/`)
6. **Relationen testen** (Verknüpfungen zwischen Entitäten)
7. **GET-Requests testen** (Alle Daten abrufen)
8. **PUT-Requests testen** (Daten aktualisieren)
9. **DELETE-Requests testen** (Daten löschen)

## Swagger UI Zugriff

Nach dem Start der API ist Swagger UI verfügbar unter:
- **URL**: `http://localhost:8000/docs`
- **Alternative**: `http://localhost:8000/redoc`

## API Endpunkte Übersicht

### Dateien
- `GET /api/dateien/` - Alle Dateien
- `POST /api/dateien/` - Datei erstellen
- `GET /api/dateien/{id}` - Datei abrufen
- `PUT /api/dateien/{id}` - Datei aktualisieren
- `DELETE /api/dateien/{id}` - Datei löschen
- `GET /api/dateien/{id}/notizen` - Notizen einer Datei
- `GET /api/dateien/{id}/quiz-sessions` - Quiz-Sessions einer Datei

### Notizen
- `GET /api/notizen/` - Alle Notizen
- `POST /api/notizen/` - Notiz erstellen
- `GET /api/notizen/{id}` - Notiz abrufen
- `PUT /api/notizen/{id}` - Notiz aktualisieren
- `DELETE /api/notizen/{id}` - Notiz löschen
- `GET /api/notizen/{id}/dateien` - Dateien einer Notiz
- `GET /api/notizen/{id}/kiantworten` - KI-Antworten einer Notiz
- `POST /api/notizen/{id}/dateien/{datei_id}` - Datei verknüpfen
- `DELETE /api/notizen/{id}/dateien/{datei_id}` - Datei trennen

### KI-Antworten
- `GET /api/kiantworten/` - Alle KI-Antworten
- `POST /api/kiantworten/` - KI-Antwort erstellen
- `GET /api/kiantworten/{id}` - KI-Antwort abrufen
- `PUT /api/kiantworten/{id}` - KI-Antwort aktualisieren
- `DELETE /api/kiantworten/{id}` - KI-Antwort löschen
- `GET /api/kiantworten/notiz/{notiz_id}` - KI-Antworten einer Notiz

### Quiz-Sessions
- `GET /api/quiz-sessions/` - Alle Quiz-Sessions
- `POST /api/quiz-sessions/` - Quiz-Session erstellen
- `GET /api/quiz-sessions/{id}` - Quiz-Session abrufen
- `PUT /api/quiz-sessions/{id}` - Quiz-Session aktualisieren
- `DELETE /api/quiz-sessions/{id}` - Quiz-Session löschen
- `GET /api/quiz-sessions/{id}/fragen` - Fragen einer Quiz-Session
- `GET /api/quiz-sessions/{id}/dateien` - Dateien einer Quiz-Session
- `POST /api/quiz-sessions/{id}/dateien/{datei_id}` - Datei verknüpfen
- `DELETE /api/quiz-sessions/{id}/dateien/{datei_id}` - Datei trennen

### Quiz-Fragen
- `GET /api/quiz-fragen/` - Alle Quiz-Fragen
- `POST /api/quiz-fragen/` - Quiz-Frage erstellen
- `GET /api/quiz-fragen/{id}` - Quiz-Frage abrufen
- `PUT /api/quiz-fragen/{id}` - Quiz-Frage aktualisieren
- `DELETE /api/quiz-fragen/{id}` - Quiz-Frage löschen
