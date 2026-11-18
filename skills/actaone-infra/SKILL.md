---
name: actaone-infra
description: Bestimme für actaOne-Infrastruktur den richtigen Dienst, die Umgebung, den Zugangsweg und die zuständige Betriebsanleitung. Nutze bei VM-, SSH-, Docker-Context- und Ansible-Zuordnung sowie beim Einstieg in unbekannte Infra-Aufgaben.
---

# actaOne-Infrastruktur erschließen

Nutze den bestehenden actaOne-Checkout und die gepflegte Wissensbasis als Quellen. Wie du sie findest und welchen Einstieg du für welchen Dienst liest, steht in [references/navigation.md](references/navigation.md). Der Skill benötigt diese privaten Quellen; sind sie nicht verfügbar, benenne die konkrete Lücke statt Host, Benutzer oder Befehl zu raten. Herkunft und Prüfumfang: [references/sources.md](references/sources.md).

## Ziel bestimmen

Löse den gewünschten Dienst, Zweck und Umgebung gegen die passende Referenz auf. „Reranker“, „Benchmark“ oder „prod“ sind ohne Zuordnung nicht eindeutig. Halte Zielrolle, Quellstand, Zugangsbenutzer und Ausführungsort fest. Ein Hostname allein belegt weder Tenant noch Umgebung; geklonte VMs können Namen und private Adressen teilen.

Erhalte bestehende Zugänge. `ssh acta-mgmt` ist ein dokumentierter Alias, aber keine portable Garantie. Prüfe bei Bedarf die aufgelösten SSH-Parameter gezielt auf Host, User, Port und ProxyJump, ohne Schlüssel oder vollständige Konfiguration auszugeben. Docker-Contexts vor Nutzung gegen ihr tatsächliches Endpoint prüfen; eine neue Context-Definition ist keine Diagnosemaßnahme.

## Identität prüfen und weiterarbeiten

Für einen autorisierten Zugriff bestätige die Umgebung lesend anhand der dokumentierten Route und mindestens eines unabhängigen Identitätsmerkmals, beispielsweise VM-ID/Inventarzuordnung und Gastidentität oder Docker-Endpoint. Bei widersprüchlichen Zielen kläre die konkrete Zuordnung vor einer Mutation. Host-Key-Fehler sind kein Anlass, Prüfungen abzuschalten oder bekannte Schlüssel blind zu ersetzen.

Unterscheide Adminzugang und Runtime-Identität. `actaone`, `actaone-admin`, ein Ansible-SSH-User und ein projektspezifischer Dev-User sind nicht austauschbar. Ermittle Berechtigungen gezielt; versuche nicht der Reihe nach Passwörter oder Benutzer.

Arbeite danach in der zum Auftrag passenden Route:

- Infrastruktur konfigurieren: aktuelle Rolle, Playbook, Inventory und Variablenquellen im Checkout.
- Kundenkonfiguration: Vault-/Template-Vertrag und vorhandene Deployment-Steuerung.
- Release: Registry und beauftragter Zielumfang; `prod` nicht als Kunden-Swarm interpretieren.
- Servicefehler: jeweilige Service-Referenz und relevante Logs im vereinbarten Zeitraum.

Andere installierte Skills können helfen, sind aber keine Voraussetzung dieses Einstiegs. Ein Diagnoseauftrag bleibt lesend. Bereits erteilte Autorisierung für konkrete Änderungen bleibt gültig.

Fertig ist die Orientierung, wenn Ziel, Beleg, Zugangsweg und nächster fachlicher Schritt eindeutig sind. Berichte, was nur dokumentiert und was tatsächlich geprüft wurde. Bei beauftragten dauerhaften Infrastrukturänderungen pflege anschließend die maßgebliche Referenz oder liefere den konkreten Nachtrag, falls sie nicht schreibbar ist.
