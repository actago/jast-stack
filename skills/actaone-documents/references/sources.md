# Herkunft und Grenzen

Stand 17.11.2026. Nutzerauftrag: vorhandene Dokument-/PDF-Fähigkeiten und einen Ablauf für schön gestaltete CI-Dokumente in JAST aufnehmen.

Grundlagen: lokal synchronisierte Claude-Skills `docx`, `pdf` und `docs` im aktiven Profil `.claude-jast`. Word-/PDF-Ordner wurden vollständig mit Apache-2.0-Lizenz und Einzeldatei-Hashes als eigene JAST-Skills übernommen. Der `docs`-Einstieg enthält ausschließlich eine Anweisung zum Claude-Docs-Connector; er wurde nicht als eigenständig funktionierender Skill kopiert.

Dieser Ordner ist eine eigene, herstellerunabhängige Ergänzung für CI-Quellenauswahl, konsistente Arbeitsquelle, Renderkontrolle und ehrliche Übergabe. Er kopiert keine konkrete Markenrichtlinie. Der Produkt-Skill `document-generation` innerhalb des LibreChat-Forks ist weiterhin nicht Bestandteil dieses Workflows.

## konkrete ci-vorlage und generator

Am 18.11.2026 auf Nutzerauftrag aus `actaOne/outputs/hardware-konzept/` ergänzt. `style.css`, das kleine actaOne-Logo und Inter Regular/SemiBold/Bold sind unverändert übernommen; Byte-Hashes stehen in [ci-source-manifest.json](ci-source-manifest.json). Das vorhandene `build.py` liefert die Seitenstruktur (Cover, band, content, Fußzeilen), Tabellen/Kacheln und das Prinzip HTML → Chromium-PDF. `scripts/build_ci.py` macht daraus einen separaten JSON-Generator mit dynamischer Seitenzahl, escaped Texten, externem Browserpfad, isoliertem Browser und Überlaufprüfung. Keine ursprünglichen Berichtstexte, Messwerte, Ledger oder fertigen Kundenunterlagen sind übernommen.

Die Inter-Lizenz liegt bei; Quelle: https://raw.githubusercontent.com/rsms/inter/master/LICENSE.txt. Die genaue Version der lokalen Schriftdateien ist nicht belegt. Logo und Layout sind Arbeitsmaterial aus dem privaten actaOne-Repo, keine pauschale Lizenzfreigabe für fremde Markenverwendung. Die Vorlage ist keine unabhängig bestätigte vollständige CI-Richtlinie.

Praktisch geprüft: neutraler JSON-Bericht → zwei PDF-Seiten mit lokalem Chrome unter Windows; beide Seiten gerendert und visuell geprüft. Keine DOCX-/PPTX-/XLSX-Abnahme damit verbunden. Die allgemeinen Prüfszenarien bleiben davon getrennt.
