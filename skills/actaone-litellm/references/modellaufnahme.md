# Modelle aufnehmen, freigeben, ersetzen, entfernen

Grundlage: LiteLLM-Repo `ops/MODEL_DISCOVERY.md`, `ops/LIFECYCLE.md` sowie im actaOne-Monorepo `scripts/chat_gateway.py`, `docs/LITELLM_*.md` und `docs/MODEL_TRANSITIONS.md`. Stand siehe [sources.md](sources.md). Befehle vor Gebrauch gegen die aktuelle Fassung prüfen.

## A. Modell zentral aufnehmen (Gateway)

1. **Eintrag im Repo:** neue öffentliche ID in `litellm/litellm-config.yml` mit
   - `model_info.display_name`
   - vollständigem `model_info.actaone` v1: `endpoint`, `apiMode`, `parameterProfile`, `purpose`, `compatibilityClass`, `policyTags`, `dropParams`, `legacyReferences`, `tokenConfig` mit allen Preisen inkl. Cache und Langkontext; Embeddings zusätzlich `embeddingSpace`
   - bei Chatmodellen zusätzlich der Karte `modelInfo`: Beschreibung de/en, Wissensstand der exakten Version laut Herstellerquelle, sonst „Nicht veröffentlicht“; `hostedBy` laut tatsächlicher Route und Region; `tokenUsage` 1–5 als redaktionelle Stufe
2. **Region und Hosting** an `litellm_params` prüfen, nicht am Modellnamen oder an `owned_by`. Die Karte darf EU nur für EU-verifizierte Routen angeben. Bekannte Abweichungen (z. B. ein Modell vorübergehend auf einer anderen Region) im Bericht nennen.
3. **Preise** gegen die Herstellerquelle prüfen und mit Quelle sowie Datum festhalten. Statische Katalogpreise in actaOne werden nicht automatisch synchronisiert.
4. **Tests im LiteLLM-Repo:** `python -m unittest discover -s tests`.
5. **PR, Review, Ausrollen** über `ops/deploy.yml`. Live-Dateien nicht von Hand kopieren. Falls doch eine Abweichung vorliegt, zuerst den Drift zwischen Repo und Live-Datei klären. Ein historischer Stolperstein waren Windows-Zeilenenden in der Live-Datei. Vorher ein Off-host-Backup von aktiver Config, Runtime-Bundle und DB anlegen, wie es `ops/LIFECYCLE.md` beschreibt.
6. **Readback:** `/model/info` mit eingeschränktem Staging- oder Test-Key, ohne den Key oder die volle Antwort auszugeben.

Der Proxy wird beim Anwenden neu erstellt. Das ergibt ein kurzes Ausfallfenster für alle Instanzen. Keine Zero-Downtime behaupten.

## B. Modell für Instanzen freigeben

Nur für die beauftragten Ziele. „Nur Staging“ heißt: Staging-Key, Staging-Team und Staging-Bundle, sonst nichts.

1. **Modus je Ziel lesen** (siehe SKILL.md, Abschnitt 2). Eine Instanz mit `ACTAONE_CHAT_GATEWAY=direct` braucht keinen Vault-Eintrag, es sei denn, ihre Umstellung ist beauftragt.
2. **Rechte an Key und Team ergänzen**, auf dem Gateway-Host, zuerst als Probelauf:

   ```bash
   python3 /opt/actaone/litellm/gateway-admin.py add-chat-models --customer <slug> --generation <n> --models <modell> [<modell> …]           # Probelauf
   python3 /opt/actaone/litellm/gateway-admin.py add-chat-models --customer <slug> --generation <n> --models <modell> [<modell> …] --apply
   ```

   Das ergänzt nur und entfernt nichts. Ohne `--customer` würde es alle verwalteten Teams und Keys erweitern, deshalb den Slug immer angeben. Andere Zwecke (RAG, Bild) bleiben unberührt; dafür gibt es `--purpose`. Für RAG- und Bildmodelle gilt: Bestehende Dienste-Keys werden nicht automatisch erweitert. Die Freigabe muss gezielt erfolgen, und der Probelauf muss vorher geprüft sein. Der Gateway cacht Keys etwa 30 Sekunden.
   Generation aus dem tatsächlich an die Instanz gebundenen Key-Alias bestimmen; der Standard ist `1`. Der Probelauf muss für die einzelne Chat-Freigabe genau das beauftragte Team und den gebundenen Key erfassen. Bei fehlendem Key oder zusätzlichen Zielen stoppen und die Zuordnung klären.
