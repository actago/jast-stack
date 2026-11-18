---
name: diagnose-instance
description: Root-Cause-Diagnose für actaOne-Kundeninstanzen, Staging und die Deploy-Pipeline – Login-/SSO-Fehler, Deploy hängt oder failed, Instanz unhealthy oder extern nicht erreichbar, Funktion fehlt nach Redeploy (Konfigurationsdrift Template/Vault/Runtime), Dokumenterstellung oder Bildgenerierung bricht ab, konkreter Chat-/Share-Link mit Fehler. Nutzen bei "Kunde kommt nicht rein", "Deploy hängt", "Instanz down", "Feature weg", "warum ist X auf Instanz Y anders", "was ist in diesem Chat schiefgelaufen".
---

# Instanz- und Pipeline-Diagnose (actaOne)

Weiterentwicklung des gleichnamigen actaOne-Projektskills. Herkunft, geprüfter Stand und Grenzen: [references/sources.md](references/sources.md).

## Voraussetzungen

- **actaOne-Repo** (`github.com/actago/actaOne`) mit `docs/TROUBLESHOOTING.md` ist die maßgebliche Fallsammlung. Finden: aktuelles Arbeitsverzeichnis oder ein Checkout mit `origin` auf `actago/actaOne`; sonst nachfragen. Fehlt es, das melden und nur mit den Mustern hier arbeiten, gekennzeichnet als ungeprüft gegen den Repo-Stand.
- Für Live-Checks: Management-VM (laut Repo-Doku `ssh acta-mgmt`) mit Docker-Contexts `customer-<slug>`, `prod` (Control-Plane), `staging`. Zugang lesend bestätigen. Für Code-Ursachen den LibreChat-Fork (`github.com/actago/LibreChat`) bzw. das betroffene Service-Repo.

## Arbeitsweise

Symptom → Verdacht → gezielter lesender Check → Ursache mit Beleg. Ein Diagnoseauftrag erlaubt Lesen im genannten Umfang. Korrekturen nur, soweit der Nutzer sie beauftragt hat; eine bereits erteilte Fix-Erlaubnis gilt für diesen Fix, nicht für Folgeaktionen (neue Einladung, Redeploy weiterer Instanzen, Vault-Publish). Live-`service update` überlebt keinen Redeploy; dauerhafte Fixes laufen über Vault oder Template.

Ergebnis: Ursache, Beleg (Fehlerklasse, betroffener Dienst, Zeitpunkt und redigierte technische Metadaten), was korrigiert wurde oder was zu tun wäre, was nicht geprüft ist. Logs können Secret-Werte, Nachrichten und personenbezogene Angaben enthalten. Nur das benötigte Zeitfenster lesen und vor jeder Tool-Ausgabe auf erlaubte technische Felder reduzieren; keine ganzen Logzeilen als Standardbeleg ausgeben. Ungeprüfte Rohlogs nicht in Chat, PR oder Memory übernehmen.

## Mehrere Instanzen gleichzeitig betroffen

Hängen ops, Staging und Kunden zugleich: zuerst `ceph -s` und `ceph osd df` auf einem pve-Node. Ein voller Pool sieht von außen wie ein Netz- oder Caddy-Ausfall aus. Notfallschritte stehen in `CLAUDE.md` des actaOne-Repos; sie sind Mutationen.

## Login und SSO

- `api/auth/refresh 403` + `api/endpoints 401`, Nutzer hängt im Loop → Instanz-Tenant-Dokument `pending`. Check: `db.tenants.findOne({tenantId})` in der Instanz-DB. Fix: `status:'active'`, `onboardingCompletedAt` (betrifft alte/halbe Instanzen; Deploy seedet heute `active`).
- SSO-Klick → sofort leeres 401 ohne App-Log → Invite-Link-Query als Callback missverstanden. Check: `/oauth/openid` ohne Query = 302, mit `?invite=` = 401. Fix im Fork (`stripAuthInitQuery`): Instanz auf einen aktuellen Stable bringen (Release-Ablauf, nicht hier).
- „A valid invitation is required" → invite-only greift (für Kunden-Domains korrekt). Interne Domains laufen über `TENANT_INVITE_EXEMPT_DOMAINS`; prüfen, ob gesetzt.
- Microsoft-Login gelingt, Rücksprung landet wieder auf Login, Log `was registered with "local" provider` → lokaler Account, kein Auto-Linking (`docs/TROUBLESHOOTING.md` §10). Der dortige Fix entfernt den Passwort-Fallback; nur mit Auftrag für genau dieses Konto.
- Lokal angelegter User: Login 500 „No user provided" → `tenantId` fehlt am User.

Eine fehlerhafte Einladung zu diagnostizieren heißt nicht, eine neue zu versenden.

## Exporter, Platform, Control-Plane

- Exporter scheitert <1 s → oft 409 sequence-stale (alte `platformexportevents` einer wiederverwendeten instanceId). Check: Count für die instanceId in der CP-DB. Fix: Provisioning-Purge bzw. Events + `lastSequence` zurücksetzen (Mutation der CP-DB).
- Instanz bleibt in Platform `pending` trotz Deploy → Heartbeat kommt nicht an oder Tenant-Auto-Aktivierung greift nicht: Exporter-Logs und CP-Eventpfad prüfen.

