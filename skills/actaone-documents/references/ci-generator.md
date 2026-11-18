# ci-pdfs erzeugen

Der Generator übernimmt Seitenstruktur und Drucklayout aus Jacobs Hardware-Konzept. Inhalt kommt aus einer JSON-Datei; er enthält keine Daten der ursprünglichen Berichte.

## start

Aus dem Repo-Root, unter Windows mit PowerShell:

```powershell
python -m venv .venv-docs
.venv-docs/Scripts/python -m pip install -r skills/actaone-documents/scripts/requirements.txt
.venv-docs/Scripts/python skills/actaone-documents/scripts/build_ci.py skills/actaone-documents/examples/report.json --output output/mein-dokument --browser 'C:/Program Files/Google/Chrome/Application/chrome.exe'
```

Der Browserpfad ist ein Beispiel. Ein vorhandener Edge funktioniert ebenfalls. Ohne `--browser` verwendet der Generator Playwright-Chromium; zuvor mit dem Python der Umgebung `-m playwright install chromium` installieren. Unter Linux/macOS liegt der Python einer venv unter `bin/python`; diese Plattformen wurden nicht praktisch geprüft.

`--output` muss ein neuer Ordner sein. Ergebnis: `document.pdf`, die editierbare `content.json`, `index.html`, `style.css` und lokale Assets. Für eine neue Fassung einen neuen Ausgabeordner verwenden. `--html-only` erzeugt nur die Quelle, ohne Browser, PDF oder Layoutprüfung.

## inhalt

Das [Beispiel](../examples/report.json) zeigt das vollständige Schema:

- `title`, `subtitle`, `date`, `label`: Titelseite und Fußzeile.
- `sections`: jeder Abschnitt wird eine eigene Inhaltsseite, zusätzlich zur Titelseite.
- je Abschnitt `title`, optional `eyebrow`, und `blocks`.
- Blöcke: `paragraph`, `heading`, `note` mit `text`; `list` mit `items`; `table` mit `headers` und `rows`; `tiles` mit ein bis vier Einträgen aus `label`, `value`, optional `note`.

Alle Texte werden als Text behandelt, HTML wird escaped. Tabellenzeilen müssen zur Spaltenzahl passen. Für Diagramme oder freiere Gestaltung die HTML-Quelle als Ausgangspunkt verwenden; der JSON-Generator bildet diese Elemente noch nicht ab.

## abnahme

Der PDF-Lauf lädt die gebündelten Schriften und das Logo, blockiert HTTP(S)-Anfragen und prüft den Inhalt gegen den Seitenbereich und die Fußzeile. Bei Überlauf entsteht keine PDF; den Abschnitt aufteilen und neu ausgeben. Dies ersetzt keine Sichtprüfung von Zeilenumbrüchen, Tabellen und Lesbarkeit.

Die finale PDF vollständig rendern und ansehen. Eine vorhandene Vorlage oder ausdrücklich benannte abweichende CI hat Vorrang. Der Generator ist für PDF/HTML; er erzeugt keine Word-Datei. Für Word den docx-Skill nutzen.
