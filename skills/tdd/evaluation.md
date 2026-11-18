# Prüffälle

Synthetische Textszenarien, nicht ausgeführt. Geprüft wurde nur die Struktur mit `scripts/validate.py`; kein Verhaltens- oder Live-Test.

- Neues Verhalten: ein Test rot, minimal grün, nächster Zyklus; Refactoring erst im Review.
- Schnittstellenform unklar: `codebase-design` als Referenz heranziehen.
- Test mockt interne Kollaborateure: nach `mocking.md` an die Systemgrenze verschieben.
- Kein Testsetup im Repo: Lücke benennen.
