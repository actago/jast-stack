# Herkunft und Pruefumfang

Stand: 2026-11-17. Abgeleitet aus vorhandenen eigenen actaOne-Anleitungen und lokalem Code.

Repository: `actago/actaOne`, Checkout-HEAD: `dd0a3347b23edbeeb2d4ee830d469d14b2cdd188`. Datei-Hashes beziehen sich auf den gelesenen Arbeitsstand; HEAD allein belegt bei lokalen Aenderungen nicht den Inhalt.

- `.claude/skills/keyvault-edit/SKILL.md`
- `scripts/keyvault-secrets.sh`
- `CLAUDE.md`

Exakte Hashes: [source-manifest.json](source-manifest.json). Quellenpfade sind relativ zum separaten actaOne-Checkout. Sie sind Laufzeitvoraussetzungen fuer operative Arbeit, keine mitgelieferten Kopien.

Die Session-Auswertung dient der Auswahl und dem Zuschnitt. Historische Sessions und Memory-Dateien sind keine verbindlichen aktuellen Betriebsanweisungen. Keine Live-Zugaenge, Deployments oder Secret-Aenderungen zur Erstellung dieses Skills ausgefuehrt.

Specific adaptations: Preserved scopes/chunking/SecretNotFound behavior; requires insertion of missing keys, manifest/part version comparison and writer coordination; Vault versions replace local restore copies.

Additional source checked after review: `docs/AZURE_KEY_VAULT.md`.

## Newer reference comparison

Compared against locally available `origin/main` at `73ce7d4ccdb5097d3916f15357da3f4a2a98a7e3` (commit 2026-11-13; no fresh fetch). The initial checkout is 754 commits behind this reference. Original working-file hashes above are historical inputs; newer blob hashes are recorded separately in the manifest. Unchanged source files remain valid at both references.

Updated behavior: defaults backfill existing customers during promotion; release-gated Self-Heal filtering distinguishes stored and deployable views. Checked promote.sh, selfheal_levels.py and the rollout document in the newer reference.
