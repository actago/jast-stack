# Bisherige Umzüge je Dienst (datiert)

Orientierung, wo die Phasen eines Umzugs für einen Dienst bereits umgesetzt oder beschrieben sind. Alle Angaben sind Quellenstand (Monorepo `origin/main` `73ce7d4`, 13.11.2026; KB `d9d678f`, 11.11.2026), nicht live geprüft. Pfade beziehen sich auf das Monorepo, wenn nicht anders angegeben.

## Presidio: lokal je Instanz → Prod-Singleton

| Phase | Umsetzung im Bestand | Quelle |
|---|---|---|
| Bereitstellung | eigene Prod-VM mit eigenem Swarm, Release-/Profildatei, `scripts/deploy-presidio.py` erst Plan, dann `--apply` | `docs/operations/presidio-singleton.md` |
| Identität | Prod-CA getrennt von Staging-CA; je Instanz Clientzertifikat (CN = Slug, 90 Tage, Erneuerung im Promote unter 30 Tagen Rest); fremde/Staging-Identität → Abbruch | `docs/rollouts/production-2026-11.md`, Abschnitt „automatische Umstellung“ |
| Anbindung | Erreichbarkeit aus beiden Kundennetzen mit TLS 1.3 und Servername, ohne Clientzertifikat abgewiesen | ebd., „Abnahme 03.11.“ |
| Konfiguration | `scripts/presidio-release-migration.sh` im `promote.sh` vor dem Env-Publish: `PRESIDIO_MODE=shared`, Endpunkt, Servername, `PRESIDIO_KEEP_LOCAL=false`; andere Zeilen bytegleich | ebd. |
| Canary/Wellen | **bewusst ohne Wellen**: alle Prod-Kunden im selben Release; als Grenze dokumentiert (volle Last ab Rollout, kein Autoscaler) | ebd., „Grenzen und offene Punkte“ |
| Rückweg | je Kunde `PRESIDIO_MODE=local` + `PRESIDIO_RELEASE_MIGRATION=hold`, redeployen; global Manifest `manual`; Release-Rollback ändert Presidio nicht | ebd. |
| Abschalten | lokale Analyzer/Anonymizer entfernt der Renderer nach allen Gates; lokaler mTLS-Proxy bleibt | ebd. |

Dienstinterna (Erkenner, Limits, Skalierung): Presidio-Runbook bzw. Skill `actaone-presidio`.

## CodeAPI: `.111` Compose → K3s-Cluster; Legacy-Pool 3112 abschalten

| Phase | Umsetzung im Bestand | Quelle |
|---|---|---|
| Bereitstellung | Cluster im historisch benannten Namespace `codeapi-k8s-lab`; Kandidaten-Digests im Manifest, vor Aktivierung erneut mit dem Cluster abgleichen | `docs/rollouts/production-2026-11.md`, „CodeAPI: vorgesehener Zustand“ |
| Identität | kurzlebige JWTs der Instanzen; Signervertrauen additiv registrieren, geladenen JWKS-Stand kontrollieren; gleiche `kid` ersetzt keinen Schlüsselvergleich je Ziel | ebd. |
| Konfiguration | `deploy-customer.sh` gleicht vor dem Rendern ab; nur bekannte Standard-URLs werden umgestellt, eigene URLs und `CODEAPI_RELEASE_MIGRATION=hold` bleiben; Offline-Helfer `scripts/prepare-codeapi-cutover.py` ändert nur die URL-Zeile und publiziert nie | ebd., „Vorbereitung der Zielbundles“ |
| Canary/Wellen | interne Canary, dann kleine Kundenwelle, dann explizite Wellen (`customerWaves`, Stand 04.11. leer); Canary actago4it am 04.11. abgenommen | ebd., „Cutover-Reihenfolge“ |
| Rückweg | Hold + bisherige URL, Publish/Readback, Redeploy; URL-Rückweg transportiert keine neuen Dateien zurück | ebd. |
| Abschalten | Pool 3112: Nutzung (Host- und Container-Namespace), laufende Services, Vault-Bundles beider Umgebungen und Defaults leer; 30 verwaiste Prod-Bundles vor dem Abschalten umgestellt; Restart-Policy `no`, `compose stop`, Unit-Disable per root offen; Daten und Images bleiben | `docs/operations/codeapi/runbook.md`, „Legacy-Pool 3112 abschalten“ |

