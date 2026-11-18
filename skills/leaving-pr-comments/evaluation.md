# Prüffälle

Synthetische Textszenarien, nicht ausgeführt. Geprüft wurde nur die Struktur mit `scripts/validate.py`; kein Verhaltens- oder Live-Test.

- Antwort auf einen Review-Bot: NOTE-Callout mit verifiziertem Modellnamen und Nutzer, Schlussfolgerung zuerst.
- Modellname nicht verfügbar: Harness-Namen nehmen.
- Nutzer verlangt wörtlichen Text ohne Attribution: kein Callout.
- Kommentar zitiert ein Log mit Secret: vorher entfernen.
- PR-Beschreibung oder Commit-Message: Format nicht anwenden.
