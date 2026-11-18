# Quellen des Skills actaone-presidio

Erstellt am 2026-11-17 durch Lesen lokaler Klone und Dateien. Es wurde nichts live geprüft, deployt oder verändert. Blob-Hashes sind Git-Objekt-IDs (gekürzt), Datei-Hashes SHA-256 (gekürzt).

## actaOne-Monorepo `github.com/actago/actaOne`

Gelesener Stand: lokale Remote-Referenz `origin/main` = `73ce7d4ccdb5` (Commit 2026-11-13). Der lokale Arbeitszweig `main` stand auf `dd0a334` (2026-09-16) und damit 754 Commits zurück; er wurde nicht verwendet. Ob `origin/main` seit dem letzten Fetch weiter ist, wurde nicht geprüft.

| Pfad | Blob | Letzter Commit | Verwendet für |
|---|---|---|---|
| `docs/operations/presidio-singleton.md` | `fd240441d11b` | `7d78995` 2026-11-06 | Topologie, Gateway, PKI, Release, Skalierung, Rückweg, Befunde |
| `docs/rollouts/production-2026-11.md` | `dd81f3ff549e` | `ccde26e` 2026-11-04 | Automatische Kundenumstellung im Promote, Ausnahmen |
| `deploy/presidio/nginx.conf` | `44356343fb7f` | `f47fee9` 2026-11-04 | Erlaubte Routen, mTLS (Limits dort sind Vorlage; wirksam sind die Profilwerte) |
| `deploy/presidio/environments/staging.env`, `prod.env` | `3f11f172070a`, `8c45b7fcffd2` | `f47fee9` 2026-11-04 | Existenz der Profile |
| `scripts/deploy-presidio.py` | `df28cc15bfd2` | `f47fee9` 2026-11-04 | nur über Runbook-Beschreibung, Code nicht im Detail gelesen |
| `scripts/presidio-release-migration.sh` | `c3b72fc606d5` | `78b366f` 2026-11-04 | nur Existenz und Runbook-Beschreibung |
| `scripts/verify-customer-presidio.sh`, `scripts/verify-presidio-infra.py` | `9a81de24a984`, `6271812c6c76` | `161f7ad` 2026-10-20 | Prüfwege |
| `tools/presidio-testservice/README.md` | `63762599d0e3` | `57720aa` 2026-10-21 | Testservice, Profile, Fallklassen |
| `.claude/agents/actaone-presidio.md` | `b95b7c690d0d` | `683ccf0` 2026-07-22 | Ausgangsprofil (s. u.) |

Im lokalen Arbeitsbaum liegen zusätzlich die nicht versionierten Dateien `docs/PRESIDIO_SINGLETON_ROLLOUT.md` und `deploy/presidio-singleton/`. Sie fehlen in `origin/main` und wurden als überholte Entwürfe nicht verwendet.

## Agentenprofil `actaone-presidio`

Projektkopie im Monorepo und Benutzerkopie im Claude-Profil sind bis auf Zeilenenden gleich (SHA-256 `c2b129a00f85` bzw. `06a7a35043c9`). Übernommen: Rolle von Analyzer/Anonymizer/Pseudonymizer, Release-Tag-Bestandteil `pii-<sha>`, Arbeitsweise Branch → Tests → Staging-Cron, Fokus auf deutsche Verwaltungsdaten, Pflicht zur Falschtreffer-Betrachtung. **Nicht übernommen** (überholt): „läuft je Kundeninstanz“ als alleiniger Betriebsmodus, Speicher-/Latenzwerte des lokalen Betriebs, die feste Co-Author-Zeile.

## Wissensbasis (Obsidian-Vault, Remote `github.com/actago/actaOneKBobsidian`)

Lokaler Stand `d9d678f1e8bd` (2026-11-11), Notiz ohne lokale Änderung.

| Notiz | Blob | Verwendet für |
|---|---|---|
| `10 actaOne/Presidio (Service-Referenz).md` | `244eb2b95ef3` | Betriebsstand 08.11. (77/77-Audit vom 05.11.), Request-Pfad, Erkenner, Fehlerbilder, offene Punkte |

Die Notiz kennzeichnet ihre Implementierungsangaben (August/September) selbst als nicht neu auditiert.

## Session-Belege (nur Herkunft, keine Befehle)

- Session-Audit des JAST-Stacks (`research/codex-session-audit.md`, §6): Presidio-Umstellung pro Instanz auf zentral am 03.11.; der Agent fragte nach Host/IP, die bereits dokumentiert waren. Begründet die Regel „Quellen und Live-Zustand zuerst“.

## Grenzen

- Keine Live-Prüfung: Releases, Replikas, Kundenmodi, Zertifikatslaufzeiten und Kapazität sind Quellenangaben mit Datum.
- Der Presidio-Fork und der LibreChat-Pseudonymisierungscode wurden nicht im Detail gelesen; Angaben dazu stammen aus Runbook und Wissensbasis.
- IP-Adressen, VM-IDs und Hostnamen sind intern, nicht geheim. Vor einer Weitergabe außerhalb des Teams prüfen.
- Aktualisierung: bei neuem Runbook-Stand oder Release die Tabellen oben neu hashen und `betrieb.md` abgleichen.
