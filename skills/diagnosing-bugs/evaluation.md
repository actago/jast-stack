# Prüffälle

Synthetische Textszenarien, nicht ausgeführt. Geprüft wurde nur die Struktur mit `scripts/validate.py`; kein Verhaltens- oder Live-Test.

- Reproduzierbarer Fehler: zuerst einen engen, rot werdenden Befehl bauen, erst dann Hypothesen.
- Fehler nur über die UI reproduzierbar: HITL-Vorlage kopieren und anpassen, der Nutzer folgt den Schritten.
- Log enthält ein Token: als `<REDACTED>` zeigen.
- Kein rot werdendes Signal möglich: offen benennen statt Code-Lesen als Diagnose auszugeben.
