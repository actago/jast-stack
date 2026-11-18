# dokumente bauen

## ci-pdf

Der [Dokument-Skill](../skills/actaone-documents/SKILL.md) enthält einen ausführbaren [Generator](../skills/actaone-documents/scripts/build_ci.py), [Stylesheet und Assets](../skills/actaone-documents/assets/ci/style.css) aus dem vorhandenen Konzeptlayout sowie ein [JSON-Beispiel](../skills/actaone-documents/examples/report.json) und die [gerenderte PDF](../skills/actaone-documents/examples/report.pdf).

Die [Startanleitung](../skills/actaone-documents/references/ci-generator.md) beschreibt Umgebung, Browser und Aufruf. JSON ist die Inhaltsquelle, HTML/CSS das Layout und PDF die Ausgabe. Einen Abschnitt pro Seite planen. Der Export stoppt bei Überlauf; Inhalte aufteilen statt die Schrift immer kleiner zu machen. Nach Änderungen neu rendern und alle Seiten ansehen.

## mitgelieferte helfer

Die Skripte liegen bei den Skills, nicht zentral unter `scripts/`. So bleibt ein vollständiger Skill-Ordner kopierbar.

| Aufgabe | Einstieg |
| --- | --- |
| Word-Dokumente erzeugen | [docx](../skills/docx/SKILL.md): Generierung über die dort beschriebene Bibliothek; kein universeller Word-Generator |
| Word-Kommentare | [comment.py](../skills/docx/scripts/comment.py) |
| Änderungen annehmen | [accept_changes.py](../skills/docx/scripts/accept_changes.py) |
| Office-Dateien prüfen | [validate.py](../skills/docx/scripts/office/validate.py) |
| LibreOffice-Konvertierung | [soffice.py](../skills/docx/scripts/office/soffice.py), auch in pptx/xlsx enthalten |
| PDF-Seiten zu Bildern | [convert_pdf_to_images.py](../skills/pdf/scripts/convert_pdf_to_images.py) |
| PDF-Formularfelder erkennen | [extract_form_field_info.py](../skills/pdf/scripts/extract_form_field_info.py) |
| PDF-Formularfelder ausfüllen | [fill_fillable_fields.py](../skills/pdf/scripts/fill_fillable_fields.py) |
| Folienübersicht rendern | [thumbnail.py](../skills/pptx/scripts/thumbnail.py) |
| Folienthema anwenden | [apply_theme.js](../skills/pptx/scripts/apply_theme.js) |
| Excel-Formeln neu berechnen | [recalc.py](../skills/xlsx/scripts/recalc.py) |

Vor dem Aufruf den jeweiligen Skill und die Skriptargumente lesen. PDF-Bildexport braucht `pdf2image` und Poppler sowie einen existierenden Ausgabeordner. Office-Konvertierung braucht LibreOffice; Folienübersichten zusätzlich Bild-/PDF-Werkzeuge. Die LibreOffice-Wrapper haben Plattformgrenzen, insbesondere auf nativem Windows. Eine Installation der Python-Anforderungen des CI-Generators installiert diese anderen Werkzeuge nicht mit.

## was ein erfolgreicher export belegt

Eine vorhandene Datei belegt nur die Ausgabe. Bei PDF/DOCX/PPTX gehören sichtbare Seiten bzw. Folien zur Abnahme; bei XLSX zusätzlich Formeln und berechnete Werte. Fehlende Schriften, Umbrüche, abgeschnittene Tabellen und fehlende Grafiken sind auch bei einem erfolgreichen Prozess möglich. Das CI-Beispiel wurde unter Windows/Chrome geprüft; die übrigen Helfer sind hier keine pauschal live getestete Toolchain.
