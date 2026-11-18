# Bestandsaufnahme

Aktueller Gesamtstand: **49 Skills**, alle strukturell geprüft. Ältere Zählungen unten dokumentieren frühere Übernahmestufen. Die vollständige Verfügbarkeit hängt von den pro Skill genannten Tools, Modellen und externen Arbeitsordnern ab.

## Zoho und Postplan

- [actaone-zoho-desk](skills/actaone-zoho-desk/SKILL.md): actaOne-Abteilungsgrenze auch bei unbekannten Ticket-IDs, Triagieren, interne Antwortentwürfe statt Kundenmail, bedarfsweiser Postplan.
- [actaone-zoho-projects](skills/actaone-zoho-projects/SKILL.md): Portal-/Projektzuordnung, korrekte Filter/Status-/Ownerformen, Änderungsvorschau, keine Löschung, bedarfsweiser Postplan.

Beide am 17.11.2026 aus Teamregeln und tatsächlich verfügbaren MCP-Schemas erstellt. Zoho bleibt maßgeblich für operative Datensätze; Postplan ist keine automatisch synchronisierte oder als vertraulich belegte Kopie. Keine Live-Abnahme, kein Zugriff auf Ticket-/Aufgabeninhalte während der Erstellung.

## Abgeschlossene Übernahme weiterer Skills

[pptx](skills/pptx/SKILL.md) und [xlsx](skills/xlsx/SKILL.md) sind vollständig übernommen und strukturell geprüft. Quelle: synchronisierter Anthropic-Bestand, Stand 16.11.2026, Apache-2.0-Lizenzdateien erhalten. Alle 27 Ergänzungen der [dritten Ausbaustufe](research/third-wave-integration.md) sind integriert, einschließlich 22 Engineering-Skills und der drei eigenen Abläufe für Release Notes, Trailer und Webhook. Praktische Ausführung und gesonderte XSD-Lizenzprüfung stehen aus. Folgende ältere Zahlen beschreiben vorherige Meilensteine.

## Dokumente und CI-PDFs

Jetzt enthalten: [actaone-documents](skills/actaone-documents/SKILL.md) als gemeinsamer CI-/Abnahmeablauf sowie die vollständigen [docx](skills/docx/SKILL.md)- und [pdf](skills/pdf/SKILL.md)-Ordner aus dem synchronisierten Claude-Bestand, mit Apache-2.0-Lizenzen und SHA-256-Quellmanifesten. Insgesamt 20 Skills. Aktive Installationen unverändert. Konkrete CI-Assets und Vorlagen sind noch nicht identifiziert; der Ablauf erfindet keine Markenwerte.

Der vorhandene `docs`-Skill ist nur ein Claude-Connector-Einstieg. Statt diese Laufzeitabhängigkeit vorauszusetzen, entscheidet `actaone-documents` anhand des gewünschten Formats und verfügbarer Werkzeuge. Word-/PDF-Hilfsskripte übernommen, aber nicht ausgeführt; Strukturprüfung ist keine Renderabnahme.

## Zweite Ausbaustufe

Ergänzung: [postplan](skills/postplan/SKILL.md) entwickelt den vorhandenen Hermes-Skill zum dauerhaft gepflegten Projekttracker weiter. Ein Artefakt pro größerem Vorhaben, Fortschreibung derselben URL und belegte Statusübergänge. Nutzerbeispiel gelesen; kein Upload oder Update ausgeführt. Insgesamt jetzt 17 Skills.

Auch [zentraler Service-Rollout](skills/actaone-service-rollout/SKILL.md) ist ausgearbeitet. Die Integration präzisiert bestehende Auftragsfreigaben, Teilfehler laufender Flottenjobs und den Unterschied zwischen Wiederanlauf und Redeploy. Abschaltung benötigt Belege sowohl aus Runtime als auch aus persistenter Konfiguration.

Fertig ausgearbeitet: [Kundenanlage](skills/actaone-provision-customer/SKILL.md) und [Wissenspflege](skills/actaone-kb-maintenance/SKILL.md). Quellen- und Strukturprüfung, keine Live-Abnahme. Vor späterer Installation den vorhandenen Projektskill `provision-customer` bzw. das vom Vault-Setup installierte `vault-refresh` auf Überschneidungen prüfen; aktive Installationen bleiben unverändert.

[actaone-vm-lifecycle](skills/actaone-vm-lifecycle/SKILL.md) ergänzt die Übergangsprüfungen zwischen Release, Instanzbetrieb und Abbau. [Benchmarks](skills/actaone-benchmarks/SKILL.md) und [Nutzungsauswertung](skills/actaone-usage-analysis/SKILL.md) sind ebenfalls integriert. Damit umfasst die Sammlung 16 Skills. Die sechs Ergänzungen sind quellengeprüfte Entwürfe mit synthetischen Fällen, noch ohne unabhängige Verhaltensprüfung oder Live-Abnahme; siehe [Integrationsstand](research/second-wave-integration.md).

