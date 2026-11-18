---
name: actaone-service-rollout
description: Instanzübergreifenden Umzug von actaOne-Kundeninstanzen auf einen neuen oder verlegten zentralen Dienst planen, durchführen oder abnehmen (Singleton, Gateway, Cluster; z. B. Presidio, CodeAPI, LiteLLM, Docling) – Identität, Anbindung, Vault-Konfiguration, Canary und Wellen, Rückweg sowie Abschalten alter Dienste oder VMs. Nutzen bei „Instanzen auf den zentralen Dienst umstellen“, „neuen Infra-Dienst für alle Kunden einführen“, „alten Pool/alte VM abschalten“ und „ist der Umzug fertig“. Dienstinterne Fehler und Tuning gehören zum jeweiligen Dienst-Runbook.
---

# actaOne-Service-Rollout

Ein zentraler Dienst ersetzt Dienste je Instanz oder einen älteren zentralen Endpunkt. Jede Kundeninstanz muss dabei die Grenze zwischen ihrem Stack und dem gemeinsamen Dienst sicher überqueren. Dieser Skill beschreibt diesen **Verkehrswechsel** und seine Phasen. Was im Dienst selbst passiert (Erkenner, Worker, Modellkatalog, Konvertierung), regeln Dienst-Runbook und gegebenenfalls ein vorhandener Dienst-Skill wie `actaone-presidio` oder `actaone-litellm`.

Vorbilder aus dem Bestand: Presidio lokal → Prod-Singleton (11/2026), CodeAPI `.111:3114` → K3s-Cluster und Abschaltung des Legacy-Pools 3112 (10–11/2026), LiteLLM direct → `litellm-global` (Opt-in je Instanz), Docling als geplanter gemeinsamer Dienst (nur Recherche). Stand und Fundstellen je Dienst: [references/dienste.md](references/dienste.md).

## 1. Quellen bestimmen

1. **actaOne-Monorepo** (Remote `actago/actaOne`): Lokalen Klon über `git remote -v` finden, Abstand mit `git rev-list --count HEAD..origin/main` melden und Verträge aus `origin/main` lesen (`git show origin/main:<pfad>`). Kern: `docs/operations/service-rollout-policy.md`, das Dienst-Runbook und ein vorhandenes Release-Manifest unter `deploy/releases/`.
2. **Dienst-Repo bzw. Fork**, wenn der Clientvertrag dort liegt (z. B. LibreChat-Fork für Transport und Fail-closed, LiteLLM-Repo für Katalog und Keys).
3. **Wissensbasis** (Obsidian-Vault, Remote `actago/actaOneKBobsidian`): Service-Referenz des Dienstes für datierte Live-Nachweise und offene Abweichungen.
4. **Live-Zustand** über den Management-Zugang laut Monorepo-`CLAUDE.md`: laufende Service-Spezifikationen, Vault-Bundles, Dienst-Health.

Fehlt eine Quelle, das ausdrücklich melden und betroffene Aussagen als ungeprüft kennzeichnen. Für den Sollvertrag gilt `origin/main`, für den Ist-Zustand die Live-Messung; Abweichungen werden berichtet. Zahlen in diesem Skill und in der KB (Instanzzahlen, IPs, Releases) sind datierte Belege, keine heutige Wahrheit.

## 2. Phase und Umfang festlegen

Ein Umzug besteht aus **Phasen**, deren Umfang vom Auftrag gedeckt sein muss. Ein Auftrag kann mehrere oder alle Phasen bereits umfassen; dafür nicht erneut um Freigabe bitten. Ein begrenzter Canary-Auftrag umfasst dagegen weder die ganze Flotte noch den Abbau gemeinsamer Ressourcen. Technische Operator-Gates des vorhandenen Workflows bleiben bestehen.

| Phase | Endet mit | Typischer Auftrag |
|---|---|---|
| **Bereitstellung** | Dienst läuft, Infrastrukturprobe grün, keine Instanz angebunden | „zentralen Dienst aufbauen“ |
| **Canary** | eine benannte Instanz umgestellt, fachlich abgenommen, Rückweg erprobt oder belegt | „erst bei actago4it umstellen“ |
| **Wellen / Flotte** | eingefrorene Zielliste umgestellt, je Ziel Ergebnis | „Welle 2“, „alle Prod-Kunden im Release“ |
| **Neukunden-Default** | Provisionierungspfad liefert das Ziel, verifiziert an einer Neuanlage | „Neukunden direkt zentral“ |
| **Abschaltung** | alte Ressource gestoppt bzw. entfernt im beauftragten Umfang | „Pool 3112 abschalten“ |

Nennt der Auftrag keinen Zielumfang (Slugs, Welle, Umgebung), zuerst den Umfang klären. Eine Diagnose oder Bestandsaufnahme ändert nichts. „Alle Kunden“ bedeutet die eingefrorene Liste aus der Inventur, nie die Erreichbarkeit zum Zeitpunkt des Laufs.

## 3. Rollout-Weg wählen

Den Weg nimmt der Umzug aus dem Bestand, nicht aus einer neuen Mechanik:

