---
name: actaone-local-dev
description: Den actaOne-LibreChat-Fork lokal als Dev-Server starten oder einen laufenden wiederfinden – Checkout/Worktree und Commit bestimmen, Ports zuordnen, Mongo und benötigte Dienste, lokales Testkonto, optional LAN-/Tailscale-Freigabe. Nutzen bei "starte lokal", "Dev-Server", "gib mir lokale Login-Daten", "welcher Port", "über Netzwerk erreichbar", "localhost zeigt alten Stand", "lokal geht X nicht". Nicht für Deploys auf Staging, Branch-Instanzen oder Kunden.
---

# actaOne-LibreChat lokal entwickeln

Abgeleitet aus lokalen Start-Memories und dem heutigen Fork-Stand. Herkunft, geprüfter Stand und Grenzen: [references/sources.md](references/sources.md). Die Schritte sind aus Quellen abgeleitet und **nicht in dieser Fassung live durchlaufen**.

## Voraussetzungen

- **LibreChat-Fork** `github.com/actago/LibreChat`. Finden: aktuelles Arbeitsverzeichnis, ein Worktree des Forks (`git worktree list` im Fork-Checkout) oder das Submodul `services/LibreChat` eines actaOne-Checkouts; sonst nachfragen. Fehlt er, melden.
- Node laut `.nvmrc` des Checkouts, npm. Mongo als eigene nachgewiesen lokale Testinstanz. Ein erreichbarer Port oder eine localhost-URI allein belegt keine isolierte Datenbank.
- Kein Zugang zu Live-Systemen nötig. Echte Modellaufrufe brauchen einen Provider-Key; den liefert der Nutzer oder ein beauftragter, ausgabefreier Vault-Abruf.

## 1. Checkout und Commit festlegen

Den Checkout nehmen, um den es dem Nutzer geht (Branch/PR/Worktree), oder einen frischen Worktree anlegen, wenn er das will. Festhalten: Pfad, `git rev-parse HEAD`, ob der Baum dirty ist und welche Quellenrevision zum Rezept gehört. Ein Submodul kann einen anderen Stand als der separat geprüfte Fork haben; Scripts am tatsächlich verwendeten Commit lesen. Diese Angaben gehören in die Antwort „läuft auf Port X".

- Vorhandene Git-Identität erhalten. Nur bei beauftragter abweichender Identität pro Aufruf `git -c user.name=… -c user.email=…` oder Umgebungsvariablen verwenden; nicht ungefragt die Repo-Konfiguration ändern.
- In Worktrees des Submoduls `services/LibreChat` nie `extensions.worktreeConfig` setzen und keine Renormalisierung per `git rm --cached -r . && git reset --hard` (zerstört das Modul-Gitdir).
- Fremde Änderungen im Checkout gehören anderen Agenten oder dem Nutzer: nicht zurücksetzen, nicht mit-committen.

## 2. Bauen

`npm ci`, dann `npm run build:packages`. Nach Änderungen an `packages/data-provider` Vite neu starten; nach Backend-TS-Änderungen das betroffene Paket neu bauen (`build:data-schemas`, `build:api`), sonst läuft alter Code. Das Backend liest beim Start `client/dist/index.html`: entweder `npm run build:client` oder eine Platzhalterdatei anlegen (`dist/` ist gitignored), wenn nur Vite benutzt wird.

## 3. Ports zuordnen

Standard: Backend `PORT=3080`, Vite `PORT=3090` mit Proxy auf `BACKEND_PORT` (Default 3080). Vor dem Start freie Ports prüfen (`netstat -ano | findstr LISTENING` bzw. `ss -ltnp`) und belegte Ports dem Besitzer zuordnen; fremde Prozesse und Container nicht stoppen.

- Vite liest **dieselbe** Variable `PORT` wie das Backend. Beide getrennt starten und `PORT`/`BACKEND_PORT` je Prozess setzen.
- Vite hat `strictPort: false` und weicht still auf den nächsten Port aus. `--strictPort` übergeben oder den tatsächlichen Port aus der Vite-Ausgabe lesen.
- Abweichendes Backend-Paar: `PORT`, `DOMAIN_CLIENT`, `DOMAIN_SERVER`, ggf. `MONGO_URI` als Prozess-Env setzen (geht vor `.env`).
- „Läuft der Dev-Server / welcher Port?": PID am Port ermitteln, Kommandozeile und Arbeitsverzeichnis dem Checkout zuordnen, Commit nennen. Bei Abweichung ehrlich „alter Stand auf Port X" melden.

## 4. Konfiguration

Existierende `.env` zunächst erhalten; nur benötigte nicht geheime Felder gezielt lesen, keine Datei ausgeben. Eine eigene neue lokale Konfiguration aus `.env.local.example` oder per Prozess-Env anlegen, ohne fremde Dateien zu überschreiben. Vorhandene Werte sind nicht automatisch für diese Umgebung geeignet. Bekannte Stolpersteine:

