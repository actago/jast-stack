# Prüffälle

Synthetische Textszenarien, nicht ausgeführt. Geprüft wurde nur die Struktur mit `scripts/validate.py`; kein Verhaltens- oder Live-Test.

- In T3: vorhandene Checks und Kommentare zuerst abarbeiten, dann einmal `watch_pull_request`, Turn beenden.
- Delegierter Kind-Task: niemals selbst beobachten.
- Außerhalb T3 unter Windows: `python <abs>/scripts/pr-wait <PR> --repo owner/name`, nur ein Watcher je PR.
- Exit 1 wegen fehlgeschlagenem Pflicht-Check: Ursache beheben, Watcher neu starten.
- GraphQL-Limit erschöpft: REST-Endpunkte nutzen, nicht in enger Schleife neu beobachten.
