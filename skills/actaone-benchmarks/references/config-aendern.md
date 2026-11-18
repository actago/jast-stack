# librechat.yaml auf benchmark ändern

Alle Befehle laufen auf dem Management-Zugang gegen `--context customer-benchmark`. Die `librechat.yaml` steckt als **unveränderliche Swarm-Config** im Dienst `customer-benchmark_api`; nur dieser Dienst mountet sie (`target=/app/librechat.yaml`). Ein Neustart reicht nicht. Es braucht eine neue Config und ein Service-Update.

## Flüchtiger Weg (Standard für Tests)

```bash
CTX=customer-benchmark; SVC=customer-benchmark_api
docker context inspect "$CTX" --format '{{.Endpoints.docker.Host}}'   # muss ssh://actaone@192.168.10.167 sein
CUR=$(docker --context $CTX service inspect $SVC \
  --format '{{range .Spec.TaskTemplate.ContainerSpec.Configs}}{{if eq .File.Name "/app/librechat.yaml"}}{{.ConfigName}}{{end}}{{end}}')
umask 077; W=$(mktemp -d)
docker --context $CTX config inspect "$CUR" --format '{{json .Spec.Data}}' \
  | python3 -c 'import base64,json,sys; sys.stdout.buffer.write(base64.b64decode(json.load(sys.stdin)))' > "$W/alt.yaml"
cp "$W/alt.yaml" "$W/neu.yaml"
# neu.yaml per Texteinfügung bearbeiten (Regeln unten), dann validieren (siehe Prüfen)
NEW="aoi-lc-benchmark-0e898208-$(sha256sum "$W/neu.yaml" | cut -c1-16)"
docker --context $CTX config create "$NEW" "$W/neu.yaml"
docker --context $CTX service update --config-rm "$CUR" \
  --config-add source="$NEW",target=/app/librechat.yaml \
  --update-order start-first $SVC
```

`$W/alt.yaml` bis zum Abschluss aufbewahren, dann mit `shred -u` löschen, falls literale Schlüssel enthalten sind. `$CUR` ist der Rückweg: dieselbe `service update` mit vertauschten Namen. Alternativ setzt `sync-benchmark-release.sh sync` auf den Staging-Stand zurück (siehe [staging-paritaet.md](staging-paritaet.md)).

Der Config-Name folgt der Formel von `deploy-customer.sh` und dem Sync-Skript: `aoi-lc-benchmark-<sha256("benchmark")[0:8]=0e898208>-<sha256(inhalt)[0:16]>`. Damit ist der Name zugleich Provenienz. Ältere Anleitungen benennen flüchtige Configs nach Zweck und Datum. Das funktioniert, liefert aber keinen Inhalts-Hash.

`{{json .Spec.Data}}` statt `{{.Spec.Data}}` verwenden. Letzteres liefert eine Byte-Liste, an der die Dekodierung scheitert.

### Bearbeitungsregeln aus echten Fehlern

- **Texteinfügung, kein YAML-Round-Trip.** Die Datei nutzt Anker wie `&actaone_prompt` mit vielen Referenzen. `yaml.dump` expandiert sie, bläht die Datei auf und verliert Kommentare.
- **Skripte über stdin schicken**, nicht in `ssh '...'` einbetten. Einfache Anführungszeichen im Skript beenden sonst die äußere Quotierung.
- **Kein leerer Schlüssel.** Ein leer stehender Key wie `defaults:` wird YAML-`null`; Zod verlangt ein Objekt, und die API landet im Crash-Loop. Den Key ganz entfernen.
- **Platzhalter `${VAR}` werden nicht überall aufgelöst.** `endpoints.custom[].apiKey` und `.baseURL` laufen durch `extractEnvVariable` (`packages/api/src/endpoints/custom/config.ts`). Für andere Felder, z. B. `mcpServers.url`, war das nicht der Fall. Vor jedem `${...}` in einem neuen Feld im Code nachsehen.
- **Kein Zeitlimit je Endpunkt.** `timeoutMs` gilt nur für Assistants. Ein Gateway mit Kaltstart sieht im Chat wie ein Defekt aus.

## Ein neues Modell braucht mehrere Ebenen

Zuerst klären, wo das Modell nutzbar sein soll: im normalen Chat oder in einem Agenten. Der actaOne-Hauptchat ist selbst ein Agent.

| # | Stelle | Wofür | Pflicht |
|---|---|---|---|
| 1 | `endpoints.custom` | Modell überhaupt erreichbar | immer |
| 2 | `modelSpecs.list` (`preset.endpoint` + `preset.model`) | im Chat wählbar | wenn `modelSpecs.enforce: true` |
| 3 | `runtimeProfiles.modelLabels` mit `"<Endpunkt>:<modell>": <Name>` | Anzeigename | sonst erscheint die rohe ID |
| 4 | `endpoints.agents.allowedProviders` | im Agenten wählbar | wenn Agenten es nutzen sollen; Groß-/Kleinschreibung des Endpunktnamens beachten |
| 5 | `getProviderGroupId()` im Client | überhaupt im Dropdown sichtbar | bei jedem **neuen Anbieter** |

Ebene 5 ist **Code, keine Konfiguration**. Laut Fork-`origin/main` vom 10.11.2026 liegt die Funktion in `client/src/utils/runtime.ts`; der Quell-Skill nannte noch `RuntimeModelSelect.tsx`. Ein Spec mit unbekanntem Anbieter verschwindet lautlos. Ein neuer Anbieter braucht dort eine Regel und ein passendes Icon. Der Weg dafür ist ein Branch-Build auf benchmark, kein Merge nach `main` nur für einen Test. Ein bekannter Anbieter unter neuem Endpunktnamen braucht Ebene 5 nicht.

