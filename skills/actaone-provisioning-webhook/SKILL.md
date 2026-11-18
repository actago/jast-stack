---
name: actaone-provisioning-webhook
description: Use when working on the actaOne provisioning webhook (hooks.ki.actago.de, webhook-receiver on the mgmt VM) - the HMAC and partner-signing contract, payload v1/v2, the OpenAPI spec and Swagger UI, deploying or restarting the receiver, debugging 400/401/403/409/429 responses, or setting up a partner integration test.
---

# actaOne Provisioning-Webhook

Nimmt signierte Provisioning-Events von Vertriebssystemen, Partnerportalen und Partner-Widgets an und arbeitet sie
in einer seriellen Job-Queue ab. Läuft als systemd-Dienst `webhook-receiver` auf der **mgmt-VM**.
Quellen, geprüfter Stand und Abweichungen vom Ausgangsskill: [references/sources.md](references/sources.md).

Maßgeblich ist der Code in `provisioning/webhook-receiver/` des actaOne-Repos (`index.js`, `partners.js`),
nicht README oder Spec. Vor jeder Vertragsaussage gegen den aktuellen Stand prüfen.

## ⚠ Der Endpunkt provisioniert PRODUKTION

Live-Konfiguration laut Ausgangsskill (07/2026):

```
WEBHOOK_CUSTOMER_ENVIRONMENT=prod
DOMAIN_BASE=ki.actago.de
PLATFORM_PROVISIONING_URL=https://control.actago.de/api/platform/v1/provisioning/instances
```

Rollen-Defaults, Beispiel-`group_vars` und README zeigen `staging` — **das ist nicht die Laufzeitkonfiguration.**
Die echten Werte kommen aus privaten `group_vars`. Immer `/proc/<MainPID>/environ` prüfen (siehe unten).

Jeder erfolgreiche `demo_request` legt einen **echten Produktionsmandanten** an, belegt einen Hotseat, erzeugt
eine Domain und plant eine Einladung an `contact_email`. Der Ausgangsskill kannte keinen Test-Eingang (nur
`hooks.ki.actago.de`, kein Receiver auf staging). Die Receiver-README beschreibt inzwischen einen manuellen
Partner-Test „auf dem Clone“ mit `WEBHOOK_PARTNER_REQUIRE_REVIEW=true`. Ob und wo diese Umgebung läuft, vor
einem Test nachweisen statt annehmen.

**Testreihenfolge für Partner** — nie mit einem echten Event anfangen:
1. **Signatur trocken prüfen** — Partner schickt Rohkörper + berechnete Signatur, gegen dasselbe
   Geheimnis nachrechnen. Kein Request.
2. **Gültig signiert, absichtlich fehlerhafter Payload** (z.B. `"schema_version": "1"` als String)
   → erwartet `400 invalid_payload`. Beweist Netzweg und Signatur, provisioniert nichts.
3. **Echtes Event erst nach Absprache**, mit Slug-Konvention (`zz-test-<datum>`) und einer
   `contact_email`, die actago gehört. Vorher klären, wer aufräumt. Ist der Partner-Review-Schalter aktiv,
   hält er das Event vor jeder Anlage im Review; das ersetzt die Absprache nicht.

## Topologie — die wichtigste Falle

| | |
|---|---|
| **Laufzeitverzeichnis** | `/opt/actaone/webhook-receiver` — `root:<deploy-gruppe> 755`, für den Dienstuser **nicht schreibbar** |
| Quelle | `provisioning/webhook-receiver/` im actaOne-Repo (auf mgmt `~/actaOne`) |
| Deployment | Ansible-Rolle `infra/roles/webhook_receiver`, Playbook `infra/playbooks/configure-webhook-receiver.yml` |
| Unit | `/etc/systemd/system/webhook-receiver.service`, `User=actaone` (Rollen-Default), `WorkingDirectory=/opt/...`, `ExecStart=/usr/bin/node index.js` |
| Env | `/etc/actaone/webhook-receiver.env`; HMAC-Secret und Provisioner-Token aus Key Vault, nicht aus der Datei |
| State | `/var/lib/actaone/webhook-receiver` (`queue/`, `jobs/`, `pending-review/`, `review-archive/`, `contracts/`, `seen-events.json`, `webhook-access.jsonl`) — personenbezogener Betriebsstate |