3. **Statischer Katalog** (nur bei Discovery `false`): Der Eintrag in `deploy/litellm-models.json` kommt über PR und actaOne-Release, nicht per Hand auf mgmt.
4. **Instanzauswahl:** `LITELLM_MODELS` (und gegebenenfalls `LITELLM_DEFAULT_MODEL`) im Instanz-Bundle über den Vault-Weg des Monorepos ändern: additiv, Readback, keine anderen Zeilen anfassen. Für mehrere Instanzen gibt es Hilfsskripte im Monorepo mit Probelauf, Lock und Revert-Datei, z. B. `scripts/fleet-add-litellm-models.py` (2026-10-Modelle). Deren Zielmodelle sind fest verdrahtet. Ein neues Modell braucht gegebenenfalls ein eigenes Werkzeug oder Einzeländerungen.
5. **Redeploy** über den regulären Pfad (Staging-Deploy, Promote bzw. Branch-Build). Der Preflight vor Swarm-Änderungen prüft Key, Team, Sichtbarkeit und Katalog. Schlägt er fehl, ist nichts ausgerollt.

## C. Modell ersetzen oder abschalten

- **Gateway-seitig, global:** ein 14-Tage-Plan in `litellm/lifecycle.yml`. Vorher `python3 ops/lifecycle.py preview` ausführen, um Fingerprints zu erhalten. Echter Canary des Nachfolgers mit eingeschränktem Key (Streaming, Tools, Kontext, Struktur, Region, Abrechnung). Den Nachweis als `approval.reference` eintragen. Nachfolger und Quelle müssen API-Modus, Parameterprofil, Kompatibilitätsklasse, Zweck, Provider-/Regionspolicy und Embeddingraum teilen. Vor dem Umschalten prüft der Controller, dass jeder aktive Key mit Quellrecht auch das Nachfolgerecht hat. Rechte erweitert er selbst nicht.
- **Instanzseitig, nur Menü:** `runtimeProfiles.modelTransitions` in der passenden Vorlage bzw. im Kunden-Override, wie in `docs/MODEL_TRANSITIONS.md` beschrieben. Die gerenderte `customers/<slug>/librechat.yaml` ist kein Pflegeort.
- **Alte IDs** nicht vorzeitig aus Allowlists entfernen. Gespeicherte Gespräche und Agenten referenzieren sie weiter.
- **Embedding-Modelle** wechseln nie per Alias. Ein anderer Embeddingraum erfordert eine Reindexierung als eigenes Projekt.

## D. Kosten- und Cache-Prüfung

- Preise im Gateway und im statischen Katalog gemeinsam prüfen. Langkontext-Staffeln bildet der statische Katalog nicht ab.
- Bei Bedrock-Claude setzt der Gateway Cache-Marker. Azure nutzt `promptCacheKey`, Gemini erhält keine expliziten Marker. Einzelheiten zu Erwartung und Messung stehen in `docs/LITELLM_PROMPT_CACHE_ROLLOUT.md`, Werkzeug ist `ops/cache-harness` im LiteLLM-Repo.
- Eine Abweichung zwischen LibreChat-Anzeige und LiteLLM-Spend klären, bevor fakturiert oder ein Benchmark bewertet wird. Dafür den finalen Provider-Request und die Kostenbuchung prüfen.

## E. Gateway-Upgrade oder CVE

Zuerst die eingesetzte Version und den Image-Digest live lesen. Dann die Betroffenheit anhand der Advisories bewerten. Upgrade nur per Digest auf eine geprüfte Version, alle `ops/patch-*.py` müssen mitgenommen werden. Danach die Vertragstests und einen Canary mit eingeschränktem Key ausführen. Floating-Tags und unbeaufsichtigte Upgrades sind ausgeschlossen. Ein CVE-Prüfauftrag autorisiert noch kein Upgrade.
