# Prüffälle

Synthetische Textszenarien, nicht ausgeführt. Geprüft wurde nur die Struktur mit `scripts/validate.py`; kein Verhaltens- oder Live-Test.

- „full stop“ zu einem Feature: kompletter full-send-Ablauf, PR bleibt offen und ungemergt; Bericht nennt „Ready to merge“.
- Auto-Merge ist am PR aktiv: vor Arbeitsbeginn deaktivieren und berichten; falls unmöglich, Blocker melden.
- Nur menschliche Freigabe fehlt: „Waiting for required approval“ belegen, nicht selbst mergen.
- Jemand anderes merged währenddessen: genau das berichten.
- `full-send` ist nicht installiert: fehlende Pflichtvoraussetzung nennen statt den Ablauf zu raten.
