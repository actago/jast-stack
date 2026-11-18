# von git-änderungen zum testplan

## änderungen nachvollziehen

1. Checkout am Remote identifizieren; Commit, Branch und lokale Abweichungen erfassen. Fehlende Referenzen gezielt über den bekannten Remote nachladen, ohne fremde Worktrees zurückzusetzen.
2. Pro Komponente Basis und Ziel auf vollständige Commit-IDs auflösen. Registry/Candidate-`sourceRevisions` bevorzugen; kurze SHAs im Release-Tag nur eindeutig auflösen, nicht erraten. Die beteiligten Repos können LibreChat, KB_RAG und Presidio sowie separat actaOne für Deploy-Verhalten sein.
3. Historie erklärt die Absicht, Diff und aktueller Code die tatsächliche Änderung:

```bash
git -C <repo> rev-parse --verify '<basis>^{commit}'
git -C <repo> rev-parse --verify '<ziel>^{commit}'
git -C <repo> log --format='%h %s' <basis>..<ziel>
git -C <repo> diff --name-status <basis> <ziel>
git -C <repo> diff <basis> <ziel> -- <relevanter-pfad>
```

4. Merge-Commits, Reverts und Hotfix-Cherry-Picks einordnen. Bei divergierenden Basen den beabsichtigten Vergleich erklären; `A..B` allein zählt keine tatsächlich ausgelieferten Features. Neue Features, Fixes, entfernte Funktionen, Migrationen und Konfigurationsänderungen erfassen. Reine Dokumentänderungen brauchen keinen erfundenen Laufzeittest.
5. Für actaOne den früher tatsächlich angewendeten Checkout/Template-Stand mit dem jetzt vom Worker verwendeten Stand vergleichen. Release-Tags enthalten diesen Infra-Stand nicht. Ist die frühere Revision unbekannt, aktive Konfiguration gegen belegten Sollzustand prüfen und die historische Lücke nennen. Nicht einfach „letzte zehn Commits“ verwenden.

## aktivierungskette pro feature

Vom Code bis zur konkreten Instanz verfolgen:

`code/artefakt → verfügbare fähigkeit → template/override → renderer/nachbearbeitung → vault/defaults/holds → redeploy/migration → wirksame runtime → funktion`

Dateien und relevante Schlüssel mit Version nennen, Secretwerte nicht kopieren. Im actaOne-Stand vom 13.11. sind insbesondere `deploy/templates/`, `scripts/deploy-customer.sh`, `customer-release-features.py`, `customer-release-env.py`, `promote.sh` und die dienstspezifischen Release-Migrationen relevant. Den aktuellen Code lesen: Profilauswahl, Default-Backfill und Nachbearbeitung können den Templatewert verändern oder bewusst erhalten. Ein Key in der Vorlage beweist weder seine Präsenz noch Wirkung auf einer Instanz.

Jeder Fähigkeit einen Sollzustand geben: aktiv, bewusst deaktiviert, nicht anwendbar oder ungeklärt. Feature-Schalter nicht pauschal aktivieren. Slug-Overrides können das Standardtemplate vollständig ersetzen; zusätzliche Renderer müssen trotzdem berücksichtigt werden.

## plan vor dem apply festhalten

Im autorisierten Arbeitsordner einen Run-Nachweis führen. Bei langen Vorhaben denselben Postplan fortschreiben, vertrauliche Details lokal lassen. Mindestfelder:

| feld | inhalt |
| --- | --- |
| lauf | auftrag, zeitfenster, testziel/zielliste, jobkennung |
| revisionen | basis und ziel je repo, image-tag/digest, wirksamer infra-/template-stand |
| änderung | feature/fix-id, commit/diff und beobachtbare verhaltensänderung |
| aktivierung | profil, schlüsselname, dauerhafte quelle, migration, voraussetzungen und reihenfolge |
| prüfung | vorbedingung, konkrete schritte, erwartetes ergebnis, testkonto/datenklasse |
| abdeckung | alle ziele oder benannte stichprobe mit begründung; ausgeschlossene fälle |
| nachweis | vorher/nachher, zeit, tatsächliches ziel, beobachtetes ergebnis, redigierter beleg |
| status | geplant, bestanden, fehlgeschlagen, blockiert, nicht anwendbar; jeweils grund |
| rückweg | vorheriger image-/konfigurationsstand, migrationsgrenzen, erlaubte maßnahme |

Keine Sammlung unbestimmter Checks wie „UI testen“. Beispiel eines **synthetischen** Features: „Dokumentexport neu“ → erforderliches Image und Template-Schlüssel im Diff finden → wirksame Aktivierung am Ziel nachweisen → mit Testkonto ein neutrales Dokument erzeugen → Download öffnen, Inhalt und relevante Darstellung prüfen → Testobjekt nur im erlaubten Testbereich bereinigen. Health allein wäre hierfür unzureichend.

Weitere Muster: Modellaufnahme → Anzeige und tatsächlicher synthetischer Aufruf; Suche → Suche/Scrape/Rerank getrennt und Ergebnisquellen; Rechteänderung → erlaubte und abgewiesene Aktion mit passenden Testrollen. Tests nur wählen, wenn die Änderung sie betrifft; erforderliche Schreib-/Kostenwirkung vorher im Testumfang benennen.

## nach deploy beweisen

Konfiguration feldbegrenzt oder als Hash prüfen. Kein ungefiltertes `docker service inspect`, keine kompletten Envs, Tokens oder Kundenlogs in den Nachweis. Runtime-Werte erst nach abgeschlossener Aktualisierung lesen; Test und Nachweis bleiben an Tag/Digest und Zeitpunkt gebunden. `bestanden` darf nicht auf einen neueren Kandidaten übertragen werden.

Bei neuem Commit, Template-Nachzug, Konfigurationsänderung oder Retry den betroffenen Plananteil und die Regressionen erneut prüfen. Ist die Auswirkung unbekannt, die frühere grüne Abnahme nicht als weiterhin gültig behandeln.
