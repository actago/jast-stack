---
name: actaone-websearch
description: actaOne-Websuche diagnostizieren, ändern oder abnehmen – Suchpfad von LibreChat über den Websearch-Singleton (SearXNG, Firecrawl, Jina-kompatibler Reranker) bis zu Quellen und Zitaten. Nutzen bei „Websuche liefert nichts/Falsches“, schlechten oder fehlenden Quellen, Fehlern von Suche, Scrape oder Rerank, Websearch-Konfiguration für Instanzen und bei der Frage, welcher Reranker gemeint ist. Nicht für KB_RAG-Dokumentsuche.
---

# actaOne-Websuche

Die Websuche ist ein Singleton-Dienst für alle Instanzen. Er läuft außerhalb des Kunden-Release-Zugs. Instanzen binden ihn nur per Konfiguration an. Die häufigste Fehlerquelle ist die Verwechslung des richtigen Dienstes, besonders beim Reranker. Deshalb wird jeder Begriff zuerst gegen die Komponententabelle in [references/suchpfad.md](references/suchpfad.md) aufgelöst.

## 1. Quellen bestimmen

Maßgeblich sind externe Quellen. Dieser Skill enthält Invarianten und Prüfwege; seine datierten Angaben sind Orientierung.

1. **Websearch-Repo** (Remote `actago/websearch`): Compose-Stack, Reranker-Fassade, SearXNG-Konfiguration, `eval/` für Retrieval-Qualität. Ohne lokalen Klon read-only über `gh api repos/actago/websearch/...` lesen.
2. **actaOne-Monorepo** (Remote `actago/actaOne`): `docs/WEBSEARCH_SERVICE.md` (Runbook, Stand Juli 2026), `webSearch`-Block der Kundenvorlagen `deploy/templates/librechat.customer*.yaml`, Env-Allowlist in `provisioning/deploy-control-api/customer-config.js`. Verträge aus `origin/main` lesen; lokale Checkouts können weit zurückliegen (`git rev-list --count HEAD..origin/main`).
3. **LibreChat-Fork** (Remote `actago/LibreChat`): Web-Tool und Zitate (`packages/api/src/tools/toolkits/web.ts`, `packages/api/src/web/`, `client/src/components/Web/`).
4. **Wissensbasis** (Obsidian-Vault, Remote `actago/actaOneKBobsidian`): Notizen „Websearch (Service-Referenz)“ und „Reranker – Eigene CPU-VM und Benchmarks 2026-09“.
5. **Live-Zustand** über den im Monorepo dokumentierten Management-Zugang.

Fehlt eine Quelle, das ausdrücklich melden und betroffene Aussagen als ungeprüft kennzeichnen. Das Runbook ist von Juli 2026 und nennt offene Punkte (fehlende Env-Befüllung, Brave-Engine, Netzabsicherung, Healthchecks), deren heutiger Stand unbekannt ist. Diese Punkte live prüfen und nicht als aktuell übernehmen. „Vault“ ist mehrdeutig: Azure Key Vault (Konfiguration) oder Obsidian-Vault (Wissen). Aus dem Kontext auflösen.

## 2. Auftrag einordnen

| Auftrag | Erlaubt | Endet mit |
|---|---|---|
| **Diagnose** | lesen, harmlose synthetische Einzelanfragen je Stufe | Befund je Stufe mit Beleg |
| **Änderung** (Dienst-Config, Image, Instanzanbindung) | genau der beauftragte Umfang | geändert, rückgelesen, Rückweg benannt |
| **Abnahme / Qualität** | Stufentests, Retrieval-Eval, ein Ende-zu-Ende-Test auf Test-/Staging-Instanz | Messergebnis mit Grenzen |

Eine Diagnose autorisiert keinen Neustart, Rebuild oder Vault-Eintrag. Ein Websearch-Auftrag autorisiert keine Änderung am KB_RAG-Reranker oder an der Reranker-Pilot-VM.

## 3. Feste Invarianten

