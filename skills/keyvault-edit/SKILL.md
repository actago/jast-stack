---
name: keyvault-edit
description: Ändere actaOne-Kunden-, Control-Plane- oder Dienstkonfiguration dauerhaft über den vorgesehenen Key-Vault-Scope und prüfe ihre Wirksamkeit nach dem beauftragten Redeploy. Nutze bei Env-/Secret-Änderungen oder verlorener Konfiguration nach Deploys.
---

# actaOne-Konfiguration im Vault ändern

Weiterentwicklung des vorhandenen gleichnamigen Skills. Benötigt den actaOne-Checkout mit `scripts/keyvault-secrets.sh` und den passenden eingerichteten Vault-Zugang. Herkunft: [references/sources.md](references/sources.md).

## Quelle und Umfang

Ordne die Einstellung dem aktuellen Konfigurationsvertrag zu: Vault-Env, Credential, Template oder dienstspezifischer Registry. Nicht jeder neue Modellname ist automatisch ein Vault-Wert. Lies bei unklarer Zuordnung den konsumierenden Renderer/Service. Dauerhafte Vault-Konfiguration nicht ausschließlich per Live-Service-Edit ändern.

Bestimme Umgebung, konkreten Scope, Zielinstanzen und Ausführungsidentität. Prüfe den konfigurierten Vault anhand nicht geheimer Metadaten. Gleiche private IPs oder ein ähnlich benannter Clone sind kein Beleg für getrennte Vaults. Eine shared Vault-Konfiguration darf nicht als isolierter Test behandelt werden.

Lies die aktuelle Schnittstelle im Skript. Sie enthält unter anderem `customer`, `customer-env`, `customer-credential`, `control-plane`, `customer-defaults`, `webhook` und `provisioner`; weitere Scopes nicht aus dieser Liste ausschließen. `customer-defaults` kann auch Bestandskunden erreichen: `promote.sh` ergänzt fehlende Schlüssel beim nächsten Promote, mit expliziten Ausnahmen und Migrationen. Prüfe dessen aktuellen Backfill-Vertrag; eine Defaults-Änderung ist nicht automatisch auf Neukunden beschränkt.

Gespeicherte und deploybare Konfiguration können sich unterscheiden. Im geprüften neueren Stand filtert `fetch customer` release-gebundene Self-Heal-Schalter anhand des Image-Pins, ebenso der Publish-Pfad. Für die Prüfung des gespeicherten Stands gibt es `fetch customer-unfiltered`; das ist kein Deploy-Fallback. Bei Änderungen an solchen Schaltern den aktuellen `scripts/selfheal_levels.py`-Vertrag und `docs/operations/selfheal-stufen-rollout.md` lesen. Kanonische `KEY=wert`-Zuweisungen verwenden; Filter nicht umgehen oder aus einer gefilterten Ansicht unbemerkt andere gespeicherte Werte entfernen.

## Ändern und belegen

Hole nur benötigte Werte in geschützte temporäre Dateien am vorgesehenen Ausführungsort. Secret-Werte weder als Shellargument, Klartext-Patch, Log noch Chat ausgeben. Nutze vorhandene Zugangsmittel; neue vom Nutzer benötigte Secrets über den sicheren Eingabekanal der Laufzeit anfordern.

Halte beim Fetch die nicht geheimen Versions-IDs des Legacy-Secrets oder des Manifests und aller referenzierten Parts fest. Vergleiche Metadaten vor und nach dem Fetch, damit eine bereits während des Lesens veränderte Zusammenstellung nicht als konsistente Basis gilt. Vor Publish diese Versionsmenge einschließlich neuer/entfallener Parts erneut vergleichen. Bei Änderung frisch holen und nur den beauftragten Schlüssel auf den neuen Stand anwenden. Sind Metadaten nicht verfügbar, ist konfliktfreies Schreiben nicht belegt; den erforderlichen koordinierten Schreibweg klären.

Ändere gezielt die beauftragten Schlüssel, erhalte den übrigen Inhalt und prüfe die Struktur. Ein noch nicht vorhandener Schlüssel muss bei gewünschter Ergänzung tatsächlich eingefügt werden; ein wirkungsloses Such-Ersetzen ist kein Erfolg. Der Versionsvergleich verhindert kein Rennen zwischen letzter Prüfung und Publish: Das Skript bietet keine atomare Compare-and-Swap-Transaktion. Konkurrierende Promotion-/Autodeploy-Schreiber über den vorgesehenen Betriebsablauf koordinieren; bei laufenden unkoordinierten Schreibern nicht veröffentlichen.

Nutze den passenden Publish-Scope. Der Rückweg läuft über die zuvor erfassten Key-Vault-Versionen, bei Chunking als konsistenter zusammengehöriger Stand; keine lokale Klartextkopie als Restore-Quelle anlegen. Arbeitsdateien sind nur für die gezielte Änderung bestimmt. Env-Bundles können aus Parts und Manifest bestehen: das vorhandene Skript verwenden, nicht Einzel-Parts ad hoc schreiben. Legacy-Fallback nur bei bestätigtem `SecretNotFound`; transienter Fehler oder fehlende Berechtigung rechtfertigt keinen alten Datenstand.

Konkrete Werkzeuge aus dem vorhandenen Ablauf: `ACTAONE_KEY_VAULT_CONFIG` wählt die eingerichtete Umgebung; den tatsächlichen Config-Pfad prüfen statt einen fremden zu übernehmen. `list-keys` prüft Schlüssel ohne Werte; je nach Implementierung zeigt es die gefilterte Ansicht. Nach dem zum Auftrag passenden Fetch für eine reine Env-Änderung nur `publish customer-env` nutzen, damit das separate Credential nicht mitgeschrieben wird. Bei `customer-defaults` die Wirkung auf neue Instanzen und den Backfill bestehender Instanzen getrennt bewerten.

Ein Publish ist noch keine Laufzeitänderung. Führe den beauftragten Redeploy über den vorgesehenen Pfad aus (bei Kunden der passende `scripts/promote.sh`-/gesteuerte Rollout-Pfad); wenn nur Konfiguration beauftragt war, berichte den ausstehenden Aktivierungsschritt. Kunden-Images auf freigegebenem unveränderlichem Release halten; `deploy/RELEASE` oder `latest` ersetzen keine Stable-Prüfung.

Verifiziere ohne Secret-Ausgabe sowohl persistierte Änderung als auch, soweit beauftragt aktiviert, die wirksame Funktion. Eine erfolgreiche Publish-Antwort reicht dafür nicht. Räume eigene temporäre Dateien auf; sicheres Überschreiben auf SSD/CoW nicht garantieren. Berichte Schlüsselbezeichnungen, Ziele und Prüfergebnis, keine Werte.
