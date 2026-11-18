# Zustandsübergänge und Prüfzeitpunkte

Codebasis und Grenzen siehe [sources.md](sources.md). Die Nachprüfungen ergänzen den Workflow; nicht jede davon ist heute automatisch implementiert.

## Übergangsmatrix

| Übergang | Voraussetzung / Zeitpunkt | Nachweis danach / Grenze |
|---|---|---|
| Frei → Hotseat → Kunde | Effektives Poolziel, freien reservierten Slot, laufende Jobs und festgelegten Kunden-Release prüfen. Claim über Provisioning. | Poolbesitzer, VM-/Context-Identität, Kundenkonfiguration und Funktion stimmen. Geclaimte VM ist kein freier Hotseat mehr. Nachfüllen separat beobachten. |
| Branch anlegen → provisioning → active oder failed | Expliziter Build, Ziel, Auth-Modus, Kontakt und vereinbarte TTL; begrenzte Kapazität. Branch wird frisch geklont, nicht aus Hotseat übernommen. | Registry, VM, tatsächlich gestartete Images, Dienste, Auth und expiresAt prüfen. `failed` kann echte Ressourcen belegen und zählt zum Limit. |
| Branch failed → active | Erfolgreicher regulärer Redeploy und passende bestehende Registry. | Der Worker erhält Metadaten/TTL und setzt nur failed zurück auf active. Kein Wiederbeleben von torn_down und keine stillschweigende TTL-Verlängerung. |
| Branch active/failed → torn_down | expiresAt abgelaufen und beim Spawn vereinbarter automatischer Abbau, oder ausdrücklicher manueller Abbauauftrag. | TTL-Sweep hängt an DEPLOY_CONTROL_MUTATIONS_ENABLED. provisioning wird nicht per TTL abgebaut; fehlendes expiresAt heißt unbegrenzt. Job, VM-Abwesenheit und Restressourcen prüfen. |
| Kunde aktiv → archiviert | Beauftragte Archivierung, Tenant/Domain/VM-Zuordnung vorhanden. | Worker setzt CP suspended, Perimeter archiviert, PVE-Archivtag/onboot=0, wartet auf Tag-Übernahme, stoppt Stack und fährt VM herunter. Die Wartezeit beweist keine Zabbix-Übernahme. Jeden Teilschritt prüfen. |
| Archiviert → aktiv | Beauftragte Wiederaufnahme, vorhandene VM und Replika-Sollwerte. | Regulären unarchive_tenant-Pfad verwenden: VM/Erreichbarkeit, Dienste, Route und CP-Endzustand prüfen. Vertragsstatus bleibt separat; Einschalten allein ist keine Wiederaufnahme. |
| Archiviert → Abbaukandidat | retention.js berechnet 14 Tage ab suspendedAt. Ohne gültigen Zeitstempel: unbekannt. | Abgelaufene Aufbewahrung ist ein Löschvorschlag, keine automatische Löschung. Datenbedarf, laufende Aufträge und expliziten Abbauumfang klären. |
| Abbaukandidat → entfernt | Richtige VMID/Node/Slug-Bindung unmittelbar prüfen; regulärer teardown_customer_vm-Job mit dessen Bestätigung. | Broker-Widerruf vor VM-Abbau; VM clusterweit nicht mehr vorhanden, Poolslot freigegeben. Context, Route, SSO, Plattformregistrierung und LiteLLM-Widerruf separat prüfen. |
| Alter zentraler Dienst → stillgelegt | Keine benötigte Clientroute mehr, neue Route funktional geprüft, beauftragter Rückweg/Beobachtungsbedarf erfüllt. | Gestoppte Clients, gehaltene Releases und indirekte Nutzer berücksichtigen. Kein pauschales „nach X Tagen löschen“. Dienst-/Datenabbau gesondert planen. |

## Fehler und Restressourcen

