# Herkunft und Grenzen

Erstellt am 17.11.2026 aus dem lokalen actaOne-Git-Objekt `origin/main` = `73ce7d4ccdb5097d3916f15357da3f4a2a98a7e3` (Commit vom 13.11.). Kein neuer Remote-Fetch und keine Live-Prüfung. Die folgenden Pfade sind relativ zum actaOne-Repo; bei Durchführung den tatsächlich verwendeten Stand prüfen.

- `provisioning/deploy-control-api/branch-instances.js`: Registry-Statusmengen, TTL-Auswahl und belegte Slots.
- `provisioning/deploy-control-api/job-worker.js`: executeArchiveTenant, executeUnarchiveTenant, executeCustomerAction, restoreBranchInstanceAfterRedeploy, revokeInstanceKeys, sweepExpiredBranchInstances und TTL-Retry-Grenzen.
- `provisioning/deploy-control-api/retention.js`: 14 Tage ab suspendedAt; expired ist ausschließlich Löschvorschlag.
- `provisioning/deploy-control-api/tenant-lifecycle.js`: Lizenz-/Trialzustand ist getrennt von VM-Power; Verlängerungen mit Konfliktprüfung.
- `ops-dashboard/src/features/fleet/lifecycleSteps.ts`: Anzeigeprojektion und unterschiedliche Zeitstempel; keine autoritative Zustandsmaschine.
- `scripts/teardown-customer-vm.sh`: VM-Abwesenheit, Poolfreigabe, best-effort Nebenschritte und Reconciliation.
- `scripts/teardown-customer.sh`: Stack-Abbau erhält Volumes.
- `scripts/reconcile-hotseats.sh`: effektives Poolziel und Reservierung/Live-Inventar. Der alte Kopfkommentar nennt Default 4; die gelesene Implementierung verwendet Env, dann Statedatei, sonst 0. Nicht den Kommentar als heutigen Sollwert übernehmen.
- `scripts/deploy-customer.sh` und `scripts/tests/test_release_image_cleanup.sh`: Zeitpunkt und getesteter Umfang lokaler Image-Bereinigung, erneuter Pull beim Rollback. Testdatei gelesen, nicht ausgeführt.
- `docs/OPS_DASHBOARD.md`, Abschnitt Branch-Instanzen: Spawn, Freigabe, TTL und Ausschluss aus Kundenrollouts.

Eigene Aggregation: Übergangsmatrix und Release-Prüfpunkte verbinden diese vorhandenen Abläufe. Daten-/Rollbackbedarf und unabhängiger Endzustandsnachweis sind Arbeitsanweisungen, keine Behauptung, dass alle Prüfungen bereits automatisch laufen. Keine vollständige neue Zustandsmaschine oder Aufbewahrungsrichtlinie implementiert. Nicht geklärt: heutiger Flottenzustand, aktive Cron-/Worker-Konfiguration und konkrete Backup-Verfügbarkeit.
