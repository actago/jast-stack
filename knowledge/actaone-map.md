# actaone-quellen finden

## welcher einstieg passt

| Frage | Quelle und Ablauf |
| --- | --- |
| Welcher Dienst, Host oder Zugang? | [Infra-Navigation](../skills/actaone-infra/references/navigation.md), Infra-MOC und passende Service-Referenz im Team-Vault |
| Welches Inventory oder Playbook? | [Ansible](../skills/actaone-ansible/SKILL.md), im actaOne-Repo `infra/ansible.cfg`, Rolle und tatsächlich verwendetes Inventory |
| Wo gehört eine dauerhafte Konfiguration hin? | [Vault](../skills/keyvault-edit/SKILL.md), Repo `docs/AZURE_KEY_VAULT.md` und `scripts/keyvault-secrets.sh` |
| Was ist freigegeben und was läuft? | [Release](../skills/cut-release/SKILL.md), Release-Registry, Zielumfang und Laufzeitnachweis je Instanz |
| Was darf beim VM-Zustandswechsel passieren? | [VM-Lifecycle](../skills/actaone-vm-lifecycle/SKILL.md) und [Kundenanlage](../skills/actaone-provision-customer/SKILL.md) |
| Warum fehlt eine Funktion nach Deploy? | [Diagnose](../skills/diagnose-instance/SKILL.md): Template, Vault, Release-Fähigkeit und Runtime vergleichen |
| Wo halte ich eine Erkenntnis fest? | [KB-Pflege](../skills/actaone-kb-maintenance/SKILL.md): gezielte Referenz, Entscheidung oder Statusnotiz im Team-Vault |

## soll, ist und nachweis

Code, Templates und persistente Konfiguration beschreiben den vorgesehenen Zustand. Die laufende Instanz belegt den Ist-Zustand. Eine datierte Notiz belegt, was zu diesem Zeitpunkt beobachtet wurde. Bei Widersprüchen zuerst Quelle, Version und Zielidentität klären. Ein alter erfolgreicher Rollout beweist nicht, dass heute alle Instanzen gleich laufen.

Die privaten Repos und der Team-Vault sind keine mitgelieferte Infrastruktur. Pfade und Remotes über die Infra-Navigation auflösen. Hier stehen bewusst keine zusätzliche Hostliste oder wechselnde Flottenzahlen; diese würden schnell von den gepflegten Quellen abweichen.

Grundlage dieser Übersicht sind die verlinkten Skill-Referenzen. Sie ist eine Arbeitslandkarte, kein aktueller Live-Status.
