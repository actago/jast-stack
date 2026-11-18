# quellen und pruefgrenzen

Erstellt am 18.11.2026 auf ausdruecklichen Nutzerauftrag: Git-Historie zuerst, daraus neue Features, Aktivierung ueber Templates und weitere Konfigurationspfade sowie einen Testplan ableiten; Release/Deploy laufend begleiten und den tatsaechlichen Endzustand nachpruefen.

## vorhandene grundlage

Eigene JAST-Skills `cut-release` samt readiness/fleet-rollout/sonderfaelle, `actaone-vm-lifecycle` und `diagnose-instance`. `babysit-pr` lieferte das Muster Beobachten/Handeln/Wiederaufnehmen, seine PR-Watcher wurden nicht als Deploy-Watcher uebernommen. Die neuen Skills beschreiben die verbindende Beobachtung und Feature-Abnahme; sie kopieren keinen neuen Release-Mechanismus.

Der Nutzer verwendet Postplan, Hark und Post-Session-Hooks. Hier sind sie optionale Integrationen der vorhandenen Umgebung, keine mitgelieferten Dienste oder automatisch installierten Hooks.

## gelesener actaone-stand

Repo `https://github.com/actago/actaOne`, lokal vorhandenes `origin/main` 73ce7d4ccdb5097d3916f15357da3f4a2a98a7e3. Ein lesendes `git ls-remote` am 18.11.2026 meldete denselben Stand. Der lokale Arbeitsbaum steht auf einem aelteren HEAD und hat fremde Aenderungen; er wurde nicht veraendert oder als Vertragsstand verwendet.

| quelle | git-blob |
| --- | --- |
| `docs/RELEASE_PROCESS.md` | `4d0cd3c9bb1a7df9949d3e25e85b0c31d4755fc3` |
| `scripts/auto-deploy-staging.sh` | `f5f130ff1296a45cf680366e1a620ff0fa98846b` |
| `scripts/deploy-customer.sh` | `60fdf754a674b42e35dbd008dca3fce9358c9401` |
| `scripts/promote.sh` | `7a4b9a88c983421e75cfe65991b530412056eef6` |
| `scripts/customer-release-features.py` | `f0795f8653530741bf833d4dde0215c771a17ff8` |
| `scripts/customer-release-env.py` | `b2e6c4eb68abb80dd16e17a00b97476450788567` |
| `provisioning/deploy-control-api/index.js` | `a5ff1f53c391b1969b420b76a210ffcc14c89640` |
| `provisioning/deploy-control-api/job-worker.js` | `65b0949be6bc56d54540e9ccc13a6ccc9d05fa97` |

Gezielt gelesen: Release-Doku bis zum Staging-Ablauf, Gate-Modi und Candidate-/Infra-Sync-Abschnitte im Staging-Skript, Templateauswahl/Feature-Renderer/Config-Hash/Validierung im Deploy-Skript, Feature-Nachbearbeitung, Job-Leseendpunkte, Flottenziel-/Skip-/Fehlerverhalten. Nicht jedes Skript wurde vollstaendig neu auditiert. Promote-Nebenwirkungen und Rollback-Unterschiede wurden zusaetzlich aus den vorhandenen JAST-Referenzen uebernommen.

Aeltere Abschnitte der Release-Doku nennen noch den Candidate als Stable-Wahrheit. Die neueren Registry-/Pin-Ablaeufe und vorhandenen Codebefunde haben fuer freigegebene Stables Vorrang. Die laufende Installation kann trotzdem abweichen; daher Versionsnachweis bei jeder Anwendung.

## pruefstand und grenzen

Struktur, Frontmatter und relative Links werden mit dem Repo-Validator und quick_validate geprueft. `evaluation.md` enthaelt synthetische Prueffaelle, keine ausgefuehrten Live-Tests. Keine SSH-, Vault-, Deploy-, Stable-, Hark- oder Postplan-Aktion zur Erstellung. Kein echter Release babysittet, keine Flotte abgefragt, keine automatische Watch-Infrastruktur installiert.

Stichprobenwahl, 10-15-Minuten-Recheck, Planfelder und Statusklassen sind JAST-Arbeitsregeln aus dem Nutzerauftrag, keine Behauptung ueber vorhandene automatische Gates. Bei laengeren asynchronen Aufgaben gilt ein fachliches Abschlusskriterium statt einer pauschalen Zeitgarantie.

`feature-test-plan.md` und `monitoring.md` liegen absichtlich in beiden Skill-Ordnern, damit jeder einzeln verwendbar bleibt. Aenderungen an den gemeinsamen Regeln in beiden Kopien nachziehen.
