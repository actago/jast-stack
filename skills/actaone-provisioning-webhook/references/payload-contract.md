# Payload-Vertrag, Freigabe und Antworten

Gelesen in actaOne `origin/main` `73ce7d4` (13.11.2026): `provisioning/webhook-receiver/index.js`
(`validatePayload`, `handleWebhook`, `enqueueEvent`, `provisionDemoLocked`) und `partners.js`. Bei Abweichung
gilt der aktuelle Code; Zeilennummern bewusst nicht genannt, sie wandern.

## Gemeinsame Felder

| Feld | Regel |
|---|---|
| `schema_version` | `1` oder `2`, **Zahl** nicht String |
| `event_id` | `^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$`, Idempotenzschlüssel. `partner_…` ist für actago-Absender reserviert |
| `event_type` | `demo_request` · `purchase` · `upgrade` · `contract_upload` · `cancel` · `credential_rotation` |
| `occurred_at` | ISO-8601; max. **900 s** alt, max. **300 s** in der Zukunft (`WEBHOOK_MAX_EVENT_AGE_SECONDS`, `WEBHOOK_MAX_FUTURE_SKEW_SECONDS`). Review-Freigaben prüfen die Frische nicht erneut |
| `plan` | optional; `standard` · `gemeinde` · `kommunal` · `enterprise`. Anderes → 400. Fehlt → `standard` |
| `contract_status` | optional; `trial` · `active`. Anderes → 400 |
| `invitation_scheduled_at` | optional; `YYYY-MM-DD` (= 00:00 Europe/Berlin) oder ISO-Instant, max. 90 Tage voraus. Fehlt → sofort fällig; die Control Plane hält die Einladung bis zur gesunden Instanz zurück |
| `customer.slug` | `^[a-z0-9][a-z0-9-]{1,56}$`, nicht `branch-…` (reserviert) |
| `customer.company_name` | 1–200 Zeichen |
| `customer.contact_email` | gültige Adresse, ≤ 254; bei `upgrade`/`contract_upload` **weglassen** |
| `contract` | PDF als `content_base64` mit `file_name`, `media_type: application/pdf`, `size_bytes` (≤ 5 MiB), `sha256`, `start_date`, `term_months` (1–120), `billing_interval` (`monthly`/`yearly`), optional `signed_date`. Pflicht bei `upgrade`/`contract_upload` |
| `releaseTag` | **verboten** → 400. Der Release kommt nie aus dem Payload |

Körper max. **8 MiB**. Unbekannte Top-Level-Felder werden nicht abgelehnt, sondern angenommen und nicht
verwendet; ein Partner bekommt `202`, obwohl die Daten nirgends ankommen. Bei „wir bauen noch Felder ein“
fragen, ob sie übernommen werden sollen — dann braucht es einen PR, keine Absprache. Die CRM-Objekte in v2
sind dagegen strikt: unbekannte Schlüssel dort ergeben `400`.

## Schema v2 (CRM)

Pflicht: `crm_account`, `crm_contact`, `target_group` (`Kommune` · `Unternehmen`). Bei Vollkunden
(`contract_status` effektiv `active`) zusätzlich `licenses` (`{standard, premium}`, ganzzahlig, Summe 1–10000)
und `contract`; bei Testkunden ist `licenses` verboten.

- `crm_account.mode: existing`: `id` (10–30 Ziffern); Adressfelder nur bei Vollkunden, dann vollständig.
- `crm_account.mode: new`: `name`, `type` aus der Institutions-Picklist im Code (`CRM_INSTITUTION_TYPES`);
  Vollkunden zusätzlich vollständige Adresse und `central_email`.
- `crm_contact`: `salutation` (`Frau`/`Herr`), `first_name`, `last_name`, `position`, `email`, optional `phone`.

## Vertragszustand

`contract_status` schlägt die Ableitung; fehlt es, gilt `demo_request` → `trial`, sonst `active`. Der Tarif
beeinflusst den Zustand nicht. `trial` setzt kein Enddatum — die Testphase startet beim ersten Admin-SSO-Login.
Wer eine Testphase **mit** Review will, sendet `purchase` + `contract_status: trial`; `demo_request` überspringt
das Event-Review. Für Partner muss ein gesetztes `contract_status` zum Typ passen, sonst `403`.

An die Control Plane geht `tenantId = slug`, Name, Kontakt, `plan`, Vertragszustand und Einladungstermin;
`primaryDomain` kommt aus der Receiver-Umgebung, nie aus dem Payload. v2-Partnerdaten (CRM, Lizenzen, Vertrag)
werden zusätzlich weitergereicht.

## Partnerbindung

Signiert ein Partner-Secret (`PARTNER_CONFIG_FILE`, siehe `docs/PARTNER_PLATFORM_OPERATIONS.md`):

