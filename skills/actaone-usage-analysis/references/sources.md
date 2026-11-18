# Quellen des Skills actaone-usage-analysis

Erstellt am 2026-11-17 durch Lesen lokaler Dateien und Git-Objekte. Live wurde nichts abgefragt; keine Abfrage aus diesem Skill wurde ausgeführt. Blob-Angaben sind gekürzte Git-Objekt-IDs.

## Ausgangslage

Es gibt keinen Vorgänger-Skill. Gesucht wurde in `~/.claude`, `~/.claude-jast`, `~/.codex`, `~/.agents` und in `actaOne/.claude`. Der Skill ist neu, aus belegten Anforderungen und vorhandenen Abfragewegen zusammengesetzt. Er ersetzt weder `actaone-platform`- noch `actaone-performance`-Agentenprofile; diese nennen Telemetrie, aber keinen Ablauf.

## Anforderungen (Session-Belege)

JAST-Stack `research/codex-session-audit.md` §3 „Nutzungsauswertung je Mandant“:

- **Trigger:** „hat Instanz X genutzt“, „wie intensiv testet Kunde Y“, „Limits zu schnell weg“, „welche Preise sind aktiv“
- **Belege:** Sessions vom 03.10. (Limitbeschwerde einer Hochschule; fehlender EU-Aufschlag bei fünf Modellen), 29.10. (Gemeinde „aber schnell“), 17.11. (Testbeginn und Intensität zweier Testkunden über rund 50 `ssh acta-mgmt`- und `transactions`-Abfragen; Vertragsstart aus Tickets, dann aus der CP-DB)
- **Erwartet:** Standardkennzahlen über ein festes Fenster, Stand, Quelle, Zeitzone, nur Aggregate, keine Chatinhalte
- **Offen laut Audit:** Datenschutzrahmen vor Veröffentlichung abstimmen

Die Sessions selbst wurden für diesen Skill nicht erneut gelesen.

## actaOne-Monorepo `origin/main` `73ce7d4ccdb5` (13.11.2026)

| Pfad | Blob | Verwendet für |
|---|---|---|
| `CLAUDE.md` | `d1cf1df520cf` (`cff7dca`, 12.11.2026) | Lesepfad `actaone-platform-analytics` auf mgmt live. Der lokale Arbeitsstand `dd0a334` sagt noch „läuft auf keiner VM“; der neuere Stand wurde übernommen und der Widerspruch im Skill vermerkt. |
| `provisioning/platform-analytics/README.md` | `8dfa86b23b1f` | Collections, Endpunkte, Fenster, Limitierung der Usage-Timeseries |
| `provisioning/platform-analytics/index.js` | `07f921ae716d` | Routen inkl. `model-usage`, `instance-token-usage`, `instance-user-ranking`; Auth über beide Header; `readColl`-Lesesperre |
| `provisioning/platform-analytics/engagement.js` | `b3e84ac29d2a` | nur als Ort der Delta-Aggregationen, Inhalt nicht gelesen |
| `provisioning/deploy-control-api/usage.js` | `5bd9f7139284` (`4c4e611`, 17.08.2026) | Metrikdefinitionen, `answerRules`, `limitations` |
| `provisioning/deploy-control-api/index.js` | `a5ff1f53c391` | Broker `/api/v1/agent-analytics/*` nur mit Service-Token |
| `infra/roles/platform_analytics/tasks/main.yml` | – | Unit-Name `actaone-platform-analytics`, Secrets-Drop-in |
| `docs/operations/usage-fallback.md` | `3643ae00f9eb` (`0fe4469`, 14.10.2026) | Nano-Fallback, Kontingent-Ausnahme, Warnschwellen |
| `docs/operations/codeapi/runbook.md` | `17a096e7b1b0` | `mongosh`-Muster je Instanz, `tenantId` über `db.users.distinct` |

## LibreChat-Fork `origin/main` `df0d5a4de` (10.11.2026)

| Pfad | Blob | Verwendet für |
|---|---|---|
| `packages/data-schemas/src/schema/transaction.ts` | `eae1ad63c87a` | Felder und `tokenType`-Enum des Ledgers, Indizes |
| `packages/data-schemas/src/methods/tenantWindowMetrics.ts` | `0f5d074a6b54` | exakte Summenformeln, Filter, aktive Nutzer |
| `packages/data-schemas/src/methods/cost.ts` | `38879c97999c` | `costSumFields` (bepreist/unbepreist) |
| `packages/data-schemas/src/schema/cost.ts` | – | `pricingVersion` `recorded-rates-v1`, EUR/USD-Felder |
| `packages/data-schemas/src/methods/usagePlan.ts` | `fa6f8c5fab8c` | `CREDITS_PER_USD`, Default-Konstanten (Werte nicht übernommen) |
| `api/server/routes/admin/platform.js` | `b518cea597ff` | CP-Analytics-Routen mit `requireJwtAuth` + `read:analytics` |
| `api/server/middleware/limiters/promptUsageLimiter.js` | – | Ratenlimit pro Minute, Abgrenzung zum Budget |

## Wissensbasis `actaOneKBobsidian`, lokaler Stand `d9d678f` (11.11.2026)

| Notiz | Blob | Verwendet für |
|---|---|---|
| `10 actaOne/Analytics-Datenhaltung (Referenz).md` (Stand 14.10.) | `436abdca2e6c` | zwei Lese-APIs, drei Datentypen, Delta/Rolling, Lücken, Live-Nachweis 06.09. |
| `10 actaOne/Kunden-Datenbanken (Referenz).md` | `d0763e0b3273` | `transactions` statt `tokens` |
| `20 Team/JAST/Memories/usage-analytics-pipeline.md` (21.08.) | `1240c7404da9` | Sweep-Muster, Slug-Zuordnung, CP-Abfrage durch den Nutzer, historische Limitwerte, interne Tenants |

Blob-Werte der Notizen mit `git hash-object` erhoben.

## Entscheidungen und lokale Anpassungen

- Das ausführbare Rezept beschränkt sich auf das Ledger-Aggregat einer Instanz. Es ist vollständig aus dem Exporter-Code abgeleitet, damit die Zahlen den CP-Delta-Fenstern entsprechen.
- Analytics-Endpunkte werden beschrieben, aber ohne Anleitung zur Token-Beschaffung. Die Memory vom 21.08. dokumentiert, dass Env- und Credential-Lesen geblockt wird bzw. nicht vorgesehen ist.
- Limits und Preise sind ausdrücklich als **begrenzter Diagnoseworkflow** markiert. Durchsetzungslogik, Ausnahmen und Live-Werte wurden nicht geprüft.
- Historische Zahlen aus Memories (Limits, interne Tenants) sind als solche gekennzeichnet und nicht als geltende Werte übernommen.

## Grenzen

- Kein Live-Test: Unit-Status, Erreichbarkeit von Port 8791, Broker-Antworten, `mongosh`-Version (Unterstützung für `process.env`) und Laufzeit der Aggregation auf großen Instanzen sind ungeprüft.
- `engagement.js` (Delta-Pipelines) und `platformAnalytics.ts` (CP-Analytics) wurden nicht im Detail gelesen. Die Gleichheit ihrer Formeln mit `tenantWindowMetrics.ts` ist angenommen, nicht belegt.
- Der Datenschutzrahmen für Nutzungsauswertungen ist laut Audit noch abzustimmen. Der Skill setzt das strengere Minimum, nur Aggregate, ersetzt aber keine Abstimmung.
