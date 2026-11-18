# Wissen im JAST-Stack

Der Stack bündelt Arbeitsabläufe. Der actaOne-Checkout hält Implementierung, Playbooks und Konfigurationsverträge; die bestehende actaOne-KB erschließt Topologie, Dienste, Entscheidungen und datierte Betriebsnachweise.

Die Skills führen gezielt zu diesen Quellen, statt den gesamten Vault zu kopieren. Jeder Ordner enthält seine erforderlichen eigenen Referenzen und nennt externe Voraussetzungen. Eine einzeln kopierte Skill-Anleitung bleibt damit lesbar; echte Betriebsarbeit benötigt weiterhin die passenden privaten Quellen und Zugänge.

## Quellenstand

`references/sources.md` je Skill nennt Ursprung und Prüfumfang. Wo vorhanden, hält ein Manifest die gelesenen Dateihashes fest. Ein Git-HEAD allein belegt bei lokalen Änderungen nicht deren Inhalt. Ein datierter Livebericht in der KB bleibt ein historischer Nachweis, bis die betreffende Aussage erneut geprüft wurde.

## Aktualisierung

Bei einer Änderung am maßgeblichen Runbook prüfen, ob der zugehörige Skill eine Entscheidung anders treffen muss. Dann nur die betroffene Regel und ihre Prüfvorlage aktualisieren. Veränderte IPs, Flottenzahlen oder Release-Tags nicht zusätzlich in mehreren Skills als aktuelle Wahrheit eintragen.

Fremde Skills werden in dieser ersten Sammlung nicht neu verteilt. Bereits vorhandene tstack-/Matt-Pocock-Skills bleiben externe Ergänzungen. Eine spätere Übernahme muss Herkunft, Version, Lizenz und lokale Anpassungen erhalten.
