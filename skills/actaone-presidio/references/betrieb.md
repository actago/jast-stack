# Presidio: Betrieb, Anbindung, Rollout und Rückweg

Befehle und Werte stammen aus `docs/operations/presidio-singleton.md` und `docs/rollouts/production-2026-11.md` im actaOne-Monorepo (`origin/main`, Stand siehe [sources.md](sources.md)). Vor Ausführung gegen die aktuelle Fassung dieser Dateien prüfen; bei Abweichung gilt das Repo.

## Inhalt

- Orientierung (datiert)
- Zentral oder lokal feststellen
- Gateway-Vertrag
- Singleton-Release und Skalierung
- Kundenanbindung im Prod-Release
- PKI und Zertifikate
- Rückwege
- Prüfskripte

## Orientierung (datiert)

Stand laut Runbook vom 06.11.2026 und Wissensbasis-Nachtrag vom 08.11.2026. Live bestätigen, bevor darauf gehandelt wird.

| | Staging-Singleton | Prod-Singleton |
|---|---|---|
| VM / Name | 315 `infra-presidio` | 318 `infra-presidio-prod` (anderer Proxmox-Node) |
| Endpunkt | `https://10.64.0.20:8443` | `https://10.64.0.21:8443` |
| TLS-Name | `presidio.infra.actaone.internal` | `presidio-prod.infra.actaone.internal` (+ IP-SAN) |
| Docker-Context auf mgmt | `customer-presidio` | `customer-presidio-prod` |
| Stack | `infra-presidio` (Analyzer, Anonymizer, Gateway) | `infra-presidio` |
| Profil | `deploy/presidio/environments/staging.env` | `deploy/presidio/environments/prod.env` |
| PKI im Prod-Vault | `presidio-ca`, `presidio-infra` | `presidio-prod-ca`, `presidio-prod-infra` |

Die generischen Secret-Namen `presidio-ca`/`presidio-infra` gehören historisch zum **Staging**-Singleton. Der Release auf beiden Singletons kann abweichen (Staging erhält neuere Erkenner zuerst); den laufenden Release aus dem Gateway-Service-Label lesen, nicht aus der Doku.

Widerspruch der Quellen: Das Runbook nennt im Kopf „Kunden noch lokal“ (06.11.), die Wissensbasis belegt ein Audit mit 77/77 umgestellten Zielen am 05.11. Für eine konkrete Instanz entscheidet nur die Live-Prüfung unten.

Bekannte Lücken laut Quellen: kein Autoscaler, kein Monitoring/Alarm auf Gateway-Kennzahlen, keine Ablaufüberwachung der Zertifikate, kein HA-Eintrag, Backup/Restore nicht nachgewiesen. Ein Ausfall eines Singletons betrifft alle angebundenen Instanzen.

## Zentral oder lokal feststellen

Reihenfolge der Belege, stärkster zuerst:

1. **Laufende Dienste der Instanz:** `docker --context customer-<slug> service ls`. Lokal: `presidio-analyzer` und `presidio-anonymizer` laufen. Shared: `presidio-gateway` (lokaler mTLS-Proxy) läuft, die lokalen NLP-Dienste fehlen bei `KEEP_LOCAL=false`. Beides gleichzeitig ist eine Beobachtungs- oder abgebrochene Umstellungsphase.
2. **Instanz-Vault-Bundle**, nur die nicht geheimen Schalter: in eine `0600`-Datei holen und ausschließlich `^PRESIDIO_(MODE|SHARED_ENDPOINT|SHARED_SERVER_NAME|KEEP_LOCAL|RELEASE_MIGRATION)=` anzeigen, danach die Datei löschen. Der Endpunkt verrät die Umgebung (Staging-Endpunkt an einem Prod-Kunden ist ein Befund).
3. **Ops-Dashboard / Fleet:** zeigt lokal/zentral und „abgewählt“ als Deploy-Soll. „Abgewählt“ beweist nicht, dass alte Dienste entfernt wurden; alte Deploys erscheinen als „Nicht erfasst“.
4. **Dokumente:** nur Stand ihres Schreibdatums.

## Gateway-Vertrag

- Erlaubte Routen, sonst 404: `POST /analyzer/analyze`, `GET /analyzer/health`, `POST /anonymizer/anonymize`, `GET /anonymizer/anonymizers`, `GET /anonymizer/health`.
- `ssl_verify_client on`; ohne gültiges Clientzertifikat HTTP 400.
- Admission-Limits je Clientzertifikat und gesamt, Werte aus dem Umgebungsprofil (`*_LIMIT_*`); darüber 429. LibreChat wiederholt nicht und bricht im Datenschutzmodus ab.
- Host-Firewall-Unit `actaone-presidio-firewall`: Port 8443 nur aus Loopback, Management- und Kundennetz. Keine öffentliche Caddy-/Traefik-Route.
- Gateway-Logs: eine JSON-Zeile je Request (Client-CN, Route, Status, Zeiten, Größen; nie Body, URI-Parameter oder Header). Auszählung je Client und Status:

```bash
docker --context customer-presidio-prod service logs --since 1h --raw infra-presidio_gateway \
  | python3 -c 'import json,sys,collections; c=collections.Counter((d["client"],d["status"]) for d in map(json.loads,(l for l in sys.stdin if l.startswith("{")))); print(c.most_common(20))'
```

Der Log-Aufruf oben gilt für Prod; für Staging `customer-presidio` verwenden. Bei einer einzelnen Instanz nach deren Client-CN und dem relevanten Zeitfenster filtern.

Lastverhalten: LibreChat analysiert je Instanz seriell in Fenstern von 2000 Zeichen (Queue-Schlüssel ist die Analyzer-URL). Lange Dokumente sind daher je Instanz langsam, unabhängig von der Singleton-Größe. „N Instanzen“ sind keine N gleichzeitigen Analysen; Kapazitätsaussagen nur aus gemessenen gleichzeitigen Requests ableiten.

## Singleton-Release und Skalierung

Auf mgmt aus einem Quellstand, der die Skripte enthält (aktueller Management-Checkout oder das Release-Quellverzeichnis):

```bash
umask 077; w=$(mktemp -d); trap 'find "$w" -type f -exec shred -u {} +; rm -rf "$w"' EXIT
# Staging: presidio-infra + staging.env; Prod: presidio-prod-infra + prod.env (beide im Prod-Vault)
ACTAONE_KEY_VAULT_CONFIG=/etc/actaone/key-vault-prod.env \
  bash scripts/keyvault-secrets.sh fetch <presidio-infra|presidio-prod-infra> "$w/tls.json" >/dev/null 2>&1
python3 scripts/deploy-presidio.py --env-file deploy/presidio/releases/<release>.env \
  --profile deploy/presidio/environments/<staging|prod>.env --tls-bundle "$w/tls.json"   # nur Plan
python3 scripts/deploy-presidio.py ... --apply                                             # gleicher Aufruf mit --apply
docker --context <customer-presidio|customer-presidio-prod> stack services infra-presidio
```

- Release-Dateien enthalten alle drei Images per Digest; `latest` wird abgelehnt. Analyzer/Anonymizer aus einem geprüften actago-Release, weil Upstream den `pseudonymizer` nicht enthält.
- `deploy-presidio.py` verweigert u. a. Reservierungen über Host-RAM, weniger als 2,5 GiB je Worker, Gesamtlimit unter Clientlimit, unbekannte Profilschlüssel, Größenwerte in der Release-Datei sowie fremden Zielhost/Context. Warnungen (CPU-Overcommit, Gesamtlimit über 2× Analyzer-Slots) im Bericht nennen.
- Der Apply-Aufruf reicht nur den Stack ein. Replikas abwarten und anschließend die Abnahme getrennt ausführen.
- Vergrößerung der VM erfordert einen Neustart und unterbricht alle angebundenen Instanzen; vorher Node-/Ceph-Reserve prüfen.

## Kundenanbindung im Prod-Release

Prod-Kunden werden im regulären `promote.sh` über `scripts/presidio-release-migration.sh` umgestellt, unter dem globalen Deploy-Lock:

1. **Plan:** nur wenn das Release-Manifest `activation: release` trägt, die Instanz im Prod-Vault liegt, der Slug ein Kunde ist (nicht `staging`, `prod`, `warm*`, `branch-*`, `infra-*`, `presidio*`, `codeapi-*`, Render-Lab) und das Bundle nicht `PRESIDIO_RELEASE_MIGRATION=hold` trägt. Abbruch vor jedem Publish bei Modus-Drift, doppelten Zeilen, eigenen lokalen URLs oder fremdem Endpunkt/TLS-Namen.
2. **Identität:** vorhandene Clientidentität nur wiederverwenden, wenn sie zu dieser Instanz und der Vault-CA passt; „fehlt“ nur bei bestätigtem `SecretNotFound`. Netz- oder Rechtefehler brechen ab.
3. **Env:** erst danach `PRESIDIO_MODE=shared`, Endpunkt, TLS-Name, Gateway-Pin, `PRESIDIO_KEEP_LOCAL=false`; alle anderen Zeilen bleiben bytegleich.
4. **Deploy-Fehler danach:** Promote veröffentlicht den Stand vor der Umstellung und deployt erneut; die lokalen Dienste laufen dann noch.