- `service-rollout-policy.md` prüfen: Ein eigener Flotten-Job ist nur gerechtfertigt, wenn alle fünf Kriterien dort erfüllt sind. Sonst läuft der Wechsel über den vorhandenen Kundenpfad (`promote.sh` / Stable-Release, Panel- und Dashboard-Rollout, Neukunden-Provisionierung).
- Bewährtes Muster: Komponente im Release-Manifest mit `activation` (`release`/`manual`), Migrationsschritt im Promote **vor** dem Env-Publish, Hold-Schalter je Instanz (`<DIENST>_RELEASE_MIGRATION=hold`), Ausschluss von Nicht-Kunden (`staging`, `prod`, `warm*`, `branch-*`, `infra-*`).
- Kunden-Deploys laufen nie gegen den Control-Plane-Swarm (`--context prod`).

Aktiviert ist ein Pfad erst, wenn alle Kopien seiner Logik nachgezogen sind, etwa das Repo auf dem Management-Host **und** die installierte Worker-Kopie der Deploy-Control-API. Sonst läuft die Automatik nur teilweise (Beispiel Presidio: Worker überspringt Instanzen auf dem Ziel-Tag).

Fertig, wenn feststeht, welcher vorhandene Pfad den Wechsel ausrollt, wer ihn aktiviert, welche Kopien dafür aktualisiert sein müssen und wie er global pausiert wird.

**Bereitstellung** eines neuen Dienstes folgt dem Infra-Bestand: VM über den vorhandenen Provisionierungspfad mit geprüfter Adresse, Konfiguration über Ansible bzw. versionierte Release-/Profildateien, getrennte Staging- und Prod-Instanz, Image per Digest, Plan vor Apply, Kapazitätsmessung mit synthetischen Daten, Eintrag in Inventar und Wissensbasis. Einzelheiten liefern Monorepo (`docs/PROXMOX_SETUP.md`, `infra/playbooks/`) und das Runbook des Vorbilddienstes.

## 4. Identität

- **Eine eigene Identität je Instanz und Zweck** (z. B. mTLS-Clientzertifikat mit CN = Slug, Virtual Key `<slug>-g<n>`, registrierter Signer). Nie zwischen Instanzen kopieren, nie einen gemeinsamen Flotten-Schlüssel in Instanz-Bundles legen.
- **Getrennte Vertrauensbereiche** für Staging und Prod. Eine fremde, Staging- oder defekte Identität wird nicht still ersetzt: abbrechen und entscheiden lassen (bereinigen oder Hold).
- **Vorhandenes zuerst:** Wiederverwenden nur nach Prüfung von Eigentum (Instanzfeld, Schlüsselpaar, Kette gegen die richtige CA bzw. Team/Key-Bindung). „Fehlt“ nur bei bestätigtem Not-Found; Netz- oder Rechtefehler brechen ab.
- **Laufzeit und Widerruf** benennen: Ablauf, wer erneuert, ob ein Ausbau die Identität widerruft. Fehlt ein Ablaufalarm, steht das im Bericht.
- Kennt der Zieldienst keine Mandantenidentität (z. B. Docling mit einem gemeinsamen `X-Api-Key`), darf nur ein vertrauenswürdiges actaOne-Backend zugreifen; der Mandant wird aus der actaOne-Identität abgeleitet, nie vom Client übernommen.

Schlüssel und Zertifikate nur als `0600`-Dateien in `mktemp -d`, nach Gebrauch `shred`; nie in Chat, Log, KB oder PR.

## 5. Anbindung

Vor dem ersten Canary aus jedem betroffenen Kundennetz belegen, idealerweise aus einem echten API-Container: Erreichbarkeit, TLS mit Servername und richtiger CA, Ablehnung ohne bzw. mit fremder Identität, Firewall auf erlaubte Netze. Dazu: Kapazität und Limits des gemeinsamen Dienstes gegen die erwartete Last der geplanten Welle, Single-Point-of-Failure (HA-Eintrag, Backup/Restore, Monitoring) als Befund. Fehlendes Monitoring blockiert nicht automatisch, wird aber vor Wellen als Risiko gemeldet.

Fertig, wenn je Kundennetz eine Probe mit Zeitpunkt vorliegt und die Kapazitätsannahme der Welle benannt ist.

## 6. Persistente Konfiguration

- **Vault-first.** Der Wechsel steht im Instanz-Bundle (bzw. erst nach Canary in `customer-defaults`). Live-`docker service update` überlebt keinen Redeploy und zählt nicht.
- Nur die Zielzeilen ändern; alle anderen Zeilen bleiben bytegleich (Image-Pins, Credentials, Hotfix-Tags). Manifest- und Teilversionen des Ausgangs-Bundles erfassen und den Rückweg über Vault-Versionen festlegen; keine dauerhafte lokale Klartextkopie als Backup anlegen. Vor Publish konkurrierende Änderungen an allen Teilen ausschließen; vorbereitete Dateien nicht über bestehende schreiben.
- Publish → Readback → Inhaltsvergleich, danach Deploy über den gewählten Pfad. Vor einem späteren Publish Input und Live-Stand erneut abgleichen.
- Defaults-Änderungen starten keinen Fleet-Job und migrieren keine expliziten Instanz-Pins; der Backfill im Promote kann aber fehlende Werte nachziehen. Das vorher prüfen.
- Alte lokale Dienste entfernt erst der Renderer nach allen Deploy-Gates, nie `--prune` oder Handarbeit.

