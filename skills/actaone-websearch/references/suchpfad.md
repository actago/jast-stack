# Websuche: Komponenten, Reranker-Abgrenzung, Prüfbefehle

Grundlage: `docs/WEBSEARCH_SERVICE.md` und Kundenvorlagen im actaOne-Monorepo, Websearch-Repo `main`, Wissensbasis. Stand siehe [sources.md](sources.md). Adressen und Ports stammen aus dem Juli-Runbook und müssen live bestätigt werden.

## Suchpfad

```
LibreChat-Web-Tool (Instanz)
  → Suche:    SearXNG          SEARXNG_INSTANCE_URL   (API-Host, nicht UI-Host)
  → Scrape:   Firecrawl-API    FIRECRAWL_API_URL, FIRECRAWL_VERSION
  → Rerank:   Jina-kompatibel  JINA_API_URL (endet auf /v1/rerank)
  → Modell mit Quellen und Zitaten (Darstellung im LibreChat-Fork)
```

Konfiguration in `deploy/templates/librechat.customer*.yaml`, Block `webSearch`: `searchProvider: searxng`, `scraperProvider: firecrawl`, `rerankerType: jina`, `scraperTimeout: 7500`, `safeSearch: 1`. Die Werte kommen aus der Instanz-Env. `SEARXNG_INSTANCE_URL` speist zusätzlich `PLATFORM_HEALTH_WEB_SEARCH_URL` der Instanz.

## Singleton (Orientierung, Stand Juli 2026)

| Komponente | Container | Port (an LAN-IP gebunden) | Hinweis |
|---|---|---|---|
| SearXNG | `websearch-searxng` | 8081 → 8080 | Laut Agentenprofil als Brave-Passthrough konfiguriert; Repo-`settings.yml` auf `main` zeigt die Standard-Engine-Liste. Live klären. |
| Firecrawl-API | `websearch-firecrawl` | 3002 | aus Git-Submodule gebaut; hat keinen Smoke-Endpoint |
| Reranker | `websearch-reranker` | 8787 (`/v1/rerank`, `/health`) | Jina-kompatible Fassade auf Bedrock `cohere.rerank-v3-5` (eu-central-1); Rollback-Image `:pre-bedrock` (altes lokales Modell) |
| playwright-service, nuq-postgres, redis, rabbitmq | intern | – | nuq-postgres bewusst ohne Volume; `POSTGRES_DB` muss `postgres` bleiben |

VM laut Runbook: 310 `infra-websearch`, `192.168.10.110`; Docker-Context `customer-websearch` laut Agentenprofil. Laut Juli-Stand fehlten Endpoint-Auth und Docker-Healthchecks für SearXNG, Firecrawl und Reranker, ein Proxmox-HA-Eintrag fehlte ebenfalls. Heutigen Stand prüfen.

## Welcher Reranker?

| Begriff | Was es ist | Konfiguriert über | Zuständig für |
|---|---|---|---|
| **Websuche-Reranker** | `websearch-reranker` auf der Websearch-VM, Fassade auf Bedrock Cohere | Instanz-`JINA_API_URL` | Rangfolge der Web-Treffer |
| **KB_RAG-Reranker** | Bedrock `cohere.rerank-v3-5:0`, direkt oder über die LiteLLM-Pass-Through-Route mit RAG-Key | Instanz-`RERANKER_PROVIDER/URL/MODEL/API_KEY` | Dokumentsuche in der Wissensdatenbank, **nicht** Websuche |
| **CPU-Reranker-Pilot** | eigene VM 313 `infra-reranker`, lokales Cross-Encoder-Modell, Benchmarks September 2026 | keine Kundenroute; laut Session 17.11. Dienste gestoppt, nur Loopback | Experimente, kein Produktionspfad |

Regeln:

- „Der Reranker“ zuerst aus dem Kontext zuordnen. Hinweise: Websuche vs. Dokumente, „eigene VM“, „lokales Modell“. Wenn das nicht eindeutig ist, eine gezielte Rückfrage mit dieser Tabelle stellen, bevor gemessen wird.
- Für Websuche-Probleme den Host aus `JINA_API_URL` der betroffenen Instanz verwenden, nicht einen bekannten Host aus der Doku.
- „Lokales Modell gegen AWS“ vergleicht den CPU-Pilot oder das Rollback-Image mit der Bedrock-Fassade. Die laufende Fassade allein ist dafür kein Vergleich.
- Ein Rate-Limit-Verdacht beim KB_RAG-Reranker war historisch ein ungültiger Key. Erst die Credential-Gültigkeit prüfen, ohne den Wert auszugeben.