- Erlaubt nur `demo_request`, `purchase`, `upgrade`, `contract_upload`; sonst `403 event_not_allowed`.
- Vom Absender gesetzte Partner-Metadaten (`_partnerId`, `partnerId`, `partner_id`, …) werden entfernt;
  Partner und Support-Adresse bestimmt allein das Secret.
- `event_id` wird zu `partner_<sha256(partner, event_id)>` umgeschrieben. Dieselbe Partner-`event_id` mit
  anderem Geschäftsinhalt → `409 event_id_conflict`.
- Neuer Kunde mit bereits vorhandenem oder anders eingereihtem Slug → `409 customer_exists`.
- Max. 30 Events pro Minute je Partner → `429 rate_limited`, `Retry-After: 60`.
- Neue Partnerkunden laufen auf den Partner-Release-Pin der Deploy-Control-API, nur `WEBHOOK_PARTNER_CUSTOMER_RELEASE_TAG`
  als Bootstrap; ohne gültigen, als Stable freigegebenen Tag bricht der Job vor jeder Anlage ab.

## Freigabe

| Ereignis | Ablauf |
|---|---|
| `demo_request` | ohne Event-Review: Konfiguration, CP-Registrierung, Vault, Deploy-Auftrag (Job-Freigabe im Ops-Dashboard bleibt) |
| `credential_rotation` | ohne Review; braucht bestehenden Kundenzustand |
| `purchase` | Review (`pending-review/`), außer `WEBHOOK_PURCHASE_AUTO_APPROVE=true` |
| `upgrade` | Review; danach CRM-Weiterleitung und `promote_to_production`-Job mit zweiter Freigabe; braucht bestehenden Kunden |
| `contract_upload` | Review; danach nur Vertrag ablegen; braucht bestehenden Kunden |
| `cancel` | Review — **siehe Warnung** |
| Partner-Events bei `WEBHOOK_PARTNER_REQUIRE_REVIEW=true` | immer Review, auch `demo_request` |

`review_approved` ist rein serverseitig: Der Review-Endpunkt setzt es, ein eingehender Wert wird seit dem
Fix stillschweigend gelöscht. (Der Ausgangsskill beschrieb noch die Lücke, dass es von außen setzbar war.)
Entschiedene Reviews landen als Beleg in `review-archive/`, ohne Vertrags-Bytes.

### ⚠ `cancel` nicht freigeben

Im geprüften Code hat `cancel` nach der Freigabe **keinen eigenen Verarbeitungszweig**: Es läuft durch denselben
Pfad wie eine Neuanlage (Konfiguration wiederherstellen oder neu anlegen, CP-Registrierung mit
Vertragszustand `active`, Vault-Publish, Deploy-Auftrag). Kündigungen über die vorgesehenen Ops-Wege
(Archivieren bzw. Teardown-Job) abwickeln und ein `cancel`-Review nicht freigeben. Befund aus Codelesen,
nicht durch Ausführung bestätigt; vor einer anderen Aussage den aktuellen Code prüfen.

## Antwortcodes

| Status | Bedeutung |
|---|---|
| `202 accepted` / `resumed` | eingereiht |
| `202 processing` | läuft gerade |
| `200 already_processed` | idempotente Wiederholung — **Erfolg** |
| `400 invalid_json` / `invalid_payload` | Absenderfehler, nennt bewusst kein Feld |
| `401 invalid_signature` | Signatur falsch, fehlt, mehrdeutig oder Partner deaktiviert |
| `403 event_not_allowed` | Partner-Eventtyp oder Vertragszustand nicht erlaubt |
| `409 event_id_conflict` | gleiche `event_id`, anderer Inhalt |
| `409 customer_exists` | Partner-Neuanlage für vorhandenen oder bereits eingereihten Slug |
| `413 payload_too_large` | > 8 MiB |
| `429 rate_limited` | Partnerlimit; nach `Retry-After` wiederholen |
| `503 queue_unavailable` / `queue_full` / `partner_configuration_unavailable` / `contract_storage_unavailable` / `event_journal_unavailable` / `shutting_down` | nur hier mit Backoff wiederholen |

## Bekannte Lücken in Spec und README (Stand `73ce7d4`)

- `openapi.yaml` dokumentiert weder `403`, `409 customer_exists` noch `429`.
- Das v2-Beispiel `demo_request` in der Spec enthält kein `crm_contact` und kein `target_group` und würde
  mit `400` abgelehnt.
- Das README-Beispiel nutzt `plan: "trial"`, `ttl_days` und `source`: `trial` ergibt `400`, die beiden anderen
  Felder wirken nicht. Die README nennt außerdem `provisioning.<domain>` als externen Host; extern ist es
  `hooks.ki.actago.de`.

Vor Weitergabe an Partner zuerst diese Lücken im Repo beheben lassen oder in der bereinigten Doku korrigieren.
