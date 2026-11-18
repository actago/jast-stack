# Hotseat-Übernahme und Klon-Fallback

Quelle: `docs/HOTSEATS.md`, `scripts/claim-hotseat.sh`, `job-worker.js` (`acquireInstanceVm`, `allocateVm`, `executeCustomerAction`) auf actaOne `origin/main`. Zahlen und Bänder vor Nutzung dort nachlesen; sie ändern sich.

## Was der Claim tut

`claim-hotseat.sh <slug>` ist nur die Übergabe, kein Deploy:

1. Ersten bereiten `hotseat-*` in `~/.actaone-autodeploy/vm-pool.json` atomar dem Slug zuschreiben. Slots mit `provisioning`-Flag und nicht per SSH/Docker erreichbare Kandidaten werden übersprungen.
2. Kunden-RAM laut Policy setzen (`scripts/lib/customer-vm-memory.sh`; Standard 10240 MiB mit fester Ausnahme). Ein RAM-Wechsel braucht Shutdown+Start, also etwa 1–2 Minuten zusätzlich; nach Neustart kann cloud-init neue SSH-Hostkeys erzeugen, die Recovery liest sie gezielt über den Proxmox-Gastagenten.
3. Proxmox-VM in `cust-<slug>` umbenennen, Tags setzen.
4. Docker-Context `customer-warm<n>` → `customer-<slug>`.
5. Perimeter-Route über `publish-caddy-route.sh`.

VMID und IP bleiben beim Kunden. Das gemeinsame Band für Hotseats und Klone verbraucht sich monoton; ist es voll, braucht es eine Netzentscheidung, keinen Config-Tweak.

## Fallback-Regel

Nur **Exit 3** („kein bereiter Hotseat“) führt zu `allocateVm()` und Klon über `provision-customer-vm.sh`. Jeder andere Claim-Fehler bricht den Job ab und ist zu diagnostizieren, nicht durch einen Klon zu überdecken. `provision-customer-vm.sh` läuft nur, wenn der Context `customer-<slug>` noch fehlt. Eine Pool-Zuweisung, deren VMID in Proxmox einen fremden Namen trägt, gilt als korrupt und stoppt.

## Warum es langsam sein kann

Das 5–7-Minuten-Ziel gilt nur bei warmem Hotseat auf dem aktuellen Neukunden-Default. `warm-hotseats.sh` wärmt laut `release-pins.json` vor (stündlich und nach Stable-Freigabe). Langsamer und kein Fehler: Stable-Wechsel noch nicht vorgewärmt, explizit anderer Partner-Release, RAM-Wechsel, Klon-Fallback. `GET /api/v1/hotseats` zeigt `stableTag`, `provisionReleaseTag`, `readyCount`/`freeCount` und je Seat `warmedTag`.

## Grenzen dieses Skills

Pool-Ziel, Reconcile und Vorwärmen sind eigene Betriebsaktionen (`set_hotseat_target`, `run_hotseat_reconcile`). Bei einer Anlage nur lesen; Änderungen daran brauchen einen eigenen Auftrag und eine Kapazitätsprüfung.