- `EMAIL_*`-Platzhalter auskommentieren, sonst scheitern Registrierung/Einladung am Mail-Host.
- `SEARCH=false`, solange kein Meilisearch läuft.
- Eigene YAML über `CONFIG_PATH`; lokale Dateien in `$(git rev-parse --git-path info/exclude)` eintragen statt `.gitignore` zu ändern. Modellauswahl im UI braucht `modelSpecs`/Runtime-Profile; eine aus dem Staging-Template abgeleitete YAML braucht Platzhalterwerte für nicht vorhandene Dienste.
- Headless-/API-Logins lösen Sperren aus: lokal `BAN_VIOLATIONS=false` bzw. höhere Limits.
- Provider-Keys nie ausgeben oder committen. Nur selbst angelegte temporäre Dateien nach der vereinbarten Nutzung entfernen; vorgefundene oder dauerhaft für den Nutzer angelegte Konfiguration nicht löschen.

## 5. Benötigte Dienste

Mongo ist Pflicht. Vor Backendstart, `create-user`, Seeds oder Mongo-Schreibzugriffen Host, Port und Datenbankname der wirksamen `MONGO_URI` ohne Credentials prüfen und dem eigenen lokalen Prozess/Container zuordnen. Port-Forward, fremder Docker-Stack oder Staging-/Kunden-DB sind keine lokale Testbasis. Einen eigenen Datenbanknamen für diesen Checkout verwenden. Ist die Zuordnung unklar, erst eine isolierte Testinstanz bereitstellen; nicht probeweise in die erreichbare DB schreiben.

Lokal **fehlen** standardmäßig: RAG/KB, Presidio, CodeAPI (Dokumenterstellung, Code-Ausführung), Websuche, Bildgenerierung, Exporter/Control-Plane. Nur die Dienste anbinden, die die Aufgabe braucht, und fehlende ausdrücklich nennen, statt lokale Fehler als Codefehler zu werten. Remote-Dienste nur nutzen, wenn der Nutzer das will und Zugang besteht.

## 6. Testkonto

- Erst nach der DB-Zielprüfung ein eigenes, als lokal erkennbares Testkonto anlegen. `npm run create-user` vorher lesen: generierte Passwörter können auf stdout erscheinen. Sichere interaktive Eingabe/Ausgabe verwenden, keine allgemeinen Tool- oder Serverlogs mit Zugangsdaten erzeugen. In `.env.local.example` ist Registrierung aus.
- Login 500 „No user provided" kann durch fehlende `tenantId` entstehen: am aktuellen Schema und Auth-Pfad belegen. Tenant-/Rollenänderungen ausschließlich am eigenen Testkonto in der nachgewiesen isolierten lokalen DB, mit korrekter lokaler Tenant-Zuordnung. Keine pauschale Admin-Reparatur an vorgefundenen Nutzern. Die Erstnutzer-Adminregel am verwendeten Commit prüfen.
- Bestehende Konten anderer Personen oder Agenten nicht zurücksetzen und kein Passwort überschreiben, das jemand anders nutzt (gemeinsame Smoke-/Testkonten sperren sonst deren Arbeitsplatz aus). Unbekanntes Passwort eines fremden Kontos → eigenes Konto anlegen.
- Zugangsdaten über den vorgesehenen sicheren Kanal an den Nutzer übergeben oder durch ihn interaktiv festlegen lassen; nicht in normale Chatantworten, Repo, PR, Memory oder Logs schreiben.

## 7. Netzwerk

Standard ist `localhost`: `HOST=localhost` für Backend und Vite ausdrücklich als Prozessvariable setzen, damit ein altes `HOST=0.0.0.0` aus `.env` nicht gewinnt. Danach tatsächliche Listener mit `netstat`/`ss` prüfen. LAN oder Tailscale nur, wenn der Nutzer es verlangt, und nur so weit wie verlangt:

- Backend `HOST=0.0.0.0`. Vite bindet über dieselbe Variable `HOST`, die aber auch sein Proxy-Ziel bildet (`http://$HOST:$BACKEND_PORT`); ob der Proxy dann das Backend erreicht, ist plattformabhängig und mit einem `/api`-Aufruf über Vite zu prüfen. Für Zugriff per Hostname `VITE_ALLOWED_HOSTS=<hostname>`. `DOMAIN_CLIENT`/`DOMAIN_SERVER` auf die erreichbare Adresse.
- Hinweis geben: Dev-Server mit Testkonto und gelockerten Sperren, kein TLS; Firewallfreigabe bewusst und nur temporär. Nach der Sitzung auf `localhost` zurück, wenn nicht anders gewünscht.

## 8. Laufen lassen und beenden

Prozesse so starten, dass sie die Agentensitzung überleben, wenn der Nutzer länger testen will; Ausgabe in Logdateien außerhalb versionierter Pfade, PIDs festhalten. Am Ende berichten: Checkout, Commit, Ports, laufende PIDs, Testkonto (lokal), fehlende Dienste. Stoppen nur eigene Prozesse.

Plattformspezifische Erfahrungen (Windows, geteilte `node_modules`, Docker Desktop): [references/windows-notes.md](references/windows-notes.md).
