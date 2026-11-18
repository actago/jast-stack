# Prüffälle

Synthetische Textszenarien, nicht ausgeführt.

- Nutzer verlangt „eine Präsentation“ ohne Format, Slide-Artifact verfügbar: Artifact/Slides-Skill vorziehen; `.pptx` nur bei ausdrücklichem Format oder vorhandener Datei.
- Bestehende Firmenvorlage befüllen: `thumbnail.py` mit eigenem Präfix, Strukturänderungen vor Inhalt, `validate.py --original`, Platzhalterreste prüfen, jede Folie rendern.
- `pptxgenjs` fehlt im Projekt: isolierte Arbeitsumgebung statt fremder Projektabhängigkeiten; keine Vorinstallation unterstellen.
- Natives Windows ohne `soffice` im `PATH`: fehlende Voraussetzung benennen, keinen Visual-QA-Erfolg behaupten; WSL/Container vorschlagen.
- Kombidiagramm mit Sekundärachse: `valAxes` und `catAxes` je zweifach, danach `validate.py`.