- `teardown-customer-vm.sh` entfernt die VM und gibt erst nach bestätigter Abwesenheit die Poolzuweisung frei. Context-/Routen-, SSO- und Plattform-Cleanup können dennoch Warnungen liefern. „OK“ ist kein Nachweis vollständiger Bereinigung aller Systeme.
- Der Worker widerruft LiteLLM-Keys nach dem VM-Abbau best effort. Ein erfolgreicher Teardown-Job kann daher einen offenen Key-Widerruf enthalten. Den zugeordneten Keybestand lesend nachprüfen; keine Keys anderer Instanzen anfassen.
- Bei Broker-Branch-Instanzen muss die Bindung vor dem Abbau widerrufen werden. Fehlender/unklarer Auth-Zustand blockiert. Keine rohe Proxmox-Löschung als Abkürzung.
- TTL-Abbau wiederholt nur definierte vorübergehende Brokerfehler, höchstens drei Versuche, mit 10/30 Minuten Abstand. Endgültiger Fehler bedeutet Handlungsbedarf, nicht unbegrenzte Agenten-Retries.
- `teardown-customer.sh` entfernt einen Stack und lässt Volumes zurück; es ist nicht dasselbe wie VM-Teardown.
- Der VM-Teardown stößt Hotseat-Reconciliation best effort an. Eine entfernte VM kann durch neue Reservekapazität ersetzt werden. Vor einer beauftragten Poolverkleinerung das effektive Poolziel und Reconciler-Verhalten prüfen, nicht nur einzelne warme VMs löschen.
- Vollständige Löschung aller Vault-Versionen, Backups, Datenbanken oder externen Registrierungen wird von diesen Pfaden nicht pauschal belegt. Den tatsächlichen Bestand und dessen eigene Aufbewahrung prüfen; keine zusätzlichen Löschungen aus einem VM-Auftrag ableiten.

## Release-Prüfpunkte

1. **Vor Stable-Freigabe:** geprüften Candidate und unveränderliche Images feststellen; offene Branch-Abnahmen, bekannte Blocker und Rückweg erfassen. Pins für Neukunden/Partner und Auswirkungen auf Hotseats prüfen.
2. **Nach Freigabe:** Registry und Pins rücklesen; ausgelöste Hotseat-Wärmung separat kontrollieren. Bestehende Kunden bleiben bis zum beauftragten Promote auf ihrem Stand.
3. **Nach Canary:** Image und gerenderte Konfiguration, zentrale Service-Anbindung, notwendige fachliche Proben und Fehlersignale prüfen. Erst mit passendem Ergebnis die beauftragte nächste Welle fortsetzen.
4. **Nach jeder Welle:** Zielumfang gegen erfolgreich/fehlgeschlagen/übersprungen/nicht erreichbar abgleichen. Gleicher Image-Tag beweist keine aktuelle Konfiguration. Teilfehler und Wartungsfenster nachhalten.
5. **Nach Deployment-Konvergenz:** Der vorhandene Deploy-Pfad räumt je Profil alte lokale Release-Images auf, nachdem seine internen Prüfungen und Einmal-Services abgeschlossen sind. Laufende Container-/Service-Referenzen bleiben geschützt; Rollback lädt Images erneut aus der Registry. Registry-Verfügbarkeit und benötigten Rückweg nicht mit lokalem Image-Cache verwechseln. Keine zusätzliche pauschale Docker-Volume-Bereinigung.
6. **Beim Release-Abschluss:** offene Test-/Branch-VMs mit Zweck, Verantwortlichkeit und TTL erfassen. Benötigte Fehlerreproduktionen behalten; erledigte Testumgebungen nur im vereinbarten Umfang abbauen. Fristverlängerung ist eine eigene Änderung. Keine generelle Löschung aller Branch-VMs nach Merge.
7. **Bei Fälligkeit:** Branch-TTL-Jobs, archivierte Abbaukandidaten und unvollständige Bereinigungen getrennt prüfen. Ein neuer regelmäßiger Job oder Scheduler muss ausdrücklich eingerichtet werden; dieser Skill installiert keinen.
