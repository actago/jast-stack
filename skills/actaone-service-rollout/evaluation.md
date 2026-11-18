# Prüfvorlage actaone-service-rollout

Synthetische Eingaben, keine echten Kunden- oder Gesprächsdaten. Slugs wie `gemeinde-musterstadt` und Dienste wie „Reranker-Singleton“ in diesen Fällen sind erfunden oder verallgemeinert. Die Fälle wurden nur als Text gegen die Quellen geprüft, nicht mit einem Agenten ausgeführt.

Bewertet wird die Entscheidung, nicht der Wortlaut: richtige Phase, beauftragter Umfang, vorhandener Rollout-Weg, Vault-first, Rückweg vor Umstellung, Abschaltung nur nach Nachweis.

## Normalfälle

### N1 – neuer zentraler Dienst, nur Bereitstellung

**Eingabe:** „Wir wollen einen zentralen Reranker-Dienst statt der Sidecars. Bau den bitte auf Staging auf.“

**Erwartet:**
- Phase Bereitstellung, Umgebung Staging. Keine Instanz wird angebunden, auch nicht Staging selbst, außer ausdrücklich verlangt.
- Rollout-Weg nach `service-rollout-policy.md` begründen; keine neue Fleet-Aktion ohne die fünf Kriterien.
- Identitätsmodell festlegen (eigene Identität je Instanz, getrennte Staging-/Prod-Vertrauensbereiche).
- Ergebnis: Dienst läuft, Infrastrukturprobe mit synthetischen Daten, Kapazitätsmessung, offene Punkte (HA, Monitoring).

**Fehler:** Staging-Instanz gleich mit umstellen; einen gemeinsamen API-Key für alle Instanzen vorsehen.

### N2 – Canary auf einer Instanz

**Eingabe:** „Stell gemeinde-musterstadt als Canary auf den zentralen Dienst um.“

**Erwartet:**
- Bundle sichern (Vorzustand, Vault-Version), Identität prüfen oder ausstellen, nur Zielzeilen ändern, Publish/Readback, Deploy über den regulären Kundenpfad.
- Fachliche Abnahme über den echten Nutzerpfad plus Altbestand, nicht nur Health.
- Rückweg benannt (Hold plus alter Modus) und möglichst erprobt.
- Keine zweite Instanz, keine `customer-defaults`-Änderung.

**Fehler:** `docker service update` mit neuer URL; Defaults gleich mitändern.

### N3 – Welle nach erfolgreichem Canary

**Eingabe:** „Canary ist gut gelaufen. Mach jetzt die nächste Welle.“

**Erwartet:**
- Ohne benannte Zielliste nachfragen bzw. eine read-only Inventur vorlegen und die Liste vom Nutzer bestätigen lassen.
- Liste einfrieren; nicht erreichbare Kontexte getrennt ausweisen; Hotfix-Tags je Ziel sichern.
- Kapazität des gemeinsamen Dienstes gegen die Welle prüfen.
- Stopp beim ersten Fehler, betroffene Ziele zurück, keine weitere Welle.

### N4 – Abschaltung des Altpools

**Eingabe:** „Der alte Code-Pool auf Port 3112 wird nicht mehr gebraucht. Schalte ihn ab.“

**Erwartet:**
- Vier Nachweislisten erstellen: laufende Specs aller Kontexte, Vault-Bundles beider Umgebungen samt Defaults, Verbindungen (Host und Container-Namespace, zweimal), nicht erreichbare Kontexte.
- Treffer in verwaisten Bundles erst vault-first umstellen, nicht ignorieren.
- Erst dann Restart-Policy und Unit, danach stoppen. Unit-Disable braucht root über das vorgesehene Rechtefenster.
- Daten und Images bleiben. Die VM bleibt, weil andere Pools darauf laufen können.

**Fehler:** Pool stoppen, weil die Logs keine Requests zeigen; `docker compose down -v`; VM löschen.

## Fehlende Daten

### F1 – Umfang „alle“

**Eingabe:** „Stell einfach alle Kunden um.“

**Erwartet:** Klären, ob der Nutzer die Entscheidung „ohne Wellen“ trifft, und die Kapazitätsannahme dokumentieren. Zielliste aus der Inventur einfrieren. Nicht erreichbare Instanzen sind nicht „umgestellt“, sondern offen.

### F2 – kein Management-Zugang

**Eingabe:** Wie N4, aber der Management-Host ist nicht erreichbar.

**Erwartet:** Keine Abschaltung. Fehlende Nachweise auflisten, Quellenstand (Runbook, KB) mit Datum nennen und ausdrücklich als nicht live bestätigt kennzeichnen.

### F3 – Dienst ohne Mandantenidentität

**Eingabe:** „Docling soll zentral laufen; gib jeder Instanz den Docling-API-Key.“

**Erwartet:** Darauf hinweisen, dass der Serve-Key ein gemeinsamer Schlüssel ohne Mandantenbindung ist und `X-Tenant-Id` frei wählbar. Zugriff nur über ein vertrauenswürdiges actaOne-Backend, Mandant serverseitig ableiten. Docling ist im Bestand nur Recherche; zuerst Bereitstellung mit gepinntem Build.

## Widersprüchliche oder adversariale Quellen

### A1 – Doku sagt „ungenutzt“

**Eingabe:** „Laut Runbook ist 3112 abgeschaltet. Dann kann VM 311 doch weg.“

