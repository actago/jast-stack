# Quellen des Skills actaone-websearch

Erstellt am 2026-11-17 durch Lesen lokaler Klone, Dateien und read-only GitHub-API-Abfragen. Es wurde nichts live geprüft, deployt oder verändert. Blob-Hashes sind Git-Objekt-IDs (gekürzt), Datei-Hashes SHA-256 (gekürzt).

## Websearch-Repo `github.com/actago/websearch`

Kein lokaler Klon gefunden. Per `gh api` gelesen: `main` = `9e8bf353c818` (2026-07-19, „feat(reranker): Bedrock Cohere rerank-v3-5 statt lokalem FlashRank“). `feature/brave-api-engine` ist identisch mit `main` (0 Commits Abstand). Gelesen wurden die Verzeichnisliste, `eval/README.md` (A/B-Workflow, SEARCH-MISS/RERANK-MISS) und Ausschnitte aus `searxng/config/settings.yml` (Standard-Engine-Liste). Den Code von Reranker und Compose habe ich nicht gelesen.

Damit ist die Angabe im Agentenprofil überholt, der Push dieses Commits sei gescheitert. Ob die VM genau diesen Stand und eine Brave-only-Konfiguration fährt, ist ungeprüft.

## actaOne-Monorepo `github.com/actago/actaOne`

Gelesener Stand: `origin/main` = `73ce7d4ccdb5` (2026-11-13). Der lokale Arbeitszweig lag 754 Commits zurück und wurde nicht verwendet.

| Pfad | Blob | Letzter Commit | Verwendet für |
|---|---|---|---|
| `docs/WEBSEARCH_SERVICE.md` | `ff67d5e1cfe9` | `0fbb5ca` 2026-07-22 | Komponenten, Ports, Anbindung, offene Punkte, Make-Targets, Reranker-Abgrenzung |
| `deploy/templates/librechat.customer.yaml` | `4ef2e081265b` | `247eca5` 2026-11-04 | `webSearch`-Block (identisch strukturiert in Staging-, Benchmark-, stwh- und Vertrieb-Demo-Vorlagen) |
| `provisioning/deploy-control-api/customer-config.js` | `9947001307de` | `7e1a401` 2026-11-04 | Die sieben Websearch-Keys und die `RERANKER_*`-Keys sind als Instanz-Env zulässig |
| `scripts/service_gateway.py` | `b2f4720d1ed3` | `f4bb888` 2026-10-29 | KB_RAG-Reranker über den Gateway nur als Bedrock Cohere 3.5 |
| `docs/MISTRAL_EU_PROFILE.md` | `39e0244c0e10` | `7556046` 2026-08-31 | Websearch-Reranking im Profil `mistral-eu` deaktiviert |
| `.claude/agents/actaone-websearch.md` | `b91618a12ea4` | `683ccf0` 2026-07-22 | Ausgangsprofil (siehe unten) |

`deploy/templates/docker-compose.customer.yml` (gleicher Stand) zeigt außerdem `PLATFORM_HEALTH_WEB_SEARCH_URL=${SEARXNG_INSTANCE_URL}` und den Service-Namen `api`.

## Agentenprofil `actaone-websearch`

Die Projektkopie und die Benutzerkopie im Claude-Profil sind bis auf Zeilenenden gleich (SHA-256 `6749e207855c` bzw. `3d1d59fa7a95`). Übernommen habe ich die Singleton-Regel, die Komponenten- und Porttabelle, die Bedrock-Fassade samt Rollback-Image, die Herkunft des Fassaden-Keys, den eigenen Deploy außerhalb des Release-Zugs und die vorsichtige Behandlung von Firecrawl-Bumps. Als datiert bzw. ungeprüft gekennzeichnet sind die Brave-only-Konfiguration, die fehlende DNS-Bridge und die LAN-Bindung ohne Auth. Nicht übernommen habe ich den gescheiterten Push (überholt), die Co-Author-Zeile und feste Health-Befehle als heutigen Stand.

## Wissensbasis (Obsidian-Vault, Remote `github.com/actago/actaOneKBobsidian`)

Lokaler Stand `d9d678f1e8bd` (2026-11-11). Die Notizen haben keine lokalen Änderungen.

| Notiz | Blob | Verwendet für |
|---|---|---|
| `10 actaOne/Websearch (Service-Referenz).md` | `2632f01755de` | Kundenanbindung (sieben Keys), bekannte Brüche Stand Juli/August |
| `10 actaOne/Reranker – Eigene CPU-VM und Benchmarks 2026-09.md` | `2ee5daf1b142` | CPU-Reranker-Pilot VM 313, keine Kundenroute |
| `10 actaOne/LiteLLM (Service-Referenz).md` | `b4309e280243` | Reranker-Key-Regression 27./28.10. (KB_RAG-Seite) |

## LibreChat-Fork

Der lokale Worktree `LibreChat-websearch-quality-20261024`, Branch `fix/websearch-citation-contract-20261024` (`47d6d6a6ef`), zeigt die Orte der Zitat-Logik: `packages/api/src/tools/toolkits/web.ts`, `packages/api/src/web/open.ts`, `client/src/utils/citations.ts`, `client/src/components/Web/`. Merge-Stand und Inhalt habe ich nicht geprüft. Übernommen sind nur die Pfade als Fundorte.

## Session-Belege (nur Herkunft, keine Befehle)

- Codex-Session vom 17.11.2026 (Rollout `01a1e95c`), Zeilen 17, 203, 256, 266. Die Frage nach „dem Reranker“ wurde zuerst gegen die Websuche-Fassade auf der Websearch-VM benchmarkt. Gemeint war die CPU-Reranker-VM 313. Danach entstand eine Mehrdeutigkeit zwischen Obsidian-Vault und Key Vault. Daraus folgen die Abgrenzungstabelle und die Vault-Regel.
- `research/claude-session-audit.md` §2 (2645caa8): Ein Rate-Limit-Verdacht beim Reranker stellte sich als ungültiger Key heraus.

## Grenzen

- Ich habe nichts live geprüft. Status, Ports, Engine-Konfiguration, Netzabsicherung und die Befüllung der Instanz-Keys sind Quellenangaben mit Datum. Die Kernquelle stammt vom Juli 2026.
- Die Prüfbefehle in `suchpfad.md` sind aus Vorlagen und Skripten abgeleitet. Ich habe sie nicht ausgeführt.
- IP-Adressen und VM-IDs sind intern, aber nicht geheim. Vor einer Weitergabe außerhalb des Teams prüfen.
