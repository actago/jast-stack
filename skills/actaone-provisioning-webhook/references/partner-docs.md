# Partnerdoku erzeugen

Für Partner nie die interne Spec weitergeben. Eine selbsttragende HTML-Seite bauen (Spec eingebettet,
kein Nachladen der Spec, funktioniert als lokale Datei) und dabei entfernen:

- Pfad `/review/{eventId}/approve` und Schema `ReviewApproveResponse`
- Feld `review_approved`
- `source` und `ttl_days`, falls sie in der aktuellen Spec wieder auftauchen (wirkungslos)
- Server `http://127.0.0.1:8787`
- Eventtypen, die der Partner nicht senden darf (`cancel`, `credential_rotation`)
- `tryItOutEnabled: false` und `supportedSubmitMethods: []` setzen — sonst kann aus der Doku heraus
  versehentlich ein echter Provisioning-Request abgehen

Zusätzlich die in [payload-contract.md](payload-contract.md) genannten Spec-Lücken korrigieren: fehlende
Antwortcodes ergänzen, ungültige Beispiele ersetzen. Beispiele nur mit erfundenen Daten
(z. B. „Stadt Musterstadt“), keine echten CRM-IDs.

YAML → JSON geht am einfachsten mit `js-yaml` in einem LibreChat-Container (mgmt hat kein pyyaml
garantiert), oder lokal mit einem vorhandenen YAML-Parser. Die Swagger-Assets kommen von unpkg.com; der
Empfänger braucht also Internet.

Weitergabe an den Partner ist ein externer Schritt: Datei und Empfänger vorher mit dem Nutzer bestätigen.