**`git pull` im Repo ändert nichts am laufenden Dienst.** `ExecStart` ist relativ, `WorkingDirectory`
zeigt auf die deployte Kopie. Nach einem Pull muss die Rolle laufen, sonst antworten neue Routen weiter 404
— auch nach einem Neustart.

Prüfen: `diff -q /opt/actaone/webhook-receiver/index.js ~/actaOne/provisioning/webhook-receiver/index.js`
(und ebenso `partners.js`, `broker.js`, `openapi.yaml`).

## Neustarten und neu laden

`actaone` hat absichtlich kein sudo; `systemctl restart` scheitert an polkit. Für Root-Schritte den
vorgesehenen Adminzugang verwenden (in JAST: Skill `sudo-window`), keine Passwörter auf Verdacht probieren —
laut Ausgangsskill können Fehlversuche root per `pam_faillock` sperren.

**Ohne Neustart:** Das HMAC-Secret wird alle 60 s (`WEBHOOK_SECRET_REFRESH_SECONDS`) und bei `SIGHUP` neu aus
Key Vault geladen; die Partnerkonfiguration (`PARTNER_CONFIG_FILE`) bei jeder Anfrage. Secret-Rotation oder
Partnerwechsel brauchen also keinen Neustart.

**Neustart ohne Root** (nur für neuen Code, der bereits in `/opt` liegt). Der Dienst läuft als `actaone`,
`Restart=on-failure`:

```bash
ls -1 /var/lib/actaone/webhook-receiver/queue | wc -l    # MUSS 0 sein
kill -9 "$(systemctl show webhook-receiver -p MainPID --value)"
sleep 6 && systemctl is-active webhook-receiver
```

Nur `SIGKILL` löst den Neustart aus. Ein normales `kill`/`SIGTERM` beendet den Dienst geordnet mit Exit 0 —
`on-failure` startet ihn dann **nicht** neu, und der Eingang ist tot. Harter Abbruch, deshalb nur bei leerer
Warteschlange; persistierte Queue-Einträge würden beim Start zwar wieder aufgenommen, ein laufender Schritt
aber mitten im Ablauf abgebrochen. Dateien nach `/opt` bringt die Ansible-Rolle, nicht `cp`, sonst driftet
das Laufzeitverzeichnis.

## Endpunkte

| Route | intern | extern über `hooks.ki.actago.de` |
|---|---|---|
| `POST /webhook` | ✓ | **✓ nur dieser Pfad** |
| `GET /healthz` | ✓ | nein |
| `GET /openapi.yaml` | ✓ | nein |
| `GET /docs` (Swagger UI) | ✓ | nein |
| `POST /review/{eventId}/approve` | ✓ | nein |

Die Schleuse ist das **mgmt-Caddyfile**, verwaltet von der Ansible-Rolle `ops_dashboard` (Hand-Edits werden
überschrieben), nicht die DMZ-Caddy:
`@provision_ext { host hooks.ki.actago.de; path /webhook; method POST; remote_ip <DMZ-Caddy> }`,
zusätzlich `@provision` für `/webhook` von der Control-Plane-VM. Alles andere fällt in `forward_auth` (→ 302).
Davon abraten, den Matcher für `/docs` zu erweitern: ein Partner braucht eine bereinigte Spec als Datei, keine
öffentliche UI.

**Docs im Browser ansehen, ohne etwas zu öffnen:**
```bash
ssh -N -L 8787:127.0.0.1:8787 acta-mgmt   # dann http://localhost:8787/docs
```
Die UI lädt Assets von unpkg.com und die Spec relativ von `/openapi.yaml` — über den Tunnel also funktionsfähig.

## Signatur

