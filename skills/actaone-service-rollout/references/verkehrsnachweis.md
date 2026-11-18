# Verkehrswechsel nachweisen und alte Ressourcen abschalten

Verallgemeinert aus dem Abschnitt „Legacy-Pool 3112 abschalten“ in `docs/operations/codeapi/runbook.md` (Monorepo, `origin/main` `73ce7d4`). Für CodeAPI gilt das Runbook selbst; für andere Dienste die Platzhalter anpassen und das jeweilige Runbook vorziehen. Alle Schleifen geben nur Namen aus, nie Env-Werte. Nichts davon wurde für diesen Skill ausgeführt.

Platzhalter: `<KEY_REGEX>` sind die Env-Schlüssel, die auf den Dienst zeigen (z. B. `LIBRECHAT_CODE_BASEURL`, `PRESIDIO_.*_URL`); `<ALT>` ist ein eindeutiges Merkmal des alten Endpunkts (z. B. `:3112`).

## 1. Laufende Service-Spezifikationen

Auf dem Management-Host über alle Kunden- und Staging-Kontexte. Nicht erreichbare Kontexte getrennt sammeln, nicht als „sauber“ zählen.

```bash
for ctx in $(docker context ls --format '{{.Name}}' | grep -E '^(customer-|staging$)'); do
  svcs=$(docker --context "$ctx" service ls --format '{{.Name}}' 2>/dev/null) || { echo "UNREACHABLE $ctx"; continue; }
  for svc in $svcs; do
    values=$(docker --context "$ctx" service inspect "$svc" \
      --format '{{range .Spec.TaskTemplate.ContainerSpec.Env}}{{println .}}{{end}}' 2>/dev/null) \
      || { echo "INSPECT_FAILED $ctx $svc"; continue; }
    printf '%s\n' "$values" | grep -E "^(<KEY_REGEX>)=" | grep -Fq -- '<ALT>' && echo "$ctx $svc"
    unset values
  done
done
```

Ohne Shell-Tracing ausführen; die temporäre Variable enthält Env-Werte und darf nicht ausgegeben werden. `INSPECT_FAILED` ist eine offene Prüfung, kein leerer Treffer. Alle Services prüfen, nicht nur `_api`: Begleitdienste (RAG, Admin) können eigene Verweise tragen. Treffer ohne Laufzeitwirkung (z. B. reine Vergleichsangaben für Prüfskripte) einzeln begründen.

## 2. Vault-Bundles und Defaults

Was der nächste Deploy ausrollt. Beide Umgebungen, nacheinander (parallele Abrufe scheitern sporadisch), Dateien nur `0600` und danach `shred`. Die Vault-Konfiguration je Umgebung explizit setzen (`ACTAONE_KEY_VAULT_CONFIG=/etc/actaone/key-vault-<env>.env`); ohne sie meldet die Schleife jedes Bundle als nicht ladbar. Vollständige Schleife: CodeAPI-Runbook.

- Treffer → Bundle vault-first auf das Ziel umstellen (Publish/Readback), auch wenn keine Instanz läuft. Ein späterer Deploy würde sonst den alten Endpunkt wieder ausrollen. Ob ein Deploypfad den Altwert selbst umstellt, ist pfadabhängig (CodeAPI 10/2026: `promote.sh` ja, direkter `deploy-customer.sh`-Lauf nein); darauf nicht verlassen.
- `SecretNotFound` in beiden Vaults → kein Bundle, nichts auszurollen.
- Andere Abruffehler → vor dem Abschalten klären.
- `customer-defaults` beider Umgebungen gehören dazu.

## 3. Verbindungen am alten Endpunkt

`ss` auf dem Host sieht keine Verbindungen, die per Docker-DNAT direkt im Container landen. Deshalb zusätzlich im Netz-Namespace des Containers prüfen und beide Prüfungen nach einigen Minuten wiederholen.

```bash
ss -Htn state established '( sport = :<PORT> )'                 # Host, muss leer sein
docker exec "$C" sh -c 'cat /proc/net/tcp /proc/net/tcp6' \
  | awk '$2 ~ /:<PORT_HEX>$/ && $4 == "01"' | wc -l               # Container, 0
docker exec "$C" cat /proc/net/snmp | awk '/^Tcp:/{if(!h){split($0,k);h=1}else{split($0,v);for(i=2;i<=NF;i++)if(k[i]=="PassiveOpens")print k[i]"="v[i]}}'
```

Steigt `PassiveOpens` zwischen zwei Prüfungen nicht, hat sich niemand verbunden. Request-Zählungen aus Dienstlogs sind nur ein Beleg, wenn der Dienst erfolgreiche Anfragen tatsächlich loggt. Für mTLS-Gateways eignen sich Kennzahlen-Logs je Client-CN.

## 4. Offene Kontexte

Nicht erreichbare Kontexte gegen Proxmox klassifizieren (gestoppt, gelöscht, Netzfehler). Ein VM- oder Stack-Start ist kein Redeploy: vorhandene Service-Spezifikationen können weiterhin den alten Endpunkt nutzen. Bei gestoppten Instanzen deshalb sowohl persistierten Runtime-Stand als auch Vault-Soll und den tatsächlichen Wiederanlaufpfad klären. Nur ein korrigiertes Bundle reicht nicht als Abschaltnachweis.

## Abschalten

Erst wenn 1–4 leer bzw. geklärt sind, mit Zeitpunkt protokolliert, und die Abschaltung beauftragt ist:

1. Vorzustand festhalten: laufende Container, Restart-Policies, Unit-Definition (ohne `Environment=`-Zeilen), Ports.
2. Laufende Jobs auslaufen lassen; Queue pausiert und leer.
3. Autostart verhindern (Restart-Policy `no`, Unit `disable`), dann stoppen. Unit-Änderungen brauchen root (temporäres Admin-Fenster nach Repo-Verfahren, danach wieder abbauen).
4. Daten, Volumes, Images und Identitäten bleiben. Löschen, Lifecycle-Regeln und VM-Entfernung sind eigene Aufträge.
5. Rückweg notieren: welche Policies und Units für einen Neustart wiederherzustellen sind.

Ergebnis: belegte Abschaltung mit Zeitpunkt, freigegebene Ressourcen (RAM/CPU) und offenen Restschritten.
