# Herkunft und Pruefumfang

Stand: 2026-11-17. Abgeleitet aus vorhandenen eigenen actaOne-Anleitungen und lokalem Code.

Repository: `actago/actaOne`, Checkout-HEAD: `dd0a3347b23edbeeb2d4ee830d469d14b2cdd188`. Datei-Hashes beziehen sich auf den gelesenen Arbeitsstand; HEAD allein belegt bei lokalen Aenderungen nicht den Inhalt.

- `.claude/agents/actaone-infra.md`
- `infra/ansible.cfg`
- `infra/inventory.example.yml`
- `infra/playbooks/configure-deploy-control-api.yml`
- `infra/playbooks/configure-ops-dashboard.yml`
- `infra/roles/deploy_control_api/tasks/main.yml`
- `infra/roles/ops_dashboard/tasks/main.yml`
- `infra/roles/webhook_receiver/tasks/main.yml`

Exakte Hashes: [source-manifest.json](source-manifest.json). Quellenpfade sind relativ zum separaten actaOne-Checkout. Sie sind Laufzeitvoraussetzungen fuer operative Arbeit, keine mitgelieferten Kopien.

Die Session-Auswertung dient der Auswahl und dem Zuschnitt. Historische Sessions und Memory-Dateien sind keine verbindlichen aktuellen Betriebsanweisungen. Keine Live-Zugaenge, Deployments oder Secret-Aenderungen zur Erstellung dieses Skills ausgefuehrt.

Specific adaptations: Extracted operational procedure from the agent profile; added actual Ansible connection identity, persistent variable sources, target overrides, job coordination and bounded check-mode claims.

Additional source checked after review: `.gitignore`.

Additional source checked after review: `provisioning/deploy-control-api/index.js`.

## Newer reference comparison

Compared against locally available `origin/main` at `73ce7d4ccdb5097d3916f15357da3f4a2a98a7e3` (commit 2026-11-13; no fresh fetch). The initial checkout is 754 commits behind this reference. Original working-file hashes above are historical inputs; newer blob hashes are recorded separately in the manifest. Unchanged source files remain valid at both references.

Updated behavior: partner inventory/route assertions and secret diff protection exist in newer roles; verify the actual execution revision.