KB-Stand 08.11.: 85 API-Konfigurationen auf dem Cluster; Benchmark, ein Branch und das STWH-Render-Lab nutzen noch VM 311 (`.111:3114`/`3115`). VM 311 ist damit **nicht** ungenutzt (`10 actaOne/Code-Interpreter (Service-Referenz).md`).

## LiteLLM: direct → `litellm-global`

| Phase | Umsetzung im Bestand | Quelle |
|---|---|---|
| Bereitstellung | Gateway-Backup/Restore, Monitoring und Ausfallverhalten vor Kunden abnehmen; einzelner Host bleibt gemeinsamer Ausfallpunkt | `docs/LITELLM_FULL_MIGRATION.md`, „Reihenfolge“ |
| Identität | Key je Instanz und Zweck (Chat, RAG, Bild, Gemini) im Team der Instanz; bestehende Keys nie erweitern; Master-Key nie im Instanz-Bundle | `docs/LITELLM_CUSTOMER_ROLLOUT.md`; LiteLLM-Repo |
| Konfiguration | `scripts/migrate-litellm.py` mit Receipt; Opt-in je Instanz, normale Promotes migrieren nicht in den Vollmodus | `docs/LITELLM_FULL_MIGRATION.md`; KB „LiteLLM (Service-Referenz)“, Fortschreibung 08.11. |
| Canary/Wellen | Staging real abnehmen, dann über Release-/Stable- und Panel-Wellenpfad; vor jeder Welle Liste von Funktionsnachweisen (Agenten, Embeddings gleiche Dimension, Bilder, Kosten bei richtiger Instanz) | ebd., „Abnahme und Wellen“ |
| Rückweg | `migrate-litellm.py rollback` mit Receipt, unverändertem Kandidaten und passendem Vorher-Bundle; danach direkte Vorlage frisch rendern; ungebundene neue Keys widerrufen | ebd., „Rückweg“ |
| Abschalten | direkte Providerkeys erst nach Abnahme gezielt je Instanz entfernen, keine Defaults-/Flottenlöschung | ebd. |

Modellkatalog, Discovery und Keys im Detail: Skill `actaone-litellm` bzw. LiteLLM-Repo.

## Docling: geplanter gemeinsamer Konvertierungsdienst

Kein Deployment, kein Rollout-Pfad, keine Kundenanbindung im Bestand. Die KB-Entscheidung vom 11.09.2026 wählte AnyDoc als Parser; ein Docling-Adapter war „vorbereitet, nicht gebaut“ (`10 actaOne/Wissensdatenbank-Überarbeitung (Konzept).md`).

Für einen späteren Umzug relevant aus der Recherche `docs/research/2026-11-17-docling-shared-service.md` (lokal, nicht versioniert, Stand 17.11.2026, nur Upstream-Quellen gelesen):

- **Identität:** `DOCLING_SERVE_API_KEY` ist ein gemeinsamer Schlüssel ohne Mandantenbindung; `X-Tenant-Id` ist frei wählbar. Nur das actaOne-Backend darf zugreifen, Mandant aus actaOne-Identität ableiten, Clear-Endpunkte nicht weiterreichen.
- **Persistenz:** Local-Orchestrator hält Queue und Ergebnisse im Prozess, ohne Wiederherstellung nach Neustart. Jobhoheit und Ergebnisablage bleiben in actaOne; das bestimmt, was ein Rückweg erhalten muss.
- **Grenzen:** Datei-/Seitenlimits sind standardmäßig unbegrenzt; Upload-Limit vor dem Dienst nötig. Kapazität (CPU/GPU) ist unbemessen.
- **Offline:** Modelle vorab bereitstellen, ausgehendes Netz sperren, Kaltstart ohne Netz prüfen.

Vor einem Umzug ist Docling zuerst eine **Bereitstellung** mit gepinntem Build; Canary-Kriterien (Seitenprovenienz, Teil-Erfolge, Mandantentrennung) sind neu zu definieren.
