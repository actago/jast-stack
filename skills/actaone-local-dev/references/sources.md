# Herkunft, geprüfter Stand und Grenzen

Stand: 2026-11-17. Kein gleichnamiger Vorgängerskill; Ausgangspunkt sind lokale Start-Memories und der heutige Fork-Stand. Keine Server gestartet, kein `npm ci`, kein Deploy, keine Änderung an Checkouts oder aktiven Installationen.

## LibreChat-Fork (`github.com/actago/LibreChat`)

Lokaler Checkout auf Branch `feat/rag-chunk-preview`; gelesen wurde **`origin/main` = `156c677d40da`** (letzter lokaler Fetch, Commit vom 2026-11-13). Hashes = Git-Blob-IDs (gekürzt).

| Datei | Blob | Geprüft |
|---|---|---|
| `package.json` | `380d7810304d` | `backend:dev`, `frontend:dev`, `build:packages`, `build:client`, `create-user`, `postinstall` (Patch-Skript) |
| `.env.local.example` | `fcb4f45949c9` | `PORT=3080`, `MONGO_URI` 27017, `ALLOW_REGISTRATION=false`, `EMAIL_*`-Platzhalter, Tenant-Schalter |
| `.env.example` | `908e69d9071b` | `BAN_VIOLATIONS`, `LOGIN_MAX`, `NON_BROWSER_VIOLATION_SCORE`, `SEARCH` |
| `client/vite.config.ts` | `8aea5e2b5c5b` | `PORT` (Default 3090), `strictPort: false`, `HOST` für Bindung und Proxy-Ziel, `BACKEND_PORT`, `VITE_ALLOWED_HOSTS` |
| `api/server/index.js` | `10fb8e416709` | `PORT`/`HOST`, `readFileSync(dist/index.html)` beim Start |
| `config/create-user.js` | `4d05211acc5f` | Passwort interaktiv, Argument nur mit Warnung |
| `.nvmrc` | – | Node `24.16.0` |

## Memories (historische Belege, keine aktuellen Befehle)

| Quelle | sha256 | Stand | Verwendet für |
|---|---|---|---|
| Memory `librechat-lokaler-dev-server` (actaOne-Projekt) | `6eba0c3997993ec1` | 2026-11-10 | Grundrezept, `.env`-Fallen, dist-Stub, Ports bei Docker Desktop, Login-Sperre, Prozessdauer, Key-Aufräumen |
| Memory `local-user-tenantid-pflicht` (actaOne-Projekt) | `dfcbe98bf91c5997` | 2026-09-30 | `tenantId`/ADMIN per roher Mongo-Shell |
| Memory `git-worktree-submodule-hazard` (actaOne-Projekt) | `16f421551e20c081` | 2026-09-12 | kein `extensions.worktreeConfig` im Submodul |
| Memory `local-real-instance` (LibreChat-Projekt) | `0b7d699f09d8cfb4` | 2026-09-10 | Mongo-Forward, Junction-Fallen, CodeAPI fehlt lokal |
| Memory `genui-local-test-instance` (LibreChat-Projekt) | `a3bf9bedaeb64fc5` | 2026-10-23 | was lokal fehlt, Rebuild nach data-provider |
| Memory `worktree-shared-node-modules` (LibreChat-Projekt) | `762b19781a3e6699` | 2026-11-13 | geteilte `node_modules`, Postinstall-Patch, Junction-Löschung |
| Memory `pr-ci-local-emulation` (LibreChat-Projekt) | `026ca72fdc56a669` | 2026-11-12 | `sort-imports` nie ohne Dateiliste, `MSYS_NO_PATHCONV` |
| Agentenprofil `actaone-librechat.md` (Standardprofil) | `ca92e6b6188eb5e2` | – | Baseline-Vergleich, kein Startrezept vorhanden |
| actaOne `docs/RELEASE_PROCESS.md` (Blob `4d0cd3c9bb1a`) | – | 2026-11-13 | gemeinsame Smoke-Testkonten nicht neu setzen |
| JAST-Stack `research/synthesis.md`, `claude-session-audit.md` §5, Befund L723 | – | 2026-11-17 | Zuschnitt, Git-Identität nicht per `git config` |

## Bewusst nicht übernommen

- Persönliche Pfade (T3-Worktree-Verzeichnisse, Hilfsskripte `mongo.mjs`/`start-dev.ps1`, `.superpowers/`-Helfer), konkrete Testkonten und Passwörter aus Memories, Tunnel-/VPN-Zugänge.
- Abruf von Provider-Keys aus dem Staging-Vault als Standardschritt; nur noch als beauftragte, ausgabefreie Option erwähnt.
- Feature-spezifische Rezepte (GenUI, Admin-Panel gegen echtes Backend, Screenshot-Harness).

## Grenzen

- Nicht live durchlaufen; Ports und Fallen gegen den Fork-Stand vom 2026-11-13 gelesen, Rechnerzustand (Docker Desktop, belegte Ports) nicht geprüft.
- Nur Windows-Erfahrungen belegt; macOS/Linux ungetestet.
- „Admin nur für den ersten User" wurde im unabhängigen Review gegen `AuthService.js` am Fork-Stand `156c677` bestätigt. Vor Anwendung den tatsächlichen Checkout prüfen; kein Live-Nachweis.
- Die Evaluation ist ein Textszenario, kein ausgeführter Test.
