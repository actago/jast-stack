---
name: actaone-litellm
description: actaOne-LiteLLM-Gateway (litellm-global) für Modellaufnahme, Modellfreigabe pro Instanz, Discovery, Team- und Key-Fragen, Modellabschaltung sowie Kosten-/Cache-Prüfung nutzen. Anwenden bei „Modell X fehlt/aufnehmen/entfernen“, „Modell nur für Staging oder eine Instanz freischalten“, „Key für Testsuite/Benchmark/Instanz“, Key ungültig oder abgelaufen, „Kosten oder Cache stimmen nicht“ und Gateway-Upgrade.
---

# actaOne-LiteLLM

`litellm-global` ist der zentrale Modellweg von actaOne. Laut Nutzerentscheidung vom 16.10.2026 sollen neue Modelle nur noch über den Gateway laufen, nicht über Sidecars oder direkte Keys. Damit ein Modell auf einer Instanz nutzbar ist, müssen drei Ebenen stimmen:

- der **zentrale Katalog** im LiteLLM-Repo,
- die **Rechte** an Key und Team,
- die **Auswahl** im Instanz-Vault.

Welche Ebene ein Auftrag tatsächlich betrifft, hängt vom Modus der Instanz ab. Historische Rezepte mit fester Schrittfolge passen deshalb oft nicht.

## 1. Quellen bestimmen

Maßgebliche Quellen, alle extern:

1. **LiteLLM-Repo** (Remote `actago/LiteLLM`): `litellm/litellm-config.yml` und `litellm/lifecycle.yml` sind kanonisch. Dazu `ops/MODEL_DISCOVERY.md`, `ops/LIFECYCLE.md`, `ops/gateway-admin.py`, `ops/deploy.yml` und `ops/PRICING.md`. Lokale Klone liegen oft auf Feature-Branches. Den Vertrag aus `origin/main` lesen (`git show origin/main:<pfad>`) bzw. read-only per `gh api`.
2. **actaOne-Monorepo** (Remote `actago/actaOne`):
   - Instanzseite: `scripts/chat_gateway.py` (Renderer und Preflight), `deploy/litellm-models.json` (statischer Katalog), `deploy/litellm-service-models.json`
   - Docs: `docs/LITELLM_CUSTOMER_ROLLOUT.md`, `docs/LITELLM_FULL_MIGRATION.md`, `docs/LITELLM_PROMPT_CACHE_ROLLOUT.md`, `docs/MODEL_TRANSITIONS.md`

   Aus `origin/main` lesen und den Abstand des lokalen Checkouts melden.
3. **Wissensbasis** (Obsidian-Vault, Remote `actago/actaOneKBobsidian`): „LiteLLM (Service-Referenz)“ und „Modellweg – LiteLLM, Claude 5.5 und Prompt-Cache 2026-10“. Liefert datierte Abweichungen, z. B. manuelle Gateway-Dateien oder Regionspins.
4. **Live-Zustand**: Gateway-Host über den Management-Zugang laut Monorepo. Instanz-Bundles über den Vault-Weg des Monorepos.

Fehlt eine Quelle, das ausdrücklich melden. Repo-Verträge (`origin/main`) und Live-Stand des Gateways sind getrennt zu berichten. Das Repo kann vom laufenden Gateway abweichen, wenn Dateien manuell kopiert wurden. Session-Memories und historische Befehlsfolgen gelten nur als Belege.

## 2. Auftrag und Modus einordnen

Zuerst den Auftragstyp bestimmen:

- **Diagnose** (fehlt, Key ungültig, Kosten falsch): nur lesen, Metadaten-Abfragen mit eingeschränktem Key.
- **Änderung**: genau der beauftragte Umfang.
- **Abnahme**: echte Probeanfrage mit eingeschränktem Key, Kostenabgleich.

Danach für jede betroffene Instanz den Modus aus dem Instanz-Bundle lesen. Nur nicht geheime Schalter anzeigen: `ACTAONE_CHAT_GATEWAY`, `LITELLM_MODEL_DISCOVERY`, `LITELLM_MODELS`, `LITELLM_DEFAULT_MODEL`, `ACTAONE_INFERENCE_GATEWAY`, `ACTAONE_INFERENCE_PROFILE`.

| Modus | Woher kommt der Katalog | Was eine Modellaufnahme braucht |
|---|---|---|
| `ACTAONE_CHAT_GATEWAY=direct` (oder fehlt) | Instanz nutzt LiteLLM für Chat nicht | Gateway-Seite allein ändert nichts an dieser Instanz. Instanz-Vault nur bei beauftragter Umstellung |
| Gateway, Discovery `false` | statisch `deploy/litellm-models.json` des ausgerollten actaOne-Stands | Gateway-Eintrag + Key/Team-Recht + Eintrag im statischen Katalog (actaOne-Release) + `LITELLM_MODELS` im Instanz-Vault + Redeploy |
| Gateway, Discovery `true` | `/v1/models` + `/model/info` mit Instanz-Key, nur Einträge mit `model_info.actaone` v1 | Gateway-Eintrag mit v1-Vertrag + Key/Team-Recht + `LITELLM_MODELS` im Instanz-Vault + Redeploy. Kein Eintrag im statischen Katalog |

