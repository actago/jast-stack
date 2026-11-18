---
name: actaone-documents
description: Erstelle oder überarbeite gestaltete Team-Dokumente und CI-PDFs für actaOne/actago aus vorhandenen Vorlagen, Logos und Schriftvorgaben. Wende dieselben CI-Quellen bei Präsentationen und gestalteten Tabellenberichten an. Nutze bei „schönes PDF“, „in unserer CI“, „Dokument im Firmenlayout“ oder einer vorgegebenen Dokumentvorlage. Nicht für die Implementierung der Dokumenterzeugung im actaOne-Produkt.
---

# Dokumente und CI-PDFs

Dieser Skill enthält den wiederverwendbaren HTML/PDF-Generator und das Layout aus Jacobs actaOne-Konzeptdokumenten: Logo, Inter-Schriften, A4-Seiten, Tabellen und Kennzahlkacheln. Das ist eine konkrete Arbeitsvorlage, keine vollständige Markenrichtlinie. Herkunft und Grenzen: [sources.md](references/sources.md).

Für ein CI-PDF in diesem Stil nutze [scripts/build_ci.py](scripts/build_ci.py) mit der Anleitung [ci-generator.md](references/ci-generator.md) und [examples/report.json](examples/report.json). Ein gerendertes [Beispiel-PDF](examples/report.pdf) liegt bei. Alle benötigten Layoutdateien liegen in diesem Skill; Python und Chromium/Chrome/Edge sind Laufzeitvoraussetzungen.

## 1. Format und Grundlage bestimmen

- Angefragtes Ausgabeformat, Zielgruppe und vorhandene Vorlage übernehmen. Ein explizites PDF bleibt ein PDF; eine editierbare Word-Datei zusätzlich liefern, wenn beauftragt oder als vereinbarte Arbeitsquelle benötigt.
- Für DOCX den verfügbaren `docx`-/Dokument-Skill, für PDF den verfügbaren `pdf`-Skill nutzen. Die vollständigen JAST-Ordner `docx` und `pdf` werden separat installiert. Fehlen sie, die im Projekt vorhandene Werkzeugkette prüfen; keine erfundenen Scriptpfade verwenden. Für kollaborative Dokumente einen vorhandenen Docs-Connector nur verwenden, wenn dessen Ziel und Freigabe zum Auftrag passen.
- Für Präsentationen den verfügbaren `pptx`-/Präsentations-Skill verwenden und jede finale Folie prüfen. Für Tabellenberichte den verfügbaren `xlsx`-/Tabellen-Skill verwenden; Formeln und Neuberechnung sind zusätzlich zum Layout zu prüfen. Dieser CI-Ablauf ersetzt keine Formatwerkzeuge und zieht gewöhnliche Datenanalysen nicht in ein Dokumentprojekt um.
- Vorhandene CI-Quelle suchen: bezeichnetes Vorlagenrepo, bereitgestellte DOCX/DOTX, Styleguide oder vom Nutzer benanntes Referenz-PDF. Maßgebliche Version bestimmen; nicht irgendeine alte PDF zur Firmenrichtlinie erklären.
- Dokumentinhalt und CI-Assets getrennt behandeln: eine Kundendatei als Vorlage autorisiert nicht die Übernahme ihrer Inhalte in andere Dokumente oder in den JAST-Stack.

## 2. CI anwenden

Mit der [CI-Prüfliste](references/ci-und-abnahme.md) Logo, Schriften, Farben, Seitengeometrie, Titel-/Kapitelhierarchie und Tabellenstil aus der Quelle übernehmen. Vorhandene Formatvorlagen statt manueller Einzelgestaltung verwenden. Bei mehreren Marken die gewählte Marke pro Dokument konsistent halten.

Fehlt ein einzelnes Asset, übrige Inhalte und Struktur weiterbearbeiten. Die fehlende Vorgabe gezielt klären, sobald sie die Ausgabe bestimmt. Ohne belegte CI kann ein neutral gestalteter Entwurf entstehen; ihn ausdrücklich als Entwurf kennzeichnen und nicht als „CI-konform“ ausgeben. Keine erfundenen Markenwerte oder Platzhalterlogos als endgültige Assets verwenden.

## 3. Erstellen und exportieren

Eine editierbare maßgebliche Quelle erhalten: bestehende Word-Vorlage, projektübliche HTML/CSS-Quelle oder Generator. Originaldateien nicht überschreiben. Wiederholte Ausgaben aus derselben Quelle erzeugen; keine parallelen manuellen Korrekturen in Word und PDF.

Inhalt hierarchisch gliedern und Layout darauf abstimmen: klare Titel, lesbare Tabellen, angemessene Abstände, zusammenhängende Beschriftungen und gezielte Seitenumbrüche. Schmuckelemente dürfen Inhalt und Lesbarkeit nicht verdrängen. Logos nicht verzerren, Schriften nicht still ersetzen.

Konverter und Renderer samt erforderlichen Schriften im tatsächlichen Arbeitsumfeld prüfen. PDF aus der finalen Quelle exportieren; Unterschiede zwischen Word-/LibreOffice-/HTML-Rendering sichtbar prüfen statt Layoutgleichheit vorauszusetzen. Neue Abhängigkeiten im vorgesehenen Dokument-Workspace einrichten, keine fremde Projektumgebung beiläufig verändern.

## 4. Visuell abnehmen

Alle Seiten der finalen PDF rendern und ansehen, nicht nur Titelseite oder Textauszug. Bei Änderungen neu exportieren; anschließend die betroffenen Seiten und den gesamten Seitenfluss prüfen. Die [CI-Prüfliste](references/ci-und-abnahme.md) trennt Inhalts-, Layout- und technische Prüfung.

Fehlender Renderer oder fehlende Schrift bedeutet einen offenen Prüfpunkt. Keine „druckfertige“, barrierefreie oder PDF/A-konforme Ausgabe behaupten, wenn diese Eigenschaft nicht passend validiert wurde.

## 5. Übergeben

Finale angefragte Datei(en) verlinken, verwendete Vorlage nennen und verbleibende Abweichungen knapp angeben. Arbeitsquelle am vereinbarten Ort erhalten. Keine Veröffentlichung, Kundenmail oder Postplan-Veröffentlichung allein aus einem PDF-Auftrag ableiten.
