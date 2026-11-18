# Herkunft, geprüfter Stand und Grenzen

Stand: 2026-11-17. Nur Quellen gelesen; keine SSH-/API-Aufrufe, kein Deploy, kein Fetch, keine Änderung an Quellrepos oder aktiven Installationen.

## actaOne-Repo (`github.com/actago/actaOne`)

Lokaler Checkout: `HEAD` = `dd0a3347b23e` (#227). Gelesen wurde **`origin/main` = `73ce7d4ccdb5`** (letzter lokaler Fetch, Commit vom 2026-11-13), weil `HEAD` 754 Commits hinter `origin/main` liegt (keine eigenen Commits voraus) und der Release-Teil (Hotfix-Pfad, Release-Pins, Self-Heal-Schalter) erst dort steht. Hashes = Git-Blob-IDs auf `origin/main` (gekürzt).

| Datei | Blob | Verwendung |
|---|---|---|
| `.claude/skills/cut-release/SKILL.md` | `5892361c2746` | Ausgangsskill: Build → Freigabe → Promote, Hotfix, Self-Heal-Schalter, Fallen. Inhalte übernommen und umgeordnet |
| `docs/RELEASE_PROCESS.md` | `4d0cd3c9bb1a` | Release-Pins, Staging-Gates, Hotfix-Runbook, Benchmark-Sync, Canary → Flotte, Rollback |
| `CLAUDE.md` | `d1cf1df520cf` | Registry als Wahrheit für letzten Stable, ältere Stables wählbar, PAUSE/Holds, Ceph-Kapazität, kein Monitoring |
| `provisioning/deploy-control-api/release-history.js` | `efe77bd4f0b7` | Registry `stable-releases.jsonl`, append-only |
| `provisioning/deploy-control-api/index.js` | `a5ff1f53c391` | Endpunkte `/api/v1/releases/{stable,history,approved,pins}`, Job-Aktionen |
| `provisioning/deploy-control-api/job-worker.js` | `65b0949be6bc` | Flottenlauf: Ausschlüsse, Same-Tag-Skip, Weiterlaufen nach Fehlern, Stable-Prüfung |
| `docs/operations/service-rollout-policy.md` | `04dc0e7f7ba6` | Rollout-Pfade je Artefakt, kein generischer Neustart |
| `docs/rollouts/production-2026-11.md` | `dd81f3ff549e` | Release-Migrationen CodeAPI/Presidio, Holds je Kunde |
| `scripts/sync-benchmark-release.sh` | `38a062d40ab3` | Existenz und Modi geprüft |
| `scripts/auto-deploy-staging.sh` | `f5f130ff1296` | `sync_infra_checkout` (Z. 425–461): fast-forward des mgmt-Checkouts nur bei sauberem `main`; Build nur bei geänderten Service-Repos; Hotfix-Modus |
| `docs/FLEET_ROLLOUT_CHECKLIST.md` | sha256 `53e557e5f47ceeec` | **unversioniert**, nur im lokalen Arbeitsbaum; Stand 31.08.2026 |

Weitere Existenzprüfungen auf `origin/main`: `scripts/selfheal_levels.py`, `scripts/fleet-selfheal-levels.py`, `scripts/validate-librechat-config.sh`, `scripts/check-submodule-pointers.sh`, Aktionen `promote_customer_vm`, `redeploy_customer_vm`, `deploy_branch_build`, `promote_all_customers`.

## Agentenprofil und Memories (historische Belege, keine aktuellen Befehle)

Sha256 gekürzt, Datum = Dateistand.

| Quelle | sha256 | Stand | Verwendet für |
|---|---|---|---|
| Agentenprofil `actaone-infra.md` (Standardprofil) | `33ae066de31bff7d` | – | Nennt noch den Candidate als Wahrheit; durch Registry ersetzt |
| Memory `release-pin-neukunden` (actaOne) | `1be668c35f34b9cf` | 2026-10-17 | Stable ≠ Neukunden-Release, Live-Tag statt Annahme |
| Memory `release-vorbereitung-gpt6-opus55` (actaOne) | `eb2426697eaf23d5` | 2026-09-30 | Image vor Template, Same-Tag-Skip, Slug-Templates |
| Memory `selfheal-stufen-rollout-kw44` (actaOne) | `0fe86bffd11e9cef` | 2026-10-23 | release-gekoppelte Vault-Schalter |
| Memory `sprint-und-release-kadenz` (actaOne) | `e93c56bca39a634e` | 2026-10-21 | Termine nicht berechnen |
| Memory `actaone-fleet-promote-parallel` (global) | `87a75e76f3e5f617` | 2026-07-27 | historische Parallel-/Rate-Limit-Falle |
| Memory `fleet-rollout-2026-08-31` (global) | `c3dbd0d4cf2f11e4` | 2026-09-01 | Checkliste als Gate |
| Memory `september-release-flotten-rollout` (global) | `dc71ad5f4e67d904` | 2026-09-30 | Nachzügler mit alter Modellliste |
| Memory `activeruns-orphan-blockt-rollout` (global) | `d3e16f6da8c9cfa7` | 2026-08-09 | Fleet-Gate durch verwaisten Prozess |
| Memory `release-hotfix-kette-2026-08-27` (global) | `b9d31320ae99f124` | 2026-08-28 | Gate prüfte keine Kernfunktionen |
| JAST-Stack `research/synthesis.md`, `claude-session-audit.md` §7, `codex-session-audit.md` §1/§5, `existing-guidance-audit.md` | – | 2026-11-17 | Zuschnitt: Registry, Zielumfang, Readiness, Ausnahmen |

## Abweichungen vom Ausgangsskill

- Candidate nur noch als Vor-Freigabe-Zustand; Registry als Wahrheit (Ausgangsskill und `actaone-infra` nannten den Candidate).
- „Flotte konsistent: prod == staging == Kunden == neuer Tag" ersetzt durch Zielumfang mit Ausnahmen und Klassen.
- Neu: Readiness, Pins `hold`/`follow`, Same-Tag-Skip, Stopp-Regel, Abschlussbericht, Ceph-Vorprüfung.
- Korrigiert gegenüber Memories (08/2026: „Poller ignoriert actaOne/main, mgmt muss manuell nachgezogen werden"): Der Cron zieht den sauberen mgmt-Checkout heute selbst nach, baut aber weiterhin nur bei Service-Repo-Änderungen.
- Self-Heal-Schritte gekürzt mit Verweis auf das Runbook; Buildkit-Kommandos durch Verweis auf `TROUBLESHOOTING.md` ersetzt.

## Grenzen

- Kein Live-Abgleich: Ob mgmt-Checkout, Registry, Pins, Cron-Schalter (`STAGING_SMOKE`, `STAGING_DOCUMENT_PROBE`) heute so stehen, ist nicht geprüft.
- `origin/main` stammt vom letzten lokalen Fetch (Commit 2026-11-13); neuere Commits sind nicht berücksichtigt.
- Kein Rollout und kein Panel-Job zur Prüfung dieses Skills ausgeführt. Die Evaluation ist ein Textszenario, kein Test.
