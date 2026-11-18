# beobachten bis zur abnahme

## vor dem warten

Zuerst vorhandene Zustände lesen und handeln, dann auf Veränderungen warten. Lauf-/Jobkennung, Startzeit, Ziel-Tag, Zielinstanzen, letzte verarbeitete Eventposition, Fehler, Testergebnisse, nächste fällige Prüfung und eigene Holds in einem lokalen Run-Nachweis festhalten. Beim Resume damit den tatsächlichen Zustand abgleichen; eine unterbrochene Sitzung ist kein fehlgeschlagener Deploy.

## beobachtungsquelle wählen

- Staging: Events, Candidate und Protokoll des konkreten `auto-deploy-staging.sh`-Laufs. Der globale State-Ordner kann mehrere Läufe enthalten.
- Ops-/Flottenjob: vorhandenes Dashboard bzw. Deploy-Control-API, Job-ID und zugehörige Ausgabe. Im geprüften Stand existieren `GET /api/v1/jobs` und `GET /api/v1/jobs/<id>/output`; den konkreten Auth-/Responsevertrag aus der aktuellen `index.js` lesen. Keine frei erfundene Watch-API.
- Direkter Promote: eigener Prozess-/Runstatus und zugehörige Logdatei, danach unabhängiges Readback. Ein abgerissener SSH-Client sagt nichts darüber, ob der entfernte Prozess beendet ist.

Eingerichtete Zugänge nutzen. Fehlende Secrets über den sicheren Secret-Mechanismus des Harness anfordern; keine Tokens in Chat, URLs oder Logs kopieren. Rohlogs bei Bedarf auf Zeitfenster und Fehlerklasse begrenzen.

## laufend begleiten

Den tatsächlich verfügbaren Ereignis-/Streaming- oder Background-Mechanismus des Harness verwenden, der bei Änderungen in diese Sitzung zurückmeldet. Pro Lauf einen Beobachter behalten. PR-Watcher beobachten PRs, keine Deploy-Jobs; nur für eine separat beauftragte PR-Voraussetzung verwenden. Bei delegierter Arbeit die vom Orchestrator vorgegebene Fortsetzung einhalten, keinen zusätzlichen Status-Poller bauen.

Falls nur Statusabfragen möglich sind, kurze begrenzte Abfragen mit einem dem Lauf angemessenen Abstand verwenden (typisch 30–60 Sekunden), keine enge Endlosschleife. Ein Gesamtzeitfenster und Stagnationsgrenze anhand Runbook/vergleichbarem Lauf oder Nutzerauftrag festhalten. Erreichter Grenzwert ist `blockiert/noch laufend`, nicht Erfolg und kein Grund für Prozess-Kill.

Neue Phase, Fehler, nötige Entscheidung und Abnahme sind relevante Ereignisse. Wiederholt identische „läuft noch“-Nachrichten vermeiden. Ein terminal erfolgreicher Job startet die Ziel-/Featuretests. Ein terminal fehlgeschlagener Job verlangt zuerst Prüfung bereits angewendeter Teiländerungen. Bei echtem Stillstand Diagnose innerhalb des Auftrags; keine parallele Wiederholung mit unbekannten Nebenwirkungen.

Ohne persistente Hintergrundfunktion nicht behaupten, nach Turn-Ende weiter zu beobachten. Entweder die laufende Sitzung bis zum vereinbarten Prüfschritt nutzen oder mit konkretem Checkpoint und noch ausstehendem Recheck übergeben. Keine neue Daueraufgabe oder Hook-Konfiguration allein aus „babysit“ installieren. Erfordert ein Zeitfenster eine andere verfügbare Laufzeit, deren Einrichtung gesondert konkret benennen.

## fortschritt und benachrichtigungen

Der Nutzer nutzt Postplan und Hark für lange Aufgaben. Wenn vorhanden und vom geltenden Auftrag gedeckt:

- denselben Postplan mit Phasen, offenen Findings und Testabdeckung aktualisieren; keine Secrets, internen Instanzlisten oder Kundendaten in veröffentlichte Pläne übernehmen;
- über den eingerichteten Hark-Skill verifizierten Abschluss, Fehler oder Entscheidungsbedarf melden. Keine Webhook-Adresse ausdenken oder aus privaten Dateien in Berichte übernehmen. Wiederholungen mit derselben Ereignis-ID deduplizieren;
- Post-Session-Hooks können die Nachbereitung übernehmen, sind aber kein Beweis einer laufenden Jobüberwachung. Nur tatsächlich vorhandene Hooks als aktiv beschreiben.

Fehlendes Postplan/Hark blockiert keine lokalen Prüfungen. Benachrichtigungsfehler separat vom Deploy-Ergebnis melden; Annahme durch einen Push-Dienst ist kein Lesebeleg. Rückfragen zusätzlich in der Sitzung stellen.

## ende

Erst beenden, wenn alle Zielstatus erfasst und die geplanten Nachprüfungen durchgeführt sind, oder einen konkreten Blocker samt offenem Umfang übergeben. Eigene Beobachter/temporäre Test-Holds beenden, fremde Ressourcen erhalten. Abschluss mit Belegen und Grenzen statt „alles grün“ aus einem Exitcode.
