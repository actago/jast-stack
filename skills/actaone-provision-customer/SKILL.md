---
name: actaone-provision-customer
description: Lege actaOne-Kundeninstanzen über den freigabepflichtigen Webhook-/Job-Pfad an, prüfe eine laufende oder abgeschlossene Anlage oder baue eine Instanz nach ausdrücklichem Auftrag ab. Nutze bei Kunde anlegen/onboarden, Hotseat-Übernahme, „Instanz fertig?“, Archivieren oder Teardown.
---

# actaOne-Kunden anlegen, prüfen, abbauen

Weiterentwicklung des Projektskills `provision-customer` auf Basis von actaOne `origin/main`. Herkunft, Stand und Abweichungen: [references/sources.md](references/sources.md).

Voraussetzungen: actaOne-Checkout auf der Management-VM (laut Repo-Doku `ssh acta-mgmt`, Repo `~/actaOne`), Ops-Dashboard bzw. Deploy-Control-API mit eigener Operator-Identität, Docker-Contexts `customer-<slug>`/`prod`. Fehlt ein Zugang, lesend melden statt ersatzweise einen anderen Weg zu nehmen.

## Zuerst den Auftrag eingrenzen

Bestimme den beauftragten **Umfang**: Anlage, Statusprüfung, Lebenszyklus-Aktion (Archivieren/Freigeben) oder Teardown. Jeder Umfang ist eine eigene Freigabe; eine Anlage autorisiert weder Kundenmail noch Abbau, eine Prüfung keine Korrektur. Bei Wiederholungen nach Fehlern nach dem ersten unklaren Zustand stoppen und berichten.

Halte vorab fest: Slug, Firma, Kontakt-E-Mail, Plan, Kundentyp (direkt, Trial, Partner), gewünschtes Release (Standard oder ausdrücklich gewählter Stable) und wer die Gates freigibt. Slugs folgen im geprüften Code `^[a-z0-9][a-z0-9-]{1,56}$`; `branch-*` ist für Branch-Instanzen reserviert.

## Anlage über den Regelpfad

Kunden entstehen über signierten Webhook → Neukunden-Review → Deploy-Job → Worker. Ein direkter `deploy-customer.sh`-Lauf gegen den geteilten prod-Swarm ist ausgeschlossen (das Skript bricht ohne `customer-<slug>`-Context ab); der Weg ist `provision_and_deploy_customer_vm`.

1. **Release klären.** Ohne freigegebenen Stable bricht die Anlage ab. Die Job-Anlage friert den Release-Tag ein: Neukunden-Pin aus `release-pins.json` (gegen die Stable-Registry geprüft), sonst neuester Stable; Broker-Aufträge zusätzlich nur mit Tag aus der Broker-Freigabeliste. `deploy/RELEASE` ist nur informativ. Release-Fragen gehören zu `cut-release`.
2. **Auslösen.** Normalfall Platform-Panel „Neuer Kunde“ oder Ops-Dashboard-Assistent (Einzel/Bulk; Bulk legt pro gültigem Eintrag einen Job an und meldet übersprungene). CLI: `bash scripts/trigger-deploy.sh <slug> "<Firma>" <kontakt@kunde>` – Firma und Kontakt immer ausdrücklich übergeben, die Skript-Defaults sind Platzhalter bzw. eine interne Adresse. Das Skript **gibt Gate 1 selbst frei**, wartet auf `vault_published` und legt den Job an; nur nutzen, wenn diese Freigabe zum Auftrag gehört.
3. **Gate 2 freigeben.** Job `provision_and_deploy_customer_vm · customer-<slug>` im Dashboard prüfen: Release-Tag, Auth-Modus (`customerAuth`), Termin. Vier-Augen ist die dokumentierte Betriebsregel; die API erzwingt Approver ≠ Requester im geprüften Stand nur für den Traefik-Flottenrollout. Eigene Aufträge daher nicht selbst approven, außer der Nutzer weist es für genau diesen Job an.
4. **Worker beobachten.** Ablauf: Broker-Vorprüfung → Hotseat-Claim → ggf. Klon → Gateway-Keys → `promote.sh <slug> <eingefrorener Tag>` → Perimeter-Route → Exporter-Heartbeat → CP-Tenant `active`. Details zur Übernahme: [references/hotseat-uebernahme.md](references/hotseat-uebernahme.md).
5. **Verifizieren** nach [references/verifikation.md](references/verifikation.md). „Job succeeded“ allein ist kein Abschluss.
6. **Owner-Einladung** („Einladung zur Instanz senden“ bzw. `reissue_owner_invite`) ist eine Kundenmail und nur mit ausdrücklichem Auftrag auszulösen. Erster Microsoft-Login über den Link macht den Kontakt zum Instanz-Admin; danach lädt er Kollegen ein (invite-only).

Läuft die Anlage schief: Job-Notizen und Stage lesen, dann `diagnose-instance`. Häufige Muster: Refresh-403-Loop bei `pending` Instanz-Tenant, leeres 401 am Invite-Link, Sequence-409 bei wiederverwendetem Slug (`docs/TROUBLESHOOTING.md` §1–3).

## Lebenszyklus und Abbau

Nur nach ausdrücklichem Auftrag für genau diese Instanz, siehe [references/lebenszyklus.md](references/lebenszyklus.md). Kurz: Archivieren ist der umkehrbare Weg (Dienste auf 0, Perimeter-Hinweisseite), Teardown löscht die VM mit Datenträgern. Teardown über den Job `teardown_customer_vm` mit `confirm=<slug>`, weil nur der Job-Pfad Kunden-Auth/Broker und Gateway-Keys widerruft.

## Bericht

Nenne Slug, Umfang, Release-Tag, Hotseat oder Klon (VMID), Job-ID und Freigebende, welche Prüfungen gelaufen sind und welche offen bleiben (z. B. Owner-Login noch `pending`). Keine Secrets, Tokens oder Einladungslinks ausgeben.