Der Renderer verlangt in beiden Gateway-Modi, dass `LITELLM_MODELS` eine explizite, eindeutige Teilmenge des autorisierten Katalogs ist und `LITELLM_DEFAULT_MODEL` darin liegt. Ob der LibreChat-Discovery-Adapter zur Laufzeit zusätzlich freigegebene Modelle ohne Vault-Änderung anzeigt, ist nicht geprüft. Das im Fork klären, bevor es behauptet wird.

## 3. Feste Invarianten

- **Metadaten erteilen keine Rechte.** Ein Modell muss am Key **und** am Team freigegeben sein. Der Preflight lehnt Keys ohne explizite Allowlist ab, `*` eingeschlossen. Ein leeres oder Wildcard-Team überlässt die Prüfung dem Key. Katalog-Updates und Redeploys erweitern bestehende Keys nie.
- **Kanonische Gateway-Config ist die Datei im Repo.** `STORE_MODEL_IN_DB=False`. `/model/update` und `/model/delete` sind nicht der Verwaltungsweg. `runtime-config.yml` wird abgeleitet und nie von Hand editiert. Ausgerollt wird über `ops/deploy.yml`.
- **Öffentliche Modell-IDs bleiben stabil.** Ersetzen und Abschalten laufen über einen 14-Tage-Plan in `lifecycle.yml`. Ein solcher Plan schaltet eine gemeinsam genutzte ID **global** um. Neue Pläne dürfen nicht unveröffentlicht bleiben, und veröffentlichte Pläne werden weder gelöscht noch umgeschrieben.
- **Keys je Instanz und Zweck:** `<slug>-g<n>` (Chat), `<slug>.rag-g<n>`, `<slug>.image-g<n>`, `<slug>.gemini-g<n>` im Team der Instanz. Der Master-Key gehört nie in einen Instanz-Vault. Tokens nur in `0600`-Dateien, nie in Chat, Log oder Wissensbasis.
- **Vorhandenes zuerst:** Vor jedem neuen Key oder Team die vorhandenen Keys und Teams sowie die Bindung im Instanz-Bundle prüfen. Nach einem abgebrochenen Lauf zuerst Receipt und Gateway prüfen, keine neue Generation erfinden.
- **Instanzfelder** (`ACTAONE_CHAT_GATEWAY`, `LITELLM_API_KEY`, `LITELLM_MODELS`, `LITELLM_DEFAULT_MODEL`, `LITELLM_MODEL_DISCOVERY`) gehören in das Instanz-Bundle, nie in `customer-defaults`.
- **Kosten nicht doppelt zählen.** LibreChat-Credits und LiteLLM-Spend messen denselben Verkehr. Spend `0` bei einer Route bedeutet fehlende Kostenbuchung, nicht kostenlos.
- **Gateway-Image nur per Digest.** Keine Floating-Tags. Eigene Patches (`ops/patch-*.py`) müssen ein Upgrade überstehen.

## 4. Teilabläufe

Details und Befehle stehen in den Referenzen:

- **Modell aufnehmen, freigeben, ersetzen, entfernen:** [references/modellaufnahme.md](references/modellaufnahme.md)
- **Keys und Teams** (Test-, Benchmark- und Instanz-Keys, ungültige oder abgelaufene Keys, Provider-Credentials): [references/keys-und-teams.md](references/keys-und-teams.md)

Ein Teilablauf ist fertig, wenn jede betroffene Ebene (Gateway, Rechte, Instanz) rückgelesen ist. Ebenen, die bewusst nicht geändert wurden, werden mit Begründung genannt.

## 5. Funktionale Abnahme

Getrennt vom Ändern durchführen und auf den beauftragten Zielumfang begrenzen:

1. `/v1/models` und `/model/info` mit dem eingeschränkten Ziel-Key. Das Modell muss sichtbar sein und die erwarteten Metadaten tragen. Key nicht ausgeben.
2. Eine echte, kurze Anfrage mit Streaming über die Zielinstanz bzw. deren Key. Einen Test-Key nur verwenden, wenn er das Modell bereits darf; zusätzliche Test-Team-Rechte sind eine eigene Änderung und gehören nicht zu „nur Staging“. Je nach Modell Tool-Aufruf und Strukturantwort zusätzlich.
3. Kosten- und Cache-Abgleich: Usage der Anfrage in LibreChat gegen den Spend-Eintrag in LiteLLM, einschließlich Cache-Lese- und Cache-Schreib-Tokens. Gemeinsame Leitwerte stehen in `docs/LITELLM_PROMPT_CACHE_ROLLOUT.md`. 100 % Cache-Treffer sind kein Kriterium.
4. Bei Instanzen: `scripts/audit-litellm.py` gegen die exakt gerenderte Konfiguration. `configurationReady` bestätigt nur die Konfiguration, nicht die Inferenz.

Rendering-Tests, Preflight und Metadaten-Probes ersetzen keine Inferenz-, Last- oder Flottenabnahme.

## 6. Bericht

Der Bericht enthält:

- Modus je Instanz
- geänderte Ebenen mit Readback
- unveränderte Ebenen mit Grund
- Rückweg
- Abnahmeergebnis mit Grenzen
- Quellenstand (LiteLLM- und actaOne-Commit)

Herkunft der Skillinhalte: [references/sources.md](references/sources.md).