Die Kundenvorlage bleibt `PRESIDIO_MODE=local` (für Staging-Rückweg und Neukunden vor Promote). Staging wird über das Staging-Vault-Bundle angebunden, nicht über diesen Automatismus. Eine Einzelinstanz gezielt ausnehmen: Hold-Schalter im Instanz-Bundle über den Vault-Weg, nicht Defaults ändern.

## PKI und Zertifikate

- Clientzertifikate gelten 90 Tage; ein Promote erneuert sie bei weniger als 30 Tagen Restlaufzeit. Ohne Promote keine Erneuerung, kein Alarm.
- Prod-Server: `bash scripts/presidio-prod-pki.sh verify` prüft Kette, Schlüsselpaare und SAN im Vault; `renew-server` erneuert, danach Prod neu ausrollen.
- Kein CRL-Dienst. Kompromittierte Zertifikate am Netz sperren und Vertrauens-/Client-Bundles rotieren; Löschen des Vault-Secrets widerruft ein verteiltes Zertifikat nicht.
- Bundle-Format (`instance`, `ca`, `certificate`, `private_key`) nur als geschützte Datei; PEM nie in Git, Logs, Chat oder Wissensbasis.

## Rückwege

### Clientidentität lesend prüfen

Vor einem Rückweg bei TLS-Fehlern die Identität prüfen: `scripts/keyvault-secrets.sh fetch customer-presidio <slug> <geschuetzte-datei>` mit dem Vault der Zielinstanz verwenden (Prod: `ACTAONE_KEY_VAULT_CONFIG=/etc/actaone/key-vault-prod.env`). Privates temporäres Verzeichnis und Dateimodus `0600` verwenden; das JSON enthält auch den privaten Schlüssel und darf nicht ausgegeben werden.

Aus `instance` und `certificate` ausschließlich Instanzzuordnung, Subject-CN, Gültigkeitszeitraum, Issuer und SHA-256-Fingerprint ermitteln. Die Zertifikatskette gegen die separat aus der richtigen Umgebung bezogene vertrauenswürdige CA prüfen; ein passender Issuer-Text allein reicht nicht. Mit der tatsächlich eingebundenen Clientidentität und dem Client-CN im begrenzten Gateway-Log abgleichen. `presidio-prod-pki.sh verify` prüft CA und Server, nicht die Identität einer beliebigen Instanz. Keine Erneuerung oder Rotation im Diagnoseauftrag. Temporäre Secret-Dateien anschließend entfernen. Dieser Prüfweg ist anhand des Bundle-Formats gelesen, nicht live erprobt.

## Rückweg ausführen

- **Instanz:** im Instanz-Bundle `PRESIDIO_MODE=local`, lokale URLs beibehalten oder wiederherstellen, denselben freigegebenen Release redeployen. Der Renderer stellt die lokalen Dienste her und entfernt den Gateway erst nach erfolgreichen Gates.
- **Singleton-Images oder -Größe:** vorherige Release-Datei bzw. vorheriges Profil mit demselben Helper; bei älteren Releases mit dem damaligen Quellstand aus dem Release-Verzeichnis auf mgmt.
- **Prod-Singleton entfernen** ist nur unkritisch, solange keine Instanz ihn nutzt; vorher den Weg aller Instanzen prüfen.

## Prüfskripte

```bash
python3 scripts/verify-presidio-infra.py --endpoint <singleton-endpunkt> --tls-bundle <probe-identitaet.json>
bash scripts/verify-customer-presidio.sh customer-<slug> <slug>   # synthetisch im API-Container der Instanz
bash scripts/verify-customer-presidio.sh staging staging
bash scripts/presidio-capacity.sh <ziel> short:15:150 long:15:60  # Last: nur mit ausdrücklichem Auftrag
```

Erwartete Infrastrukturprobe: alle Abläufe erfolgreich, stabile und getrennte Mappings, Ablehnung ohne Clientzertifikat. `verify-customer-presidio.sh` unterdrückt die interne Ausgabe und liefert nur einen binären Funktionsnachweis. Es wiederholt standardmäßig bis 300 Sekunden; für eine begrenzte Diagnose `PRESIDIO_VERIFY_TIMEOUT_SECONDS` passend kürzer setzen. Zur Ursachenzuordnung die Gateway-Metadaten hinzuziehen. Ausgaben enthalten keine Payloads, Mappings oder Secrets. Probe-Identitäten liegen geschützt auf mgmt und werden nicht kopiert.

Entwicklungstests im Monorepo: den Abschnitt „Entwicklungsprüfungen“ des Runbooks verwenden (u. a. `test_presidio_runtime.py`, `test_deploy_presidio.py`, `test_presidio_pki.py`, `verify-presidio.test.cjs`). Der Transporttest braucht zusätzlich Docker und einen gepinnten Nginx-Digest.
