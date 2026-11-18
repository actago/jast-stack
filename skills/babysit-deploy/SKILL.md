---
name: babysit-deploy
description: Begleite einen actaOne-Deploy oder Flottenrollout mit Git-basierter Feature- und Aktivierungsanalyse, Testplan, Jobüberwachung, Konfigurationsnachweis auf allen Zielen und risikobasierten Funktionstests während und nach dem Rollout. Nutze bei „babysit deploy“, „behalte den Rollout im Blick“, „prüfe ob alles angewendet wurde“ und „teste danach stichprobenartig die Instanzen“.
---

# babysit deploy

Beobachte den beauftragten Deploy bis zum nachgewiesenen Endzustand, einschließlich wirksamer Features. Ein grüner Job oder gleicher Image-Tag genügt nicht. Dieser Skill ergänzt `cut-release`, ersetzt aber weder die aktuellen Repo-Runbooks noch deren Release-Gates. Er kann ohne installierten Geschwisterskill anhand der [Quellen](references/sources.md) verwendet werden.

## 1. zielumfang und featureplan einfrieren

- Auftrag und vorhandenen Job erfassen: nur laufenden Deploy beobachten/testen oder selbst den Deploy starten. Keine doppelte Jobanlage beim Wiederaufnehmen. Bereits erteilte Autorisierung gilt; zusätzliche Zielinstanzen, Vault-Migrationen und Rollbacks sind nicht automatisch enthalten.
- Eine aktuelle Zielliste mit stabiler Instanzidentität, Umgebung, Ist-Tag, gewünschtem Ziel-Tag und Konfigurationsprofil erstellen. Ausnahmen, Holds, gestoppte/nicht erreichbare Ziele und nicht beauftragte Hotseats/Branch-/Benchmark-/Lab-Instanzen ausdrücklich trennen. Keine Flotte aus einem alten Inventar ableiten.
- Produktions-Tags gegen die Stable-Registry prüfen. Die Flotte kann mehrere Ausgangs- und erlaubte Ziel-Tags haben. Der geprüfte Flottenworker akzeptiert nur den neuesten Stable; für ältere oder gemischte Tags muss der aktuell unterstützte Einzelpfad gewählt werden.
- Vor einem neuen Apply den [Änderungs- und Testplan](references/feature-test-plan.md) aus Git-Historie und tatsächlichen Ausgangsständen ableiten. Auch bei **gleichem Image-Tag** Template-, Renderer-, Vault-Default- und Migrationsänderungen erfassen. Bei schon laufendem Job die Analyse nachholen, ohne seine bisherigen Schritte als ungeschehen zu behandeln.

## 2. aktivierung vor der ersten welle prüfen

Im Management-Checkout Version und lokale Abweichungen lesen. Die tatsächlich verwendeten Templates, Slug-Overrides, Profil-Renderer, Release-Feature-/Env-Nachbearbeitung und Migrationsregeln bestimmen. Ein Standardtemplate ist nicht automatisch die endgültige Kundenkonfiguration.

Je Änderung dokumentieren: erforderliche Image-Version, dauerhafte Quelle, Default/Opt-in, Zielprofil, Aktivierungsreihenfolge, beauftragte Mutation, Laufzeitnachweis und Rückweg. Fehlende Freigabe für einen zusätzlichen Schalter als konkreten Blocker melden; nicht im Namen eines Tests aktivieren.

Der reguläre Promote kann Vault-Bundles publizieren, fehlende Defaults ergänzen und Presidio-/CodeAPI-Migrationen anstoßen. Diese Nebenwirkungen gehören in die Vorprüfung. Template und Image müssen kompatibel sein. Globale Defaults nicht vorzeitig für noch inkompatible Instanzen freischalten.

## 3. canary und wellen begleiten

Canary aus dem beauftragten Zielumfang wählen. Wenn mehrere relevante Profile/Overrides betroffen sind, vor breiter Fortsetzung mindestens einen Vertreter je betroffener Klasse testen. Hat der Nutzer bereits Canary/Wellen festgelegt, diese übernehmen und verbleibende Abdeckungslücken benennen.

Den aktuellen Ops-/Panel-/Promote-Pfad verwenden und über den [Beobachtungsablauf](references/monitoring.md) begleiten. Zwei unterschiedliche Fehlerverhalten beachten:

- Eigene serielle Einzel-Promotes: beim ersten Fehler keine nächste Instanz starten, Teilzustand prüfen.
- Ein bereits gestarteter `promote_all_customers`-Job kann nach Fehlern weiterlaufen. Fehler sofort melden und keine weitere eigene Welle starten. Nicht behaupten, der laufende Worker sei angehalten. Nur einen im aktuellen System vorhandenen, autorisierten Abbruchweg verwenden; kein improvisierter Prozess-Kill.

