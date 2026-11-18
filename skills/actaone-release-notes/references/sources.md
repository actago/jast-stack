# Herkunft, geprüfter Stand und Grenzen

Stand: 2026-11-17. Nur Quellen gelesen; keine Release-Notes erzeugt, kein Validator ausgeführt, kein Fetch, kein GitHub-Schreibzugriff, keine Änderung an Quellrepos oder aktiven Installationen.

## Ausgangsskill

Vollständiger Ordner `agent/hermes/skills/actaone-release-notes` aus dem actaOne-Monorepo (`github.com/actago/actaOne`, intern). Letzter Commit auf dem Ordner `e25ee61` (28.08.2026); identisch auf lokalem `HEAD` `dd0a334` und `origin/main` `73ce7d4`. Sechs Dateien übernommen, Hashes des unveränderten Ausgangsstands: [source-manifest.json](source-manifest.json). Eigene actago-Quelle, keine separate Lizenzdatei vorhanden; Nutzungsrechte folgen dem internen Repo. Eine Freigabe zur Veröffentlichung außerhalb von actago ist damit nicht belegt.

## JAST-Änderungen (für spätere Updates)

- `SKILL.md`: Verweis auf `$actaone-core` ersetzt durch die neue Datei [actaone-context.md](actaone-context.md). Ergänzt: Range je Komponente aus dem Release-Tag ableiten. Zeilenenden auf LF normalisiert. Sonst unverändert.
- `references/actaone-context.md`: neu. Statt des ganzen `actaone-core` (Snapshot 08/2026 mit elf Referenzdateien, Betriebsregeln und Live-Zustand) nur die für Release-Notes nötigen Fakten, jeweils mit maßgeblicher Repoquelle.
- `references/librechat-ui-payload.md`: Schema an den aktuellen Fork angeglichen (siehe Abweichungen). PR-Übergabe um gebündelte Assets erweitert. „agent Git identity“ als die vom Repo/Nutzer vorgesehene Agentenidentität formuliert, weil die Hermes-Identität außerhalb der Hermes-Laufzeit nicht existiert.
- `references/editorial-policy.md`, `output-schema.md`, `safety-policy.md`, `agents/openai.yaml`: inhaltlich unverändert (nur LF).
- `references/sources.md`, `source-manifest.json`, `evaluation.md`: neu.

## Geprüfte Quellverträge

actaOne `origin/main` `73ce7d4` (13.11.2026), gekürzte Blob-IDs:

| Datei | Blob | Verwendung |
|---|---|---|
| `CLAUDE.md` | `d1cf1df520cf` | Release-Registry als Wahrheit für „letzter Stable“ |
| `docs/RELEASE_PROCESS.md` | `4d0cd3c9bb1a` | Tag-Format, Stable-Gating, Release-Pins, Canary/Flotte |
| `agent/hermes/skills/actaone-core/SKILL.md` und `references/` | – | Nur gelesen, um den Bedarf abzugrenzen; nicht übernommen |

LibreChat-Fork `origin/main` `f29a7aafa2dc` (16.11.2026; der lokale Checkout steht auf einem Feature-Branch, gelesen wurde `origin/main`):

| Datei | Blob | Verwendung |
|---|---|---|
| `packages/api/src/release/notes.ts` | `630e02bd0d6d` | Produktschema, Rollenfilter |
| `scripts/validate-release-notes.mjs` | `677010a1c4ad` | Validator, lädt `@librechat/api` |
| `api/server/routes/release-notes.js` | `9644745b860d` | `GET /current`, Rollenfilter |
| `api/server/data/release-notes.json` | `52af435a5973` | Aktuelles Beispiel mit `layout`, `images` |

## Abweichungen vom Ausgangsskill

- Der Ausgangsskill nannte das Produktschema „exactly this shape“ und „strict“. Der Fork kennt inzwischen optional `layout: "chapters"`, `documentUrl` und je Eintrag `images`; die November-Release-Notes nutzen sie. Ergänzt.
- `audience` ist im Schema optional mit Default `all`. Die Regel „explizit setzen“ bleibt als lokale Schutzregel.
- Nur die Dateiebene ist `.strict()`. Unbekannte Schlüssel in `release` und Einträgen werden still entfernt. Die Regel „keine Zusatzschlüssel“ bleibt, ist aber eine Regel für den Agenten, kein Validatorbefund.
- Kein Widerspruch gefunden zu Zielgruppenabgrenzung, Sicherheits- und Freigaberegeln.

## Grenzen

- Darstellung von `layout`, `images` und `documentUrl` im Modal nicht im Code geprüft und nicht gerendert.
- Ob der Validator ohne Build von `packages/api` lauffähig ist, wurde nicht getestet.
- `agents/openai.yaml` und die `$skill`-Schreibweise stammen aus der Hermes/Codex-Laufzeit. Andere Agenten ignorieren die Datei; nicht geprüft, ob eine Zielumgebung sie auswertet.
- `evaluation.md` enthält Textszenarien, keinen ausgeführten Test.
