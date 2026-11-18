# Konfigurationsdrift lesend diagnostizieren

Lesen bei „Feature X ist auf Instanz Y weg", „warum verhält sich Y anders als Staging", „was von Staging muss ins Template/den Vault", „fehlen der Flotte Defaults". Ergebnis ist eine Einordnung mit Beleg; jede Änderung ist ein eigener, beauftragter Schritt. Vorbild für Methode und Klassen: `docs/rollouts/staging-env-audit-2026-11-04.md` im actaOne-Repo.

## 1. Frage festlegen

Referenz (z. B. Staging, eine Nachbarinstanz, das Kunden-Template) und Ziel (eine Instanz oder eine benannte Liste) benennen, dazu den betroffenen Bereich (Modelle, ein Tool, ein Schalter). „Ganze Flotte" nur, wenn ausdrücklich gefragt; dann Ausnahmen und nicht erreichbare Instanzen getrennt ausweisen.

## 2. Schichten lesen

Die effektive Konfiguration einer Instanz entsteht aus mehreren Schichten. Jede Schicht getrennt lesen und den Stand mit Zeitpunkt notieren:

| Schicht | Wo | Lesen |
|---|---|---|
| Template | `deploy/templates/librechat.customer*.yaml` im Repo **und** im mgmt-Checkout (deployt wird aus mgmt); Slug-Templates ersetzen die Standardvorlage komplett, manche sind unversioniert | Datei/Commit vergleichen |
| Vault-Defaults | `customer-defaults` je Umgebung (staging/prod getrennt) | über `scripts/keyvault-secrets.sh fetch …` in `mktemp`-Verzeichnis (0600), danach `shred` |
| Kunden-Bundle | `customer-env <slug>` im Vault der Umgebung | wie oben |
| Runtime | Service-Spec und laufender Container | ausschließlich explizite nicht geheime Felder, Env-Key-Namen und Config-Namen projizieren; niemals unbeschränktes `service inspect` ausgeben |
| Gerenderte YAML | Swarm-Config `aoi-lc-<slug, max. 16 Zeichen>-<sha8(slug)>-<sha16(inhalt)>` am `_api`-Service | gleicher Inhalts-Hash = gleiche YAML |
| Mandantendaten | Einstellungen in der Instanz-DB (z. B. Rollen, Tenant-Schalter) | nur die betroffenen Dokumente/Felder |

Secrets: nur Key-Namen, Vorhandensein und ggf. Hash-Vergleich berichten, nie Werte ausgeben oder in Logs/Tool-Ausgaben bringen. Die Credential-Datei aus `keyvault-secrets.sh fetch` ist kein `KEY=VALUE`-Format; nicht zeilenweise „Namen" daraus schneiden.

Beispiel: Diese Projektion gibt nur Env-Schlüsselnamen aus, keine Werte (Bash am bestätigten Ausführungsort):

```bash
docker --context customer-<slug> service inspect customer-<slug>_api \
  --format '{{range .Spec.TaskTemplate.ContainerSpec.Env}}{{index (split . "=") 0}}{{println}}{{end}}'
```

Für gezielte nicht geheime Werte die Projektion direkt auf die erlaubten Schlüssel beschränken. Eine Base-URL vor Ausgabe zusätzlich auf eingebettete Credentials oder geheime Query-Parameter prüfen. Vollständige Rohdaten nur intern in einem geeigneten ausgabefreien Parser verarbeiten; keine Pipeline mit unredigiertem Zwischen-Logging.

## 3. Unterschiede einordnen

Jede Abweichung genau einer Klasse zuordnen:

- **Gewollt:** Produktentscheidung je Umgebung oder Kunde (z. B. Invite-only, Proxy-Vertrauen, kundenspezifische Endpunkte, `*_RELEASE_MIGRATION=hold`, eigene Slug-Vorlage). Bleibt.
- **Staging-/Dev-only:** Debug-Schalter, Staging-Modell-Overlays, Test-Identitäten, Diagnoseoberflächen. Nie in Prod-Defaults kopieren.
- **Abgeleitet:** zur Laufzeit aus Compose oder Gateway-Logik erzeugt (z. B. `MONGO_URI`, `MEILI_HOST`, Gateway-abgeleitete Embedding-/Reranker-Werte). Nicht zurück in Vault oder Template schreiben.
- **Release-bedingt offen:** Wert wirkt erst ab einem Release, das die Instanz noch nicht fährt.
- **Drift:** Soll laut Template/Defaults vorhanden, fehlt oder ist veraltet in Bundle bzw. Runtime.

Bei neuen Aktivierungen (Staging hat etwas an, Prod nicht) ist die Übernahme eine Produktentscheidung, keine Drift-Behebung.

## 4. Bekannte Mechanismen hinter Drift

- `promote.sh` ergänzt bei jedem Promote **fehlende** Keys aus `customer-defaults`, überschreibt keine gesetzten Kundenwerte und migriert keine veralteten Werte (außer ausdrücklich implementierten Migrationen). Alte Bundles behalten daher alte Werte.
- Ein Flotten-Rollout überspringt Instanzen, die den Ziel-Tag schon fahren; Template- und Default-Änderungen erreichen sie erst beim nächsten Einzel-Redeploy.
- Templates sind nicht release-gegated und werden aus dem mgmt-Checkout gerendert. Der Staging-Cron zieht diesen Checkout auf `main` nach, aber nur, wenn er sauber auf `main` steht (sonst Event `infra_sync failed` in `staging-autodeploy-events.jsonl`); ein abweichender Checkout ist eine eigene Driftquelle. Instanzen, die seit einem Template-Merge nicht neu deployt wurden, tragen noch die alte YAML.
- Ein Image-Wechsel allein aktualisiert eine bereits gerenderte YAML nicht.
- Manuelle `service update`-Änderungen verschwinden beim nächsten Redeploy (häufig bei Branch-Instanzen).
- Provisioner (Deploy-Control-API, Webhook-Receiver) haben eigene Default-Allowlists; ein Key, der dort fehlt, kommt bei Neukunden nicht an.

## 5. Werkzeuge im Repo (lesend)

- `scripts/tests/test_librechat_template_drift.sh`: Templates untereinander (Standard, Staging, Benchmark, Slug-Templates).
- `scripts/caddy-drift-check.sh`: Perimeter-Routen gegen Soll.
- `scripts/sync-benchmark-release.sh status|check`: Benchmark gegen Staging (Release, Config-Hash, Gateway-Werte).
- `scripts/validate-librechat-config.sh`: Template gegen ein Ziel-Image.

Ein generisches Paritätsskript über die Flotte gab es zum Prüfzeitpunkt nicht; Vergleiche je Instanz ad hoc mit den Befehlen oben.

## 6. Ergebnis und Übergabe

```
Frage: <Referenz> vs <Ziel>, Bereich <…>, gelesen am <Zeit>
Schicht-Befunde: Template <…> · Defaults <…> · Bundle <…> · Runtime <…> · YAML-Hash <…>
Einordnung: gewollt <…> · dev-only <…> · abgeleitet <…> · release-bedingt <…> · Drift <…>
Ursache: <Mechanismus mit Beleg>
Behebung (nicht ausgeführt, falls nicht beauftragt): Vault-Key <name> in <scope> / Template-PR / Redeploy <slug>
Nicht geprüft: <…>
```

Behebung: dauerhaft im Vault (`keyvault-secrets.sh`, vault-first) oder per Template-PR, danach Redeploy der betroffenen Instanz und erneute Lesung der Runtime als Nachweis.