Im geprüften Stand überspringt der Worker gleiche Image-Tags ohne offene Release-Migration. Ein solcher Skip beweist keinen Template-/Vault-Nachzug. Bei erforderlichem Same-Tag-Redeploy den vorgesehenen Pfad erst gegen den Code prüfen: `promote_customer_vm` kann den gleichen Tag ablehnen; nicht einfach denselben Flottenjob wiederholen. Bereits angewendete Teiländerungen vor einem Retry erfassen.

## 4. alle ziele prüfen, funktionen gezielt testen

**Jede Zielinstanz** erhält nach ihrem Deploy einen Status mit Nachweis: Identität, Live-Images, dauerhafte Service-Replikas, Health/Erreichbarkeit, erwartete Konfiguration und betroffene Migrationen. Erfolgreich abgeschlossene One-shot-Tasks nicht als dauerhaft fehlenden Service werten. Erwartete Konfigurationshashes sind je Instanz verschieden; nicht pauschal alle mit Staging gleichsetzen. Ohne einen nebenwirkungsarmen Soll-Render oder feldbegrenzten Sollnachweis Konfiguration als ungeprüft markieren. Ein vermeintlicher Dry-Run darf keine Bundles schreiben.

**Funktionstests als begründete Stichprobe:**

1. Nach Canary alle für diese Klasse relevanten neuen Features testen.
2. Nach jeder Welle mindestens einen Vertreter jeder darin neu auftretenden Aktivierungsklasse prüfen, außerdem fehlgeschlagene/nachgebesserte Ziele und auffällige Same-Tag-Skips gezielt aufnehmen. Bei nur einer Instanz diese vollständig testen.
3. Für weitere Stichproben die Auswahl wechseln; nicht immer nur den bekannten Canary testen. Kriterien und ausgewählte Slugs protokollieren. Auswahl nach Profil, Ausgangsrelease, Override, Migration und Feature-Risiko, nicht nach einer unbegründeten festen Prozentzahl.
4. Nach Abschluss einen zeitversetzten Recheck wichtiger Funktionen und Gesundheit durchführen; als Ausgangspunkt 10–15 Minuten, angepasst an Migration/Cache/Warm-up. Keine automatische Dauerüberwachung für spätere Tage einrichten.

Tests verwenden synthetische Daten und passende Testidentitäten. Wenn ein Produktivtest neue Daten, Kosten oder sichtbare Aktionen verursacht, muss er vom vereinbarten Testumfang gedeckt sein. Fehlende sichere Testmöglichkeit melden, nicht auf reale Kundenchats ausweichen. Sicherheit, Datenintegrität oder eine instanzspezifische Migration können Funktionsnachweise auf **allen betroffenen Zielen** verlangen; eine Stichprobe ersetzt sie dann nicht.

Bei Funktionsfehlern weitere eigene Wellen aussetzen, die betroffene Klasse komplett auf Aktivierung/Drift prüfen und die funktionale Stichprobe erweitern. Eine Korrektur erfolgt an der dauerhaften Quelle, im autorisierten Umfang, mit erneutem Readback. Kein Live-Patch, der beim nächsten Deploy verschwindet.

## 5. belegter abschluss

Jedes eingefrorene Ziel ist als `verifiziert`, `fehlgeschlagen`, `nicht erreichbar`, `ausgenommen` oder `offen/nicht geprüft` erfasst. „Bereits auf Ziel“ zählt erst nach den gleichen Basisnachweisen wie ein neuer Deploy. Gesamtanzahl gegen Zielliste abgleichen, fehlende Contexts nicht als harmlose Skips verschlucken.

Bericht: Ziel-Tags und tatsächlicher Template-/Worker-Stand, Jobstatus, Status je Instanz, Testabdeckung je Feature/Klasse, Stichproben und Zeitpunkt, Nachprüfung, offene Ausnahmen sowie Rückweg. Erfolgreich ausgerollt und funktional nur stichprobenartig geprüft getrennt ausdrücken. Ungeprüfte Pflichtaktivierung verhindert einen vollständigen Erfolg.

Wenn Rollback beauftragt ist, den aktuellen regulären Rückweg nutzen und Image-, Konfigurations-, Vault- und Migrationswirkungen getrennt prüfen. Im geprüften Stand setzt `rollback_customer_vm` einen Presidio-Migrations-Skip; ein beliebiger manueller Promote auf einen alten Tag ist deshalb nicht gleichwertig. Kein zusätzlicher VM-Abbau oder Pruning aus einem Deploy-Auftrag ableiten.
