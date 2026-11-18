# Herkunft und lokale Änderungen

Snapshot des installierten Skills `~/.agents/skills/babysit-pr` vom 17.11.2026. `~/.codex/skills`, `~/.claude/skills`, `~/.claude-jast/skills` und `~/.claude-firma/skills` verlinken per Junction auf denselben Ordner; abweichende Kopien gibt es nicht. Upstream: [t3dotgg/tstack](https://github.com/t3dotgg/tstack/tree/7de017b3fc9d50c03cf3ecb98fb71e0ca65a78bd/skills/babysit-pr), Commit `7de017b3fc9d50c03cf3ecb98fb71e0ca65a78bd` laut `~/.agents/tstack/installation.json`. Die dort abgelegte Upstream-Kopie wurde am 17.11.2026 online (read-only, GitHub-API) blobweise gegen diesen Commit geprüft: identisch nach LF-Normalisierung. Hashes des installierten Ausgangsstands: [source-manifest.json](source-manifest.json).

## Lizenz

MIT, © 2026 Theo Browne. `LICENSE` stammt aus `~/.agents/tstack/LICENSE` und ist blobgleich mit der `LICENSE` in t3dotgg/tstack@7de017b. Die Skill-Dateien tragen keine eigenen Lizenzhinweise.

## Voraussetzungen

Optionaler Geschwisterskill `leaving-pr-comments`. Laufzeit: T3 `watch_pull_request` oder das gebündelte `scripts/pr-wait` (Python 3, authentifiziertes `gh`; Zustand unter `~/.local/state/pr-wait/`).

## JAST-Änderungen

- Verweis auf die lokale Datei `C:/Users/<user>/.agents/tstack/T3-MULTI-HARNESS.md` durch den Ordnerverweis [t3-multi-harness.md](t3-multi-harness.md) ersetzt. Diese Referenz kopiert die lokale Fassung vom 26.10.2026; JAST hat darin nur den Installationsumfang („für diesen Windows-Nutzer“), persönliche Kontonamen (`Claude_jast`/`Claude_uno` → zwei Claude-Kontoprofile) und die Watcher-Zeile (Python 3 und `gh` als Voraussetzung, POSIX-Aufruf, nur `babysit-pr` enthält `pr-wait`) verallgemeinert. Markiert per HTML-Kommentar am Dateianfang.
- Erhaltene lokale tstack-Anpassung in `scripts/pr-wait` (laut `installation.json`): Windows-Lock über `msvcrt` neben POSIX-`fcntl` und plattformneutrale Stop-Hinweise. Unverändert übernommen. Laut `~/.agents/tstack/validation.json` wurden Syntax, Hilfe und Windows-Lock am 26.10.2026 lokal getestet, Live-PR-Überwachung nicht. Für diese Übernahme wurde das Skript nicht ausgeführt.
- Neu: `LICENSE`, diese Herkunftsdatei, Manifest und `evaluation.md`.

Aktualisierung: Upstream-Commit neu bestimmen, Ordner gegen das Manifest vergleichen, die JAST-Änderungen oben erneut anwenden. Workflows und Skripte wurden für diese Übernahme nicht ausgeführt.
