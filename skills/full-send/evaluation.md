# Prüffälle

Synthetische Textszenarien, nicht ausgeführt. Geprüft wurde nur die Struktur mit `scripts/validate.py`; kein Verhaltens- oder Live-Test.

- Nutzer schreibt „full send“ zu einem kleinen Bugfix: Branch, Reproduktion vor und nach dem Fix, `sol-loop`, PR, Babysitting, Merge erst bei erfülltem Merge-Gate; Bericht mit PR-Link und Merge-Commit.
- Ohne ausdrückliches „full send“: keine autonome Merge-Befugnis annehmen.
- Produktionsänderung oder Datenlöschung nötig: über das Frage-Werkzeug blockieren; die Testfreigabe deckt das nicht.
- Review-Bot verlangt Änderungen, Branch ist BEHIND: rebasen, `--force-with-lease`, erneut beweisen; nie `--admin`.
- UI-Änderung: Screenshots über `file-pr` in die PR-Beschreibung oder konkreten Hinderungsgrund nennen.
