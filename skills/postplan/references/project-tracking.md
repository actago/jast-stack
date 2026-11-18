# Modell für ein dauerhaftes Projektartefakt

## Mindestinhalt

- Projekt: stabile ID, Titel, Ziel, Nicht-Ziele, Planquelle, Aktualisierungsdatum mit Zeitzone, veröffentlichte URL.
- Arbeitspaket: stabile ID, Ergebnis, Status, Abhängigkeiten, konkrete Aufgaben und Abnahmekriterien. Verantwortliche und Schätzung nur soweit bekannt.
- Nachweise: zugehörige PR/Commit, durchgeführte Prüfung mit Ergebnis und Datum, Rollout-Ziel/-Stand. Nicht erforderliche oder unbekannte Felder nicht erfinden.
- Entscheidungen: Datum, Entscheidung, Begründung und Auswirkung auf Umfang oder Reihenfolge.
- Blocker: Ursache, betroffene Pakete, benötigte Entscheidung/Information und nächster Schritt.
- Änderungsverlauf: wesentliche Änderungen seit der letzten Veröffentlichung; Ausgangsplan bleibt nachvollziehbar.

Repo-Konventionen für Datenformat und Rendering verwenden. Maschinenlesbare Daten und HTML nicht unabhängig per Hand fortschreiben: eine Quelle bestimmen und die Darstellung daraus aktualisieren. Bestehende Tracker mit eingebettetem Datenmodell beibehalten, solange die Pflege verlässlich ist.

## Status und Abschluss

| Status | Bedeutung / Übergang |
|---|---|
| offen | Ergebnis beschrieben, noch nicht begonnen |
| in Arbeit | konkrete Umsetzung läuft |
| Review | Umsetzung zur Prüfung bereit; Review noch nicht abgeschlossen |
| blockiert | Fortschritt hängt an einem benannten Hindernis; letzten Arbeitsstand erhalten |
| fertig | vereinbarte Abnahmekriterien des Pakets mit Nachweis erfüllt |
| entfallen | bewusst aus dem Umfang genommen, mit Grund und Datum |

Review, Test, Merge und Rollout als getrennte Nachweise führen. Ein Entwicklungsprojekt kann vor dem Rollout technisch fertig sein, wenn der vereinbarte Umfang so lautet; das Artefakt darf daraus keinen Live-Abschluss machen. Neue Befunde können ein fertiges Paket wieder öffnen; Grund dokumentieren.

## Fortschritt und Zeitplan

Einfachster belastbarer Fortschritt: erfüllte verpflichtende Aufgaben / alle verpflichtenden Aufgaben, plus offene Gates. Entfallene Aufgaben separat ausweisen. Bei geänderten Nennern den Umfangszuwachs erklären.

Gewichteter Fortschritt ist optional: Gewicht je Paket explizit als Schätzung ausweisen, Paketanteil aus erledigten Aufgaben berechnen. Eine Statusänderung auf „fertig“ darf offene Abnahmekriterien nicht verdecken. 99 % ist keine Zusage über Restdauer. Aufwand und verstrichene Zeit nicht gleichsetzen.

Abhängigkeiten anhand stabiler IDs führen. Einen kritischen Pfad oder ein Gantt-Diagramm nur zeigen, wenn Abhängigkeiten, Dauerannahmen und Parallelität vorliegen. Fehlende Termine bleiben unbekannt; keine künstlichen Kalenderdaten erzeugen.

## Rückmeldungen

Das gelesene PDF-Editor-Beispiel hat Checkboxen, Statusauswahl und Kommentare. Deren Änderungen liegen laut HTML im URL-Fragment; ein kopierbarer Text dient der Übergabe in den Chat. Es gibt dabei keinen belegten serverseitigen Schreibweg.

Beim Übernehmen solcher Rückmeldungen Projekt, Basisstand und IDs prüfen. Kommentare und Häkchen sind Eingaben, keine unabhängigen technischen Nachweise. Widersprüche zum aktuellen Tracker lösen; bestehende neuere Änderungen erhalten. Erst die aktualisierte Quelldatei und deren erfolgreicher Upload ergeben einen neuen veröffentlichten Stand.

Keine vertraulichen Rückmeldungen in URL-Fragmente schreiben: sie können über geteilte Links und Browserhistorie weitergegeben werden. Für die normale agentengepflegte Version genügt ein statisches Artefakt mit Rückmeldungen im bestehenden Projektchat.

## Abschluss einer Arbeitssitzung

Quellstand, geänderte Paketstatus, neue Entscheidungen/Blocker und nächste Schritte abgleichen. Falls Veröffentlichung beauftragt und möglich: dasselbe Artefakt aktualisieren und rücklesen. Sonst lokal erhalten und den unveröffentlichten Unterschied nennen. Kein periodisches Polling oder Scheduler ohne Auftrag einrichten.
