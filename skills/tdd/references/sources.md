# Herkunft und lokale Änderungen

Snapshot des installierten Skills `~/.agents/skills/tdd` vom 17.11.2026, installiert am 19.08.2026 laut `~/.agents/.skill-lock.json` (Quelle `mattpocock/skills`, Pfad `skills/engineering/tdd`, Ordner-Tree `79288be15c67b849f22b6572056601090fd20913`). Nur unter `~/.agents/skills` vorhanden; keine Kopien unter `~/.codex`, `~/.claude` oder `~/.claude-jast`. Am 17.11.2026 online (read-only, GitHub-API) bestimmt: Der Tree-Hash entspricht Upstream-Commit [`885e2ca4d842d139e9aef4e48d366c63cb1b8013`](https://github.com/mattpocock/skills/tree/885e2ca4d842d139e9aef4e48d366c63cb1b8013/skills/engineering/tdd) (Merge #911, 19.08.2026). Der lokale Ordner ist nach LF-Normalisierung tree-gleich mit Upstream; lokale Anpassungen gab es nicht. Hashes des installierten Ausgangsstands: [source-manifest.json](source-manifest.json).

## Lizenz

MIT, © 2026 Matt Pocock, als Repo-Lizenz von `mattpocock/skills`. Die lokale Installation enthielt keine Lizenzdatei; `LICENSE` wurde read-only aus dem Upstream-Commit geholt (Blob `f1dd2c09`). Die Skill-Dateien tragen keine eigenen Lizenzhinweise.

## Voraussetzungen

Optionale Geschwisterskills: `codebase-design` (Vokabular bei Schnittstellenfragen) und `code-review` (Refactoring-Phase). Laufzeit: vorhandenes Testsetup des Repos.

## JAST-Änderungen

- Keine inhaltlichen Änderungen. Neu sind nur `LICENSE`, diese Herkunftsdatei, Manifest und `evaluation.md`.

Aktualisierung: Upstream-Commit neu bestimmen, Ordner gegen das Manifest vergleichen, die JAST-Änderungen oben erneut anwenden. Workflows und Skripte wurden für diese Übernahme nicht ausgeführt.
