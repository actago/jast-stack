# Verifikation einer Kundenanlage

Alle Prüfungen sind lesend. Ergebnis je Punkt als bestanden, fehlgeschlagen oder nicht geprüft berichten. Befehle sind Vorlagen für die Management-VM; Kontext und Hostnamen vorher bestätigen.

## 1. Job und Release

- Job-Status, Notizen und Audit im Dashboard bzw. `GET /api/v1/jobs`: Wer hat freigegeben, welcher Tag war eingefroren, Hotseat oder Klon?
- Laufende Images entsprechen dem eingefrorenen Tag:

```bash
docker --context customer-<slug> service ls --format '{{.Name}} {{.Replicas}} {{.Image}}'
```

Jeder Dienst hat seine Soll-Replicas erreicht (z. B. `1/1`). Die Dienstanzahl ist keine feste Zahl: Overlays (Broker, LiteLLM, RAG-Gateway, Workflows) ändern sie; Altquellen nennen 12 oder 13. Kein `:latest`.

## 2. Erreichbarkeit

Die Management-VM erreicht die eigene Public-IP nicht (Hairpin), daher über den DMZ-Caddy auflösen:

```bash
curl -sk --resolve <slug>.ki.actago.de:443:192.168.15.100 \
  -o /dev/null -w '%{http_code}\n' https://<slug>.ki.actago.de/
curl -sk --resolve admin-<slug>.ki.actago.de:443:192.168.15.100 \
  -o /dev/null -w '%{http_code}\n' https://admin-<slug>.ki.actago.de/
```

DNS ist Wildcard; fehlende Erreichbarkeit spricht für Route oder Traefik, nicht für DNS.

## 3. SSO-Einstieg

Echte Einladungslinks werden von der API nicht ausgegeben und gehören nicht in Chat oder Ticket. Ohne Token prüfen, dass der OpenID-Einstieg zu Microsoft weiterleitet:

```bash
curl -sk --resolve <slug>.ki.actago.de:443:192.168.15.100 -D - -o /dev/null \
  "https://<slug>.ki.actago.de/oauth/openid" | grep -i '^HTTP\|^location'
```

Erwartet 302 zu Microsoft. Leeres 401 nur mit Query deutet auf den Invite-Query-Fehler (`TROUBLESHOOTING.md` §2).

## 4. Control-Plane und Instanz-Tenant

- Platform-Instanz hat Heartbeat; CP-Tenant `active` (Panel „healthy“ bzw. `actaone-platform`-Abfrage).
- Instanz-Tenant-Dokument in der Instanz-DB ist `active` (Deploy seedet das; `pending` erzeugt den Refresh-403-Loop).
- Broker-Kunden: CP-Status `/api/platform/v1/auth-broker/instances/<uuid>/enrollment`. `pending` heißt: Owner hat Microsoft noch nicht verbunden. Eine laufende VM ist kein abgeschlossener Owner-Login.

## 5. Was nicht zur Verifikation gehört

Einladung senden, Tenant-Dokumente korrigieren, Redeploy oder Vault-Änderung sind Korrekturen mit eigenem Auftrag. Fehler hier an `diagnose-instance` übergeben.
