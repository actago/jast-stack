# Prüffälle

Synthetische Textszenarien, nicht ausgeführt. Geprüft wurde nur die Struktur mit `scripts/validate.py`; kein Verhaltens- oder Live-Test.

- UI-Änderung mit Screenshots aus der Session: in die PR-Beschreibung mit Bildunterschrift und erreichbarer GitHub-URL einbetten.
- UI-Änderung ohne Erfassungsmöglichkeit: konkreten Grund in die PR schreiben, keine Platzhalterbilder.
- Reine Backend-Änderung: keine Screenshots erzwingen; Titel nach Repo-Konvention, Beschreibung beginnt mit dem Problem.
- GraphQL-Limit erschöpft: PR über REST anlegen.
- Beschreibung enthält ein Token aus einem Log: vor dem Absenden entfernen.
