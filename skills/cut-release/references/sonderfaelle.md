# Sonderfälle: Hotfix, Vault-Schalter, Benchmark

Nur den Abschnitt lesen, der zum Auftrag passt. Maßgeblich ist jeweils das genannte Runbook im actaOne-Checkout; hier stehen die Entscheidungen, die man ohne das Runbook leicht falsch trifft.

## Hotfix auf den laufenden Stable

Wenn `main` schon ungeprüfte Änderungen enthält, aber ein Fix auf den laufenden Stable soll. Runbook: `docs/RELEASE_PROCESS.md`, „Hotfix-Release".

- Nicht `main` freigeben und keinen `branch-`-Build auf Bestandskunden promoten (CodeAPI-Abgleich akzeptiert nur offizielle Release-Tags).
- Quellstand: LibreChat-Branch auf dem Commit des laufenden Stable plus Fix-Commits; KB_RAG/presidio aus `sourceRevisions` des laufenden Stable in der Registry.
- Bei pausiertem Cron (`touch ~/.actaone-autodeploy/PAUSE`) auf mgmt: `bash scripts/auto-deploy-staging.sh --hotfix --reason "…" --librechat … --kb-rag … --presidio …`. Exit 2 = Cron nicht pausiert, 3 = Test-Hold aktiv, 4 = Staging-Lock belegt, 5 = Quellstand nicht auflösbar.
- Danach fachlich auf Staging prüfen, normal freigeben (vorher ggf. Pin `hold`), Pause erst nach fertiger Hotseat-Wärmung aufheben, dann Bestandskunden mit dem offiziellen Tag über [fleet-rollout.md](fleet-rollout.md).
- Die `PAUSE` gehört diesem Lauf nur, wenn dieser Lauf sie gesetzt hat. Bestand sie schon vorher, mit dem Nutzer klären, statt sie zu entfernen.

## Release-gekoppelte Vault-Schalter

`promote.sh` ergänzt bei jedem Promote fehlende Keys aus `customer-defaults` (überschreibt keine gesetzten Kundenwerte). Schalter, die erst ab einem bestimmten Code wirken, dürfen nicht vor dem Release beim Kunden ankommen. Aktuell dokumentiert: Self-Heal-Stufen `DOCUMENT_SELF_HEAL_{S1,S3,S4,INFRA}` (ab LibreChat #550), Ablauf und Rückweg in `docs/operations/selfheal-stufen-rollout.md` und `.claude/skills/cut-release/SKILL.md` des actaOne-Checkouts. Kurzform laut Repo-Stand:

1. nach Freigabe `python3 scripts/selfheal_levels.py release-check <tag>` → rc 0,
2. vor Canary/Rollout `python3 scripts/fleet-selfheal-levels.py --environment prod --defaults --apply`,
3. Nachzügler auf dem Tag: `--all --release <tag> --apply`, dann Redeploy der gelisteten Instanzen,
4. Nachweis `--all --verify`.

Schritte 2–3 sind Vault-Mutationen: nur mit ausdrücklichem Auftrag. Werden Webhook-Receiver oder Deploy-Control-API wegen geänderter Default-Allowlists neu ausgerollt, nicht während laufender Jobs und ohne `ansible-playbook --diff` (Secret-Templates).

Für andere neue Defaults gilt dasselbe Muster: Ab welchem Code wirkt der Key, und erreicht der Backfill Instanzen, die schon auf dem Tag sind (nein, nur per Einzel-Redeploy)?

## Benchmark an Staging angleichen

Benchmark folgt nicht dem Kunden-Stable, sondern auf Wunsch dem Staging-Stand (Testsuite-Parität). Werkzeug: `scripts/sync-benchmark-release.sh status|check|sync` auf mgmt (`status`/`check` ändern nichts). `sync` nur, wenn der Abgleich beauftragt ist; Benchmark nie als Teil eines Kunden-Rollouts mitziehen. Ein normales `deploy-customer.sh benchmark` ergibt keine exakte Staging-Kopie; danach erneut `sync`.

## Branch-Instanzen

`branch-*` laufen auf eigenen Builds (Job `deploy_branch_build`) und werden von Flotten-Rollouts ausgeschlossen. Ein Redeploy verwirft manuelle `service update`-Einstellungen dieser Instanz; vorher erfassen, nachher wieder setzen oder als Lücke melden.
## Lifecycle beim Releaseabschluss

Vor der Freigabe Neukunden-/Partner-Pins und Hotseat-Auswirkungen prüfen; danach Registry, Pins und ausgelöste Wärmung getrennt nachweisen. Nach jeder Rollout-Welle den tatsächlichen Stand aller beauftragten Ziele prüfen. Beim Abschluss offene Branch-/Testumgebungen nach Zweck, Zuständigkeit, TTL und benötigtem Rückweg erfassen. Ein Merge oder neuer Stable autorisiert keinen VM-Abbau.

Für Archivierung, Wiederaufnahme und Teardown kann der separat verfügbare Skill `actaone-vm-lifecycle` verwendet werden. Ohne ihn die maßgeblichen `job-worker.js`, `branch-instances.js`, `retention.js` und Teardown-Skripte lesen. Branch-TTL und Kundenaufbewahrung sind verschieden: erstere kann vereinbarten automatischen Abbau auslösen, letztere liefert einen Löschvorschlag. Alte lokale Release-Images räumt der reguläre Deploy-Pfad profilabhängig nach interner Verifikation auf; Rollback benötigt dann einen erneuten Registry-Pull. Kein zusätzliches pauschales Pruning von Volumes oder VMs.

