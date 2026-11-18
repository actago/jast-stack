# Prüffälle

Synthetische Textszenarien, nicht ausgeführt. Geprüft wurde nur die Struktur mit `scripts/validate.py`; kein Verhaltens- oder Live-Test.

- Alter PR mit Konflikten: Absicht festhalten, Basisänderungen seit der Merge-Base prüfen, rebasen, `--force-with-lease` gegen den beobachteten Head.
- Basis enthält bereits eine konkurrierende Implementierung: berichten statt doppelt umzusetzen.
- Arbeitsbaum ist schmutzig: separaten Worktree verwenden.
- Basis-Branch ändern oder PR schließen: nicht ohne Auftrag.
- Kein Kommentarwunsch: keinen PR-Kommentar posten.
