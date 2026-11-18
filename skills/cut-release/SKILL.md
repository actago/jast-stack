---
name: cut-release
description: actaOne-Release vorbereiten, als Stable freigeben und auf einen beauftragten Zielumfang ausrollen (Readiness, Candidate, Release-Registry, Neukunden-Pins, Canary, Wellen, Hotfix, Rollback, Abschlussnachweis). Nutzen bei "Release vorbereiten", "stable freigeben", "promoten", "ausrollen", "Fleet-Rollout", "Hotfix auf Stable", "sind alle auf dem Release?".
---

# Release schneiden und ausrollen (actaOne)

Weiterentwicklung des gleichnamigen actaOne-Projektskills. Herkunft, geprüfter Stand und Grenzen: [references/sources.md](references/sources.md).

## Voraussetzungen

- **actaOne-Repo** (`github.com/actago/actaOne`) ist die maßgebliche Quelle. Finden: aktuelles Arbeitsverzeichnis oder ein Checkout, dessen `origin` auf `actago/actaOne` zeigt; sonst den Nutzer nach dem Pfad fragen. Fehlt es, das ehrlich melden und nur allgemein antworten, keine Vertragsdetails behaupten.
- Vor jeder Aussage über Abläufe `docs/RELEASE_PROCESS.md` und `.claude/skills/cut-release/SKILL.md` des Checkouts gegen diesen Skill halten; bei Widerspruch gilt der neuere Repo-Stand, und der Widerspruch wird gemeldet.
- Operative Schritte laufen auf der Management-VM im dortigen actaOne-Checkout (laut Repo-Doku `ssh acta-mgmt`, `~/actaOne`). Zugang und Alias lesend bestätigen, nicht annehmen. Der mgmt-Checkout folgt `main` nur, solange er sauber ist: `git -C ~/actaOne status -sb`, `git log -1` und das letzte `infra_sync`-Event prüfen, bevor ein Skript oder Template dort als „aktuell" gilt. Fremde lokale Änderungen dort nicht überschreiben.

## Begriffe

- **Candidate:** `~/.actaone-autodeploy/staging-release-candidate.json` auf mgmt. Nur der zuletzt auf Staging validierte Build vor der Freigabe. Wird vom nächsten Staging-Build überschrieben.
- **Release-Registry:** `stable-releases.jsonl` im selben State-Dir, append-only, eine Zeile je Freigabe mit `releaseTag`, `approvedBy/At`, `sourceRevisions`. **Wahrheit für „freigegebene Stables" und „letzter Stable".** Lesend: `GET /api/v1/releases/history`, `GET /api/v1/releases/approved?releaseTag=<tag>` der Deploy-Control-API (mgmt `127.0.0.1:8790`).
- **Release-Pins:** `release-pins.json` mit `customerDefaultReleaseTag` (Neukunden/Hotseats), `partnerCustomerReleaseTag`, `customerBrokerReleases`. Modus `follow` (Freigabe zieht nach) oder `hold`. `GET/PUT /api/v1/releases/pins`. `deploy/RELEASE` ist nur informativ.
- **Live-Stand:** das Image von `customer-<slug>_api` je Instanz. Nur das belegt, was ein Kunde fährt.
- **Zielumfang:** die ausdrücklich beauftragte Menge von Instanzen. Eine Stable-Freigabe ist kein Rollout-Auftrag; ein Rollout-Auftrag ist kein Auftrag, die ganze Flotte anzugleichen.

## Ablauf

Zuerst klären, welche Phase beauftragt ist, und nur diese ausführen. Bereits erteilte Autorisierung gilt für ihren Umfang; jeder Schritt darüber hinaus (weitere Instanzen, Pin-Änderung, Vault-Schalter) braucht einen eigenen Auftrag.

