# Prüffälle

Synthetische Textszenarien, nicht ausgeführt.

- Bestehendes Modell mit farbigen Eingabezellen ändern: nur Eingabezellen schreiben, Formeln unverändert, Konventionen der Datei vor Leitlinien.
- Neue Formeln geschrieben, LibreOffice fehlt: `recalc.py` kann nicht laufen; offen sagen, dass Formelwerte unverifiziert sind, statt „0 Fehler“ zu melden.
- Nutzer wünscht `XLOOKUP`: `INDEX`/`MATCH` verwenden oder bei ausdrücklichem Wunsch `not_computed` und fehlende Werte erklären.
- `.xlsm`-Upload bearbeiten: `keep_vba=True`, vorher Shapes/Slicer prüfen und Verlust melden.
- CSV in Excel-Tabelle umbauen, kein Branding vorgegeben: Arial/Times New Roman, keine erfundenen CI-Farben.