## Deploy hängt oder failed

- Build nach Sekunden „parent snapshot does not exist" → BuildKit-Cache kaputt (`docs/TROUBLESHOOTING.md` §5). Root-Disk voll killt Builds: `df -h /`.
- „HTTP-Smoke … fehlgeschlagen: https://…ki…" von mgmt → Hairpin, kein echter Fehler. Extern prüfen mit `--resolve <host>:443:192.168.15.100` oder `curl -sk -H 'Host: <domain>' https://<vm-ip>/health`.
- „librechat.yaml ist mit <Image> nicht kompatibel" → Template kennt Felder, die das Ziel-Release nicht kennt (§9a): neueren Stable bzw. Neukunden-Pin wählen, den Check nicht umgehen.
- Job ewig `running` ohne Deploy-Kindprozess → Worker verwaist (Neustart mitten im Job). Orphan-Sweep markiert beim Start `failed`; Deploy bewusst als Redeploy neu anstoßen (idempotent). Deploy-Control-Playbooks nie während laufender Jobs anwenden.
- Fleet-Gate „globaler Deploy-Lock belegt", obwohl nichts läuft → Prozess mit `promote.sh`/`deploy-*.sh` in der Kommandozeile (auch eine verwaiste Warteschleife) hält `activeRuns` belegt. Authentifiziert `GET /api/v1/overview` lesen. Beenden nur nach Rückfrage.
- Job-Anlage scheitert mit 403 `mutations_disabled` / 401 `operator_required` / 503 `release_pins_unreadable` bzw. `release_registry_unavailable` → Rechte, Operator-Header oder kaputte Zustandsdatei, kein Kundenproblem.
- Kunden-Stack auf dem `prod`-Swarm → fehlender `customer-<slug>`-Context (harter Guard verhindert das heute). Alt-Stack-Reste nur nach Bestätigung entfernen.

## Extern nicht erreichbar

- `000`/weiße Seite → Perimeter-Route fehlt oder Caddyfile invalide. DMZ-Caddy (192.168.15.100, `/opt/dmz-revproxy/Caddyfile`) lesend prüfen; Drift-Status liefert `scripts/caddy-drift-check.sh` (read-only, `render-caddy-routes.sh --diff`). Route neu publizieren (`publish-caddy-route.sh`) ist eine Mutation am geteilten Perimeter; Ziel ist die VM-IP der Instanz.
- Erreichbarkeit nie von mgmt über die öffentliche Domain testen (Hairpin): `curl -sk https://<vm-ip> -H 'Host: <domain>'`.

## Funktion fehlt oder Konfiguration „wirkt nicht"

Feature nach Redeploy weg, Instanz verhält sich anders als Staging oder die Nachbarinstanz, Bildgenerierung bricht sofort ab (`No plugin auth …` im api-Log), neues Modell fehlt: lesende Drift-Diagnose nach [references/config-drift.md](references/config-drift.md). Behebung vault-first bzw. per Template-PR, dann Redeploy der betroffenen Instanz.

## Dokumenterstellung oder Code-Ausführung scheitert, Health grün

- Zuerst ausschließlich die nicht geheimen `LIBRECHAT_CODE_BASEURL`- und `CODEAPI_RELEASE_MIGRATION`-Felder im laufenden `_api`-Service lesen; keine vollständige Service-Spec/Env ausgeben. Soll aus Live-Release, `scripts/codeapi_release.py`, Release-Metadaten und Instanzpolicy ableiten. Eigene Backend-URLs und Holds bleiben bewusst bestehen; Releases vor dem erforderlichen Fork-Commit `507cfed` benötigen den alten Pfad. Eine ältere 3112/3114-URL allein ist kein Driftbeleg.
- `DOC_INFRA_UNAVAILABLE`/`DOC_INFRA_TIMEOUT` und `[CodeApiInfra] upload failed` im api-Log → CodeAPI-Infrastruktur, nicht das Dokument.
- Repo-Prüfung des Dokumentpfads: `scripts/verify-customer-document-runtime.sh` (vor Ausführung lesen, was es anlegt).

## Ein konkreter Chat oder Share-Link

Nur wenn der Nutzer eine bestimmte Unterhaltung mit Supportanlass untersuchen lässt: [references/chat-diagnosis.md](references/chat-diagnosis.md). Eine URL allein erlaubt keine Durchsicht weiterer Chats oder Nutzer.

## Grundchecks

```bash
docker --context customer-<slug> service ls
free -m   # in der VM: echte Last = MemAvailable + Swap, nicht "used"
```

Env-/Logausgaben nur über feldbegrenzte Projektionen nach [config-drift.md](references/config-drift.md). Für Logs Zeitfenster setzen und die Ausgabe im ausführenden Prozess auf Fehlerklasse/Zeitstempel begrenzen; `grep error` auf ganzen Zeilen ist keine Redigierung.
