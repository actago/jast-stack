# Herkunft und lokale Änderungen

Vollständiger lokaler Snapshot des synchronisierten Claude-Skills `docx` aus dem aktiven Profil `.claude-jast`, 17.11.2026. Alle 61 Quelldateien einschließlich Hilfsskripten, Schemas und `LICENSE.txt` übernommen. Lizenz: Apache-2.0 laut mitgelieferter Datei; Hinweise in den Quellen erhalten. Ein Upstream-Commit ist aus diesem Snapshot nicht belegt. Dateihashes des unveränderten Ausgangsstands: [source-manifest.json](source-manifest.json).

JAST ändert `SKILL.md`: ausdrücklich gewünschtes Format und bestehende Vorlage gehen Connector-Defaults vor; keine vorausgesetzte Vorinstallation von npm `docx`; Plattform-/Abhängigkeitsprüfung sowie CI- und visuelle Abnahme ergänzen. Diese Herkunftsdatei und `evaluation.md` sind neu. Die übernommenen Skripte wurden nicht verändert oder ausgeführt. Kein Office-/PDF-Rendertest erfolgt.
