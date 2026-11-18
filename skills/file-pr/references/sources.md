# Herkunft und lokale Änderungen

Snapshot des installierten Skills `~/.agents/skills/file-pr` vom 17.11.2026. `~/.codex/skills`, `~/.claude/skills`, `~/.claude-jast/skills` und `~/.claude-firma/skills` verlinken per Junction auf denselben Ordner; abweichende Kopien gibt es nicht. Upstream: [t3dotgg/tstack](https://github.com/t3dotgg/tstack/tree/7de017b3fc9d50c03cf3ecb98fb71e0ca65a78bd/skills/file-pr), Commit `7de017b3fc9d50c03cf3ecb98fb71e0ca65a78bd` laut `~/.agents/tstack/installation.json`. Die dort abgelegte Upstream-Kopie wurde am 17.11.2026 online (read-only, GitHub-API) blobweise gegen diesen Commit geprüft: identisch nach LF-Normalisierung. Hashes des installierten Ausgangsstands: [source-manifest.json](source-manifest.json).

## Lizenz

MIT, © 2026 Theo Browne. `LICENSE` stammt aus `~/.agents/tstack/LICENSE` und ist blobgleich mit der `LICENSE` in t3dotgg/tstack@7de017b. Die Skill-Dateien tragen keine eigenen Lizenzhinweise.

## Voraussetzungen

Laufzeit: Git, `gh` (alternativ REST über `gh api`). Optionale Geschwisterskills: `babysit-pr` (wenn Überwachung verlangt) und `leaving-pr-comments` (für Kommentare). Für Screenshots ein autorisierter Erfassungsweg und ein dauerhafter, für GitHub erreichbarer Ablageort.

## JAST-Änderungen

- Verweis auf die lokale Datei `C:/Users/<user>/.agents/tstack/T3-MULTI-HARNESS.md` durch den Ordnerverweis [t3-multi-harness.md](t3-multi-harness.md) ersetzt. Diese Referenz kopiert die lokale Fassung vom 26.10.2026; JAST hat darin nur den Installationsumfang („für diesen Windows-Nutzer“), persönliche Kontonamen (`Claude_jast`/`Claude_uno` → zwei Claude-Kontoprofile) und die Watcher-Zeile (Python 3 und `gh` als Voraussetzung, POSIX-Aufruf, nur `babysit-pr` enthält `pr-wait`) verallgemeinert. Markiert per HTML-Kommentar am Dateianfang.
- Erhaltene lokale tstack-Anpassung: Absatz zu Pflicht-Screenshots bei sichtbaren UI-Änderungen (vorhandene Screenshots wiederverwenden, dauerhafte GitHub-URLs, Bildunterschriften, Kennzeichnung von Seed-/Mock-Zustand, URL-Prüfung, sonst konkreten Grund nennen). Er fehlt im Upstream-Commit und in der Anpassungsliste von `installation.json`, steht aber im Ausgangsstand des Manifests. Unverändert übernommen; wer ihn wann ergänzt hat, ist lokal nicht dokumentiert.
- Neu: `LICENSE`, diese Herkunftsdatei, Manifest und `evaluation.md`.

Aktualisierung: Upstream-Commit neu bestimmen, Ordner gegen das Manifest vergleichen, die JAST-Änderungen oben erneut anwenden. Workflows und Skripte wurden für diese Übernahme nicht ausgeführt.
