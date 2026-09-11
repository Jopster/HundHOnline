# HHOnline Standalone

Eigenstaendige HHOnline-Webanwendung mit einem Python-FastAPI-Server, lokaler MariaDB und dem vorhandenen HTML-/JavaScript-Frontend. Dieses Projekt hat keine Abhaengigkeit von Odoo oder Docker.

## Lokaler Start

Die lokale MariaDB verwendet folgende Einrichtung:

- Datenverzeichnis: `/opt/hhonline/mysql/data`
- Datenbank: `hhonline`
- Benutzer: `hhonline_user`
- Passwort: `hh2026_Mysql`

MariaDB muss aktiv sein:

```bash
systemctl start mariadb
```

Im Ordner `HHOnlineStandalone` den API-Server starten:

```bash
./start-api.sh
```

Das Skript legt bei Bedarf `.venv` an, installiert die Abhaengigkeiten und startet den Dienst auf `http://0.0.0.0:8000`. Die Anwendung ist lokal unter `http://localhost:8000` erreichbar. Die API-Dokumentation ist unter `http://localhost:8000/docs` verfuegbar.

Beim ersten Seitenaufruf erscheint ein Login-Dialog. Die lokalen Zugangsdaten sind Benutzername `HHOnline` und Passwort `HHOnline`. Der Browser erhaelt nach erfolgreicher Anmeldung eine signierte Session; die API und jede bedienbare Aktion pruefen ihre Gueltigkeit. Fuer eine oeffentliche Bereitstellung muessen `AUTH_PASSWORD` und `SESSION_SECRET` als Umgebungsvariablen gesetzt werden.

Fuer einen anderen Port kann `PORT` gesetzt werden:

```bash
PORT=8001 ./start-api.sh
```

## API

- `GET /api/health` prueft den Dienst.
- `GET /api/articles` listet Artikel. Optional: `search` und `group_name`.
- `POST /api/articles` legt einen Artikel an.
- `PUT /api/articles/{article_id}` aktualisiert einen Artikel.
- `DELETE /api/articles/{article_id}` loescht einen Artikel.
