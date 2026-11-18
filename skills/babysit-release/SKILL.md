---
name: babysit-release
description: Begleite einen actaOne-Release-Kandidaten vom Git-Vergleich über Build und Staging-Deploy bis zu featurebezogenen Tests und einer belegten Release-Empfehlung. Nutze bei „babysit release“, „behalte den Release im Blick“, „teste die neuen Features nach dem Build“ oder „prüfe, ob der Kandidat bereit ist“. Fokus ist Staging oder eine benannte Testinstanz, nicht der Flottenrollout.
---

# babysit release

Begleite den konkreten Kandidaten bis zur fachlichen Abnahme. Ein erfolgreicher Build ist noch kein erfolgreich getestetes Release. Dieser Skill ergänzt `cut-release` um laufende Beobachtung und einen aus Änderungen abgeleiteten Testplan; er setzt dessen Installation nicht voraus. Maßgeblich bleiben die aktuellen Quellen im actaOne-Repo, siehe [sources.md](references/sources.md).

## 1. lauf und vergleich festlegen

- Bestehenden Auftrag übernehmen: beobachten/testen, Build auslösen oder zusätzlich Stable freigeben. „Babysit“ allein autorisiert keine Stable-Freigabe, Kunden-Promotion oder Pin-Änderung. Bereits beauftragte Schritte ohne erneute Pauschalbestätigung ausführen.
- Testziel, Remote/Checkout, Lauf-/Jobkennung, konkreten Ziel-Tag und Quellrevisionen erfassen. Ein Release-Kandidat ist hier Staging bzw. eine ausdrücklich benannte Testinstanz. Hat der Nutzer andere Begriffe, nach seinem Ziel arbeiten, nicht aus dem Namen „Release“ eine Flotte ableiten.
- Zwei Baselines unterscheiden: letzter auf diesem Testziel erfolgreich geprüfter Stand für Regressionen und tatsächlich relevanter Kunden-Stable für die spätere Release-Empfehlung. Unterschiedliche Deltas sichtbar machen. Registry und tatsächliche Zielstände heranziehen; ein beweglicher Candidate oder `deploy/RELEASE` ersetzt die Registry nicht.
- Vor dem Warten den [Änderungs- und Testplan](references/feature-test-plan.md) erstellen: Git-Historie **und Diffs**, Aktivierungspfad, Risiken, konkrete Prüfungen. Fehlende Git-Objekte oder Live-Zugänge begrenzen die Aussage, sie werden nicht durch Vermutungen ersetzt.

## 2. build und staging-deploy begleiten

Im vorgesehenen Management-Checkout `docs/RELEASE_PROCESS.md`, `scripts/auto-deploy-staging.sh` und die installierte Fassung prüfen. Der lokale JAST-Stand ist kein Beleg für den aktuell laufenden Worker. Management-Zugang/Umgebung bestätigen; keine IP aus Erinnerungen übernehmen.

Der reguläre Staging-Pfad baut und pusht unveränderliche Tags, aktualisiert Control-Plane und Staging und schreibt nach den Gates einen Candidate. Beobachtungsquellen sind im geprüften Stand `~/.actaone-autodeploy/staging-autodeploy-events.jsonl`, Laufprotokoll und `staging-release-candidate.json`. Events nach Zeitfenster, Tag und vorhandenen Laufkennungen zuordnen, nicht den letzten grünen Eintrag eines anderen Builds verwenden. Aktuelle Dateinamen/Schema im Skript bestätigen.

Nutze den [Beobachtungsablauf](references/monitoring.md). Kein zweiter manueller Build neben Cron/Worker, kein Entfernen fremder Locks, Holds oder `PAUSE`. Ein aktiver fremder Test-Hold ist ein Wartezustand, kein Defekt.

Besonders prüfen:

