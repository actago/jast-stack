---
name: actaone-vm-lifecycle
description: Prüfe und begleite Zustandswechsel von actaOne-VMs und Instanzen, einschließlich Branch-TTL, Hotseat-Übernahme, Archivierung, Wiederaufnahme und Abbau sowie Ressourcenbereinigung nach Releases.
---

# VM- und Instanz-Lebenszyklus

Nutze diesen Skill bei „was kann weg?“, überfälligen Branch-VMs, Archivierung/Wiederaufnahme und bei der Frage, welche Lifecycle-Prüfung zu einem Release gehört. Ein Releaseauftrag allein autorisiert keinen Kundenabbau.

## 1. Zustand und Auftrag bestimmen

Lies den verwendeten actaOne-Stand und die für den Übergang genannten Quellen aus [sources.md](references/sources.md). Die [Übergangsmatrix](references/transitions.md) beschreibt den geprüften Code und zusätzliche Abschlussprüfungen; sie ist kein Live-Inventar.

Erfasse je Ziel nur notwendige Metadaten: Umgebung, Slug, Tenant-/Instanzidentität, VMID/Node, Docker-Context, Rolle (Kunde, Branch, Hotseat, Benchmark, Infra), Ist-/Ziel-Release, zuständiger Auftrag, TTL bzw. Aufbewahrungsfrist und laufende Jobs. Prüfe die Identität gegen Proxmox, Pool und Registry; gleiche IPs im Clone und Prod sind kein Identitätsbeleg.

Halte die Zustände getrennt:

- **Release:** Candidate, freigegebener Stable, tatsächlich je Ziel ausgerollter Stand.
- **Mandant:** Vertragsstatus/Testphase und aktiv/suspended.
- **Betrieb:** Perimeter-Route, Stack-Replikas, VM-Power und Erreichbarkeit.
- **Branch-Registry:** provisioning, active, failed, torn_down; dazu expiresAt und Teardown-Job.

„Offline“, „Trial vorbei“, „archiviert“ und „gelöscht“ dürfen nicht ineinander übersetzt werden. Ein fehlgeschlagener Job kann bereits Teiländerungen bewirkt haben.

## 2. Übergang vorbereiten und ausführen

1. Gewünschten Übergang aus der Matrix wählen; bei einer Bestandsprüfung nur einen Plan mit Kandidaten und Gründen liefern.
2. Voraussetzungen unmittelbar vor dem Übergang neu prüfen: Identität, konkurrierende Jobs/Locks, beauftragter Umfang, Datenbedarf und erforderlicher Rückweg. Fristen aus vorhandenen Zeitstempeln berechnen, nicht aus VM-Alter oder letzter Session ableiten.
3. Vor einem beauftragten Abbau prüfen, ob benötigte Daten und Prüfnachweise gesichert sind und welcher Wiederherstellungsweg tatsächlich existiert. Archivierung ist kein Backup. Keine neue pauschale Aufbewahrungsfrist erfinden.
4. Regulären Ops-Job verwenden. API-Bestätigung, Operator-Freigabe und Broker-Widerruf nicht durch direkte Skriptaufrufe umgehen. Die aktuell geltende Job-Payload im API-Code lesen.
5. Nach jedem Übergang Zielzustand unabhängig vom Jobstatus rücklesen. Warnungen und unvollständige Schritte als Teilabschluss ausweisen; weder den Job blind wiederholen noch Registry/Pool von Hand „grün“ setzen.

## 3. Release-Zyklus und Aufräumen

Nutze die [Release-Prüfpunkte](references/transitions.md#release-prüfpunkte): vor Freigabe, nach Freigabe, nach Canary, nach jeder Welle und beim Abschluss. Ein Zeitplan ersetzt keinen Nachweis des vorherigen Zustands.

Alte lokale Release-Images, Branch-VMs, archivierte Kunden und abgelöste zentrale Dienste haben verschiedene Abbaukriterien. Insbesondere ist ein Merge kein TTL-Ablauf, eine TTL kein Nachweis erfolgreicher Löschung und ein neuer Stable kein Anlass, alle Hotseats oder Testumgebungen zu entfernen.

## 4. Abschluss

Berichte pro Ziel: vorheriger Zustand → belegter Endzustand, Zeit des Readbacks, Release, verbleibende Ressourcen/Keys/Routen, offene Warnungen und nächste fällige Prüfung. Bei Abbau zusätzlich VM-Abwesenheit und Poolfreigabe getrennt nachweisen. Pflege den Betriebsnachtrag an der vorhandenen maßgeblichen Quelle, ohne Secret- oder Kundengesprächsinhalte zu übernehmen.
