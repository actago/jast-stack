# Prüf- und Apply-Vertrag

## Vorprüfung

Das konkrete Playbook und Inventory kommen aus der Zielklärung. Beispielhafte Befehlsform im Verzeichnis `infra/`:

```text
ansible-playbook -i <geprüftes-inventory> <playbook> --syntax-check
ansible-playbook -i <geprüftes-inventory> <playbook> --list-hosts --limit <zielumfang>
ansible-playbook -i <geprüftes-inventory> <playbook> --check --limit <zielumfang>
```

Das sind Formen mit Platzhaltern, keine sofort auszuführenden Befehle. Ein YAML-Parser allein prüft weder Ansible-Semantik noch Rollenauflösung. Vor Remote-Check Tasks auf `check_mode: false`, delegierte Aktionen und nicht unterstützten Check-Modus prüfen: ein Dry-Run ist nicht automatisch ohne Seiteneffekt.

`--diff` nur für nicht geheime Renderpfade verwenden, deren Ausgaben sicher sind. `no_log`/`diff: false` für sensible Tasks respektieren; vollständige Inventories, Environment-Bundles und Systemd-Secret-Drop-ins nicht in den Chat drucken. Diff bei geheimen Änderungen über Schlüsselpräsenz und gezielte redigierte Nachweise ersetzen.

Stoppsignale: falsche Zielhostliste, unerklärtes Entfernen von Routen oder Partnerwerten, überschriebenes fremdes Arbeitsverzeichnis, leerer erforderlicher Wert oder unerwartete Neustarts. Einen nur teilweise möglichen Check ehrlich als solchen ausweisen; keine grüne Gesamtprüfung behaupten.

## Spezifische Repo-Eigenschaften

`infra/inventory.yml` und mehrere umgebungsspezifische Dateien unter `infra/group_vars/all/` sind absichtlich gitignored. Prüfe `.gitignore`, die vorhandenen `.example`-Dateien und den Controller: ein fehlender Wert im Git-Checkout ist kein Beweis, dass er nirgends persistent liegt. Nicht geheime gemeinsame Sollwerte gehören in die gepflegte versionierte Quelle; umgebungsspezifische Werte in die dafür vorhandene geschützte Variablenquelle. Secrets nicht in neue versionierte YAML-Dateien schreiben. Vor der Korrektur sicherstellen, dass der konkrete Playbook-Aufruf diese Quelle tatsächlich lädt.

- `configure-deploy-control-api.yml` und `configure-ops-dashboard.yml` laufen auf `management_vms` mit `become: true` und `serial: 1`.
- `deploy_control_api` prüft einen gesetzten Kunden-Release gegen `stable-releases.jsonl` und schreibt den Provisioning-Pin. Änderung dieses Pins kann auch Hotseats/Neukunden betreffen.
- Handler der Deploy-Control-Rolle starten API/Worker neu. Vorher tatsächliche Jobaktivität über die im aktuellen `provisioning/deploy-control-api/index.js` definierten lesenden Statuswege prüfen, beispielsweise `GET /api/v1/overview` und `/api/v1/jobs` mit vorgesehener Authentisierung. Status unmittelbar vor dem restart-auslösenden Apply erneut prüfen. Ein früherer Leerlauf ist keine Reservierung; vorhandene Koordination/Freigabe der Deployment-Steuerung nutzen und bei nicht beherrschbaren konkurrierenden Jobs verschieben.
- Dashboard-Tasks bauen im Repo als Runtime-User und kopieren anschließend in das Web-Root. Ein Checkout allein belegt nicht den ausgelieferten Stand; erfolgreiche Dependencies allein nicht den Build.
- Rolle und Templates sind die Wahrheit über Variablen und Nebenwirkungen. Diese Hinweise sind aus einem lokalen Stand abgeleitet und vor späterer Anwendung abzugleichen.

Abgleich mit lokal vorhandenem `origin/main` vom 13.11.2026: Die Deploy-Control- und Dashboard-Rollen haben inzwischen Assertions gegen den Verlust bestehender Partner-Inventare/-Routen. Secret-Units und Drop-ins sind teilweise ausdrücklich `no_log: true`, `diff: false`. Diese Guards erhalten; ihr Vorhandensein am tatsächlich ausgeführten Commit prüfen. Ein alter Checkout besitzt sie möglicherweise noch nicht. Das macht Ziel-, Variablen- und Jobprüfung nicht überflüssig.

## Nachprüfung

Prüfe zielbezogen Unit-Zustand, erwartete Version/Datei sowie die fachliche Route oder API. Bei einer Gateway-/Partneränderung auch die betroffene Route testen; ein gesundes Dashboard allein genügt nicht. Zugangsdaten nur über vorhandene Secret-Verfahren. Temporäre eigene Dateien und Rechte entfernen, bestehende Rechte erhalten.