- Gehören Candidate, `sourceRevisions`, Live-Images und Events zum vereinbarten Kandidaten? Ein Hotfix kann absichtlich außerhalb von `main` liegen.
- Ist `infra_sync` erfolgreich und welcher actaOne-Commit liefert Templates/Skripte? Ein reiner Template-Commit löst im geprüften Stand keinen Image-Build aus, kann aber beim nächsten Deploy wirken.
- Welche Gates liefen wirklich? `STAGING_SMOKE` und `STAGING_DOCUMENT_PROBE` können `off`, `observe` oder `enforce` sein. `observe` blockiert nicht; ein übersprungener Smoke kann selbst bei `enforce` nicht blockieren. `failed`, `skipped`, fehlend und `ok` getrennt protokollieren.
- Ein Terminalevent `complete/succeeded` ist der Übergang zur Abnahme, nicht ihr Ersatz.

## 3. neue funktionen tatsächlich testen

Vor Tests Zielidentität, Tag und wirksame Konfiguration erneut lesen. Falls ein stabiler Staging-Testzeitraum benötigt wird, den vorgesehenen eigenen Test-Hold mit Laufkennung und Ablauf verwenden. Ein Hold stoppt keinen bereits laufenden Deploy. Vorher/nachher Revisionen vergleichen; bei Wechsel den Lauf als gemischt markieren und betroffene Tests neu durchführen. Nur eigene Holds entfernen.

Auf diesem kleinen Zielumfang **alle anwendbaren neuen oder geänderten Fähigkeiten** aus dem Testplan prüfen, nicht nur Stichproben. Dazu die betroffenen Regressionen. Für jedes Feature die Aktivierung und ein beobachtbares Ergebnis nachweisen: beispielsweise Modell sichtbar **und** synthetischer Aufruf erfolgreich, Dokument erzeugt **und** geöffnet, Rollenbeschränkung im zulässigen Testkonto wirksam. Ein YAML-Key allein beweist kein funktionierendes Feature.

Abschließend die wichtigen Pfade nach einer im Plan benannten kurzen Stabilisierungsphase erneut prüfen. Praktischer Ausgangspunkt: ein Recheck nach 10–15 Minuten; asynchrone Migrationen und Caches brauchen ihr eigenes fachliches Abschlusskriterium. Zeitpunkt und Grenzen im Plan festhalten, keine permanente Überwachung behaupten.

Produktionsprüfungen, echte Einladungsmails oder Kundendaten sind damit nicht erlaubt. Synthetische Daten und vorhandene Testkonten verwenden. Ein fehlender Account oder nicht prüfbarer externer Dienst bleibt offen.

## 4. empfehlung und gegebenenfalls freigabe

Berichte `bereit`, `nicht bereit` oder `teilweise geprüft`, jeweils für den exakten Kandidaten. Rote Pflichtprüfungen und ungeklärte Aktivierung verhindern „bereit“. Für bewusst deaktivierte Features ist korrekt deaktiviert ein prüfbarer Sollzustand, kein Auftrag zum Aktivieren.

Wenn Stable-Freigabe beauftragt ist: unmittelbar davor Candidate und Testergebnisse erneut abgleichen. Freigabe über den regulären Ops-Pfad. Registry-Eintrag, Pins samt Warnungen und ausgelöste Hotseat-Wärmung getrennt nachweisen. Die Freigabe kann Pins nachziehen und Hotseats aktualisieren; der Auftrag und der Testplan müssen diese Wirkung abdecken. Bei unbekanntem gewünschtem Pin-Verhalten gezielt klären, keine eigenmächtige Hold-Änderung. Ohne Freigabeauftrag bei der belegten Empfehlung enden.

Abschluss: Basis → Kandidat, aktiver actaOne-/Template-Stand, Aktivierungs- und Testmatrix, Gate-Modi, Ergebnisse des Rechecks, offene Punkte und vorhandener Rückweg. Bei längeren Läufen vorhandenen Postplan aktualisieren und eingerichtete Hark-Benachrichtigungen nach dem geltenden Auftrag nutzen; Details in der Beobachtungsreferenz. Kundenrollout bleibt ein eigener Zielumfang, gegebenenfalls für `babysit-deploy`.
