---
name: actaone-usage-analysis
description: Nutzung einer actaOne-Instanz oder eines Mandanten lesend als Aggregat auswerten (aktive/registrierte Nutzer, Tokens, Credits, Tagesverteilung, Top-Modelle). Anwenden bei „hat Instanz X actaOne genutzt“, „wie intensiv testet Kunde Y“, „seit wann nutzt Z“, „Limits zu schnell weg“ und „welche Kosten/Preise sind aktiv“. Nicht für Rechnungen und nicht für Inhalte einzelner Chats.
---

# actaOne-Nutzungsauswertung

Ziel ist eine kleine, belegte Kennzahlenantwort mit **Quelle, Zeitfenster, Zeitzone und Stand**. Die Auswertung ist ausschließlich lesend und datensparsam:

- nur Aggregate
- keine Chatinhalte, Prompts, Dateinamen, E-Mail-Adressen oder Nutzer-IDs in Ausgabe, Log oder Wissensbasis
- Rohabfragen, die Einzelzeilen liefern, nur in `0600`-Dateien und ausschließlich als Zählung berichten

## 1. Frage schärfen

Vor der ersten Abfrage festlegen:

- **Zielumfang:** Slug bzw. Tenant. Mehrere Instanzen können zu einem Tenant gehören. Staging, benchmark, Branch- und Testinstanzen bewusst ein- oder ausschließen.
- **Zeitfenster:** Anfang und Ende als Datum mit Zeitzone. Ohne Angabe die letzten 30 Tage nehmen und das nennen.
- **Kennzahlen:** nur die gefragten. Eine einfache Nutzungsfrage bekommt keine Vertrags-, Health- oder Lizenzzahlen dazu.

## 2. Quelle wählen

| Frage | Bevorzugte Quelle | Weg |
|---|---|---|
| Flotte oder mehrere Mandanten, Ranking, Trend | CP-`usagesnapshots` mit `windowKind: delta` (über Management-Analytics oder CP-Analytics) | [references/quellen-und-kennzahlen.md](references/quellen-und-kennzahlen.md) |
| Ein Mandant, genaue Tageswerte, Modelle, aktive Nutzer | Ledger `transactions` der Instanz-DB | [references/instanz-ledger.md](references/instanz-ledger.md) |
| Testbeginn, Vertrags- oder Trialstatus | CP-`tenants` (`trialStartedAt`, `contractStatus`, …) | [references/quellen-und-kennzahlen.md](references/quellen-und-kennzahlen.md#vertragsdaten) |
| „Limits zu schnell weg“, „welche Preise gelten“ | Ledger plus Plan- und Preisquellen | **begrenzt:** [references/limits-und-preise.md](references/limits-und-preise.md) |

Ist eine Instanz gestoppt oder archiviert, ist ihr Ledger nicht erreichbar. Dann bleibt nur die CP-Historie. Die Lücke benennen und nichts hochrechnen.

## 3. Feste Lesart

- **Registriert ist nicht aktiv.** Aktiv heißt: Nutzer mit Prompt- oder Completion-Buchung im Fenster. Das ist kein Login-Zähler. Bestandszahlen aus mehreren Snapshots werden nicht addiert.
- **Snapshot ist nicht Verbrauch.** Letzte bzw. kumulative Snapshot-Werte (`usage-totals`, `platforminstances.usageSnapshot`) sind kein Verbrauch im Fenster. `/analytics/usage-timeseries` verbindet historische Events mit dem *aktuellen* Snapshot und taugt nicht für Tokenverläufe. Für Zeiträume nur Delta-Fenster oder den Ledger summieren.
- **Kosten sind keine Abrechnung.**
  - `tokenCredits` ist eine interne Buchungseinheit; im Code gilt `CREDITS_PER_USD = 1_000_000`.
  - `cost.amountEur` ist eine Schätzung zu aufgezeichneten Raten (`recorded-rates-v1`) mit eigenem Zähler für unbepreiste Buchungen.
  - LiteLLM-Spend misst denselben Verkehr ein zweites Mal und wird nicht addiert.
  - Rechnungs-, Vertrags- oder Umsatzbeträge kommen aus keiner dieser Quellen. Danach gefragt: Lücke nennen.
- **Lücken sind keine Nullen.** Fehlende Exporter-Fenster, nicht erreichbare VMs, ungebuchte Toolkosten und Zeiträume vor Einführung der Delta-Fenster bleiben als „unbekannt“ stehen.
- **Zeit:** Ledger-Zeitstempel sind UTC. Tagesgrenzen in der Zeitzone des Fragenden (meist Europe/Berlin) bilden und das angeben.

## 4. Zugang

Alle Wege laufen über den Management-Zugang (`ssh acta-mgmt`) laut Monorepo-Doku.

- **Lesend sind:** Instanz-Mongo per `docker --context customer-<slug> exec … mongosh` und CP-Lesewege. Trotzdem nicht in einer prod- oder Kundenumgebung ohne passenden Auftrag ausführen.
- **Tokens nicht beschaffen.** Analytics-Token, Mongo-URIs und Service-Tokens weder aus Env, systemd-Drop-ins noch Vault lesen, nur um eine Abfrage zu ermöglichen. Fehlt ein freigegebener Weg, den nächsten Schritt mit dem Nutzer klären, z. B. Ops-Dashboard, Ausführung durch den Nutzer oder freigegebener Lesezugang.
- **Keine Schreiboperationen**, auch keine „Reparatur“ von Snapshots, Plänen oder Buchungen.

## 5. Bericht

Kurz und tabellarisch:

- Zielumfang
- Fenster mit Zeitzone
- Quelle mit Abfragezeitpunkt
- je Kennzahl Wert und Definition in einem Halbsatz
- Lücken und ausgeschlossene Instanzen
- Hinweis „keine Abrechnungszahl“, sobald Credits oder Euro vorkommen

Eine Interpretation („testet intensiv“, „Limit zu knapp“) nur mit Vergleichsmaßstab, z. B. andere Tage, Plan-Limit oder Mittelwert ähnlicher Mandanten.

Herkunft, Prüfstand und Grenzen: [references/sources.md](references/sources.md).
