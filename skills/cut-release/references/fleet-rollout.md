# Rollout auf einen beauftragten Zielumfang

Lesen, wenn ein freigegebener Stable auf mehr als eine Bestandsinstanz soll oder gefragt wird, ob ein Rollout vollständig war. Grundlage: `docs/RELEASE_PROCESS.md` („Produktion: gegatete Promotion", „Hotfix-Release" Schritt 8), `docs/operations/service-rollout-policy.md` und der Flotten-Pfad in `provisioning/deploy-control-api/job-worker.js` (Stand siehe [sources.md](sources.md)).

## 1. Ziel-Tag festlegen

- Tag aus der Registry nehmen (`GET /api/v1/releases/history` bzw. `/approved?releaseTag=`), nicht aus dem Candidate und nicht aus `deploy/RELEASE`. Wählt der Nutzer einen älteren freigegebenen Stable, diesen verwenden.
- Ist der Tag nicht in der Registry: stoppen und melden. Der geprüfte Panel-Flottenworker akzeptiert nur den neuesten Registry-Stable; ein älterer Tag kann bei Jobanlage akzeptiert werden und erst im Worker scheitern. Für ältere oder gemischte freigegebene Ziel-Tags Einzel-Promotes verwenden. Je Instanz den Ziel-Tag festhalten. Ändert sich der aktuelle Stable seit Jobfreigabe, bricht der Flottenworker ebenfalls ab.

## 2. Zielliste aus dem Live-Stand bilden

Nicht aus dem Gedächtnis oder einer alten Liste. Auf mgmt:

```bash
docker context ls --format '{{.Name}}' | grep '^customer-'
docker --context customer-<slug> service inspect customer-<slug>_api \
  --format '{{.Spec.TaskTemplate.ContainerSpec.Image}}'
```

Jeden Context genau einer Klasse zuordnen und die Klasse im Bericht nennen:

| Klasse | Vorgabe |
|---|---|
| Ziel | im Auftrag enthalten, läuft auf dem vorherigen Stable oder einem älteren regulären Tag |
| Ausnahme | bewusst nicht anfassen, mit Grund (Kunden-Hold, eigener Stand, Kundenwunsch, Slug-Template-Entscheidung offen) |
| Nicht im Umfang | `warm<n>` (Hotseats, ziehen über die Freigabe nach), `branch-*`, `staging`, `benchmark`, Labs, Infra-Contexts ohne `_api` |
| Nicht erreichbar / gestoppt | kein Inspect möglich; nicht als „ok" zählen, separat melden |
| Bereits auf Ziel | nur „fertig", wenn Image, erforderliche gerenderte Template-/Config-Version und beauftragte Funktion passen und keine beauftragte Release-Migration offen ist |

Benchmark, Hotseats und Branch-Instanzen werden nur aktualisiert, wenn der Nutzer sie ausdrücklich einschließt. Vor jedem einzelnen Promote den Live-Tag erneut prüfen.

## 3. Vorprüfungen

