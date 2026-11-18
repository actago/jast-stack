# Messen und auswerten

## Provenienz zuerst

Vor jedem Messlauf festhalten:

```bash
CTX=customer-benchmark
docker --context $CTX service inspect customer-benchmark_api \
  --format '{{.Spec.TaskTemplate.ContainerSpec.Image}} {{range .Spec.TaskTemplate.ContainerSpec.Configs}}{{.ConfigName}} {{end}}'
```

Ergänzend `scripts/sync-benchmark-release.sh status` (nur lesend). Es liefert Release-Tag, `configSha16` und Abweichungen zu Staging. Diese Angaben gehören in jede Messreihe. Ändert sich der Stand zwischen zwei Läufen, sind sie getrennte Reihen.

Für Messreihen datierte Modell-Snapshots verwenden. `-latest`-Aliase sind beweglich. Beim Pinnen den passenden `modelLabels`-Schlüssel mitziehen.

## Harness

Der Quell-Skill (Stand 30.07.2026) beschreibt einen Harness unter `~/bench-harness/` auf dem Management-Host: `run-bench.mjs`, `prompts.json`, `bench.env` (`0600`).

```bash
cd ~/bench-harness
node run-bench.mjs --probe                  # ein Lauf, gibt die Rohantwort aus
node run-bench.mjs                          # alle Prompts × alle Specs
node run-bench.mjs --spec <spec-name>       # einzelne Spec
```

Ob Harness, Prompt-Satz und Spec-Namen nach der Kopplung an Staging (12.11.2026) noch passen, ist nicht geprüft. Vor dem ersten Lauf Dateien und `--probe` prüfen. Die Spec-Namen kommen jetzt aus dem Staging-Template.

Damit ein eigener Client gegen benchmark funktioniert, braucht er vier Dinge:

- **Interne Adresse plus Host-Header.** Ziel ist `https://192.168.10.167` mit Host `benchmark.ki.actago.de` und passender SNI. mgmt erreicht die öffentliche Adresse nicht (kein Hairpin-NAT). Alternativ `--resolve benchmark.ki.actago.de:443:192.168.15.100` über den DMZ-Caddy.
- **`node:https` statt `fetch`.** undici überschreibt den `Host`-Header, Traefik antwortet dann 404.
- **Browser-User-Agent.** `api/server/middleware/uaParser.js` weist andere Clients mit `Illegal request` ab.
- **Testnutzer mit `tenantId: "benchmark"`.** `config/create-user.js` setzt ihn nicht; ohne ihn folgt auf „Login successful“ ein 500. Ohne `--email-verified=true` fragt das Skript interaktiv nach und hängt ohne TTY. Testzugänge liegen in `0600`-Dateien und werden nicht ausgegeben.

## Ergebnisse aus Mongo lesen

Mongo-Container: `docker --context customer-benchmark ps -q --filter name=customer-benchmark_mongodb`, Datenbank `LibreChat`, Collection `messages`. Nur die Felder für die Auswertung lesen, nicht ganze Dokumente ausgeben.

| Frage | Feld | Achtung |
|---|---|---|
| Eingabe- und Ausgabetokens | `metadata.usage.input` / `.output` | `tokenCount` ist ungefähr die Ausgabe, nicht die Kontextlast |
| Kontextbudget und Anteile | `metadata.contextUsage.contextBudget`, `.breakdown.instructionTokens`, `.toolSchemaTokens` | |
| Antworttext | `content[]`, Teile mit `type: "text"` | `text` ist bei Content-Part-Nachrichten leer; das ist normal |
| Fehlschlag | kein `text`-Part oder `unfinished: true` | Letzteres schreibt der Abbruchpfad |
| Quellenbelege | Marker `turn\d+search\d+` im Text | eindeutige gegen gesamte zählen |
| Erzeugte Dateien | `files.filepath`, im API-Container unter `/app/uploads/...` | PDFs auf `/Encoding`, `/Producer`, Größe und Seitenzahl prüfen |

Für Kostenfragen ist der Ledger `transactions` die Quelle, nicht `messages`. LibreChat-Credits und LiteLLM-Spend sind zwei Messungen desselben Verkehrs und werden nicht addiert.

## Code-Interpreter-Sandbox

Laut Quell-Skill (30.07.2026) verfügbar: `reportlab`, DejaVu-Fonts unter `/usr/share/fonts/truetype/dejavu`. Nicht verfügbar: `pandoc`, `fpdf`, `wkhtmltopdf`, `apt-get`, `which` und Netzzugang (`pip install` scheitert). Modelle, die das nicht prüfen, verbrauchen Tool-Aufrufe. Der Stand kann sich mit dem Code-Interpreter-Singleton geändert haben. Bei überraschendem Verhalten das Sandbox-Inventar neu erheben.

## Auswertungsregeln

- Ein Fehlschlag eines Modells ist keine Umgebungsgrenze, solange kein zweites Modell unter gleichen Bedingungen gegenkontrolliert wurde.
- Unterschiede bei Konfiguration, Prompt-Hilfen oder Temperatur im Ergebnis ausweisen.
- Einzelläufe nicht als Qualitätsurteil verallgemeinern. Wiederholungen und Streuung angeben, wenn eine Rangfolge behauptet wird.