- **Ein Singleton für die Flotte**, nie pro Kunden-VM. Eigenes Deploy über Compose/`make` auf der Websearch-VM, nicht über `promote.sh`.
- **Drei verschiedene Reranker** existieren. Die Websuche nutzt ausschließlich den Dienst hinter `JINA_API_URL` der Instanz. Benchmarks, Health-Checks und Key-Fragen gelten nur für den tatsächlich konfigurierten Dienst.
- **Instanzanbindung über sieben Env-Keys** (`SEARXNG_INSTANCE_URL`, `SEARXNG_API_KEY`, `FIRECRAWL_API_URL`, `FIRECRAWL_API_KEY`, `FIRECRAWL_VERSION`, `JINA_API_URL`, `JINA_API_KEY`). Sie werden über den Vault-Weg gesetzt (Instanz-Bundle oder `customer-defaults`). Ein LibreChat-Fork-Change ist dafür nicht nötig. Live-`docker service update` überlebt keinen Redeploy.
- **Erreichbarkeit aus der Instanz prüfen**, nicht nur von mgmt: Kunden-VMs nutzen interne Adressen, mgmt hat einen Hairpin auf die Public-IP.
- **Keine öffentliche Exposition** von SearXNG, Firecrawl oder Reranker ohne Schutz. API-Keys und `.env`-Werte der VM nie ausgeben.
- **Keine echten Nutzeranfragen** für Tests oder Berichte. Für Tests harmlose öffentliche Suchbegriffe verwenden.
- **Profil `mistral-eu`:** Websearch-Reranking ist dort laut Profil-Doku deaktiviert. Fehlendes Reranking ist bei diesen Instanzen gewollt.

## 4. Diagnose

1. **Instanz und Symptom festlegen.** Mögliche Symptome: keine Ergebnisse, Fehler, schlechte Quellen, falsche Zitate.
2. **Effektive Anbindung lesen.** In der Laufzeit-Env der Instanz nur die drei URL-Keys anzeigen, keine API-Keys. Leer, Platzhalter oder alte `*.actago.info`-Hosts sind bereits ein Befund.
3. **Stufen einzeln aus dem API-Container der Instanz prüfen:**
   - Suche: Liefert sie Kandidaten?
   - Scrape: Gelingt er für eine öffentliche URL?
   - Rerank: Kommen Scores für synthetische Dokumente zurück?
   Suchprobe und vertragsabhängige Rerank-/Scrape-Prüfung stehen in [references/suchpfad.md](references/suchpfad.md#stufenprüfung). Bei „langsam“ dort die Latenz je Stufe aus dem tatsächlichen Clientpfad messen; einen gestoppten Pilotdienst nicht starten.
4. **Singleton prüfen:** Containerstatus und Logs der betroffenen Dienste. Die Basislast von RabbitMQ gilt nicht als Störung.
5. **Fehler zuordnen:**
   - Erreichbarkeit oder DNS: Netz bzw. Anbindung.
   - Fehler hinter dem Reranker: Bedrock-Credential oder Region des Fassadendienstes.
   - Nur schlechte Treffer: Qualität (Abschnitt 6).
   - Zitate falsch, obwohl die Quelle stimmt: App-Pfad im LibreChat-Fork.

Die Diagnose ist fertig, wenn jede Stufe einzeln als gut, defekt oder ungeprüft belegt ist und die Ursache der richtigen Komponente zugeordnet ist.

## 5. Änderung

- **Dienst** (SearXNG-Engines, Reranker-Fassade, Firecrawl): Änderung im Websearch-Repo per Branch und Commit, danach Rebuild bzw. Neustart nur der betroffenen Dienste auf der VM. Secrets bleiben in der `.env` der VM, nicht in Git. Firecrawl-Submodule-Bumps nur bewusst durchführen, weil Source-Build und Ressourcen aufwendig sind. Reranker-Rückweg: vorhandenes Rollback-Image.
- **Instanzanbindung:** Keys über den Vault-Weg des Monorepos (Instanz-Bundle zuerst, `customer-defaults` nur bei gewollter Flottenänderung), Readback, Redeploy über den regulären Pfad.
- Für jede Änderung gehört der Vorher-Zustand in den Bericht: Image-Tag, Konfigurationsdatei oder Vault-Wert. Werte, die Geheimnisse sind, nur als „gesetzt/leer“ angeben.

## 6. Qualität und funktionale Abnahme

- **Retrieval-Qualität** im Websearch-Repo mit `eval/run_eval.py` messen. Die Ausgabe trennt `SEARCH-MISS` (Quelle nie Kandidat: Engines oder Query) und `RERANK-MISS` (Kandidat, aber nicht in Top-K: Reranker). A/B immer mit Label und gleichem `--k` laufen lassen.
- **Quellenqualität in der Antwort** (Zitate, Anker, Kartendarstellung) ist App-Logik im LibreChat-Fork. Ein Eval-Ergebnis des Dienstes belegt sie nicht.
- **Ende-zu-Ende:** eine Websuche mit harmloser Frage auf einer Test- oder Staging-Instanz. Zitierte Quellen müssen öffnen und die Aussage stützen. Das ist kein Flottennachweis.

## 7. Bericht

Enthält:
- betroffene Instanz und den tatsächlich verwendeten Dienst je Stufe (URL ohne Key)
- Ergebnis je Stufe
- Änderungen mit Rückweg
- nicht geprüfte Punkte
- Quellenstand

Herkunft der Skillinhalte: [references/sources.md](references/sources.md).
