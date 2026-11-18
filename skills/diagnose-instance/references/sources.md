# Herkunft, geprüfter Stand und Grenzen

Stand: 2026-11-17. Nur Quellen gelesen; keine SSH-/API-Aufrufe, keine DB-Abfragen, kein Fetch, keine Änderung an Quellrepos oder aktiven Installationen.

## actaOne-Repo (`github.com/actago/actaOne`)

Lokaler Checkout `HEAD` = `dd0a3347b23e`, 754 Commits hinter `origin/main`. Gelesen wurde **`origin/main` = `73ce7d4ccdb5`** (letzter lokaler Fetch, Commit vom 2026-11-13). Hashes = Git-Blob-IDs (gekürzt).

| Datei | Blob | Verwendung |
|---|---|---|
| `.claude/skills/diagnose-instance/SKILL.md` | `54e03b5cc8ce` | Ausgangsskill (auf `HEAD` und `origin/main` gleich): Login-, Exporter-, Deploy-, Perimeter-Muster und Grundchecks; alle Fälle übernommen |
| `docs/TROUBLESHOOTING.md` | `952306a5efec` | §1–§10, §9a (Config-Inkompatibilität), RAG-Quellenlinks |
| `CLAUDE.md` | `d1cf1df520cf` | Ceph-Vollauf als Mehrfachausfall, Hairpin, Perimeter |
| `docs/rollouts/staging-env-audit-2026-11-04.md` | `0ee7959f2923` | Methode und Klassen der Drift-Einordnung |
| `docs/rollouts/production-2026-11.md` | `dd81f3ff549e` | CodeAPI-/Presidio-Release-Migration, Holds |
| `docs/RELEASE_PROCESS.md` | `4d0cd3c9bb1a` | Backfill, Benchmark-Sync, Config-Namensschema |
| `scripts/caddy-drift-check.sh` | `4cb81034ea20` | read-only Perimeter-Drift |
| `scripts/auto-deploy-staging.sh` | `f5f130ff1296` | `sync_infra_checkout`: mgmt-Checkout folgt `main` nur, wenn sauber |
| `scripts/tests/test_librechat_template_drift.sh` | `5e2968f6736f` | Template-Drift-Vertrag |
| `scripts/deploy-customer.sh` | (Zeile 616) | Präfix der `librechat.yaml`-Config |
| `provisioning/deploy-control-api/index.js` | `a5ff1f53c391` | Fehlercodes `mutations_disabled`, `operator_required`, `release_pins_unreadable`, `release_registry_unavailable` |

## LibreChat-Fork (`github.com/actago/LibreChat`)

Lokaler Checkout, gelesen `origin/main` = `156c677d40da` (Commit 2026-11-13). Collections `sharedlinks`, `conversations`, `messages`, `transactions` aus `packages/data-schemas/src/models/*`; Felder `shareId`, `conversationId`, `parentMessageId`, `error`, `unfinished`, `tokenCount` aus `schema/{share,message}.ts`.

## Memories und Agentenprofile (historische Belege, keine aktuellen Befehle)

| Quelle | sha256 | Stand | Verwendet für |
|---|---|---|---|
| Memory `moos-flux-imagegen-envdrift` (global) | `febb701115d7030e` | 2026-08-28 | `No plugin auth` = Env-Drift alter Bundles |
| Memory `codeapi-port-drift-3112-3114` (global) | `8e44ac32641929f0` | 2026-08-28 | Dokumentfehler bei grünem Health = CodeAPI-URL |
| Memory `actaone-caddy-perimeter-drift` (global) | `544df0adb15bcc39` | 2026-07-30 | Perimeter-Fehler non-fatal, Ziel VM-IP |
| Memory `activeruns-orphan-blockt-rollout` (global) | `d3e16f6da8c9cfa7` | 2026-08-09 | Fleet-Gate durch verwaisten Prozess |
| Memory `local-user-tenantid-pflicht` (actaOne) | `dfcbe98bf91c5997` | 2026-09-30 | Login 500 ohne `tenantId` |
| Memory `staging-chat-qa-harness` (LibreChat) | `d2e499ab648011f2` | 2026-10-24 | Chat-Metadaten, `createdAt`-Sortierung, gekürzte Tool-Argumente, `DOC_INFRA_*` |
| Memory `branch-instance-redeploy` (LibreChat) | `b375216c33485388` | 2026-11-14 | Redeploy verwirft manuelle Service-Updates |
| JAST-Stack `research/synthesis.md`, `claude-session-audit.md` §8, `codex-session-audit.md` §2/§4 | – | 2026-11-17 | Zuschnitt Drift-Referenz und begrenzte Chatdiagnose |

## Abweichungen vom Ausgangsskill

- Neu: Autorisierungsregel (Diagnose = lesen, Fix nur im beauftragten Umfang), Ceph-Mehrfachausfall, SSO-`local`-Provider, Fehlercodes der Deploy-Control-API, §9a, Dokument-/CodeAPI-Pfad ohne festen Port, Drift-Referenz, Chat-Referenz mit Datenschutzgrenzen.
- Konkrete CodeAPI-Ports bewusst nicht übernommen (mehrfach gewechselt: 3112 → 3114 → Cluster laut Repo 11/2026).
- `docker logs <cid>` durch `docker service logs` ersetzt; Inhalt sonst gleich.

## Grenzen

- Kein Live-Abgleich, keine DB- oder Log-Abfrage zur Prüfung; Feldprojektionen sind aus dem Schema abgeleitet, nicht an einer Instanz ausgeführt.
- Ob die organisatorische Freigabe für Agenten-Zugriff auf Kundenchats besteht, ist offen (siehe Research). Die Chat-Referenz setzt den konkreten Nutzerauftrag voraus und ersetzt diese Freigabe nicht.
- Die Evaluation ist ein Textszenario, kein ausgeführter Test.
