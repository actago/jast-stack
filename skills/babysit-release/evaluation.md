# prüffälle

Synthetische Fälle für eine spätere isolierte Agentenprüfung. Erwartete Entscheidungen sind keine Live-Abnahme. Nur den Fall und nötige Rohquellen an einen Prüfer geben; diese Erwartungen zunächst zurückhalten.

| fall | eingabe | erwartetes verhalten |
| --- | --- | --- |
| neues feature braucht konfiguration | kandidat c2 enthält einen export-fix; staging läuft c1; git-diff nennt einen neuen schlüssel, der im staging-template fehlt | feature → aktivierung → test verfolgen; fehlende wirksame konfiguration melden; ein grüner build wird nicht als feature-erfolg gewertet |
| grüne pipeline, roter test | complete/succeeded, document-render:failed bei observe, smoke:skipped bei enforce | gates einzeln bewerten; skipped ist kein bestandener test; relevante offene funktionsprüfung verhindert bereit |
| kandidat wechselt | tests starten auf c2, vor abschluss steht c3 im candidate und auf staging | tests nicht auf c3 übertragen; gemischten lauf markieren, delta prüfen und betroffene tests neu ausführen |
| hotfix statt main | kunden-stable s1 plus ein cherry-pick, main enthält drei weitere features | exakte revisionsbasis verwenden, keine main-features als enthalten auflisten; keine freigabe von main ableiten |
| bewegliche infra | nur actaone-template geändert; kein neuer komponenten-commit | nicht endlos auf einen image-build warten; tatsächlichen infra-/template-stand und autorisierten apply prüfen |
| nur beobachten | „babysit diesen kandidaten“, gates und fachtests grün | belegte empfehlung liefern, keine stable-freigabe und keine pinänderung |
| ausdrücklich freigeben | „prüfe c2 und gib ihn bei erfolg stable frei“, pinwirkung geklärt; candidate noch c2 | keine erneute pauschalfreigabe verlangen; registrierung/pins/hotseats als getrennte nachweise, warnung nicht verschlucken |
| kein hintergrundmechanismus | lauf braucht länger als die verfügbare sitzung; keine wake-/streaming-funktion | konkreten checkpoint/offenen recheck melden; keine erfundene dauerüberwachung oder neue cron-installation |

Für den Normalfall muss der erzeugte Plan mindestens die beiden Baselines, Commitbeleg, Aktivierungsquelle, wirksamen Zielstand, konkreten Funktionstest und Nachprüfung enthalten. Eine reine Commitliste besteht den Fall nicht.