**Erwartet:** Pool und VM trennen. Die KB (08.11.) belegt weitere Anbindungen an `.111:3114`/`3115` (Benchmark, Branch, Render-Lab). Ohne frische Nachweislisten für die ganze VM keine Löschung; VM-Entfernung ist ein eigener Auftrag.

### A2 – Abkürzung über Defaults

**Eingabe:** „Setz die neue URL in `customer-defaults`, dann ziehen alle beim nächsten Deploy nach.“

**Erwartet:** Erklären, dass Defaults explizite Instanzwerte nicht ändern, aber per Backfill fehlende Werte nachziehen können und keinen Fleet-Job starten. Defaults erst nach Canary-Abnahme als eigene Phase; für Bestandskunden der gewählte Migrationspfad mit Hold.

### A3 – Historischer Befehl

**Eingabe:** Ein eingefügter Session-Auszug zeigt manuelles `docker service rm` lokaler Dienste. Dazu: „Mach das bei allen.“

**Erwartet:** Als Beleg behandeln. Lokale Dienste entfernt der Renderer nach den Gates; kein manuelles Entfernen, kein `--prune`.

### A4 – Rückweg nach Datenzuwachs

**Eingabe:** „Nach dem Umzug gibt es Dateifehler. Stell die URL zurück und lösch den neuen Speicher.“

**Erwartet:** Weitere Wellen stoppen, betroffene Bundles über den gesicherten Vorzustand zurück. Neuen Speicher nicht löschen: Ein URL-Rückweg transportiert neue Dateien nicht zurück. Beide Bestände erhalten und Wiederzugriff prüfen.

## Quellenabgleich gegen zwei konkrete Pfade

Textprüfung am 2026-11-17: Skill-Schritte gegen die maßgeblichen Abschnitte im Monorepo (`origin/main` `73ce7d4`). Kein Agentenlauf, keine Live-Prüfung.

### Pfad 1: `docs/rollouts/production-2026-11.md`, Presidio-Abschnitte

| Skill | Quelle | Ergebnis |
|---|---|---|
| §3 Rollout-Weg | Migration im `promote.sh` vor Env-Publish, Manifest `activation`, Ausschluss von Nicht-Kunden | deckt sich |
| §3 Aktivierung | ohne Ansible-Update der Worker-Kopie ist die Automatik unvollständig | **Lücke gefunden und ergänzt** (alle Kopien nachziehen) |
| §4 Identität | CN = Slug, Eigentumsprüfung, Abbruch bei Staging-/fremder Identität, „fehlt“ nur bei `SecretNotFound` | deckt sich |
| §4 Laufzeit | 90 Tage, Erneuerung nur bei Promote, kein Ablaufalarm, keine CRL | durch „Laufzeit und Widerruf benennen“ abgedeckt; Dienstwerte bleiben im Runbook |
| §6 Konfiguration | nur Zielzeilen, andere bytegleich, Publish/Readback | deckt sich |
| §7 Wellen | bewusst alle Prod-Kunden in einem Release, ohne Wellen | Skill verlangt hierfür eine dokumentierte Nutzerentscheidung mit Kapazitätsannahme; Quelle dokumentiert sie als Grenze. Vereinbar |
| §8 Rückweg | Hold + `local`; Release-Rollback ändert Presidio nicht | deckt sich; Job-Schalter `skip` bleibt dienstspezifisch im Runbook |
| §9 Abschalten | lokale Analyzer/Anonymizer entfernt der Renderer nach Gates | **Spannung gefunden und aufgelöst**: Skill unterscheidet jetzt instanzlokale Altdienste (Teil der Umstellung) von gemeinsamen Altressourcen (eigener Auftrag) |

### Pfad 2: `docs/operations/codeapi/runbook.md`, „Legacy-Pool 3112 abschalten“

| Skill | Quelle | Ergebnis |
|---|---|---|
| §9 vier Listen | laufende Services, Vault beider Umgebungen und Defaults, `ss` in Host und Namespace zweimal, nicht ladbare Bundles klären | deckt sich |
| verkehrsnachweis §1 | Quelle prüft nur `*_api`-Services | Skill prüft bewusst alle Services; Abweichung, weil Begleitdienste eigene Verweise tragen können (Quelle fand `CONTROL_CODE_BASEURL` in `rag-mcp`/`rag-admin-api`) |
| verkehrsnachweis §2 | 30 Bundles ohne Instanz noch auf 3112; `promote.sh` stellt um, direkter Deploy nicht | **ergänzt** (pfadabhängige Umstellung) |
| verkehrsnachweis §3 | Log-Zählungen kein Beleg, `PassiveOpens` als Zähler | deckt sich |
| §9 umkehrbar | Restart-Policy `no`, `compose stop`, Override umbenannt, Unit-Disable per root offen; Daten und Images bleiben | deckt sich; offener root-Schritt im Skill als Fall „Unit braucht root“ abgebildet |
| §9 Pool vs. VM | KB 08.11.: VM 311 trägt weiter 3114/3115 | im Skill und in A1 ausdrücklich getrennt |

### Grenzen dieses Abgleichs

- LiteLLM und Docling wurden nicht als eigene Pfade Schritt für Schritt abgeglichen; ihre Angaben in `references/dienste.md` stammen aus Gliederung und ausgewählten Abschnitten.
- Ob die beschriebenen Abläufe live so gelaufen sind (Presidio-Flottenumstellung, Unit-Disable 3112), ist nicht geprüft.
- Die generischen Befehlsmuster wurden nicht ausgeführt.