## Stufenprüfung

Aus dem API-Container der Instanz ausführen (Service `customer-<slug>_api`, wie in `scripts/verify-customer-presidio.sh`). Die URLs kommen aus der Env, nicht aus der Doku. Keys nie ausgeben.

```bash
c=$(docker --context customer-<slug> ps -q --filter "label=com.docker.swarm.service.name=customer-<slug>_api" --filter status=running | head -1)
docker --context customer-<slug> exec "$c" sh -c 'for k in SEARXNG_INSTANCE_URL FIRECRAWL_API_URL JINA_API_URL; do eval v=\$$k; echo "$k=${v:-(leer)}"; done'
# Erreichbarkeit je Stufe (nur Statuscode). Bei Rerank zuerst /health am Host aus JINA_API_URL
docker --context customer-<slug> exec "$c" sh -c 'curl -sS -o /dev/null -w "%{http_code}\n" --max-time 10 "$SEARXNG_INSTANCE_URL/search?q=wetter+berlin&format=json"'
```

Für Rerank und Scrape den Request-Vertrag zuerst im eingesetzten Client und Service prüfen: Rerank verwendet die vollständige `JINA_API_URL`, Scrape den zur `FIRECRAWL_VERSION` passenden Pfad relativ zur konfigurierten Basis. Keine unbestätigte `/v1/scrape`-Route anhängen. Danach aus demselben API-Container einen einzelnen Request mit zwei synthetischen Dokumenten bzw. einer harmlosen öffentlichen URL senden. Credentials nur innerhalb des Prozesses aus dessen Env lesen; Request-Header, Body und Antwort nicht protokollieren. HTTP-Status und Gesamtdauer erfassen, etwa mit curl `-o /dev/null -w '%{http_code} %{time_total}\n'` und begrenztem Timeout. Diese Anleitung ist kein ausgeführter Probe-Nachweis; ohne lesbaren Vertrag den fehlenden Prüfweg melden.

Bei **langsamer Websuche** Suche, Scrape und Rerank einzeln aus diesem Clientpfad messen; die Fassadenzeit enthält den Bedrock-Roundtrip. KB_RAG benötigt separat seinen RAG-Clientpfad und dessen Betriebsanleitung. Einen gestoppten CPU-Pilot nicht zur Diagnose starten. Messungen aus unterschiedlichen Netzen oder mit unterschiedlichen Nutzlasten nicht als direkten Modellvergleich ausgeben.

Auf dem Singleton (ergänzt die Instanzprüfung, ersetzt sie nicht; Health-Host aus `JINA_API_URL` ohne `/v1/rerank` ableiten):

```bash
docker --context customer-websearch ps
docker --context customer-websearch logs --tail 100 websearch-reranker
curl -fsS http://<websearch-host>:8787/health
```

Wenn das Image `curl` nicht enthält, ein vorhandenes Werkzeug im Container verwenden (z. B. `node -e` mit `fetch`). Nicht nachinstallieren. Einen Firecrawl-Scrape mit einer öffentlichen, harmlosen URL testen. Für Rerank zwei bis drei synthetische Dokumente mit offensichtlicher Relevanzordnung senden.

## Änderungs- und Rückwege am Dienst

Make-Targets laut Runbook: `make ps`, `make logs`, `make restart`, `make pull`, `make firecrawl-update`, `make config` bzw. `make validate`. Bei Schemafehlern der Firecrawl-Queue nur die betroffenen Dienste ohne Cache neu bauen (siehe Runbook). Die Reranker-Fassade erwartet `BEDROCK_RERANK_URL/MODEL/API_KEY` in der VM-`.env`. Laut Agentenprofil stammt der Key aus Vault `customer-defaults` `RERANKER_API_KEY`. Bei Key-Rotation diese Kopie mitziehen. Rückweg Reranker: Rollback-Image `:pre-bedrock` starten und die Antwortform prüfen, die Instanzanbindung bleibt dabei unverändert.
