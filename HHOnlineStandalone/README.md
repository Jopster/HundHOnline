# HHOnline Standalone

Eigenstaendige HHOnline-Webanwendung mit einem Python-FastAPI-Server, MariaDB und dem vorhandenen HTML-/JavaScript-Frontend. Dieses Projekt hat keine Abhaengigkeit von Odoo.

## Start mit Docker

1. Docker Desktop starten.
2. Im Ordner `HHOnlineStandalone` ausfuehren:

```powershell
docker compose up --build
```

3. `http://localhost:8000` im Browser oeffnen.

Der API-Service erstellt die Tabelle `articles` beim ersten Start und importiert Beispieldaten. Die API-Dokumentation ist unter `http://localhost:8000/docs` verfuegbar.

## Lokaler Python-Start

Eine MariaDB-Datenbank muss erreichbar sein. Die Verbindungszeichenfolge wird ueber `DATABASE_URL` gesetzt; siehe `.env.example`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL = "mysql+pymysql://hhonline:hhonline@localhost:3306/hhonline?charset=utf8mb4"
uvicorn app:app --reload
```

## API

- `GET /api/health` prueft den Dienst.
- `GET /api/articles` listet Artikel. Optional: `search` und `group_name`.
- `POST /api/articles` legt einen Artikel an.
- `PUT /api/articles/{article_id}` aktualisiert einen Artikel.
- `DELETE /api/articles/{article_id}` loescht einen Artikel.