Die Dropdown-Specs entstehen zur Laufzeit als `runtime-<endpunkt>-<modell>` aus `models.default` (`packages/data-schemas/src/app/specs.ts`). `modelSpecs.list` steuert den normalen Chat.

Läuft das Modell über LiteLLM, kommt die Freigabe an Key und Team dazu. Sie ist eine Gateway-Änderung und gehört nicht zu diesem Skill; das Sync-Skript meldet fehlende Modellrechte des benchmark-Keys gegenüber Staging als `keyModelsMissing`.

## Parameterfallen beim Messen

| Annahme | Wirklichkeit laut Quell-Skill (30.07.2026) |
|---|---|
| `maxContextTokens` im `modelSpec.preset` steuert das Kontextbudget | Wirksam ist `endpoints.custom[].tokenConfig.<modell>.context`; `tokenConfig` verlangt zusätzlich `prompt` und `completion`. |
| Token-Map greift für jede Modell-ID | Präfix-Match: `mistral-*` trifft den Mistral-Eintrag, `magistral-*` keinen und fällt auf den Default. |
| Preset-`temperature` wirkt | Mit `runtimeProfiles.enforce: true` überschreiben Profil-`defaults` jedes Preset (`packages/api/src/runtime/profile.ts`, `shouldUseProfileValue`). |
| `promptAddenda` sind Nutzeranweisungen | Sie landen im System-Prompt. Manche Modelle befolgen dort Fakten, aber keine Verhaltensregeln. |
| `rerankerType: jina` beschreibt den Reranker | Es beschreibt nur das Protokoll; tatsächlicher Dienst und `top_n` stehen in der Websearch-Konfiguration. |

Die Wirkung im laufenden Container prüfen, z. B. durch direkten Aufruf der Token-Funktion. Die Tabelle stammt aus einem älteren Template-Stand; vor einer Aussage gegen den aktuellen Code prüfen.

## Prüfen

Vor dem `config create`: Schema-Validierung mit dem echten Zod-Schema im laufenden Container. YAML-Syntax allein reicht nicht.

```bash
CID=$(docker --context $CTX ps --filter name=customer-benchmark_api --format '{{.ID}}' | head -1)
docker --context $CTX exec -i "$CID" node -e '
let raw=""; process.stdin.setEncoding("utf8"); process.stdin.on("data",d=>raw+=d);
process.stdin.on("end",()=>{ const yaml=require("js-yaml"), dp=require("librechat-data-provider");
  const r=dp.configSchema.safeParse(yaml.load(raw));
  if(!r.success){r.error.issues.slice(0,8).forEach(i=>console.log(i.path.join(".")+": "+i.message));process.exit(1);}
  const d=r.data; console.log("SCHEMA OK");
  console.log("custom   :", (d.endpoints?.custom||[]).map(e=>e.name));
  console.log("specs    :", (d.modelSpecs?.list||[]).map(s=>s.name));
  console.log("labels   :", Object.keys(d.runtimeProfiles?.modelLabels||{}));
  console.log("agents   :", d.endpoints?.agents?.allowedProviders); });' < "$W/neu.yaml"
```

Nach dem Update:

1. **Nur der beabsichtigte Block hat sich geändert.** `alt.yaml` und `neu.yaml` parsen, den geänderten Teilbaum entfernen und den Rest vergleichen. Der Anker `&actaone_prompt` muss weiterhin genau einmal vorkommen.
2. **Im Container liegt genau diese Datei.** `sha256sum /app/librechat.yaml` im neuen Task gegen `sha256sum "$W/neu.yaml"`.
3. **Der Dienst läuft.** `service ps` zeigt Running. `service logs --since 3m` enthält kein `invalid custom config`, `ZodError` oder `exiting`.
4. **Die App sieht die Ebenen.** Dieselbe Ausgabe wie oben, diesmal gegen `/app/librechat.yaml` im Container.

Das Startprotokoll `Custom config file loaded:` wird von `docker service logs` abgeschnitten. Ein fehlender Eintrag dort beweist nichts. Wer im Protokoll sucht, prüft immer auch einen Eintrag, der sicher vorhanden sein muss.

Danach im Browser hart neu laden. Fehlt das Modell weiterhin, liegt es fast immer an einer der Ebenen oben, nicht am Cache.

## Dauerhaft

benchmark hat seit 12.11.2026 keine eigene dauerhafte Konfiguration mehr. Das Template ist das Staging-Template, `scripts/tests/test_librechat_template_drift.sh` prüft das. Was dauerhaft gelten soll, gehört:

- in das Staging- bzw. Kundentemplate per PR und danach über den normalen Release-Weg,
- oder als Secret in das Vault-Bundle `customer-env benchmark` über den Vault-Ablauf des Monorepos.

Nicht geheime Laufzeitwerte, die benchmark wie Staging führen soll, stehen in `customers/benchmark/sync-env-overlay.env`. Das Sync-Skript lehnt Keys ab, die nach Geheimnis aussehen.

Eine Änderung nur am benchmark-Template oder an `customers/benchmark/librechat.yaml` bricht die Parität und wird beim nächsten Sync bzw. Drift-Test überschrieben oder rot. Ältere Anleitungen, die „beide Dateien patchen“ empfehlen, stammen aus der Zeit vor der Kopplung.
