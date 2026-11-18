# Quellen des Skills actaone-benchmarks

Erstellt am 2026-11-17 durch Lesen lokaler Dateien und Git-Objekte. Nichts wurde live geprüft, ausgeführt, deployt oder verändert. Blob-Angaben sind gekürzte Git-Objekt-IDs, Datei-Hashes gekürzte SHA-256-Werte.

## Zusammengeführte Custom Skills

| Skill | Ort | Stand | Hash | Übernommen |
|---|---|---|---|---|
| `benchmark-tweak` | actaOne-Monorepo `.claude/skills/benchmark-tweak/SKILL.md` | lokaler Arbeitsstand `HEAD` `dd0a334`, Blob `428abcca56cb`; in `origin/main` (`73ce7d4`, 13.11.2026) Blob `8ef0591fde75` mit Kopplungsabsatz aus `3fc7571` (12.11.2026) | SHA-256 lokal `ab584f89078a` | flüchtiger Weg, Ebenen pro Modell, Bearbeitungsregeln, Prüfung, Hinweis auf Kopplung |
| `running-actaone-benchmarks` | `~/.claude/skills/running-actaone-benchmarks/SKILL.md` (einzige Datei im Ordner) | Dateidatum 30.07.2026 | SHA-256 `49adee58e051` | Scope-Grenze, Zod-Validierung, Config-Hash als Provenienz, Parameterfallen, Harness, Mongo-Felder, Sandbox, Auswertungsfehler |

Geprüfte Profile: In `~/.claude-jast/skills` und `~/.codex/skills` gibt es keinen Benchmark-Skill. In `~/.agents/skills` ebenfalls nicht. Beide Quell-Skills bleiben unverändert installiert.

**Überschneidung:** Beide beschreiben denselben Config-Wechsel über Swarm-Configs. `benchmark-tweak` deckt Änderungen und Sichtbarkeit ab, `running-actaone-benchmarks` Messung und Auswertung. Die Zusammenlegung ist durch die gemeinsamen Auslöser begründet, etwa „Modell testen, dann messen“. Der Session-Audit belegt zudem, dass `benchmark-tweak` erst nach langer Suche gefunden wurde.

## Lokale Anpassungen gegenüber den Quell-Skills

1. **Kopplung an Staging (ab 12.11.2026).** `running-actaone-benchmarks` empfiehlt, `customers/benchmark/librechat.yaml` *und* das benchmark-Template zu patchen. Seit `3fc7571` ist das Template das Staging-Template, und ein Drift-Test prüft das. Der Skill führt Dauerhaftes deshalb über Staging-Template bzw. Vault und Experimente nur flüchtig.
2. **Config-Name.** `benchmark-tweak` benennt flüchtige Configs nach Zweck und Datum. Der Skill nutzt die Inhalts-Hash-Formel aus `deploy-customer.sh` bzw. dem Sync-Skript, wie sie `running-actaone-benchmarks` als Provenienz beschreibt. Die Slug-Komponente `0e898208` wurde lokal nachgerechnet.
3. **Dekodierung.** Statt `tr -d '"' | base64 -d` wird der JSON-sichere Python-Weg aus dem Sync-Skript verwendet.
4. **Ebene 5.** `getProviderGroupId` liegt laut LibreChat-Fork `origin/main` (`df0d5a4de`, 10.11.2026) in `client/src/utils/runtime.ts`, Blob `8bc073a8b830`. Der Quell-Skill nannte `RuntimeModelSelect.tsx`. Zeilennummern wurden entfernt.
5. **Neu ergänzt aus Monorepo-Dokumenten:** Sync-Skript, Testsuite-Ziel, Deploy-Lock, `keyModelsMissing`, Overlay-Datei.
6. **Nicht übernommen:**
   - die persönliche Permission-Rule in `~/.claude/settings.json`
   - konkrete Testnutzer, LiteLLM-Key-Aliase und Ablaufdaten aus Memories
   - `.bak`-Dateinamensmuster
   - feste Zeilenangaben im Code
   - die Behauptung, `librechat.customer.yaml` werde nicht berührt; sie ist durch die Kopplung gegenstandslos

