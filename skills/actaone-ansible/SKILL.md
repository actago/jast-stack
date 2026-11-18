---
name: actaone-ansible
description: Prüfe oder ändere actaOne-Ansible-Playbooks und führe beauftragte Infrastruktur-Applies mit passendem Inventory, persistenten Variablen und fachlicher Abnahme aus. Nutze für Ops-Dashboard, Deploy-Control, Webhook und andere Rollen unter infra.
---

# actaOne-Ansible

Benötigt den zum Auftrag passenden actaOne-Checkout, sein Inventory und für einen Live-Apply den eingerichteten Controller-/Adminzugang. Herkunft: [references/sources.md](references/sources.md). Fehlen diese Quellen, benenne sie. Es gibt keine fest eingebaute Management-IP oder verpflichtende lokale WSL-Installation.

## Vorbereiten

Bestimme Rolle, Playbook, Zielumgebung und gewünschten Effekt. Prüfe Checkout/Commit und lokale Änderungen; überschreibe keinen fremden Arbeitsstand. Lies `infra/ansible.cfg`, das Playbook, Tasks, Handler, Templates und relevante Variablenquellen. `inventory.example.yml` ist eine Vorlage und kann historische Adressen oder Platzhalter enthalten.

Ermittle den tatsächlich vorgesehenen Controller, SSH-User, `become`-Weg und Runtime-User. `infra/ansible.cfg` setzt relative Pfade; führe Befehle aus `infra/` aus oder setze Pfade und Config ausdrücklich. Prüfe die bereits vorhandene Ansible-Version und erforderlichen Collections; erzeuge nicht routinemäßig eine neue Toolchain auf dem Laptop.

Binde die Zielprüfung an genau den späteren Ansible-Verbindungsweg: wirksamen `ansible_host`, User, Port, SSH-/ProxyJump-Argumente und deren Variablenherkunft gezielt auflösen, ohne das gesamte Inventory auszugeben. `--list-hosts` liefert nur Namen. Bestätige die Gastidentität mit einer lesenden Aktion über dieselbe Ansible-Konfiguration und denselben Controller. Eine erfolgreiche Prüfung eines anderen SSH-Alias reicht bei identischen Clone-/Prod-Adressen nicht.

Leite aus geänderten Templates ab, welche Werte beim nächsten Apply erhalten bleiben müssen. Vergleiche gezielt Sollwerte und wirksamen Ist-Stand, ohne Secrets auszugeben. Dauerhafte Konfiguration gehört in die vorgesehene persistente Quelle; ein früheres `-e` ersetzt diese nicht. Leere Werte sind nicht pauschal Fehler, müssen aber bei Routen, Partnerkonfiguration oder Pins ausdrücklich als beabsichtigt belegt sein.

Prüfe zusätzlich betroffene zielspezifische Overrides außerhalb der Templates: Systemd-Drop-ins, Umgebungsdateien, Cron-/Autodeploy-Einstellungen und Clone-Routen. Eine nicht im Template-Diff sichtbare Abweichung kann trotzdem überschrieben oder reaktiviert werden. Überführe beauftragte dauerhafte Werte in die tatsächlich verwendeten `group_vars`/`host_vars` oder das geschützte Controller-Inventory; Details in der Apply-Referenz. Erhalte bewusst abweichende Clone-Policies und benenne ungeklärte Herkunft vor dem Apply.

## Prüfen und anwenden

Arbeite nach [references/apply.md](references/apply.md). Für reine Codeänderungen reichen die zum Patch passenden lokalen Prüfungen; sie autorisieren kein Live-Apply. Bei autorisiertem Apply verwende genau den geprüften Stand und Zielumfang. Bereits erteilte Autorisierung erneut abzufragen ist nicht erforderlich.

Plane Neustarts anhand der Handler. Besonders Deploy-Control/Worker nicht in laufende Deployment-Jobs hinein neu starten. Falls aktive Jobs die sichere Ausführung verhindern, benenne den Konflikt und verschiebe den Apply statt Jobs abzubrechen.

Fertig ist der Apply erst mit fachlichem Nachweis: erwartete Units/Routes/Worker und konfigurierte Funktion, nicht nur Exitcode 0. Zeige Ziel, Commit, relevante Änderung, Prüfresultat und offene Einschränkungen. Halte einen nachvollziehbaren Rückweg bereit; Daten-/Secret-Rollbacks nicht aus einem alten Snapshot ungeprüft einspielen.
