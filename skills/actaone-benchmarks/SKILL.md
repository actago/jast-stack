---
name: actaone-benchmarks
description: actaOne-Benchmark-Instanz (customer-benchmark, benchmark.ki.actago.de) für Modell- und Providervergleiche, Messreihen und Testsuite-Ziel nutzen. Anwenden bei „Modell/Endpunkt auf benchmark testen“, „Modell erscheint nicht in der Auswahl“, „Benchmark-Prompts laufen lassen/auswerten“, „Benchmark auf Staging-Stand bringen“ und bei Fragen, ob benchmark und Staging dasselbe messen.
---

# actaOne-Benchmarks

`benchmark` ist die Messinstanz ohne Kundendaten: Docker-Context `customer-benchmark`, Slug `benchmark`, VM 367, `192.168.10.167`. Sie ist die einzige Instanz, auf der kurzfristige Live-Änderungen vorgesehen sind. Der Zugang läuft wie bei allen Instanzen über den Management-Zugang (`ssh acta-mgmt`). Von dort erreicht man aber die ganze Flotte.

**Seit 12.11.2026 ist benchmark an Staging gekoppelt.** Die Testsuite läuft standardmäßig gegen benchmark (`TESTSUITE_TARGET=benchmark`). Das Template `librechat.customer.benchmark.yaml` ist das Staging-Template plus Kopfkommentar, ein Drift-Test sichert das ab. `scripts/sync-benchmark-release.sh` zieht Release, gemountete `librechat.yaml` und nicht geheime Overlay-Werte von Staging nach. Daraus folgt:

- Jede Änderung auf benchmark verändert das Testsuite-Ziel.
- Dauerhafte benchmark-eigene Abweichungen brechen die Parität. Experimente sind deshalb **flüchtig** und werden vor dem nächsten Testsuite-Lauf zurückgenommen.

## 1. Ziel festhalten

Vor jedem Befehl prüfen:

- Der Context heißt `customer-benchmark`.
- Den Endpunkt mit der aktuellen Benchmark-Zuordnung im Inventar und der VM-Identität abgleichen (`docker context inspect customer-benchmark`); `ssh://actaone@192.168.10.167` ist der dokumentierte Ausgangsstand, kein zeitloser Identitätsnachweis.

Andere Contexte werden höchstens gelesen. Das gilt auch für Staging als Vergleichsquelle und für geteilte Infrastruktur wie Websearch/Reranker, Code-Interpreter, Presidio und LiteLLM. Eine Freigabe für benchmark erstreckt sich nicht auf sie. Fehlt ein Recht auf einer dieser Ebenen, die Lücke melden und nichts ersatzweise ändern.

## 2. Auftrag einordnen

| Auftrag | Weg | Referenz |
|---|---|---|
| Benchmark-Prompts laufen lassen, Ergebnisse aus Mongo auswerten, Modelle vergleichen | lesend plus Messlauf | [references/messen.md](references/messen.md) |
| Endpunkt, Modell oder Parameter zum Testen einbauen; „Modell erscheint nicht“ | flüchtige Swarm-Config | [references/config-aendern.md](references/config-aendern.md) |
| „benchmark auf Staging-Stand“, „misst benchmark dasselbe wie Staging?“, Experiment zurücknehmen | Sync-Skript | [references/staging-paritaet.md](references/staging-paritaet.md) |
| Änderung soll dauerhaft gelten | über Staging-Template bzw. Vault, nicht über benchmark | [references/config-aendern.md](references/config-aendern.md#dauerhaft) |

Kombinierte Aufträge (einbauen, messen, zurücksetzen) nacheinander abarbeiten. Jeden Teil mit seinem eigenen Nachweis abschließen.

## 3. Feste Regeln

- **Testsuite zuerst prüfen.** Vor einer flüchtigen Änderung `sync-benchmark-release.sh status` lesen und mit dem Nutzer klären, ob in diesem Zeitraum ein Testsuite-Lauf benchmark nutzt. Nach dem Experiment den Paritätsstand wiederherstellen oder ausdrücklich als offen melden.
- **Inhalts-Hash ist Provenienz.** Jede Messreihe nennt Image-Tag, Config-Name und den SHA-256 der gemounteten `librechat.yaml`. Ohne diese Angaben sind zwei Läufe nicht vergleichbar.
- **Wirkung messen, nicht annehmen.** Konfiguration rücklesen, nach Schema-Validierung aus Sicht der App prüfen und mit einem zweiten Modell gegenkontrollieren, bevor eine Umgebungsgrenze behauptet wird.
- **Vergleichbarkeit wahren.** Providerspezifische Prompt-Hilfen, andere Temperaturen oder bewegliche `-latest`-Aliase im Protokoll kennzeichnen oder vermeiden.
- **Secrets** gehören in das Vault-Bundle `customer-env benchmark` bzw. geschützte Übergabedateien. Swarm-Configs sind unverschlüsselt; auch flüchtige Tests verwenden Secret-/Env-Referenzen statt literaler Schlüssel in der YAML.
- **Kundeninstanzen** sind tabu für diese Wege. Live-Configs überleben dort keinen Redeploy; das wäre ein stiller Rückschritt.

## 4. Bericht

Der Bericht enthält:

- Ziel-Context mit Endpunkt-Nachweis
- Ausgangs- und Endstand: Release-Tag, Config-Name, `configSha16`
- Was geändert wurde und mit welchem Readback
- Messergebnis mit Provenienz und den Grenzen der Messung
- Paritätsstand zu Staging nach Abschluss (synchron, bewusst abweichend, offen)

Herkunft, lokale Anpassungen und ungeprüfte Annahmen: [references/sources.md](references/sources.md).
