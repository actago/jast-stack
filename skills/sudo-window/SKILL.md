---
name: sudo-window
description: Ermittle und verwende den vorgesehenen administrativen Zugang für autorisierte actaOne-Systemänderungen auf Management-, Infrastruktur- oder Kunden-VMs. Nutze bei become-/sudo-Problemen oder einem benötigten temporären Rechtefenster.
---

# Administrative Identität und temporäre Rechte

Dieser Skill aktualisiert den vorhandenen `sudo-window`-Ablauf. Der frühere pauschale Weg über temporäres `NOPASSWD:ALL` ist kein Standard für jeden Host. Quellen und Grenzen: [references/sources.md](references/sources.md).

Bestimme Zielumgebung, SSH-Identität und genehmigte Systemänderung anhand aktueller Zugangsreferenz oder Inventory. Der Runtime-User `actaone` kann absichtlich ohne sudo betrieben werden; ein anderer Adminuser kann bereits den benötigten become-Weg haben. Prüfe passende vorhandene Berechtigungen lesend, beispielsweise `sudo -n` für den konkreten erforderlichen Befehl. Probiere keine fremden Benutzerpasswörter auf Verdacht.

Wenn eine vom Nutzer beauftragte Änderung erhöhte Rechte benötigt, verwende den vorgesehenen Adminzugang. Fehlt nur ein Secret, fordere es über das Secret-Werkzeug der Laufzeit an (in T3 `request_secret`, für stdin-Verwendung `delivery: file`). Kein Passwort im Chat oder in Kommandoargumenten anfordern. Ist kein sicherer Kanal verfügbar, liefere einen konkreten vorbereiteten Schritt zur Ausführung durch den Nutzer; kein Klartext-Fallback.

Bei `sudo -S` fließt das Secret ausschließlich aus der geschützten Datei über stdin; das auszuführende Skript erhältst du über einen separaten Dateipfad, nicht denselben Stream. Bei erforderlichem `su` eine Login-Umgebung verwenden und Root-PATH prüfen; die genaue nichtinteraktive Secret-Übergabe nur mit dafür geeignetem vorhandenen Mechanismus. Keine unbekannten Rechte aus einem fehlenden Programm ableiten.

Ein temporäres sudoers-Fenster ist selbst eine Rechteänderung. Verwende es nur, wenn dieser konkrete Weg durch den Auftrag gedeckt und tatsächlich nötig ist; bevorzuge begrenzte Rechte für die konkrete Arbeit. Bestehende sudoers-Dateien und Rechte nicht überschreiben. Wähle einen eigenen eindeutigen Namen und prüfe vor dem Schreiben, dass er nicht existiert. Bereite Rückbau und Wiederverbindung vor der Änderung vor, prüfe die eigene Datei mit `visudo`, und entferne sie auch nach Fehlern.

Nach der Arbeit prüfe, dass nur die selbst eingerichteten temporären Rechte entfernt wurden und legitime vorherige Adminrechte erhalten bleiben. Ein fehlgeschlagenes `sudo -n true` allein beweist weder vollständigen Rückbau noch den korrekten Host. Lösche eigene Secret- und Skriptdateien im Rahmen ihrer vorgesehenen Lebensdauer. Berichte Ziel, ausgeführte Änderung und Rückbau, keine Zugangsdaten.