- Kein laufender Deploy, kein fremder Test-Hold auf Staging, `PAUSE`-Status bekannt.
- Werden Images vorab auf alle VMs gezogen: Ceph-Füllstand (`ceph df` auf einem pve-Node). Frei sein müssen mindestens Zielanzahl × ~14 GiB logisch; ein voller Pool legt die ganze Flotte lahm.
- Template-Stand im mgmt-Checkout passt zum Ziel-Tag (siehe Invariante „Templates nicht release-gegated" im SKILL.md). Slug-Templates ersetzen die Standardvorlage vollständig und erben deren Änderungen nicht.
- Release-gekoppelte Vault-Schalter geklärt ([sonderfaelle.md](sonderfaelle.md)).
- Jeder Promote veröffentlicht das Kunden-Bundle, ergänzt zulässige fehlende Defaults und kann Presidio-/CodeAPI-Migrationen ausführen. Diese Wirkungen gegen Auftrag, Release-Vertrag und Holds prüfen; ein gleicher Image-Tag macht den Aufruf nicht wirkungslos.
- Gleicher Tag bei neuen Templates: tatsächlichen `aoi-lc`-Inhaltshash gegen den für diese Instanz erwarteten neu gerenderten Stand prüfen, ohne Env/Secrets auszugeben. Renderprüfung nur mit dafür vorgesehenem nebenwirkungsarmem Pfad; bei fehlendem Sollnachweis nicht „bereits fertig“ melden. Unterschiedliche Kundenwerte können unterschiedliche korrekte Hashes ergeben.

## 4. Canary

Eine Instanz aus der Zielliste, die den realistischen Fall abdeckt und keinen lokalen Sonderstand trägt. `promote.sh <slug> <tag>` (mit `ACTAONE_KEY_VAULT_CONFIG` der Prod-Umgebung) oder Panel-Einzeljob `promote_customer_vm`. Abnahme: Nachweis aus SKILL.md plus die fachliche Prüfung, wegen der das Release gemacht wurde (z. B. RAG-Frage, Dokumenterstellung, neues Modell im Picker). Erst nach grünem Canary weiter, sofern der Nutzer nicht ausdrücklich anders entschieden hat.

## 5. Wellen

Zwei Wege, beide seriell:

- **Einzeln per `promote.sh`:** hält eine globale Deploy-Sperre, ca. 4–5 min je Instanz. Lange Serien detached auf mgmt starten (`setsid nohup … &`, Log in Datei), nicht über eine Laptop-SSH-Sitzung. Je Instanz auf „Deployed und verifiziert" im Log und den Live-Tag prüfen. **Beim ersten Fehler anhalten** und Ursache klären.
- **Panel-Job `promote_all_customers`** nur für den neuesten Stable, mit eingefrorenem `targetSlugs`: nimmt nur existierende `customer-*`-Contexts, schließt `warm<n>`, `branch-*` und Contexts ohne `_api` selbst aus. Er **läuft nach Fehlern weiter** und meldet am Ende `promoted/skipped/failed`. Er **überspringt** Instanzen, deren api-Image den Ziel-Tag schon trägt, außer eine Presidio- oder CodeAPI-Release-Migration ist offen. Reine Template-/Vault-Änderungen brauchen dann einen passenden Einzel-Redeploy, etwa `promote.sh` auf denselben Tag oder den geprüften `redeploy_customer_vm`-Pfad. `promote_customer_vm` lehnt im geprüften Stand einen bereits gefahrenen Ziel-Tag ab und ist dafür kein Ausweg.

Der Flottenworker versucht ein Zabbix-Wartungsfenster anzulegen. Erfolg oder Warnung im Jobbericht ausweisen; eine erfolgreiche Anlage beweist keine vollständige Monitoringabdeckung und ein Fehlschlag darf nicht als gesetztes Fenster berichtet werden.

Wellengröße und Pausen bestimmt der Nutzer oder das Risiko des Releases. Ein Jobantrag braucht die Freigabe im Panel; der Agent genehmigt nur, wenn genau diese Freigabe zum Auftrag gehört.

## 6. Rollback und Abbruch

- Einzelinstanz: bevorzugt geprüfter Panel-Pfad `rollback_customer_vm`; dieser setzt `ACTAONE_PRESIDIO_RELEASE_MIGRATION=skip`. Bei beauftragtem manuellem Rollback diese Option explizit für `promote.sh <slug> <vorheriger-tag>` setzen, damit der Rückweg nicht zugleich eine neue Presidio-Umstellung auslöst. CodeAPI- und Vault-Auswirkungen anhand des Ziel-Releases prüfen. Release-gekoppelte Schalter unterliegen weiterhin ihren Riegeln; siehe `sonderfaelle.md`.
- Neukunden: vorherigen Stable per Pin `hold` halten.
- Laufenden Panel-Job nicht durch Prozess-Kill abbrechen, ohne die Folgen zu kennen (verwaiste Jobs, belegter Lock); Vorgehen mit dem Nutzer klären.

## 7. Paritätsprüfung (nur wenn gefragt)

„Haben jetzt alle denselben Stand?" bezieht sich auf den Zielumfang, nicht automatisch auf alle Contexts. Vergleichen gegen eine benannte Referenzinstanz:

- Image-Tag aller Stack-Services (nicht nur `_api`).
- Name der `librechat.yaml`-Swarm-Config (`aoi-lc-<slug, max. 16 Zeichen>-<sha8(slug)>-<sha16(inhalt)>`): gleicher Inhalts-Hash = gleiche gerenderte YAML.
- Erwartete Modelle, Feature-Schalter und Fähigkeiten, die das Release einführt (z. B. Modellliste, OCR, Marketplace, Presidio-Ziel). Werte nur als vorhanden/abweichend berichten, Secrets nie ausgeben.

Unterschiede einordnen: gewollt (Ausnahme), Release-bedingt offen (Nachzügler), Drift. Für die Ursachenanalyse von Drift ist eine eigene lesende Diagnose sinnvoll (Template ↔ Vault ↔ Runtime); Behebung vault-first, nicht per Live-`service update`.

## 8. Abschlussbericht

```
Ziel-Tags: <slug -> tag, Registry-Eintrag und Freigabe je verwendetem Tag>
Zielumfang: <n> Instanzen, eingefroren am <Zeit>, Quelle: Live-Inspect
Canary: <slug> – <Ergebnis, fachliche Prüfung>
Ergebnis: <x> promotet · <y> bereits auf Ziel · <z> fehlgeschlagen (<slugs>, Ursache)
Ausnahmen: <slug> – <Grund>
Nicht im Umfang: Hotseats / branch-* / staging / benchmark / Labs (Anzahl)
Nicht erreichbar/gestoppt: <slugs>
Offen: Nachzügler, Template-Nachzug, Vault-Schalter, Pins
Nicht geprüft: <was ausdrücklich nicht verifiziert wurde>
```

## Historische Erfahrungen (nicht als aktuelle Befehle verwenden)

- 10/2026: Ein Agent meldete einen Rollout als vollständig, prüfte aber nur die Rollout-Ziele, nicht Hotseats, Branch-Instanzen und gestoppte VMs. Deshalb die Klassen oben.
- 09/2026: Nach Template-Nachzug mitten im Rollout hatten die zuerst promoteten Instanzen das neue Image, aber die alte Modellliste; der Flottenjob übersprang sie wegen gleichen Tags.
- 07/2026: Parallele Promotes scheiterten an Docker-Hub-Limits für Fremd-Images und an geteiltem Perimeter-Zustand. Der heutige Repo-Vertrag ist seriell; Parallelisierung nur, wenn das Repo sie ausdrücklich vorsieht.