HMAC-SHA256 über den **Rohkörper**, 64 Hex-Zeichen, Header `x-signature`, Präfix `sha256=` optional.
Geprüft wird gegen die actago-Secrets aus Key Vault **und** alle Partner-Secrets. Gültig ist eine Signatur nur,
wenn genau ein Absender passt; ein deaktivierter Partner ergibt `401`. Mehrere Secrets je Absender erlauben
Rotation ohne Ausfall.

Fehlerquelle Nummer eins beim Partner: **den Payload nach dem Signieren erneut serialisieren.**
Bei `401 invalid_signature` zuerst danach fragen, nicht am Geheimnis zweifeln.

## Payload, Freigabe und Antworten

Vertrag (v1/v2, Felder, Partnerbindung, Freigaberegeln, Antwortcodes) und bekannte Spec-Lücken:
[references/payload-contract.md](references/payload-contract.md). Lesen, bevor du einen Payload bewertest,
einen Partner berätst oder einen 4xx/5xx erklärst.

Kurz: `demo_request` und `credential_rotation` laufen ohne Event-Review; `purchase` geht ins Review, außer
`WEBHOOK_PURCHASE_AUTO_APPROVE=true`; `upgrade`/`contract_upload` erzeugen erst nach Freigabe einen eigenen
`promote_to_production`-Job mit zweiter Freigabe. `200 already_processed` ist Erfolg; wiederholen nur bei
`503` (Backoff) und `429` (`Retry-After`).

## Partnerdoku erzeugen

Für Partner nie die interne Spec weitergeben. Ablauf und Streichliste:
[references/partner-docs.md](references/partner-docs.md).

## Beobachten und debuggen

```bash
journalctl -u webhook-receiver -f -n 0 -q          # jede Anfrage als [webhook-access]-JSON
```
Die Zeile enthält `status`, `sig_valid`, `outcome`, `event_id`, `event_type`, `slug`, `ip`, `ua`; dieselben
Zeilen liegen dauerhaft in `webhook-access.jsonl` im State-Verzeichnis. Job-Fortschritt je Event:
`jobs/<event_id>.json` (`stage`, `error`, `attempts`). Partner-Events tragen eine serverseitig umgeschriebene
`event_id` (`partner_<hash>`), nicht die des Partners.

Laufzeit-Env **ohne Root** lesen (Prozess gehört `actaone`):
```bash
tr '\0' '\n' < /proc/$(systemctl show webhook-receiver -p MainPID --value)/environ | grep -viE 'secret|token|key|password'
```

**Bleibt der Monitor still, obwohl der Partner gesendet hat**, hat der Request den Receiver nie
erreicht — dann in den Caddy-Logs suchen, nicht im Receiver. Ein `GET /webhook` aus einem Browser
ergibt `404` bzw. vor dem Receiver einen Redirect; das beweist noch keinen funktionierenden POST-Weg.

## Häufige Fehler

- **Nach `git pull` den Dienst neu starten und sich über 404 wundern.** Das Laufzeitverzeichnis ist
  eine andere Kopie.
- **Mit `SIGTERM` „neu starten“.** Der Dienst endet sauber und bleibt aus.
- **Der README-Konfiguration glauben.** Sie zeigt Staging, live läuft laut Ausgangsskill `prod`.
- **Das README-Beispiel als Partnervorlage nehmen.** `plan: "trial"` ergibt `400`.
- **Einen Partner „mal testen" lassen.** Das erzeugt Produktionsmandanten mit Einladungsmail.
- **Bei `401` am Geheimnis zweifeln.** Fast immer ist es erneutes Serialisieren des Payloads.
- **`/docs` extern freigeben, um es dem Partner zu zeigen.** Eine bereinigte Spec als Datei genügt.
- **Annehmen, dass zusätzliche Top-Level-Felder übernommen werden.** Sie ergeben `202` und verschwinden.
- **Der Spec glauben, ohne den Code zu prüfen.** Antwortcodes und Beispiele hinken hinterher
  (siehe Payload-Vertrag).
- **Die interne Spec an einen Partner geben.** Sie enthält den Review-Endpunkt und `review_approved`.
