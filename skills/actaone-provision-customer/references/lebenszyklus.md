# Lebenszyklus: Archivieren, Freigeben, Teardown

Nur ausführen, wenn der Nutzer genau diese Aktion für genau diese Instanz beauftragt hat. Vorher Slug, Tenant-ID, VM-Name `cust-<slug>` und Datenfolgen bestätigen. Quelle: `provisioning/deploy-control-api/index.js` und `job-worker.js` auf actaOne `origin/main`.

## Umkehrbar zuerst: Archivieren

- `archive_tenant` setzt die CP auf suspended, stellt die Perimeter-Route auf eine Archiv-Seite, setzt den PVE-Archivtag und onboot=0, skaliert nach der vorgesehenen Wartezeit die Dienste auf 0 und fährt die VM herunter. Replika-Schnappschuss bleibt erhalten. Erfordert `confirm=<tenantId>` und eine Dashboard-Freigabe. Teilfehler können bereits geänderte Zustände hinterlassen; jeden Schritt rücklesen.
- `unarchive_tenant` stellt den Zugriff wieder her und ist automatisch freigegeben.
- Lizenzaktionen (Testphase verlängern, Umstellung auf Produktion) schreiben in die Control-Plane und hängen am dortigen Fork-Endpunkt; ob sie wirken, laut aktuellem `CLAUDE.md` des actaOne-Repos prüfen. Nicht Teil von Anlage oder Teardown.

Wenn der Nutzer „Kunde weg“ sagt, aber nicht ausdrücklich Datenlöschung, Archivieren als Option nennen und nachfragen.

## Teardown (zerstörend)

Teardown löscht die VM mit `purge=1` samt Datenträgern. Ob eine aktuelle, wiederherstellbare Sicherung der VM existiert, ist vorher zu prüfen statt anzunehmen: `CLAUDE.md` (Stand 10/2026) meldet einen seit Wochen scheiternden PBS-Job neben einem zweiten vzdump-Ziel; Details beim Resilience-Agenten. Ausdrückliche Bestätigung der Datenlöschung einholen.

Weg: Job `teardown_customer_vm` mit `confirm=<slug>`; VMID weglassen, der Worker löst sie über den Proxmox-Namen auf und bricht bei Abweichung ab. Reihenfolge im Worker:

1. Branch-Instanzen im Broker-Modus: Broker-Bindung widerrufen, vorher keine VM-Arbeit.
2. Kunden: Kunden-Auth über den Vault widerrufen.
3. `scripts/teardown-customer-vm.sh <slug> <vmid>`: Entra-Redirect-URIs entfernen (best effort, Warnung beachten), Caddy-Route, Docker-Context, VM stoppen und löschen mit Nachprüfung, Pool-Slot freigeben, CP-Registrierungen über `cleanup-platform-registrations.sh` bereinigen (Schutzliste für interne Slugs), Hotseat-Reconcile im Hintergrund.
4. LiteLLM-/Gateway-Keys widerrufen; bei Warnung `scripts/revoke-gateway-keys.py --slug <slug>` nachholen.

Den Skript-Direktaufruf nicht verwenden, um fehlende Job-Freigabe oder gescheiterten Auth-/Broker-Widerruf zu umgehen. Ein gesondert beauftragter Reparaturpfad muss dieselben Voraussetzungen erfüllen und verbleibende Widerrufe nachweisen. `scripts/teardown-customer.sh` ist ein anderer, älterer Pfad (Stack auf geteiltem Swarm entfernen, Volumes bleiben) und passt nicht zum 1-VM-Modell.

Ältere Anleitungen verlangen danach ein manuelles Löschen von `tenants`/`platforminstances`/`platformexportevents`. Im geprüften Stand übernimmt das Skript diesen Schritt; nur bei seiner Warnung gezielt nachziehen.

## Nach dem Teardown prüfen

VM nicht mehr im Cluster, Context und Route entfernt, Pool-Zuweisung frei, CP-Registrierung weg, Job-Notizen ohne Widerrufswarnung. Eine Neuanlage desselben Slugs ist möglich; ohne bereinigte Export-Events entsteht Sequence-409. Slugs und Secrets abgebauter Testinstanzen nicht für andere Kunden wiederverwenden (Broker-Runbook).
