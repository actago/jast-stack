# Herkunft und lokale Änderungen

Vollständiger lokaler Snapshot des synchronisierten Claude-Skills `pptx` aus dem aktiven Profil `.claude-jast` (Sync-Ordner `2fb35048-…_f77e4d1d-…`), 17.11.2026. Laut Sync-Manifest Quelle `anthropic`, Stand `2026-11-16T17:00:22Z`. Alle 58 Quelldateien einschließlich Hilfsskripten, OOXML-Schemas und `LICENSE.txt` übernommen; keine Cache- oder versteckten Dateien vorhanden. Dateihashes des unveränderten Ausgangsstands: [source-manifest.json](source-manifest.json).

## Lizenz

Apache-2.0 laut mitgelieferter `LICENSE.txt` (bytegleich mit `docx`/`xlsx`); Frontmatter-Feld `license` erhalten. Eine `NOTICE`-Datei liegt der Quelle nicht bei, ein Copyright-Vermerk ist im Snapshot nicht enthalten. Ein Upstream-Repository oder -Commit ist aus dem Snapshot nicht belegt. Die mitgelieferten XSD-Schemas (ECMA-376/ISO-IEC 29500, Microsoft-Erweiterungen) tragen keine eigenen Lizenzhinweise im Ordner; ihre Weitergabebedingungen sind nicht gesondert geprüft.

## Gemeinsamer Code

`scripts/office/` ist bytegleich in `docx`, `pptx` und `xlsx` enthalten. Jeder Ordner behält seine Kopie, damit er einzeln nutzbar bleibt; Updates müssen in allen drei Ordnern nachgezogen werden.

## JAST-Änderungen (nur `SKILL.md`)

- Einleitender Absatz „JAST adaptation“: Abhängigkeiten prüfen, Plattformhinweis, belegte CI-/Vorlagenquellen statt erfundener Gestaltung, optionaler Verweis auf `actaone-documents`.
- Zusage „`pptxgenjs` / `react-icons`, `react`, `react-dom`, `sharp` preinstalled“ ersetzt: Die Vorinstallation gilt nur für die Anthropic-Ausführungsumgebung und ist hier unbelegt.
- Skripttabelle: „bare `soffice` hangs in this sandbox“ durch die tatsächliche Wirkung von `soffice.py` ersetzt (temporäres Profil, `LD_PRELOAD`-Shim per `gcc` nur bei blockierten AF_UNIX-Sockets).
- Abschnitt „Dependencies“: Plattformgrenzen (natives Windows, PowerShell) und Verbot unbelegter Render-/Kompatibilitätsaussagen ergänzt.

Alle übrigen fachlichen Regeln (Gotchas, Design, QA) bleiben wörtlich. Skripte wurden weder verändert noch ausgeführt.

## Offene Punkte

- `scripts/office/soffice.py` prüft `socket.AF_UNIX`; auf nativem Windows-Python ohne dieses Attribut ist das Verhalten ungetestet. Der Shim setzt Linux und `gcc` voraus.
- Kein Render-, PowerPoint- oder LibreOffice-Test durchgeführt; keine Ausgabedatei erzeugt.

## Aktualisierung

Neuen Sync-Stand gegen `source-manifest.json` vergleichen, unveränderte Dateien übernehmen, die oben genannten `SKILL.md`-Änderungen neu anwenden und das Manifest neu erzeugen.
