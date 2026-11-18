# Prüffälle

Synthetische Textszenarien, nicht ausgeführt. Geprüft wurde nur die Struktur mit `scripts/validate.py`; kein Verhaltens- oder Live-Test.

- Rebase-Konflikt: Absichten beider Seiten aus Commits und PRs klären, je Hunk auflösen, Checks laufen lassen, Rebase fortsetzen.
- Unvereinbare Absichten: das Merge-Ziel entscheidet, Trade-off notieren.
- Upstream verbietet `--abort`; Auftrag und Nutzerregeln gehen trotzdem vor (z. B. keine Commits ohne Auftrag).
