# Herkunft und lokale Änderungen

Vollständiger lokaler Snapshot des synchronisierten Claude-Skills `xlsx` aus dem aktiven Profil `.claude-jast` (Sync-Ordner `2fb35048-…_f77e4d1d-…`), 17.11.2026. Laut Sync-Manifest Quelle `anthropic`, Stand `2026-11-16T17:00:22Z`. Alle 53 Quelldateien einschließlich `scripts/recalc.py`, OOXML-Schemas und `LICENSE.txt` übernommen; keine Cache- oder versteckten Dateien vorhanden. Dateihashes des unveränderten Ausgangsstands: [source-manifest.json](source-manifest.json).

## Lizenz

Apache-2.0 laut mitgelieferter `LICENSE.txt` (bytegleich mit `docx`/`pptx`); Frontmatter-Feld `license` erhalten. Eine `NOTICE`-Datei liegt der Quelle nicht bei, ein Copyright-Vermerk ist im Snapshot nicht enthalten. Ein Upstream-Repository oder -Commit ist aus dem Snapshot nicht belegt. Die mitgelieferten XSD-Schemas tragen keine eigenen Lizenzhinweise im Ordner; ihre Weitergabebedingungen sind nicht gesondert geprüft.

## Gemeinsamer Code

`scripts/office/` ist bytegleich in `docx`, `pptx` und `xlsx` enthalten, einschließlich der für `xlsx` ungenutzten PPTX-Helfer und DOCX-Validatoren. Für vollständige Übernahme nicht entfernt; Updates in allen drei Ordnern nachziehen.

## JAST-Änderungen (nur `SKILL.md`)

- Hinweis „`openpyxl`, `pandas`, `markitdown` are preinstalled“ ersetzt durch Verfügbarkeitsprüfung und Installation in Projekt- oder isolierte Umgebung; die Vorinstallation gilt nur für die Anthropic-Ausführungsumgebung und ist hier unbelegt. Dort auch Verweis auf diese Datei, belegte CI-Vorlagen und optional `actaone-documents`.
- Abschnitt „Dependencies“: tatsächliche Wirkung von `soffice.py`, Plattformgrenzen von `recalc.py` (Timeout-Wrapper nur Linux/macOS) und Pflicht, eine nicht gelaufene Neuberechnung offen zu nennen.

Alle übrigen fachlichen Regeln (Ausgabeanforderungen, Recalc, Formelwahl, openpyxl, Finanzmodelle) bleiben wörtlich. Skripte wurden weder verändert noch ausgeführt.

## Offene Punkte

- `scripts/office/soffice.py` prüft `socket.AF_UNIX`; auf nativem Windows-Python ist das Verhalten ungetestet. Der Shim setzt Linux und `gcc` voraus.
- Kein `recalc.py`-Lauf, kein LibreOffice- oder Excel-Test durchgeführt; keine Ausgabedatei erzeugt.

## Aktualisierung

Neuen Sync-Stand gegen `source-manifest.json` vergleichen, unveränderte Dateien übernehmen, die oben genannten `SKILL.md`-Änderungen neu anwenden und das Manifest neu erzeugen.