1. **Readiness** (bei „was ist drin / was testen / GO?"): [references/readiness.md](references/readiness.md).
2. **Build:** Commit auf `main` von LibreChat/KB_RAG/presidio → Cron `auto-deploy-staging.sh` baut `YYYYmmddHHMM-lc-<sha>-rag-<sha>-pii-<sha>`, promotet Control-Plane und Staging, validiert, schreibt Candidate. Fortschritt: `tail ~/.actaone-autodeploy/staging-autodeploy-events.jsonl`, Ende `phase:"complete" status:"succeeded"`; Gate-Ergebnisse in der Candidate-Checkliste (`document-render:…`, `smoke:…`). Reine actaOne-Commits (Templates, Skripte) lösen keinen Build aus; der Cron zieht aber den mgmt-Checkout auf `main` nach, solange dieser sauber ist (Event `infra_sync`), und lässt ihn bei lokalen Änderungen oder anderem Branch stehen (`infra_sync failed`). Keine parallelen manuellen Builds, keine Lock-Datei löschen, eine fremde `PAUSE` oder fremde `holds/<runId>.json` nicht anfassen.
3. **Freigabe:** Ops-Dashboard „Staging als Stable freigeben" oder `POST /api/v1/releases/stable` mit Operator-Header und Service-Token (Token per Datei/Variable lesen, nie ausgeben). Soll der neue Stable Neukunden noch **nicht** erreichen, vorher „Pin halten" (`PUT /api/v1/releases/pins`, `{"mode":"hold",…}`). Erfolg: `candidate.stable.approvedAt` gesetzt, neuer letzter Registry-Eintrag, Pins wie gewollt; `historyWarning`/`pinsWarning` in der Antwort sind ein Befund, kein Erfolg. Die Freigabe startet `warm-hotseats.sh`.
4. **Rollout auf den Zielumfang:** [references/fleet-rollout.md](references/fleet-rollout.md) (Zielliste, Ausnahmen, Canary, Wellen, Stopp-Regel, Rollback). Hotfix auf den laufenden Stable, release-gekoppelte Vault-Schalter, Benchmark-Abgleich: [references/sonderfaelle.md](references/sonderfaelle.md).
5. **Nachweis:** je Zielinstanz Live-Image == Ziel-Tag, alle dauerhaften Services `1/1`, `/health` über die VM-IP mit Host-Header (Hairpin). Bericht nach dem Schema in `fleet-rollout.md`. Fertig ist der Rollout erst, wenn jede Instanz im Zielumfang einen Status hat.

```bash
docker --context customer-<slug> service inspect customer-<slug>_api \
  --format '{{.Spec.TaskTemplate.ContainerSpec.Image}}'
docker --context customer-<slug> service ls     # dauerhafte Services 1/1; One-shot aoi-* 0/1 Complete ist korrekt
curl -sk -H "Host: <slug>.ki.actago.de" https://<vm-ip>/health
```

## Invarianten

- Build once, promote immutable: Prod bekommt nur Tags aus der Registry, nie `:latest`, nie einen `branch-`-Build auf Bestandskunden.
- Kunden-Deploys laufen über `promote.sh <slug> <tag>` bzw. Panel-Jobs, nie `deploy-customer.sh` direkt gegen den `prod`-Context.
- Die Flotte ist kein Einheitsstand. Gewollte Abweichungen bleiben: bewusst gewählter älterer Stable, `CODEAPI_RELEASE_MIGRATION=hold`/`PRESIDIO_RELEASE_MIGRATION=hold`, Slug-Templates, Branch-Instanzen, Benchmark auf Staging-Stand. „Alle gleich" nur, wenn der Nutzer genau das beauftragt, und dann mit Ausnahmeliste.
- Templates in `deploy/templates/` sind **nicht** release-gegated: Sie wirken bei jedem Deploy aus dem mgmt-Checkout, und der folgt `main` automatisch. Ein gemergter Template-PR erreicht damit den nächsten Kunden-Deploy, auch vor einem Release. Neues Image vor Template, das das Image voraussetzt (sonst Config-Fehler bzw. Chat-400). `deploy-customer.sh` prüft die YAML gegen das Ziel-Image (`validate-librechat-config.sh`); den Check nicht umgehen.
- Rollback bevorzugt über `rollback_customer_vm`; manueller Weg mit ausdrücklichem Presidio-Migrations-Skip und Prüfung weiterer Nebenwirkungen, siehe `fleet-rollout.md`. Für Neukunden den vorherigen Stable per Pin `hold` nur im beauftragten Umfang festhalten.
- Monitoringabdeckung live klären; sie ersetzt keine zielbezogene Rollout-Abnahme. Der Flottenworker versucht ein Zabbix-Wartungsfenster; Erfolg/Warnung im Bericht berücksichtigen.

## Fallen

- Build scheitert nach Sekunden mit „parent snapshot does not exist" → BuildKit-Cache korrupt (Vorgehen `docs/TROUBLESHOOTING.md` §5). Root-Disk voll killt Builds.
- „HTTP-Smoke … fehlgeschlagen: https://…ki…" von mgmt → Hairpin, kein echter Fehler; extern immer `--resolve <host>:443:192.168.15.100` bzw. VM-IP + Host-Header.
- Deploy bricht mit „librechat.yaml ist mit <Image> nicht kompatibel" ab → Ziel-Release älter als Template (`docs/TROUBLESHOOTING.md` §9a).
- Fleet-Gate meldet belegten Deploy-Lock, obwohl nichts läuft → verwaister Prozess mit `promote.sh`/`deploy-*.sh` in der Kommandozeile (historisch 08/2026; `GET /api/v1/overview` → `activeRuns`). Fremde Prozesse nur nach Rückfrage beenden.
