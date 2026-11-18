# Quellen des Skills actaone-service-rollout

Erstellt am 2026-11-17 durch Lesen lokaler Klone und Dateien. Es wurde nichts live geprüft, deployt, abgeschaltet oder verändert. Blob-Hashes sind Git-Objekt-IDs (gekürzt), Datei-Hashes SHA-256 (gekürzt).

## Anlass

Die Session-Auswertung des JAST-Stacks (`research/codex-session-audit.md`, §6 „Zentralen Infra-Dienst einführen“) belegt den wiederkehrenden Ablauf mit Sessions zu Presidio (03.11.), CodeAPI-Cluster-Umzug (03.11.), Docling (17.11.) und LiteLLM-VM (09.09.). Sie stellt fest, dass es nur dienstspezifische Agenten und einmalige Runbooks gibt, keinen dienstübergreifenden Ablauf. Die Sessions sind Herkunft, keine Befehle; sie wurden für diesen Skill nicht erneut gelesen.

## actaOne-Monorepo `github.com/actago/actaOne`

Gelesener Stand: lokale Remote-Referenz `origin/main` = `73ce7d4ccdb5` (Commit 2026-11-13). Lokaler Arbeitszweig `main` steht auf `dd0a334` und wurde nicht verwendet. Kein frischer Fetch.

| Pfad | Blob | Letzter Commit | Verwendet für |
|---|---|---|---|
| `docs/operations/service-rollout-policy.md` | `04dc0e7f7ba6` | `e761874` 2026-08-10 | Kriterien für eigene Fleet-Aktion, Rollout-Weg je Artefakt |
| `docs/rollouts/production-2026-11.md` | `dd81f3ff549e` | `ccde26e` 2026-11-04 | Presidio- und CodeAPI-Umstellung: Manifest-Aktivierung, Hold, Identität, Vault-Vorbereitung, Wellen, Rückweg, Grenzen |
| `deploy/releases/production-2026-11.json` | `994c2d65b7f7` | `ccde26e` 2026-11-04 | nur Struktur: Komponenten `codeapi`/`presidio` mit `activation` |
| `docs/operations/presidio-singleton.md` | `fd240441d11b` | `7d78995` 2026-11-06 | Bereitstellung, getrennte CAs, Kapazität, Rollback, Cutover über `promote.sh` |
| `docs/operations/codeapi/runbook.md` | `17a096e7b1b0` | `7801c97` 2026-10-23 | Abschnitt „Legacy-Pool 3112 abschalten“: Nachweislisten, Namespace-Prüfung, verwaiste Bundles, umkehrbares Abschalten |
| `docs/LITELLM_FULL_MIGRATION.md` | `e89ca883bac6` | `33ff08e` 2026-10-29 | Reihenfolge, Abnahme vor Wellen, Receipt-Rückweg, gezieltes Entfernen direkter Keys |
| `docs/LITELLM_CUSTOMER_ROLLOUT.md` | `91f47c0ff4b5` | `658d827` 2026-11-02 | nur Gliederung (Keys je Instanz, Rollback/Rotation) |
| `scripts/prepare-codeapi-cutover.py` | `8c7f62f54ab5` | `ccde26e` 2026-11-04 | Kopf gelesen: nur Plan bzw. neue Datei, nie Publish/Deploy/SSH |
| `scripts/presidio-release-migration.py` | `b560c0c4caaf` | `78b366f` 2026-11-04 | Planzustände `inactive/not-prod/not-customer/hold/migrate/current` per Suche bestätigt |
| `scripts/presidio-release-migration.sh`, `scripts/codeapi-cutover-inventory.py`, `scripts/migrate-litellm.py`, `scripts/promote.sh` | `c3b72fc606d5`, `a0bdfa2c8bf6`, `649b953f66f4`, `7a4b9a88c983` | 2026-10-29 bis 2026-11-11 | nur Existenz und Runbook-Beschreibung, Code nicht im Detail gelesen |

Nicht versioniert im lokalen Arbeitsbaum:

| Datei | SHA-256 | Verwendet für |
|---|---|---|
| `docs/research/2026-11-17-docling-shared-service.md` | `0c1051308b92` | Docling-Fakten (Auth ohne Mandantenbindung, Persistenz, Limits, Offline); Design-Recherche gegen Upstream, kein Betriebstest |

Die ebenfalls unversionierten Entwürfe `docs/PRESIDIO_SINGLETON_ROLLOUT.md` und `deploy/presidio-singleton/` fehlen in `origin/main` und wurden nicht verwendet.

## Wissensbasis (Obsidian-Vault, Remote `github.com/actago/actaOneKBobsidian`)

Lokaler Stand `d9d678f` (2026-11-11), Notizen ohne lokale Änderung.

| Notiz | Blob | Verwendet für |
|---|---|---|
| `10 actaOne/Code-Interpreter (Service-Referenz).md` | `76d608425b1b` | Live-Audit 08.11.: 85 Konfigurationen auf dem Cluster, VM 311 weiter von Benchmark/Branch/Render-Lab genutzt, 63 Kontexte nicht auswertbar, Single-Point VM 460 |
| `10 actaOne/LiteLLM (Service-Referenz).md` | `b4309e280243` | Opt-in je Instanz statt Promote-Migration, Betriebsvoraussetzungen vor globalem Cutover |
| `10 actaOne/Presidio (Service-Referenz).md` | `244eb2b95ef3` | Vault-first-Rückweg auf Staging |
| `10 actaOne/Wissensdatenbank-Überarbeitung (Konzept).md` | `40d535e90ddc` | Entscheidung AnyDoc statt Docling (11.09.), Docling-Adapter nicht gebaut |

## Abgrenzung zu vorhandenen Skills

Dienstinterna bleiben bei `actaone-presidio`, `actaone-litellm` und dem Agentenprofil `actaone-codeinterpreter`; Vault-Bearbeitung bei `keyvault-edit`, Release-Pfad bei `cut-release`, Playbooks bei `actaone-ansible`, Rechtefenster bei `sudo-window`. Dieser Skill verweist auf sie nur als optionale Ergänzung; er bleibt ohne sie lesbar, echte Arbeit braucht aber Monorepo und Management-Zugang.

## Grenzen

- Keine Live-Prüfung: Instanzzahlen, Endpunkte, Releases und Abschaltstände sind datierte Quellenangaben. Ob die Unit des Legacy-Pools 3112 inzwischen disabled ist, ist offen.
- Die Fleet-weite Presidio-Umstellung ist im Runbook beschrieben; ob und wann sie live lief, wurde nicht geprüft.
- Die Befehlsmuster in `verkehrsnachweis.md` sind aus dem CodeAPI-Runbook verallgemeinert und nicht ausgeführt; der Platzhalter-Ansatz ist für andere Dienste ungetestet.
- Docling hat keinen Betriebsstand; seine Angaben stammen aus einer Recherche gegen Upstream-`main` ohne gepinnten Build.
- IP-Adressen, VM-IDs und Slugs sind intern, nicht geheim. Vor einer Weitergabe außerhalb des Teams prüfen.
- Aktualisierung: bei neuem Release-Manifest oder Runbook-Stand die Tabellen neu hashen und `dienste.md` abgleichen.
