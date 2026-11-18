# Herkunft

Stand: 17.11.2026.

- Ausgangsskill: actaOne `agent/hermes-skills/postplan/SKILL.md`, mit `agents/openai.yaml`. Letzter lokaler Commit am Skill: `bd12927cde15f83ae61a3fe057f133c5a0b3eb17`, 12.08.2026. Der einzige Ressourcenordner enthielt UI-Metadaten; keine Skripte oder Vorlagen. JAST übernimmt den fachlichen Ablauf, die optionale UI-Datei nicht.
- Herstellerseite [Postplan](https://postplan.dev/), am 17.11. gelesen: statische HTML-Drafts, CLI-Aufruf `npx postplan upload ./plan.html`.
- [CLI-Zugang](https://postplan.dev/cli/auth), am 17.11. gelesen: Publishing benötigt einen Account-API-Key. Kein Login durchgeführt.
- Nutzerbeispiel [PDF-Editor Tracker](https://1k1jbpvz4aap.postplan.dev/), HTML über `/raw` am 17.11. gelesen, angezeigter Stand 13.11.2026. Wiederverwendbare Merkmale: Arbeitspaket-IDs, Aufgaben, Kategorien, Abhängigkeiten, Aufwand, Fortschritt, Verlauf und Rückmeldung. Keine vollständige Kopie oder projektspezifischen Inhalte übernommen.

## Eigene Erweiterungen

Automatischer Auslöser für größere Vorhaben, ein dauerhaftes Artefakt pro Projekt, Pflege an Zustandsübergängen, stabile IDs, nachvollziehbare Fortschrittsberechnung und getrennte Nachweise für Implementierung/Review/Merge/Rollout. Das ursprüngliche statische HTML-Profil bleibt Standard. Das Beispiel enthält JavaScript; dessen Existenz ist keine allgemeine Freigabe oder dokumentierte Plattformgarantie dafür.

## Prüfgrenzen

Kein `postplan`-Befehl im aktuellen PATH gefunden. Keine Installation, Authentifizierung oder Veröffentlichung, keine Änderung des Beispielartefakts. Upload- und Dateimapping-Verhalten stammen aus dem Ausgangsskill und sind hier nicht ausgeführt geprüft. Das Beispiel wurde als HTML gelesen, nicht im Browser bedient; seine Interaktivität wurde nicht getestet. Struktur- und Linkprüfung ersetzen keinen Upload-/Update-Test.