## Aus dem Bestand ausgearbeitete erste Sammlung

Die [README](README.md#erste-sammlung) erschließt zehn Skill-Ordner. `cut-release`, `diagnose-instance`, `keyvault-edit` und `sudo-window` entwickeln vorhandene gleichnamige Skills weiter. `actaone-infra`, `actaone-ansible`, `actaone-presidio` und `actaone-websearch` erschließen vorhandene Agentenprofile und Betriebswissen. `actaone-local-dev` und `actaone-litellm` bündeln die in Sessions und Quellrepos belegten Abläufe. Herkunft und Grenzen stehen je Skill in `references/sources.md`.

Die nachfolgende Liste dokumentiert weiterhin den Ausgangsbestand. Aktive Installationen wurden nicht migriert. Engineering-Skills und Office-Snapshots sind inzwischen im Repo enthalten. Die unabhängigen Textprüfungen der ersten zehn Skills sind abgeschlossen; siehe [Korrekturen und Grenzen](research/final-review-resolution.md).

Ergänzung aus der [Session-Auswertung](research/synthesis.md): Neben den zuerst erfassten Standardverzeichnissen ist `~/.claude-jast` ein verwendetes Profil; außerdem existiert `~/.claude-firma`. Profil- und projektspezifische Memories enthalten zusätzliche Abläufe. Die ursprüngliche Inventur deckt diese Quellen nicht vollständig ab.

Stand: 2026-11-17. Grundlage sind lokale Dateien, ausgewählte gelesene Skill-Einstiege und `~/.agents/.skill-lock.json`. Das belegt vorhandene Installationen, nicht Nutzungshäufigkeit oder heutige Funktionstüchtigkeit. `~` bezeichnet das lokale Benutzerverzeichnis.

## actaOne-spezifische Grundlagen

Unter `actaOne/.claude/skills/`:

- `cut-release`: Releases, Staging, Stable und Promotion.
- `diagnose-instance`: Instanz- und Pipeline-Diagnose.
- `keyvault-edit`: Konfiguration und Secrets über den Vault.
- `provision-customer`: Kundenanlage und Onboarding.
- `benchmark-tweak`: Änderungen an der Benchmark-Instanz.
- `sudo-window`: temporäre administrative Rechte; vor Übernahme auf aktuelle Umgebung und Secret-Übergabe prüfen.

Unter `~/.claude/skills/`:

- `actaone-provisioning-webhook`: Webhook-Vertrag und Integrationen.
- `running-actaone-benchmarks`: Modellvergleiche und Benchmark-Auswertung.
- `making-actaone-feature-trailers`: bestehende Trailer-Produktion, abhängig vom separaten Trailer-Repo und dessen Werkzeugen.
- `vault-refresh`: Aktualisierung der bestehenden Wissensbasis.

Unter `~/.codex/skills/`:

- `obsidian-actaone-kb`: Wissen lesen und pflegen; enthält einen persönlichen absoluten Pfad.
- `hark-notify`: persönliche Benachrichtigungen; auch unter Claude installiert. Persönliches Ziel vor einer Teamübernahme auslagern.

Weitere Kandidaten im actaOne-Repo:

- `agent/hermes/skills/actaone-core`: Plattformwissen und Engineering-/Betriebsregeln mit zwölf referenzierten Themenbereichen.
- `agent/hermes/skills/actaone-release-notes`: Release-Entwürfe mit Quellenbelegen, Zielgruppen und Ausgabeschema; verweist auf `actaone-core`.
- `agent/hermes-skills/postplan`: geprüft und als `skills/postplan` um Projekttracking erweitert; aktive Quelle unverändert.

Die Hermes-Skills sind wegen ihres Entwicklerbezugs Kandidaten. Ihre Laufzeitannahmen müssen vor Übernahme geprüft werden. Der Produkt-Skill `document-generation` wurde gesichtet, gehört aber nicht zum jetzt vereinbarten Umfang.

## Infrastruktur, Ansible und Verbindungen

Die erste Inventur war zu eng auf `SKILL.md` beschränkt. Weitere vorhandene Bausteine:

- `actaOne/.claude/agents/actaone-infra.md`: Agentenprofil mit Ansible-Arbeitsweise, Rollen, Prüfungen, Management-Zugang und Betriebsregeln. Enthält historische Flottenangaben vom 21.07.2026; vor Übernahme mit neueren Quellen abgleichen.
- `actaOne/infra/playbooks/`: tatsächliche Playbooks, darunter `configure-deploy-control-api.yml`, `configure-ops-dashboard.yml`, `configure-webhook-receiver.yml`, `management-vm.yml` und `site.yml`. Rollen, group_vars und `inventory.example.yml` liegen ebenfalls in `infra/`.
- `actaOne/docs/PROXMOX_SETUP.md`: Ansible-Control-Node, SSH-/Docker-Kontext-Einrichtung und Runtime-Identitäten; verweist für konkrete Ansible-/Vault-Kommandos auf `docs/AZURE_KEY_VAULT.md`.
- Bestehende Wissensbasis `~/Obsidian/actaOne-KB/10 actaOne/Infrastruktur (MOC).md`: Navigation zu Topologie, Service-Referenzen, Betriebswissen und Klon-Testumgebung. Ergänzungsdatum 08.11.2026; ältere Abschnitte behalten ihren historischen Stand.
- Dieselbe Wissensbasis: `Klon-Testumgebung pvetest (Referenz)` sowie `Helsinki Clone - Zugang und Mailversand` als Einstieg zu gesonderten Klon-Zugängen. Nicht mit dem Produktionszugang gleichsetzen.
- `ssh acta-mgmt` und Repo `~/actaOne` sind in vorhandenen Agenten-/Skill-Anleitungen dokumentiert. Ein aktueller Verbindungs- oder Berechtigungstest wurde bei dieser Bestandsaufnahme nicht durchgeführt.

Damit gehört zum JAST-Stack auch die gezielte Erschließung bestehender Agentenprofile, Runbooks und MOCs. Ein eigener Ansible-Skill wurde in den bisher geprüften Skill-Verzeichnissen nicht gefunden; Ansible-Wissen ist bereits in diesen Quellen vorhanden.

Umsetzungsnachtrag: Dieses vorhandene Wissen wurde inzwischen in `skills/actaone-ansible` als eigener Ablauf erschlossen. `skills/actaone-infra` führt zu den bestehenden Quellen. Der Befund „kein Ansible-Skill gefunden“ beschreibt den Ausgangsbestand, nicht den heutigen Entwurf.

## Externe Engineering-Grundlage

Die lokalen Installationsmetadaten weisen unter anderem folgende Skills `mattpocock/skills` zu:

- Qualität: `diagnosing-bugs`, `code-review`, `tdd`.
- Planung und Umsetzung: `grilling`, `to-spec`, `to-tickets`, `implement`, `triage`.
- Architektur und Wissen: `codebase-design`, `domain-modeling`, `research`, `writing-for-agents`.

Die 13 übernommenen Engineering-Skills wurden gegen `mattpocock/skills@885e2ca` abgeglichen. MIT-Lizenzen sind je Ordner enthalten, Herkunft und SHA-256-Manifeste dokumentiert. Zusätzlich enthalten ist `resolving-merge-conflicts`; siehe jeweilige `references/sources.md` für Abhängigkeiten und Anpassungen.

Die vorhandene tstack-Gruppe umfasst `full-send`, `full-stop`, `council`, `sol-loop`, `file-pr`, `takeover`, `babysit-pr`, `modernize` und `leaving-pr-comments`. Alle neun sind übernommen; Upstream-Abgleich gegen `t3dotgg/tstack@7de017b`, MIT-Lizenz je Ordner. Lokale PR-Screenshot-Regel und Windows-/POSIX-Sperre von `pr-wait` bleiben erhalten. Die Herkunft des Screenshot-Zusatzes ist nicht über Upstream/Installationsmetadaten belegt.

## Doppelte Installationen

Die Profilkopien der neun tstack-Skills verweisen auf denselben Bestand unter `.agents/skills`. Bei der dritten Übernahme wurden vollständige Ordner und Upstream-Herkunft geprüft. Bei `hark-notify` wurden nur die beiden Einstiegstexte als bytegleich festgestellt; dieser persönliche Skill wurde nicht übernommen.

Ein gemeinsamer Quellbestand mit kontrollierter Installation könnte die parallelen Kopien ersetzen. Die vorhandenen Installationen wurden nicht geändert.

## Vor einer Übernahme klären

- `benchmark-tweak` und `running-actaone-benchmarks`: ergänzende Abläufe oder doppelte Regeln?
- `vault-refresh` und `obsidian-actaone-kb`: gemeinsamer Wissenszugriff mit getrennten Pflegeabläufen?
- `actaone-core` und Runbooks: maßgebliche Quellen oder veraltbare Snapshots?
- Externe Engineering-Skills: welche werden tatsächlich eingesetzt und passen zusammen?
- Persönliche Pfade, Benachrichtigungen und Tools: was gehört zum Entwickler, was zum gemeinsamen Stack?

Nächste Übernahmeeinheit ist jeweils ein bestehender Skill mit allen Ressourcen und belegter Herkunft. Die Bestandsaufnahme ist noch keine validierte Distribution.
