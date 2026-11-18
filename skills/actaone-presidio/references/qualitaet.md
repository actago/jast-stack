# Presidio: Entitäten, Erkennungsqualität und Testservice

Grundlage: Runbook `docs/operations/presidio-singleton.md`, `tools/presidio-testservice/README.md` (actaOne-Monorepo) und die Wissensbasis-Notiz „Presidio (Service-Referenz)“. Werte sind datiert; für Aussagen über den heutigen Release neu messen.

## Erkennungskette

- spaCy (`de_core_news_md`, `en_core_web_lg`) plus GLiNER (`urchade/gliner_multi_pii-v1`, im Image) plus Muster-Erkenner. `ORGANIZATION` wird bewusst ignoriert (Falschtreffer).
- Deutsche Erkenner u. a. Steuer-ID, Pass, Personalausweis, Sozialversicherung, KV-Nummer, Kfz, Handelsregister, PLZ, LANR/BSNR, USt-ID, Führerschein; generisch IBAN, E-Mail, Telefon, IP, Kreditkarte. actago-eigen: Familienstand (Deny-List), Personalausweis-Regex.
- Token-Format `<TYP_n>`, Index je Typ; gleicher Originalwert ergibt über alle Nachrichten einer Anfrage dasselbe Token.

Den heute aktiven Satz an Erkennern und Labels im Fork (`services/presidio` bzw. `actago/presidio`) und in der Release-Datei des Ziel-Singletons nachsehen. Staging-Releases enthalten Erkennerverbesserungen oft vor Prod; Verbesserungen nicht als in Prod vorhanden ausgeben, ohne den Prod-Release zu prüfen.

## Bekannte Fehlerbilder

| Bild | Ursache laut Quellen | Prüfung |
|---|---|---|
| Massenhaft Zahlen, Beträge, Versionen als Token | leerer `PSEUDONYMIZATION_SCORE_THRESHOLD=` wird in LibreChat zu 0 | effektiven Wert der Instanz lesen; Analyzer-Standard ist 0,30 |
| Passwortrest im Klartext (`…#Amt`) | SECRET-Regex bei `#`/`!` (älterer Release) | Release-Stand der Erkenner prüfen, Testservice-Fall E-17 |
| Rollen, Pronomen als PERSON; Vorlagennummern als Telefon; Beträge als Steuernummer | GLiNER/Muster auf Fachtexten | Korpuslauf; kein Leck, aber Qualitätsverlust |
| `[PERSON_1]` bleibt in der Antwort stehen | Modell schreibt eckige statt spitze Klammern; LibreChat-Regex erwartet `<…>` | LibreChat-Fork, nicht Presidio |
| Klartext im Konversationstitel | Titelpfad der App (separat gefixt, Stand je Release prüfen) | LibreChat-Release der Instanz |
| Bereits gesetzte Tokens erneut als PERSON | GLiNER erkennt `<PERSON_0>` | Testservice-Fall, Release vergleichen |

Leck und Falschtreffer getrennt berichten: Ein Leck (Klartext erreicht den Anbieter) ist ein Datenschutzbefund; ein Falschtreffer kostet Antwortqualität, weil der Rückweg den Text wiederherstellt.

## Testservice (`tools/presidio-testservice`)

Lokales Node-Werkzeug mit synthetischen Fällen. Klassen: `E` Erkennung, `N` Falschtreffer, `M` Mischtexte, `L` lange Texte über Fenstergrenzen, `P` Pseudonymisierung über mehrere Nachrichten, `K` Kontrakt (Health, Operator, Zugriffsschutz, Routen, Validierung).

- Ziele: `singleton` (über mgmt-Relay mit der Probe-Identität; Schlüssel bleiben auf mgmt), `local` (Container per Digest), `url`.
- Profile: `staging` (Schwelle 0, bildet den leeren Staging-Wert nach) und `analyzer` (Analyzer-Standard 0,30). Für Aussagen über Kundenverhalten das Profil passend zur effektiven Instanzkonfiguration wählen.
- Standard seriell. Lange Fälle und Last nur mit `--allow-load` und nur bei ausdrücklichem Auftrag, weil Staging am selben Singleton hängt.
- Bewertung: Punkte, Präzision auf Negativwerten, Gates. Immer gegen den Vorrelease mit gleichem Profil vergleichen. Datierte Referenzwerte laut Runbook (Staging, Profil `analyzer`): 2026.11.03.1 92,6 Punkte; 2026.11.06.1 95,2 Punkte; der Release 2026.10.20.2 war mit 49/100 „No-Go“.

Neue Erkenner oder Regeln: synthetische Positiv- und Negativbeispiele als Testfälle ergänzen, Falschtreffer-Wirkung auf Fachtexte (Urteile, Ratsdokumente) betrachten, Latenz und Speicher je Worker prüfen. Testdaten mit gültigen Prüfziffern synthetisch erzeugen, nie aus Kundendaten.
