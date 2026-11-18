# benchmark an Staging angleichen

Maßgeblich ist `docs/RELEASE_PROCESS.md`, Abschnitt „Benchmark an Staging angleichen (Testsuite)“, im actaOne-Monorepo, dazu der Kopf von `scripts/sync-benchmark-release.sh`. Beide vor der Nutzung aus `origin/main` lesen. Diese Datei fasst den Stand vom 13.11.2026 zusammen.

## Modi

Auf dem Management-Host als `actaone` im Infra-Checkout:

```bash
scripts/sync-benchmark-release.sh status   # JSON: Quelle, Ziel, Abweichungen; ändert nichts
scripts/sync-benchmark-release.sh check    # wie status, Exit 10 bei Abweichung
scripts/sync-benchmark-release.sh sync     # angleichen
```

Die letzte stdout-Zeile ist immer ein JSON-Objekt. Für Diagnose und Provenienz `status` verwenden. `sync` ist eine Änderung an benchmark und braucht den entsprechenden Auftrag.

## Was sync tut und was nicht

- **Quelle:** Image-Tag von `customer-staging_api` und dessen gemountete Swarm-Config, also der Inhalt, nicht die Datei auf mgmt. Staging wird nur gelesen.
- **Abbruch mit Exit 3:** Staging uneinheitlich, im Update oder das Tag ist noch kein verifizierter Candidate. `REQUIRE_CANDIDATE=false` hebt nur das Candidate-Gate auf; das nur auf ausdrücklichen Wunsch.
- **Zielschutz Exit 2:** Der Context `customer-benchmark` zeigt nicht auf `ssh://actaone@192.168.10.167`.
- **Deploy-Lock:** `sync` hält denselben globalen Lock wie `promote.sh` und `deploy-customer.sh`. Während des Laufs kann Staging nicht deployt werden und kein Promote laufen. Exit 75 heißt: Lock belegt. Nicht erzwingen.
- **Mutiert ausschließlich:** benchmark-Dienste (Image, Config, Overlay, RAG-Gateway-Werte, Hosts), einen Einmal-Dienst für den Handbuch-Import, alte benchmark-Configs und -Images sowie `customers/benchmark/librechat.yaml` mit Sicherung.
- **Fehler Exit 1:** Der betroffene Dienst wird per Swarm-Rollback zurückgesetzt. Weitere Fehlercodes im JSON sind etwa `rag_gateway_preflight`, `rag_gateway_inspect_failed`, `overlay_gateway_conflict` und `handbook_import`. Das JSON nennt nur Key-Namen, nie Werte.
- **`handbookPending: true`:** Für das aktuelle Release fehlt der Handbuch-Import. Der Stand gilt dann als nicht synchron.
- **`keyModelsMissing`:** Modelle, die der Staging-LiteLLM-Key darf, der benchmark-Key aber nicht. Das ist eine Gateway-Rechtefrage. Der Sync ändert keine Keys.

Unterschiede, die laut Commit-Text bewusst bleiben: Staging-Modell-Overlay und OCR-Weg. Paritätsaussagen deshalb auf die Felder stützen, die `status` vergleicht, nicht auf „gleiches Template“.

## Testsuite-Bezug

- Ziel der Testsuite: `TESTSUITE_TARGET`, seit 12.11.2026 `benchmark`. Die Rolle `testsuite_target` pflegt den Wert. Ein Wechsel zurück auf Staging geht nur über diese Variable und ist eine Infra-Änderung, siehe `docs/operations/testsuite-vm.md`.
- Das Testsuite-Konto auf mgmt hat Docker-API-Zugriff auf `staging` und `customer-benchmark`. Diese API ist root-gleich, auch wenn sie keine Shell bietet.
- benchmark bewegt sich nur, wenn jemand den Sync auslöst. Ein flüchtiges Experiment bleibt bis dahin aktiv und verfälscht Testsuite-Läufe. Nach dem Experiment `status` erneut lesen und das Ergebnis im Bericht nennen.

## „Stable statt Staging auf benchmark“

Das Sync-Skript kennt nur Staging als Quelle. Für einen anderen Stand gibt es hier keinen geprüften Weg. `deploy-customer.sh` bzw. `promote.sh` auf benchmark sind Release-Vorgänge mit dem Release-Ablauf des Monorepos und brechen die Testsuite-Parität. Die Folgen nennen und den Nutzer entscheiden lassen.
