# Session-Harvest

Zusammengeführt aus `vault-refresh` Schritt 2b, `actaone-harvest` und `Vault-Pflege.md` (Harvest-Methode, Quellen-Nachträge 11.09. und 08.11.2026).

## Quellen bestimmen

- Codex und T3 (Codex-Sessions): `00 Meta/harvest-codex.ps1` listet Sessions seit dem eigenen Marker (`harvest-state-<Kürzel>.json`). Der Vorfilter (Arbeitsverzeichnis, Keywords) liefert nur Kandidaten.
- Claude-Verläufe separat sammeln: Projektverläufe aller verwendeten Claude-Profile (z. B. `~/.claude/projects` **und** zusätzliche Profile wie `~/.claude-jast/projects`), Änderungsdatum nach dem Marker. T3 nutzt auch Claude; Codex-JSONL allein deckt T3 nicht ab.
- Hermes-Verläufe sind nicht harvestbar; nur manuell.
- Automatische Session-Spiegel einzelner Teammitglieder (z. B. Auto-Harvest-Notizen mit `status/pruefen`) sind Rohmaterial, keine destillierten oder geprüften Fakten.

## Destillieren

1. Rohdateien nie vollständig lesen (bis über 200 MB). `python "00 Meta/harvest-extract.py" <datei> --since <Stichtag>` streamt Meta, Nutzeranliegen und Abschlussantworten ohne Tool-Ausgaben.
2. Bei vielen Sessions nach Tagen gruppieren; parallele Helfer liefern nur Textberichte und schreiben keine Dateien.
3. PR-Aussagen gegen GitHub, Release-Aussagen gegen die Stable-Registry, Codeaussagen gegen den Code prüfen. Audit- oder Harvest-Sessions bestätigen ihre eigenen Aussagen nicht.
4. Belegte, wiederverwendbare Fakten in `10 actaOne/`-Referenzen, `Offene Baustellen`, `Gelöst-Log`; eigene Arbeitsnotizen in den eigenen Bereich. Unbestätigte Vorschläge als ☐ in `10 actaOne/Harvest-Draft YYYY-MM-DD.md` mit Quelle und offenem Prüfpunkt. Gefundene Geheimnisse nie übernehmen.
5. Substanzielles Wissen ggf. zusätzlich als Memory in der Quelle, dann Mapping und Sync wie beim Statusabgleich.

## Marker setzen

`harvest-codex.ps1 -MarkDone` erst, wenn alle ausgewählten Sessions verarbeitet sind; bei Inventur bis zu einem Stichtag `-MarkDone -Through <Datum>`. Teil- oder Themenabgleiche verschieben den Marker nicht und werden in `Vault-Pflege.md` bzw. einer Harvest-Notiz als solche benannt. Danach `-Check`, Linkprüfung und `git diff`; im Bericht verarbeitete Quellen und offene Prüfungen nennen.