## actaOne-Monorepo `github.com/actago/actaOne`, `origin/main` `73ce7d4ccdb5` (13.11.2026)

Kein frischer Fetch. Der lokale Arbeitszweig `dd0a334` liegt dahinter.

| Pfad | Blob | Letzter Commit | Verwendet für |
|---|---|---|---|
| `scripts/sync-benchmark-release.sh` | `38a062d40ab3` | `19e2349` 2026-11-13 | Modi, Exit-Codes, Zielschutz, Lock, Mutationsumfang, Overlay, RAG-Gateway, Handbuch, Config-Formel |
| `docs/RELEASE_PROCESS.md` | `4d0cd3c9bb1a` | – | Abschnitt „Benchmark an Staging angleichen“, Hotfix-Hinweis zu benchmark |
| `docs/operations/testsuite-vm.md` | `4ae6fb976123` | `19e2349` 2026-11-13 | `TESTSUITE_TARGET=benchmark`, Testsuite-Konto und Contexte |
| `deploy/templates/librechat.customer.benchmark.yaml` | `8aa9f5a83f7d` | `3fc7571` 2026-11-12 | nur Existenz und Kopplung laut Commit-Text; Inhalt nicht gelesen |
| Commit `3fc7571` | – | 2026-11-12 | Kopplung, Drift-Test, Restunterschiede (Modell-Overlay, OCR) |

## LibreChat-Fork `github.com/actago/LibreChat`, `origin/main` `df0d5a4de` (10.11.2026)

Gezielte Existenzprüfung der im Skill genannten Code-Anker, ohne Verhaltensprüfung:

- `client/src/utils/runtime.ts`: `getProviderGroupId`
- `packages/api/src/runtime/profile.ts`: `shouldUseProfileValue`
- `api/server/middleware/uaParser.js`: `Illegal request`
- `packages/api/src/endpoints/custom/config.ts` (Blob `fdf829ad7cae`): `extractEnvVariable` für `apiKey` und `baseURL`

Nicht nachgeprüft:

- Token-Map-Präfixe und `tokenConfig`-Vorrang in `packages/api/src/utils/tokens.ts`
- Spec-Erzeugung in `packages/data-schemas/src/app/specs.ts`
- Umgang mit `mcpServers.url`-Platzhaltern nach PR #62

## Memories und Sessions (nur Belege)

- `~/.claude-jast/projects/C--Users-j-starrermay130-Projekte-benchb0t/memory/benchmark-vm-setup.md` (09.11.2026): VM 367, Zugang über mgmt, Vorliebe für benchmark statt Staging, temporäres Setup. Keine Zugangsdaten übernommen.
- JAST-Stack `research/claude-session-audit.md` §1 und §7: Session `51739188` (Zugang zu benchmark erst über Umwege, `benchmark-tweak` erst spät gefunden) und `6e58e450` („Staging und Benchmark gleicher Stand“, umschaltbares Testsuite-Ziel).
- JAST-Stack `research/codex-session-audit.md`: Benchmark-Sessions am 20.10., 24.10. und 30.10. nur erwähnt und nicht im Detail geprüft.

## Grenzen

- Nicht live geprüft: aktueller Release- und Config-Stand von benchmark, Existenz und Funktion von `~/bench-harness`, Testsuite-Zeitplan, Sandbox-Inventar, Endpunkt des Contexts.
- Die Fallen-Tabelle in `references/config-aendern.md` stammt aus einem Template-Stand vor der Kopplung. Sie gilt als Prüfhinweis, nicht als belegter Ist-Zustand.
- Ob ein „Stable statt Staging“-Stand auf benchmark heute gewünscht oder vorgesehen ist, ist offen.
