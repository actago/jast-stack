# Keys und Teams

Grundlage: `ops/gateway-admin.py` (LiteLLM-Repo), `docs/LITELLM_CUSTOMER_ROLLOUT.md` und `docs/LITELLM_FULL_MIGRATION.md` (actaOne-Monorepo). Stand siehe [sources.md](sources.md).

## Werkzeug

`gateway-admin.py` liegt auf dem Gateway-Host unter `/opt/actaone/litellm/` (laut Repo-Doku). Der Gateway-Host ist nur über den Management-Zugang erreichbar. Aktionen: `create`, `info`, `revoke`, `clear-budgets`, `add-chat-models`. Optionen: `--customer`, `--purpose`, `--generation`, `--models`, `--budget`, `--duration`. `--apply` gibt es nur für `add-chat-models`; ohne `--apply` läuft ein Probelauf. `create` legt Team und Key an und schreibt den Token in eine `0600`-Datei auf dem Gateway-Host. Fehlende Modelle ergänzt `create` in der Team-Liste; vorhandene entfernt es nie.

Fallen, die der Code zeigt (Stand `origin/main`, siehe [sources.md](sources.md)):

- `create` ohne `--duration` vergibt **Chat-Keys 7 Tage Laufzeit**, Dienste-Keys keine. Für Instanz-Chat-Keys deshalb ausdrücklich `--duration none` angeben.
- `add-chat-models` ohne `--customer` plant die Erweiterung für **alle** verwalteten Teams und Keys des gewählten Zwecks und der gewählten Generation. Für gezielte Freigaben `--customer` immer setzen. Den Probelauf lesen und nur die beauftragten Ziele anwenden.
- `--purpose` wählt die Key-Familie (Standard `chat`). RAG- und Bildrechte erfordern den passenden Zweck.
- Unbeschränkte Teams oder Keys (leer, `*`) bleiben unbeschränkt. Der Instanz-Preflight lehnt solche Keys ab.

## Vor jedem neuen Key

1. **Zweck klären:** Instanz-Key (Chat, RAG, Bild, Gemini) oder Test-/Benchmark-Key für Personen oder Werkzeuge.
2. **Vorhandenes suchen:**
   - Bestand an Teams und Keys über den lesenden Management-Zugang oder die Admin-UI prüfen; `info` ist keine Bestandsliste,
   - bei Instanzen die Bindung im Instanz-Bundle prüfen,
   - bei Test-Keys nachfragen, ob lokal bereits ein Key vorliegt.

   `info --customer <name> --purpose <zweck> --generation <n>` liest genau einen bekannten Key aus `~/.config/litellm-keys/<alias>.json` des ausführenden Nutzers und fragt `/key/info` ab. Ohne diese lokale Datei funktioniert es nicht. Es zeigt Alias, Team-ID, Modelle, Ablauf, Spend und Key-Budget, keinen Sperrstatus oder Team-Budget. Eine fehlende Datei beweist nicht, dass der Key serverseitig fehlt.

   `create` verweigert die Anlage bei vorhandener Keydatei oder `.pending`-Datei. Dann den Bestand abgleichen; weder Dateien löschen noch die Generation blind erhöhen. Ohne `--budget` ist ein Key unbudgetiert, mit `--duration none` zusätzlich unbefristet. Diese Kombination muss vom Auftrag gedeckt sein; fehlen Budget- oder Laufzeitvorgaben für einen Test-Key, vor der Anlage klären.

   `add-chat-models` erfasst nur verwaltete Keys mit passendem Alias-Schema und `metadata.purpose`. Manuell in der UI angelegte Test-Keys werden dadurch nicht automatisch erweitert.
3. **Nur bei Bedarf neu anlegen.** Name nach Konvention, Modelle explizit angeben. Budget und Laufzeit so wählen, wie es beauftragt ist. Für Instanzen gilt: seit 24.09.2026 kein Budget, keine Laufzeit (`--duration none`). Test-Keys haben üblicherweise Budget und Ablauf; die Werte bestimmt der Nutzer, nicht der Agent.
4. **Übergabe:** Den Token nie ausgeben. Für Instanzen das Monorepo-Werkzeug verwenden: `scripts/configure-chat-gateway.py` bzw. die Vorbereitung im Migrations- oder Provisioning-Pfad. Es liest die `0600`-Datei, publiziert nur das Instanz-Bundle und liest es zurück. Für Personen oder Werkzeuge über das jeweilige Secret-Verfahren der Laufzeitumgebung übergeben, nicht im Chat.

## Instanz-Keys

- Chat `<slug>-g<n>`, Dienste `<slug>.rag-g<n>`, `<slug>.image-g<n>`, `<slug>.gemini-g<n>`, alle im Team der Instanz.
- Preflight beim Deploy: `metadata.customer_slug` gleich Slug, Team vorhanden und nicht gesperrt, Key nicht gesperrt, explizite Allowlist, alle `LITELLM_MODELS` sichtbar und in Key und Team erlaubt.
- Rotation läuft über den vorhandenen Ops-Job „actaOne-Keys rotieren“: neue Generation, Bundle aktualisieren, Redeploy, erst danach Widerruf. Eine laufende Rotation wird fortgesetzt, nicht neu begonnen.
- Teardown widerruft die Keys der Instanz. Unbefristete Keys bleiben bis zum Widerruf gültig.
- Neukunden: Ob der Worker inzwischen auch den Chat-Key anlegt, war zuletzt offen (Stand 08.11.2026). Im Code und am Worker prüfen, nicht annehmen.

## Ungültig, abgelaufen, gesperrt, Budget

- **Symptom zuerst zuordnen.** Bei 401/403 ist der Key ungültig, widerrufen oder gehört zum falschen Team. Bei 429 mit „Budget exceeded“ ist ein Key- oder Team-Budget überschritten (getrennte Sperren). Liegt der Fehler beim Provider, ist das Upstream-Credential im Gateway-Vault die Ursache, nicht der Instanz-Key.
- **Bei Diagnose nur lesen.** Mit `info` den bekannten Key auf Ablauf, Key-Budget, Spend und Modelle prüfen. Sperrstatus und Team-Budget separat über den lesenden Management-Zugang prüfen, ohne Token auszugeben.
- **Verlängern, Budget zurücksetzen, neu ausstellen** sind Änderungen und nur im beauftragten Umfang erlaubt. Vor DB-nahen Eingriffen ein Backup anlegen.
- **Nach einer Rotation von Provider-Credentials** (z. B. Bedrock-Token) alle Kopien prüfen: Gateway-Vault, `customer-defaults` und Instanz-Bundles mit direktem Pfad, außerdem die Fassaden anderer Dienste. Historisch lief ein KB_RAG-Reranker nach einer Rotation still mit altem Key weiter (Fallback auf Keyword-Scoring). Vault-Korrekturen wirken erst nach Redeploy.

## Grenzen

- Master-Key, Salt, DB- und Redis-Secrets nie anfassen oder ausgeben. `bootstrap-secrets.py` ist nur für die Erstinstallation gedacht.
- Rollen in der LiteLLM-UI nur nach Prüfung der Sicherheitslage der eingesetzten Version vergeben. Zur damaligen Version gab es eine bekannte Rechteausweitung; heutigen Stand prüfen.
