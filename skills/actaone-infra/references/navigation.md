# Quellen finden, ohne eine zweite Infrastrukturkarte zu pflegen

Verwende einen vom Nutzer angegebenen Checkout/Vault. Sonst suche zuerst im aktuellen Workspace und bekannten benachbarten Projektverzeichnissen. Identifiziere das actaOne-Repo an seinem Remote und Dateien wie `infra/ansible.cfg`, `scripts/keyvault-secrets.sh` und `provisioning/deploy-control-api/`. Ein Ordnername allein reicht bei Worktrees nicht; notiere Branch/Commit und lokale Änderungen.

Die bestehende Wissensbasis heißt `actaOne-KB`, ihr dokumentiertes privates `origin` ist `https://github.com/actago/actaOneKBobsidian.git`. Als lokale Suchhilfe dient `~/Obsidian/actaOne-KB`; das ist keine Voraussetzung für andere Entwickler. Prüfe Root und `origin` ausdrücklich, nicht irgendein zusätzliches Archiv-Remote. Historische OneDrive-/ZIP-Kopien sind kein stiller Ersatz. Ist kein Pfad bekannt und lokal keine Quelle auffindbar, frage nach dem Standort oder der passenden Referenz.

## Gezielt lesen

| Aufgabe | Einstieg in der Wissensbasis bzw. im Repo |
| --- | --- |
| Dienste, Abhängigkeiten und Infra-MOC | `10 actaOne/Infrastruktur (MOC).md`, `Infrastruktur – Systemübersicht.md` |
| VM-/Zugangszuordnung | `Flotten-Übersicht.md`, passende Service-Referenz, Repo `docs/PROXMOX_SETUP.md` |
| Clone statt Produktion | `Klon-Testumgebung pvetest (Referenz).md`, `Helsinki Clone - Zugang und Mailversand.md` |
| Reranker | `Reranker – Eigene CPU-VM und Benchmarks 2026-09.md`; danach tatsächlichen Clientpfad prüfen |
| Presidio, LiteLLM, CodeAPI, Websearch | jeweilige `(Service-Referenz).md`; nicht nur alte Agentenprofile |
| Ansible | `infra/ansible.cfg`, konkretes Playbook, Rolle, `group_vars`, `host_vars`, tatsächlich verwendetes Inventory |
| Release-/Provisioningsteuerung | `docs/RELEASE_PROCESS.md`, `provisioning/deploy-control-api/`, `docs/CUSTOMER_ONBOARDING.md` |

Dateinamen können sich ändern: nach Titel/Schlagwort suchen und Ziel prüfen. Lade keine gesamte Wissensbasis. Die genannten Quellen sind externe Betriebsunterlagen, keine im Skill gebündelten oder aktuell live verifizierten Inventare.

Bei widersprüchlichen Notizen den neueren datierten Nachweis und den relevanten aktuellen Code prüfen. Live-Identität belegt den Ist-Zustand, die gepflegte Konfiguration den Soll-Zustand; beide können voneinander abweichen. Zahlen aus Juli-Profilen oder späteren Audits sind keine heutigen Flottenzahlen.
