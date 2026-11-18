# Quellen und Kennzahlen

## Datenfluss

Jede Kundeninstanz bucht in ihrer eigenen Mongo (`LibreChat`) in die Collection `transactions`. Der Platform-Exporter der Instanz aggregiert daraus Fenster und meldet sie an die Control-Plane (CP). Dort landen:

| CP-Collection | Inhalt | Lesart |
|---|---|---|
| `platforminstances` | letzter `usageSnapshot` je Instanz, `tenantId` (= Slug), `lastSeenAt`, `build` | letzter Stand, keine Historie |
| `platformexportevents` | Empfangsbelege für Heartbeat und Snapshot, ohne Usage-Payload, 90-Tage-TTL laut KB | Exportkanal-Aktivität, nicht Nutzeraktivität |
| `usagesnapshots` | persistierte Fenster mit `windowKind`, Fenstergrenzen, Tokens, Credits, `byModel`, Nutzerzahlen | einzige CP-Historie; für Zeiträume nur `windowKind: delta` summieren |
| `tenants` | Lifecycle und Vertrag | siehe [Vertragsdaten](#vertragsdaten) |

CP-`tenants` hat keinen Slug. Die Zuordnung läuft über `platforminstances.tenantId`.

## Kennzahlen aus dem Exporter-Code

Diese Definitionen sind für den Exporter belegt. Eine identische Berechnung in `engagement.js` und den CP-Aggregationen wurde nicht geprüft. Vor Vergleichen über verschiedene Lesewege deren konkrete Definitionen, Fenster und Filter abgleichen; gleich benannte Felder nicht automatisch gleichsetzen.

Gemäß `packages/data-schemas/src/methods/tenantWindowMetrics.ts` im LibreChat-Fork. Gefiltert wird auf `tenantId`, `createdAt ∈ [since, until)` und `tokenType ∈ {prompt, completion}`.

| Kennzahl | Herleitung | Nicht verwechseln mit |
|---|---|---|
| `inputTokens` | Prompt-Buchungen: `abs(inputTokens ?? rawAmount)` | Kontextlast einer einzelnen Nachricht |
| `outputTokens` | Completion-Buchungen: `abs(rawAmount)` | `messages.tokenCount` |
| `cacheWriteTokens`, `cacheReadTokens` | Prompt-Buchungen: `abs(writeTokens)`, `abs(readTokens)` | zusätzlichen Input; Cache-Anteile separat ausweisen |
| `tokenCredits` | `abs(tokenValue)` von Prompt und Completion | Euro oder Rechnungsbetrag |
| `cost` | Summe `cost.amountEur` sowie Zahl bepreister und unbepreister Buchungen | Rechnung; bei unbepreisten Buchungen ist die Summe eine Untergrenze |
| `activeUserCount24h/7d/30d` | verschiedene `user` mit Prompt- oder Completion-Buchung im rollierenden Zeitraum vor dem Fensterende | Logins, registrierte Konten, eindeutige Monatsnutzer aus mehreren Snapshots |
| `userCount` | registrierte Konten im Bestand | aktive Nutzer |
| `conversationCount`, `messageCount` | im Delta-Fenster neu angelegt | Gesamtbestand |
| `byModel` | wie oben, gruppiert nach `model` | Nutzerzahl oder Qualität je Modell |

`tokenType: credits` (z. B. Gutschriften) zählt nicht als Verbrauch. Der Nano-Fallback bei erreichtem Limit bleibt laut `docs/operations/usage-fallback.md` im Ledger sichtbar, zählt aber nicht ins persönliche Kontingent.

## Lesewege zur CP-Historie

Drei Wege existieren im Code. Für jeden gelten eigene Rechte:

1. **Management-Analytics** `actaone-platform-analytics` auf mgmt, `127.0.0.1:8791`. Laut Monorepo-`CLAUDE.md` (`origin/main`, 12.11.2026) läuft der Lesepfad live. Ältere lokale Fassungen sagen das Gegenteil; vor Nutzung den Unit-Status lesend prüfen.
   - Endpunkte: `GET /analytics/<name>`, Fenster `?window=7d|30d|90d`
   - Nutzungsrelevant: `model-usage`, `instance-token-usage` (exakte Delta-Tokens im Fenster), `instance-user-ranking` (aktive und registrierte Konten getrennt), `engagement`, `usage-totals`, `tenant-usage`
   - Auth: Token im Header `x-actaone-analytics-token` oder `Authorization: Bearer`. Das Token liegt in systemd-Konfiguration und wird **nicht** eigenmächtig ausgelesen.
2. **Ops-API-Broker** `GET /api/v1/agent-analytics/<overview|usage|growth|activity|engagement|models|instance-tokens|instance-users>?window=…` der Deploy-Control-API. Er ist nur mit Service-Token nutzbar und für einen separaten Agent-Lesedienst gedacht, sonst 404. Die Antworten enthalten `metricDefinitions`, `answerRules` und `limitations`. Diese Regeln in die Antwort übernehmen, wenn der Weg verfügbar ist.
3. **CP-Analytics** in der CP-API (`/api/admin/platform/analytics/*`, u. a. `overview`, `usage`, `costs`). Sie verlangt Nutzer-JWT mit `read:analytics`. Das ist der Weg über Panel bzw. UI des Nutzers.

Ist keiner dieser Wege freigegeben, bleibt der Instanz-Ledger je Mandant ([instanz-ledger.md](instanz-ledger.md)). Eine CP-Mongo-Abfrage im CP-API-Container auf Context `prod` ist in einer Memory vom 21.08.2026 belegt; dort führte der Nutzer sie selbst aus. Sie berührt die Produktions-Control-Plane und braucht deshalb ausdrückliche Freigabe.

Die Endpunktnamen stammen aus dem Code (`provisioning/platform-analytics/index.js`, `provisioning/deploy-control-api/usage.js`). Live-Antworten wurden für diesen Skill nicht abgerufen.

## Vertragsdaten

Für „seit wann testet …“: In CP-`tenants` stehen `trialStartedAt`, `trialEndsAt`, `contractStatus`, `onboardingCompletedAt`, `createdAt`. Diese Daten zuerst nehmen, Tickets nur ergänzend. Erste Nutzung ist eine **andere** Kennzahl: die früheste Prompt- oder Completion-Buchung im Ledger bzw. das erste Delta-Fenster mit Tokens größer 0. Beides getrennt nennen.

## Fallstricke

- Zwei `userCount: 20` sind zwei Messungen von 20 Konten, nicht 40.
- Rollierende Fenster überlappen. Vier 24-h-Fenster ergeben nicht vier unabhängige Tage.
- Der Exporter holt nach einem Ausfall höchstens 24 Stunden nach. ACKs beweisen keine Vollständigkeit.
- `observedAt` stammt von der Instanz, `receivedAt` von der CP. Clock-Skew ist möglich.
- Interne und Test-Tenants laut Memory 08/2026: actago-intern, benchmark, vertrieb-demo, test-stadt, stwh. Die Liste vor Nutzung aktualisieren und nicht als vollständig behandeln.
