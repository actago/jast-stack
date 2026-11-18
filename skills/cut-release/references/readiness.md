# Release-Readiness (vor der Freigabe)

Lesen bei „was ist seit dem letzten Kunden-Release drin", „was testen wir", „können wir heute releasen", „welche PRs noch mergen". Ergebnis ist eine Empfehlung mit Bedingungen, keine Freigabe. Freigeben, mergen oder deployen nur, wenn der Nutzer das zusätzlich beauftragt.

## Vergleichsbasis festlegen

- **Basis:** der Stand, den Kunden tatsächlich fahren. Primär `customerDefaultReleaseTag` aus den Release-Pins und der Live-Tag der Bestandsflotte (Stichprobe oder Zielliste, siehe [fleet-rollout.md](fleet-rollout.md)). Weichen beide ab, beide nennen; nicht still den neuesten Registry-Eintrag nehmen, wenn die Flotte älter ist.
- **Kandidat:** Candidate-Datei (Tag, `sourceRevisions`, Gate-Checkliste) oder ein benannter Registry-Eintrag.
- Fehlt eine der beiden Seiten (kein Zugriff auf mgmt, Registry nicht lesbar), das als Lücke melden und den Vergleich nur über die im Tag kodierten SHAs führen (`lc-<sha>-rag-<sha>-pii-<sha>`), gekennzeichnet als Teilprüfung.

## Änderungen erheben

Je Repo `git log --oneline <basis-sha>..<kandidat-sha>` im passenden Checkout (LibreChat-Fork, KB_RAG, presidio). Für actaOne `main` getrennt betrachten: Templates, `promote.sh`/`deploy-customer.sh`, Provisioner und Vault-Allowlists wirken **ohne** Release-Gate beim nächsten Deploy aus dem mgmt-Checkout. Diese Änderungen gehören in die Bewertung, auch wenn sie nicht im Tag stehen. `scripts/check-submodule-pointers.sh` zeigt, ob die Submodul-Zeiger im Repo zum neuesten Registry-Eintrag passen.

Kurze SHAs gegen Force-Pushes und fehlende Objekte absichern (`git cat-file -t`); fehlende Objekte melden statt raten.

## Bewerten

Pro fachlichem Bereich (Auth/SSO, Chat/Modelle, RAG, Dokumente/CodeAPI, PII, Abrechnung/Limits, Admin/Panel, Exporter/Control-Plane, Templates/Config):

- Was ändert sich für Kunden, welches Risiko, welche Abhängigkeit (Template vor/nach Image, Vault-Default, Migration).
- Welche Prüfung belegt es: automatisches Gate (Candidate-Checks `document-render`, `smoke`; Modus `observe` blockiert nie), vorhandene Tests, manueller Staging-Test.
- Was das Gate nicht prüft. Historisch prüfte das Stable-Gate keine echten RAG- und Dokumentläufe; ob Render-Probe und Smoke heute `enforce` sind, im Repo und in der Cron-Zeile nachsehen statt annehmen.

## Ergebnis

```
Basis: <tag/Quelle> → Kandidat: <tag/Quelle>
Änderungen: <je Repo Anzahl Commits/PRs, wesentliche Bereiche>
Ungegatete actaOne-Änderungen: <Templates/Provisioner/Allowlists>
Testplan: <Bereich – Prüfung – Ort (Staging/Canary) – Status>
Offene PRs: <PR – Empfehlung mergen/warten/nicht – Grund>
Empfehlung: GO | GO mit Bedingungen (<liste>) | NO-GO (<blocker>)
Nicht geprüft: <…>
```

Release-Termine und Sprintenden nicht aus einer vermuteten Kadenz berechnen, sondern vom Nutzer übernehmen.

Eine vorhandene, im actaOne-Checkout ggf. **unversionierte** `docs/FLEET_ROLLOUT_CHECKLIST.md` (Stand 31.08.2026) kann als Themenliste für große Versionssprünge dienen. Ihre Befunde sind historisch; nur die Prüfthemen übernehmen.
