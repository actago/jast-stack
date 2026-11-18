# Herkunft, geprüfter Stand und Grenzen

Stand: 2026-11-17. Nur Quellen gelesen; keine SSH-/API-Aufrufe, keine Jobs, kein Deploy, kein Fetch, keine Änderung an Quellrepos oder aktiven Installationen.

## actaOne-Repo (`github.com/actago/actaOne`)

Lokaler Checkout-`HEAD` `dd0a3347b23e` liegt hinter `origin/main`. Gelesen wurde **`origin/main` = `73ce7d4ccdb5`** (Commit 2026-11-13). Ein lesendes `git ls-remote` am 2026-11-17 zeigte denselben Commit als Remote-`main`; der gelesene Stand war damit zum Prüfzeitpunkt aktuell. Hashes = gekürzte Git-Blob-IDs auf diesem Commit.

| Datei | Blob | Verwendung |
|---|---|---|
| `.claude/skills/provision-customer/SKILL.md` | `9c55bb74fb55` | Ausgangsskill (zwischen `HEAD` und `origin/main` unverändert): Wege A/B, Gates, Verifikation, Fallen, Teardown |
| `CLAUDE.md` | `d1cf1df520cf` | Kunden-Lebenszyklus, Assistenten, Lizenzaktionen, Backup-Stand 10/2026, Hairpin |
| `docs/CUSTOMER_ONBOARDING.md` | `0ee92c531f45` | Regelpfad, Neukunden-Pin, Zugangsregeln, Invite-Verhalten |
| `docs/HOTSEATS.md` | `670754ac4e6c` | Claim, gemeinsames VM-Band, Vorwärmen, RAM-Policy, SSH-Hostkey-Recovery |
| `docs/AUTH_BROKER_CUSTOMER_ONBOARDING.md` | `30dbd273f05f` | Broker als Neukunden-Standard, Release-Allowlist, `pending`, Widerruf beim Teardown |
| `docs/PROD_VM_PER_CUSTOMER.md` | `953494dc5427` | Manueller Fallback (siehe Abweichungen) |
| `docs/TROUBLESHOOTING.md` | `952306a5efec` | §1 Refresh-403, §2 Invite-401, §3 Sequence-409 |
| `scripts/trigger-deploy.sh` | `0c64741a9d6b` | Gate-1-Selbstfreigabe, Defaults, Job-Anlage |
| `scripts/claim-hotseat.sh` | `6c3a2be43d0f` | Übergabeschritte, RAM, Exit 3 |
| `scripts/teardown-customer-vm.sh` | `533a35bf2c4b` | Abbauschritte inkl. CP-Bereinigung und Reconcile |
| `scripts/teardown-customer.sh` | `3d134257dcf3` | Abgrenzung: alter Shared-Swarm-Pfad |
| `scripts/cleanup-platform-registrations.sh` | `572e0f9ef1ea` | Schutzliste, idempotente CP-Bereinigung |
| `scripts/deploy-customer.sh` | `60fdf754a674` | Abbruch ohne Kunden-Context, `:latest`-Sperre |
| `provisioning/deploy-control-api/index.js` | `a5ff1f53c391` | Slug-Muster, Release-Auflösung, `confirm`-Pflichten, Auto-Approve-Liste, Bulk-Endpunkt, `approveJob` |
| `provisioning/deploy-control-api/job-worker.js` | `65b0949be6bc` | `acquireInstanceVm`, `allocateVm`, Ablauf von Anlage und Teardown, Archiv-Stack-Funktionen |
| `agent/hermes/skills/actaone-core/references/{customer-onboarding,hotseats}.md` | `be66c58d8433`, `f6c6d67e5cab` | Nur verglichen: ältere Kopien der Docs (08/2026), keine eigenständige Quelle |

Existenzprüfungen: `scripts/warm-hotseats.sh`, `scripts/reconcile-hotseats.sh`, `scripts/provision-customer-vm.sh`, `scripts/new-customer.sh`, `scripts/publish-caddy-route.sh`, Webhook-Receiver-Slugmuster.

## Abweichungen vom Ausgangsskill

- Slug-Muster: Ausgangsskill `{1,39}`; Webhook-Receiver, API und Skripte prüfen `{1,56}`. Ob das Panel enger begrenzt, wurde im LibreChat-Fork nicht geprüft.
- Dienstanzahl: Ausgangsskill erwartet 13, Docs nennen 12; durch Overlays variabel. Jetzt: Soll-Replicas je Dienst statt fester Zahl.
- Teardown: Ausgangsskill ruft das Skript direkt und verlangt danach manuelles CP-Löschen. Jetzt Job `teardown_customer_vm`, weil nur dieser Auth-/Broker- und Key-Widerruf ausführt; CP-Bereinigung macht das Skript selbst.
- Claim-Fallback: ein älterer Code-Kommentar nennt „Fehler → Klon“; der geprüfte Code fällt nur bei Exit 3 zurück.
- Release: Neukunden-Pin aus `release-pins.json` und Broker-Allowlist ergänzt; Job friert den Tag bei Anlage ein.
- `trigger-deploy.sh` gibt Gate 1 selbst frei und hat eine interne Default-Kontaktadresse; im Skill ausdrücklich gemacht, Adresse nicht übernommen.
- Vier-Augen: im API-Code nur beim Traefik-Flottenrollout erzwungen; als Betriebsregel beibehalten.
- Invite-Prüfung: Ausgangsskill nutzt einen echten Token; die API gibt Links nicht aus. Jetzt tokenlose Prüfung.
- Neu: Archivieren als umkehrbare Alternative, Broker-Status, Backup-Vorprüfung vor Teardown.
- `PROD_VM_PER_CUSTOMER.md` §Manueller Flow pinnt mit `deploy/RELEASE` und widerspricht damit dem Stable-Gating im selben Dokument; nicht übernommen.

## Grenzen

- Kein Live-Abgleich: Pool-Belegung, Pins, Broker-Schalter, Dashboard-Oberfläche und tatsächliche Freigabepraxis sind nicht geprüft.
- Panel-Code (LibreChat-Fork) und `new-customer.sh`-Interna nicht im Detail gelesen.
- Keine Anlage, kein Teardown und keine Job-Freigabe zur Prüfung ausgeführt. `evaluation.md` enthält Textszenarien, keinen Test.
