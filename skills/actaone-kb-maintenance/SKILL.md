---
name: actaone-kb-maintenance
description: Lies und pflege die actaOne-Obsidian-Wissensbasis (Team-Vault) – Recherche, gezielte Notizpflege, Status-/PR-Abgleich („Vault-Refresh“) und Destillation von Codex-/T3-/Claude-Sessions („Harvest“). Nutze bei actaOne-KB, Vault, Sprint-Notiz, Offene Baustellen, Gelöst-Log oder Memories.
---

# actaOne-KB lesen und pflegen

Bündelt die vorhandenen Skills `vault-refresh` (Claude), `obsidian-actaone-kb` (Codex) und die im Vault versionierten Codex-Skills `actaone-knowledge-base`, `actaone-updates`, `actaone-harvest`. Herkunft und Abweichungen: [references/sources.md](references/sources.md).

## Vault finden und Stand klären

1. Arbeitskopie bestimmen: Git-Root, dessen `origin` auf `actago/actaOneKBobsidian` zeigt. Teamkonvention ist `~/Obsidian/actaOne-KB`, andere Rechner nutzen andere Pfade. Fehlt sie oder zeigt das Remote woanders hin, melden. OneDrive-`actaone-kb-master` und ZIP-Exporte sind historische Kopien, nur für ausdrücklich gewünschte Wiederherstellung.
2. Kürzel und Memory-Quellen aus `00 Meta/local.json` lesen (gitignored, von `setup.ps1` erzeugt). Eigener Bereich ist `20 Team/<Kürzel>/`; ohne Kürzel nur lesen und geteilte Bereiche nicht ändern.
3. Lokalen `HEAD` mit dem Remote-Branch vergleichen und Arbeitsbaum prüfen. Obsidian Git pullt und pusht automatisch; bei Rückstand oder fremden uncommitteten Änderungen vor dem Schreiben klären, wie synchronisiert wird. Git-Synchronität heißt nicht, dass Sessions eingearbeitet sind.
4. Die Vault-Regeln lesen, bevor du schreibst: `00 Meta/Vault-Pflege.md`, `00 Meta/Wissensseiten – Aufbau & Pflege.md`, `README.md`, `Home.md`.

## Modus wählen

- **Lesen/Recherche:** Bei breiten Fragen `Home.md`, dann die MOCs unter `10 actaOne/`. Gezielt suchen (`rg -n -i --glob '*.md'`), gefundene Notizen vollständig lesen. Sprintfragen: datierte Sprint-Notiz unter `20 Team/<Kürzel>/Sprints/` mit `Sprint-Board.md` und `Sprint-Übersicht.md` abgleichen; explizite Daten schlagen ein altes `status/aktuell`.
- **Gezielte Notizpflege:** kleinste maßgebliche Notiz ändern, bestehende ergänzen statt duplizieren, Vorlagen aus `00 Meta/Vorlagen/` für Neues.
- **Statusabgleich (Vault-Refresh):** [references/statusabgleich.md](references/statusabgleich.md).
- **Session-Harvest:** [references/harvest.md](references/harvest.md).

## Schreibregeln

- Notizen sind datierte Arbeitsnachweise, kein Beweis für heutigen Code-, GitHub- oder Infrastrukturstand. Volatile Aussagen an der Quelle prüfen und im Ergebnis „verzeichnet“ von „unabhängig geprüft“ trennen.
- `20 Team/*/Memories/` und Auto-Harvest-Spiegel sind generiert: nie von Hand ändern. Korrekturen in der Quell-Memory und im Mapping `apply-tags-<Kürzel>.ps1`, dann Sync.
- Fremde Team-Bereiche nur lesen. Geteiltes Wissen nach `10 actaOne/`, Persönliches in den eigenen Bereich.
- Format erhalten: UTF-8, YAML-Frontmatter, Wikilinks, Callouts, Task-Syntax, Überschriftenstil; neue Notizen enden mit `🏠 [[Home]]`.
- Status-Tags (`aktuell`, `teilweise`, `pruefen`, `veraltet`, `erledigt`, `archiv`) und `stand:`/`ergaenzt:` ehrlich setzen: `stand:` nur bei inhaltlicher Neuprüfung; `ergaenzt:` wertet alte Abschnitte nicht auf. Auf Systemseiten keine unbestätigten `pflegeverantwortung`- oder `pruefstatus`-Werte.
- Nichts als erledigt markieren ohne Beleg (gemergter PR, Nutzer-Häkchen, Infra-Nachweis). Ein Merge belegt keinen Rollout; Infra-Zustände ohne Prüfung als `pruefen` führen.
- Keine Zugangsdaten, Tokens, Webhook-URLs oder privaten Schlüssel ins Vault. Das Repo enthält Kundennamen und Interna; Inhalte nicht außerhalb des beauftragten Rahmens weitergeben, Sichtbarkeit nicht ändern.

## Abschluss

`python "00 Meta/check-links.py"` ausführen (bekannte Fehlalarme: Vorlagen-Platzhalter, Mermaid-Labels, Vault-relative Ziele gegen tatsächlichen Pfad gegenprüfen), dann `git diff` und `git status`. Geänderte Dateien und inhaltliche Änderungen berichten. Commit und Push nur mit Auftrag und nur auf das vorhandene private Remote; sonst übernimmt Obsidian Git.
