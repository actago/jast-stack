# Quellen des Skills actaone-litellm

Erstellt am 2026-11-17 durch Lesen lokaler Klone und Dateien. Live wurde nichts geprüft, nichts deployt und nichts verändert. Bei Blob-Hashes handelt es sich um gekürzte Git-Objekt-IDs, bei Datei-Hashes um gekürzte SHA-256-Werte.

## LiteLLM-Repo `github.com/actago/LiteLLM`

Gelesen wurde der lokale Klon `LiteLLM-discovery` mit der Remote-Referenz `origin/main` = `ddfd0e4ef415` (Stand des letzten Fetch, Commit 2026-10-29). Der Arbeitszweig dort steht auf einem älteren Stand und wurde nicht verwendet. Ob `main` seither weitergelaufen ist, wurde nicht geprüft. Die Wissensbasis nennt zum Beispiel LiteLLM #20 als am 08.11. gemergt.

| Pfad | Blob | Letzter Commit | Verwendet für |
|---|---|---|---|
| `ops/MODEL_DISCOVERY.md` | `9fe94db67f0e` | `fc7ca9d` 2026-10-29 | Consumer-Vertrag, Modellkarten, Schritte für neue Modelle, Rückweg |
| `ops/LIFECYCLE.md` | `d325a33d5bf1` | `b326e53` 2026-10-29 | `model_info.actaone` v1, Kanon-Dateien, Deploy, 14-Tage-Pläne, Zugriffsprüfungen |
| `ops/gateway-admin.py` | `e8b2863afe6d` | `744863c` 2026-10-17 | Aktionen und Optionen, Standardlaufzeit 7d für Chat, Wirkung ohne `--customer` |
| `ops/deploy.yml` | – | – | nur der Kopf gelesen (Ziel `litellm_vms`, Pfad `/opt/actaone/litellm`) |

## actaOne-Monorepo `github.com/actago/actaOne`

Gelesen wurde `origin/main` = `73ce7d4ccdb5` (2026-11-13). Der lokale Arbeitszweig lag 754 Commits zurück und wurde nicht verwendet.

| Pfad | Blob | Letzter Commit | Verwendet für |
|---|---|---|---|
| `scripts/chat_gateway.py` | `4c543d9ea59d` | `5c36520` 2026-10-29 | Katalogwahl statisch/Discovery, Pflicht `LITELLM_MODELS` ⊆ Katalog, Preflight Key/Team |
| `docs/LITELLM_FULL_MIGRATION.md` | `e89ca883bac6` | `33ff08e` 2026-10-29 | Vollmodus, Discovery-Vertrag, Dienstepfade, Abnahme, Rückweg |
| `docs/LITELLM_CUSTOMER_ROLLOUT.md` | `91f47c0ff4b5` | `658d827` 2026-11-02 | Instanzfelder, Key-Konventionen, Preflight, Kosten, Rotation |
| `docs/LITELLM_PROMPT_CACHE_ROLLOUT.md` | `2881b52da292` | `a505bea` 2026-10-30 | Cache-Verhalten je Anbieter, Reihenfolge Allowlist → Vault → Staging, Key-Cache 30 s |
| `docs/MODEL_TRANSITIONS.md` | `832ac6d5b1a2` | `354872c` 2026-10-16 | instanzseitige Modellübergänge |
| `scripts/fleet-add-litellm-models.py` | `87730d59bd43` | `98afd06` 2026-10-16 | Vault-Helfer mit fest verdrahteten 2026-10-Zielen |
| `scripts/migrate-litellm.py`, `scripts/audit-litellm.py` | `649b953f66f4`, `21c3303d52fb` | 2026-10-29, 2026-10-19 | nur über die Doku-Beschreibung |
| `deploy/litellm-models.json`, `deploy/litellm-service-models.json` | `1bc775a00a2f`, `0413bd174a64` | 2026-10-29, 2026-10-19 | Existenz statischer Kataloge |

`scripts/configure-chat-gateway.py` und `scripts/revoke-gateway-keys.py` liegen in `origin/main`, ihr Inhalt wurde nicht gelesen.

## Wissensbasis (Obsidian-Vault, Remote `github.com/actago/actaOneKBobsidian`)

Lokaler Stand `d9d678f1e8bd` (2026-11-11), Notizen ohne lokale Änderung.

| Notiz | Blob | Verwendet für |
|---|---|---|
| `10 actaOne/LiteLLM (Service-Referenz).md` | `b4309e280243` | Nachtrag 08.11.: Regionspin, Reranker-Key-Regression, manuelle Gateway-Dateien, offener Neukunden-Chat-Key, Kostenbuchung |
| `10 actaOne/Modellweg – LiteLLM, Claude 5.5 und Prompt-Cache 2026-10.md` | `fea1964004d8` | nur der Titel; im Detail nicht gelesen |

## Memories und Sessions (nur Herkunft, keine Befehle)

Persönliche Claude-Profile, als Belege gelesen:

- Projekt-Memory `litellm-einziger-modellweg.md` (SHA-256 `e4acc447634c`): Entscheidung vom 16.10.2026 und Inventar der Restwege mit Stand 17./18.10.
- Projekt-Memory `litellm-sicherheitslage-2026-10.md` (`04570abbc726`): Supply-Chain-Vorfall bei einer LiteLLM-Version und eine offene Rechteausweitung für die damals eingesetzte Version. Übernommen nur als Regel „Digest, Patches, Sicherheitslage prüfen“.
- Profil-Memory `litellm-testsuite-key.md` (`22c64f094b52`): Team `testsuite` und ein Test-Key mit Budget und Ablauf. Übernommen nur als Regel „Vorhandenes zuerst“. Lokale Ablageorte und Werte wurden nicht übernommen.
- `research/claude-session-audit.md` §2 im JAST-Stack: sechs Sessions zu Modellaufnahme, Keys und Teams. Daraus stammen die Zeilenenden-Falle, die Nutzerkorrektur „wieso Vault“ und die Rückfrage zum vorhandenen Team bzw. Key.

## Agentenprofil

Es gibt kein LiteLLM-Agentenprofil (Suche über die Agenten- und Skillverzeichnisse, bestätigt vom Session-Audit). Dieser Skill ist neu, er stützt sich auf die Repo-Verträge oben und ersetzt kein vorhandenes Profil.

## Grenzen

- Nicht live geprüft: Gateway-Version und Digest, laufende Config gegenüber Repo, Regionen, Keys, Teams, Budgets, Discovery-Status je Instanz.
- Ob der LibreChat-Discovery-Adapter freigegebene Modelle über `LITELLM_MODELS` hinaus anzeigt, wurde im Fork nicht geprüft.
- Die Pfade auf dem Gateway-Host stammen aus Repo-Dokumenten, nicht aus einer Live-Ansicht.
# Nachprüfung 17.11.2026

Für die Review-Korrekturen wurde `ops/gateway-admin.py` zusätzlich lesend von GitHub geprüft: Blob `d470c74f9e2f18090027cbb8a8348de983b221dd`. `info` bleibt eine Einzel-Key-Abfrage mit lokaler Datei, `--generation` hat weiterhin Default `1`, und `create` schützt vorhandene bzw. pending Generationen. Dieser gezielte Abgleich ersetzt keinen aktuellen Abgleich aller übrigen Quellen oder der Live-Version.

