# Herkunft, geprüfter Stand und Grenzen

Stand: 2026-11-17. Nur Quellen gelesen; kein SSH, kein Request an den Receiver, kein Dienstneustart, keine Partnerdoku erzeugt, kein Fetch, keine Änderung an Quellrepo oder aktiver Installation.

## Ausgangsskill

Persönlicher Claude-Skill `actaone-provisioning-webhook` (Ordner enthält nur `SKILL.md`, Änderungsdatum 31.07.2026, beschreibt den Vertrag „Stand `5ce8b18`“). Keine Lizenzdatei; vom Nutzer für actago-Arbeit geschrieben, Nutzungsrechte folgen dem internen actaOne-Kontext. Hash des Ausgangsstands: [source-manifest.json](source-manifest.json).

## Geprüfte Quellverträge

actaOne (`github.com/actago/actaOne`, intern), gelesen auf `origin/main` `73ce7d4` (13.11.2026); der lokale Checkout-`HEAD` `dd0a334` liegt dahinter. Letzte Änderung am Receiver-Code: `2c5778b` (PR #405). Gekürzte Blob-IDs:

| Datei | Blob | Verwendung |
|---|---|---|
| `provisioning/webhook-receiver/index.js` | `8545af491522` | Validierung, Routing, Freigabe, Antwortcodes, Shutdown/SIGHUP, Access-Log |
| `provisioning/webhook-receiver/partners.js` | `8c9afd16d158` | Partner-Signatur, Bindung, Ratenlimit, Konfliktprüfung |
| `provisioning/webhook-receiver/openapi.yaml` | `89d91a752502` | Spec-Stand und Lücken |
| `provisioning/webhook-receiver/README.md` | `1f54f08f9648` | Ablauf, Partner-Test „auf dem Clone“, veraltetes Beispiel |
| `provisioning/webhook-receiver/webhook-receiver.service` | `7686a1af53a4` | Repo-Unit (nennt `User=deploy`, abweichend von der Rolle) |
| `infra/roles/webhook_receiver/templates/webhook-receiver.service.j2` | `fe72b67623c4` | `Restart=on-failure`, `KillSignal=SIGTERM`, `WorkingDirectory` |
| `infra/roles/webhook_receiver/defaults/main.yml` | `342f44ae1280` | Default-User `actaone`, Staging-Defaults |
| `infra/roles/webhook_receiver/templates/webhook-receiver.env.j2` | `5ef8207aa749` | Env-Schlüssel |
| `infra/roles/webhook_receiver/tasks/main.yml` | `fd9e6423a354` | `/opt`-Installation `root:<gruppe> 0755` |
| `infra/group_vars/all/webhook_receiver.yml.example` | `736971695d61` | Beispielwerte staging |
| `infra/roles/ops_dashboard/tasks/main.yml` | `47332bb8a95a` | Caddy-Matcher `@provision`, `@provision_ext` |
| `docs/PARTNER_PLATFORM_OPERATIONS.md` | `a14359cf1362` | Partnerkonfiguration |
| `docs/RELEASE_PROCESS.md` | `4d0cd3c9bb1a` | Partner-Release-Pin |

## Abweichungen vom Ausgangsskill (JAST-Änderungen)

- **`review_approved`**: Ausgangsskill beschrieb, dass das Feld von außen das Review umgeht. Inzwischen löscht `handleWebhook` es beim Eingang. Warnung durch historischen Hinweis ersetzt; Streichung aus Partnerdoku beibehalten.
- **Vertrag**: `schema_version` 1 **oder 2** (CRM), neuer Typ `contract_upload`, `contract_status`, `invitation_scheduled_at`, `contract`, `licenses`, `releaseTag`-Verbot, Slug `{1,56}` ohne `branch-` (vorher `{1,39}`), Körper 8 MiB (vorher 1 MiB). In [payload-contract.md](payload-contract.md) ausgelagert.
- **`contractStatus`**: nicht mehr allein aus `event_type`; explizites `contract_status` gewinnt.
- **`source`/`ttl_days`**: nicht mehr in der Spec, nur noch im README-Beispiel.
- **Partner**: Partner-Secrets, Bindung, `event_id`-Umschreibung, `403`, `409 customer_exists`, `429`, Partner-Review-Schalter neu.
- **Neustart**: `kill -9`-Weg beibehalten; ergänzt, dass `SIGTERM` sauber mit Exit 0 endet und dann nicht neu startet, sowie Secret-Reload ohne Neustart (60 s, `SIGHUP`) und Partnerkonfiguration je Anfrage.
- **Root-Zugang**: Satz „Root-Passwort hilft nicht / nicht mit su hantieren“ ersetzt durch Verweis auf den vorgesehenen Adminzugang (JAST-Skill `sudo-window`), weil die JAST-Sammlung inzwischen einen geregelten Weg beschreibt. Die `pam_faillock`-Warnung bleibt als Angabe des Ausgangsskills, nicht nachgeprüft.
- **Caddy**: Matcher enthält zusätzlich `method POST` und `remote_ip` der DMZ-Caddy; Verwaltung durch Rolle `ops_dashboard` ergänzt.
- **Test-Eingang**: „Es gibt keinen“ relativiert, weil die README einen Partner-Test auf einem Clone beschreibt; Existenz dort nicht geprüft.
- **Neu gefunden**: `cancel` ohne eigenen Verarbeitungszweig (siehe Payload-Vertrag); Spec-/README-Lücken.
- Struktur: Payload-Vertrag und Partnerdoku nach `references/` verschoben, damit `SKILL.md` die Betriebsfallen zuerst zeigt. Unveränderte Regeln: Testreihenfolge, Topologie-Falle, Tunnel für `/docs`, Signaturfehler Nummer eins, Häufige Fehler.

## Grenzen

- **Live-Zustand nicht geprüft**: `WEBHOOK_CUSTOMER_ENVIRONMENT=prod`, `DOMAIN_BASE`, gesetzte Schalter (`PURCHASE_AUTO_APPROVE`, `PARTNER_REQUIRE_REVIEW`), aktive Partner, ob `/opt` dem Repo entspricht und welcher User die Unit wirklich ausführt. Die Prod-Werte stammen aus dem Ausgangsskill (07/2026).
- Repo-Unit (`User=deploy`) und Rolle (`User=actaone`) widersprechen sich; welche live gilt, ist offen.
- `cancel`-Befund und Antwortcodes aus Codelesen, nicht aus Tests oder Requests.
- Control-Plane-Seite (Einladungsversand, CRM-Jobs) nur über Receiver-Kommentare und README erfasst.
- `evaluation.md` enthält Textszenarien, keinen ausgeführten Test.
