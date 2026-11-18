# Limits und Preise: begrenzter Diagnoseworkflow

Für Limit- und Preisfragen gibt es **kein geprüftes, ausführbares Rezept**. Die Quellen belegen, wo die Daten liegen. Die genaue Durchsetzungslogik und die live aktiven Werte wurden für diesen Skill nicht geprüft. Das Ergebnis ist deshalb eine eingegrenzte Diagnose mit offenen Punkten, kein Urteil.

## Was belegt ist

- **Pläne und Defaults im LibreChat-Fork:**
  - `packages/data-schemas/src/methods/usagePlan.ts`: `CREDITS_PER_USD = 1_000_000`, Standard- und Premium-Monatsbudgets, Tagesbudget aus Monatsbudget durch Arbeitstage, sofern nicht gesetzt.
  - `packages/data-schemas/src/schema/usagePlan.ts`: Schema der Plan-Konfiguration.
  - `packages/api/src/admin/usagePlans.ts`: Admin-Pfad mit Audit-Aktion `tenant_usage_reset_requested`.

  Die konkreten Zahlen in einer Memory vom 21.08.2026 (Standard 8 M bzw. Premium 40 M Credits pro Monat, Tag = Monat ÷ 20, Ausnahmen für Trials, Nicht-Produktion und interne E-Mails) sind historische Werte. Vor Verwendung im Code und in der Instanz-Konfiguration nachlesen.
- **Fallback:** Nach Erreichen des Tages- oder Monatslimits nutzen Standardinstanzen `azureOpenAI:gpt-5-nano`. Diese Buchungen bleiben im Ledger und zählen nicht ins Kontingent (`docs/operations/usage-fallback.md`). Warnungen erscheinen bei 75 und 90 %.
- **`api/server/middleware/limiters/promptUsageLimiter.js`** ist ein Ratenlimit pro Minute, kein Budgetlimit. Nicht mit dem Kontingent verwechseln.
- **Preise:** `transactions.rate`, `rateDetail` und `cost.rates` halten die bei der Buchung verwendeten Raten fest. Die Preiskonfiguration der Instanz ergibt sich aus Template, Vault und Gateway-Katalog. Fehlende EU-Aufschläge wurden in einer Session vom 03.10.2026 so gefunden.

## Vorgehen

1. **Beschwerde einordnen:** Wer, seit wann, welche Meldung (Warnung, Fallback-Hinweis, Fehler)? Einzelne Nutzer nicht namentlich in den Bericht übernehmen.
2. **Verbrauch messen:** mit dem Ledger-Aggregat ([instanz-ledger.md](instanz-ledger.md)), zusätzlich gruppiert nach Tag. Je Nutzer nur als anonymisierte Verteilung, z. B. Anzahl der Nutzertage über X Credits, nie mit IDs.
3. **Geltendes Limit bestimmen:** Plan des Tenants, Instanz-Overrides und Ausnahmen aus den oben genannten Codepfaden und der Instanz-Konfiguration lesen. Was nicht eindeutig lesbar ist, als offen markieren.
4. **Gegenüberstellen:** Verbrauch je Nutzertag gegen das Tagesbudget, Monat gegen das Monatsbudget. Schubweise Nutzung (wenige sehr hohe Tage) von gleichmäßig hoher Nutzung unterscheiden.
5. **Preisprüfung, falls gefragt:** Rate je Modell aus aktuellen Buchungen gegen die erwartete Preisquelle vergleichen. Unterschiede melden; Preise nicht ändern.

## Bericht

- Belegt: Verbrauch, Verteilung, gebuchte Raten
- Abgeleitet: geltendes Limit mit Quelle
- Offen: Durchsetzungslogik, Ausnahmen, Live-Werte
- Antwort auf „unsere Schuld oder teuer?“ nur so weit, wie die Belege tragen

Konfigurationsänderungen (Plan, Limit, Preis) sind eigene Aufträge über den Vault- bzw. Release-Weg und nicht Teil dieser Auswertung.
