# Herkunft und Pruefumfang

Stand: 2026-11-17. Abgeleitet aus vorhandenen eigenen actaOne-Anleitungen und lokalem Code.

Repository: `actago/actaOne`, Checkout-HEAD: `dd0a3347b23edbeeb2d4ee830d469d14b2cdd188`. Datei-Hashes beziehen sich auf den gelesenen Arbeitsstand; HEAD allein belegt bei lokalen Aenderungen nicht den Inhalt.

- `.claude/skills/sudo-window/SKILL.md`
- `infra/inventory.example.yml`
- `docs/PROXMOX_SETUP.md`

Exakte Hashes: [source-manifest.json](source-manifest.json). Quellenpfade sind relativ zum separaten actaOne-Checkout. Sie sind Laufzeitvoraussetzungen fuer operative Arbeit, keine mitgelieferten Kopien.

Die Session-Auswertung dient der Auswahl und dem Zuschnitt. Historische Sessions und Memory-Dateien sind keine verbindlichen aktuellen Betriebsanweisungen. Keine Live-Zugaenge, Deployments oder Secret-Aenderungen zur Erstellung dieses Skills ausgefuehrt.

Specific adaptations: Replaces fixed NOPASSWD:ALL/file-name recipe with existing admin identity first, safe secret handoff, unique own temporary rules and ownership-aware cleanup.

## Newer reference comparison

Compared against locally available `origin/main` at `73ce7d4ccdb5097d3916f15357da3f4a2a98a7e3` (commit 2026-11-13; no fresh fetch). The initial checkout is 754 commits behind this reference. Original working-file hashes above are historical inputs; newer blob hashes are recorded separately in the manifest. Unchanged source files remain valid at both references.
