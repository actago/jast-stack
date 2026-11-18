# Herkunft, geprüfter Stand und Grenzen

Stand: 2026-11-17. Nur Quellen gelesen; keine Skripte ausgeführt, kein Sync, kein Harvest, kein Fetch, keine Änderung am Vault oder an aktiven Installationen.

## Vault-Repo (`github.com/actago/actaOneKBobsidian`, privat)

Lokaler Stand: `HEAD` = lokales `origin/main` = `d9d678f1e8bd` (Commit 2026-11-11). Ein lesendes `git ls-remote` zeigte Remote-`main` = `317a8f52c9ab` (Commit 2026-11-17), 61 Commits voraus. Über die GitHub-Compare-API (read-only) geprüft: Keine der unten genannten Quelldateien wurde in diesen Commits geändert; die Blob-IDs gelten damit auch für den Remote-Stand. Geändert wurden u. a. Fachnotizen, Harvest-Status-Dateien anderer Kürzel und die Auto-Harvest-Notizen eines Teammitglieds (gelesen: `20 Team/JADR/Auto-Harvest/Auto-Harvest Einrichtung JADR.md`, Remote-Stand).

| Datei | Blob | Verwendung |
|---|---|---|
| `00 Meta/claude/skills/vault-refresh/SKILL.md` | `93db25a60eae` | Ausgangsskill; inhaltsgleich mit der aktiven Installation |
| `00 Meta/codex/skills/actaone-knowledge-base/SKILL.md` | `4d4670f8c522` | Recherche-/Notizmodus |
| `00 Meta/codex/skills/actaone-updates/SKILL.md` | `cebb542ccf27` | Statusabgleich, Merge ≠ Rollout |
| `00 Meta/codex/skills/actaone-harvest/SKILL.md` | `c80f2fec68be` | Harvest, Marker nur nach Vollständigkeit |
| `00 Meta/Vault-Pflege.md` | `d8b856346058` | Status-Taxonomie, Harvest-Methode, zusätzliche Claude-Profile, Teilabgleich ≠ Vollharvest |
| `00 Meta/Wissensseiten – Aufbau & Pflege.md` | `cd7d0f5af291` | Systemseiten-Metadaten ohne falsche Sicherheit |
| `README.md` | `5d318e0f6bb4` | Einrichtung, Automatik-Schichten, Werkzeuge |
| `AGENTS.md` | `603af866945a` | Codex-Arbeitsweise im Vault |
| `00 Meta/harvest-codex.ps1` | `d1040814c29f` | Modi `-Check`, `-MarkDone`, `-Through` |
| `00 Meta/kb-common.ps1` | `f57f936dd674` | `local.json`, Markerdateien je Kürzel |
| `00 Meta/harvest-extract.py` | `a0a57958baf2` | Streamender Extrakt ohne Tool-Ausgaben |
| `00 Meta/check-links.py`, `00 Meta/sync-memories.ps1` | `eb3a1c98928d`, `5e08adeb62e0` | Existenz und Rolle |

## Aktive Installationen (lokal)

| Quelle | sha256 (gekürzt) | Verwendung |
|---|---|---|
| `~/.claude/skills/vault-refresh/SKILL.md` | `3f9b9a9c826a7767` | Identisch mit der Vault-Kopie |
| `~/.codex/skills/obsidian-actaone-kb/SKILL.md` (+ `agents/openai.yaml`) | `970dfbd03894271b` | Lese-/Schreibworkflow, Leitplanken; enthält einen persönlichen absoluten Vault-Pfad |

## Anpassungen

- Persönliche Pfade (Vault-Root, Memory-Verzeichnisse, Python-Pfade) durch Auffinden über das Remote und `local.json` ersetzt.
- Kürzel-gebundene Aussagen (JAST, LUED) auf „eigener Bereich laut `local.json`“ verallgemeinert.
- Vier Modi in einem Skill; Refresh und Harvest als Referenzen ausgelagert. Harvest-Quellen um zusätzliche Claude-Profile und den Hinweis auf Auto-Harvest-Rohmaterial ergänzt (aus `Vault-Pflege.md` bzw. Auto-Harvest-Notiz).
- Fachregeln (Häkchen-Verbuchung, Spiegel nicht editieren, Marker-Regel, keine Zugangsdaten) unverändert übernommen.

## Gefundene Widersprüche in den Quellen

- Vault-`AGENTS.md` verweist auf `$lued-vault-refresh`; versioniert sind `actaone-updates`/`actaone-harvest`.
- `vault-refresh` nennt nur `~/.claude/projects`; `Vault-Pflege.md` (08.11.2026) verlangt zusätzlich weitere Claude-Profile.
- `Vault-Pflege.md` nennt als Memory-Quelle einmal das Root- und einmal das Projekt-Memory-Verzeichnis; maßgeblich ist `local.json`.
- README: `setup.ps1` installiert `/vault-refresh` nach `~/.claude/skills/`. Eine parallele Installation dieses Skills sollte daher mit dem vorhandenen Namen abgestimmt werden.

## Grenzen

- Kein Lauf von Sync, Harvest-Skripten oder Linkprüfer; Verhalten der Skripte nur aus Quelltext und Doku.
- Inhalte der Fachnotizen nicht auf Aktualität geprüft.
- `evaluation.md` enthält Textszenarien, keinen ausgeführten Test.