## 7. Begrenzter Canary und Wellen

1. **Zielliste einfrieren** aus einer read-only Inventur (laufende Services, Vault-Bundles, nicht erreichbare Kontexte getrennt ausweisen). Hotfix-Tags und Sonderwege je Ziel sichern.
2. **Interne Canary** → kleine Kundenwelle → weitere ausdrücklich benannte Wellen. Eine Entscheidung „alle in einem Release“ trifft der Nutzer; sie wird mit ihrer Kapazitätsannahme dokumentiert.
3. **Fachliche Abnahme je Ziel**, nicht nur Health: echter Nutzerpfad durch die Instanz, Mandantentrennung, Altbestand (alte Dateien/Sessions/Indizes weiter nutzbar), Kostenbuchung bei der richtigen Instanz, Fehlerquote am Dienst (z. B. 429/5xx je Client).
4. **Stopp beim ersten Fehler** eines Ziels: keine weitere Welle starten. Ein bereits laufender Flottenjob kann nach Fehlern weiterlaufen; dessen tatsächlichen Fortschritt feststellen und den unterstützten Pause-/Abbruchweg verwenden. Teilzustand prüfen und den vereinbarten Rückweg nur bei passenden Voraussetzungen anwenden, dann dieselben Prüfungen wiederholen. Kein blindes Rollback bei unklarem Datenzustand.

Ein grüner Canary sagt nichts über nicht erreichbare oder gestoppte Instanzen; diese bleiben als offen im Bericht.

## 8. Rückweg

Vor der ersten Umstellung festlegen und, wo möglich, am Canary erproben:

- **Je Instanz:** gesicherter Vorzustand oder Hold-Schalter plus alter Modus im Bundle, Publish/Readback, regulär redeployen. Ohne Hold stellt der nächste Promote wieder um.
- **Global:** Manifest auf `manual`, Defaults zurück. Das routet bereits migrierte Instanzen nicht zurück.
- **Dienst selbst:** vorherige Release-/Profildatei mit dem damaligen Quellstand.
- **Daten:** Ein URL-Rückweg transportiert neu entstandene Daten nicht zurück. Alter und neuer Datenbestand bleiben erhalten, bis der Wiederzugriff nachgewiesen ist.

Der alte Dienst muss weiterlaufen, solange ein Rückweg auf ihn zeigt.

## 9. Abschalten alter Ressourcen

Zwei Fälle trennen:

- **Instanzlokale Altdienste**, deren Entfernung Teil des beauftragten Migrationsvertrags ist (z. B. lokale Presidio-Analyzer nach `PRESIDIO_KEEP_LOCAL=false`), entfernt der Renderer derselben Instanz nach allen Gates. Das ist Teil der Umstellung, kein eigener Abschaltauftrag.
- **Gemeinsame Altressourcen** (alter Pool, Unit, Singleton, VM) nur mit eigenem Auftrag, der die Ressource nennt, und erst nach nachgewiesenem **Verkehrswechsel**. Pool und VM getrennt betrachten: Ein leerer Pool belegt keine ungenutzte VM. Prüfungen und Befehlsmuster: [references/verkehrsnachweis.md](references/verkehrsnachweis.md).

Nachgewiesen ist der Wechsel, wenn alle vier Listen leer sind und ihr Zeitpunkt feststeht:

1. laufende Service-Spezifikationen aller Kontexte (inkl. Staging, Benchmark, Branch, Render-Lab, Partner),
2. Vault-Bundles beider Umgebungen und beide `customer-defaults`,
3. Verbindungen am alten Endpunkt, zweimal im Abstand von Minuten, auch im Netz-Namespace des Containers,
4. nicht erreichbare Kontexte und nicht ladbare Bundles, jeweils geklärt.

Dann schrittweise und umkehrbar abschalten: Restart-Policy und Autostart (Unit) zuerst, dann stoppen. Daten, Volumes, Images und Identitäten bleiben, bis Löschen gesondert beauftragt ist. Eine VM zu löschen ist ein eigener Auftrag nach Ablauf des Rückwegfensters.

## 10. Bericht

Phase und Zielumfang, gewählter Rollout-Weg, je Ziel: Identität (geprüft/neu, Ablauf), Anbindung, Vault-Version vorher/nachher, Abnahmeergebnis, Rückweg. Bei Abschaltung die vier Nachweislisten mit Zeitpunkt. Ausdrücklich nicht geprüft: nicht erreichbare Instanzen, Last, HA, Monitoring. Quellenstand (Repo-Commit, Notizdatum). Herkunft der Skillinhalte: [references/sources.md](references/sources.md).
