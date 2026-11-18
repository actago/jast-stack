# Ledger einer Instanz auswerten

**Prüfstand:** Abfrage aus dem Exporter-Code (`tenantWindowMetrics.ts`) und dem `mongosh`-Muster des Monorepo-Runbooks `docs/operations/codeapi/runbook.md` abgeleitet. Sie wurde für diesen Skill **nicht ausgeführt**. Beim ersten Einsatz Ergebnis und Laufzeit prüfen. Nur auf laufenden Instanzen möglich.

## Ziel bestimmen

```bash
# auf acta-mgmt
SLUG=<slug>; CTX=customer-$SLUG
docker context inspect "$CTX" --format '{{.Endpoints.docker.Host}}'     # Ziel prüfen
M=$(docker --context "$CTX" ps -q --filter name=customer-${SLUG}_mongodb. | head -1)
docker --context "$CTX" exec "$M" mongosh LibreChat --quiet \
  --eval 'print(JSON.stringify(db.users.distinct("tenantId")))'         # genau ein Wert erwartet
```

Mehr als ein `tenantId` oder keiner: Befund melden. Nicht raten.

## Aggregat abfragen

Die Abfrage liefert ausschließlich Summen und Zählungen. Keine Nutzer-IDs, Konversationen oder Texte. Das Skript wird per Datei übergeben, denn `mongosh` über stdin gibt REPL-Ausgaben mit aus.

```bash
umask 077; Q=$(mktemp --suffix=.js)
cat > "$Q" <<'JS'
const T = process.env.T, since = new Date(process.env.SINCE), until = new Date(process.env.UNTIL);
const tz = process.env.TZ_NAME || 'Europe/Berlin';
if (!T || !Number.isFinite(+since) || !Number.isFinite(+until) || since >= until) {
  throw new Error('Tenant und gueltiges begrenztes Zeitfenster erforderlich');
}
new Intl.DateTimeFormat('en', { timeZone: tz }).format(since);
const match = { tenantId: T, createdAt: { $gte: since, $lt: until }, tokenType: { $in: ['prompt', 'completion'] } };
const sums = {
  inputTokens: { $sum: { $cond: [{ $eq: ['$tokenType', 'prompt'] }, { $abs: { $ifNull: ['$inputTokens', { $ifNull: ['$rawAmount', 0] }] } }, 0] } },
  outputTokens: { $sum: { $cond: [{ $eq: ['$tokenType', 'completion'] }, { $abs: { $ifNull: ['$rawAmount', 0] } }, 0] } },
  cacheWriteTokens: { $sum: { $cond: [{ $eq: ['$tokenType', 'prompt'] }, { $abs: { $ifNull: ['$writeTokens', 0] } }, 0] } },
  cacheReadTokens: { $sum: { $cond: [{ $eq: ['$tokenType', 'prompt'] }, { $abs: { $ifNull: ['$readTokens', 0] } }, 0] } },
  tokenCredits: { $sum: { $abs: { $ifNull: ['$tokenValue', 0] } } },
  amountEur: { $sum: { $ifNull: ['$cost.amountEur', 0] } },
  pricedTransactions: { $sum: { $cond: [{ $isNumber: '$cost.amountEur' }, 1, 0] } },
  unpricedTransactions: { $sum: { $cond: [{ $isNumber: '$cost.amountEur' }, 0, 1] } },
  users: { $addToSet: '$user' },
};
const strip = ({ users, ...rest }) => ({ ...rest, activeUsers: users.length });
const tx = db.transactions;
print(JSON.stringify({
  tenantId: T, since, until, tz, queriedAt: new Date(),
  registeredUsers: db.users.countDocuments({ tenantId: T }),
  total: tx.aggregate([{ $match: match }, { $group: { _id: null, ...sums } }]).toArray().map(strip)[0] || null,
  byDay: tx.aggregate([{ $match: match },
    { $group: { _id: { $dateToString: { format: '%Y-%m-%d', date: '$createdAt', timezone: tz } }, ...sums } },
    { $sort: { _id: 1 } }]).toArray().map(strip),
  byModel: tx.aggregate([{ $match: { ...match, model: { $exists: true, $nin: [null, ''] } } },
    { $group: { _id: '$model', ...sums } }, { $sort: { tokenCredits: -1 } }, { $limit: 10 }]).toArray().map(strip),
  firstUsage: (tx.find({ tenantId: T, tokenType: { $in: ['prompt', 'completion'] } }, { createdAt: 1, _id: 0 })
    .sort({ createdAt: 1 }).limit(1).toArray()[0] || {}).createdAt || null,
}));
JS
docker --context "$CTX" cp "$Q" "$M:/tmp/usage-q.js"
docker --context "$CTX" exec -e T=<tenantId> -e SINCE=2026-11-01T00:00:00+01:00 -e UNTIL=2026-11-17T00:00:00+01:00 \
  -e TZ_NAME=Europe/Berlin "$M" mongosh LibreChat --quiet --file /tmp/usage-q.js
docker --context "$CTX" exec "$M" rm -f /tmp/usage-q.js; rm -f "$Q"
```

Hinweise:

- `docker cp` und das Löschen der Datei im Container sind die einzigen Schreibvorgänge, beide in `/tmp` des Containers. Ist das unerwünscht, das Skript als `--eval` übergeben (Quotierung beachten).
- `process.env` setzt ein `mongosh` voraus, das die Node-Umgebung durchreicht; das ist im Runbook nicht belegt. Fehlt es, die Werte im Skript ersetzen.
- `activeUsers` je Tag oder Modell ist eine Zählung je Gruppe. Über Tage summiert ergibt das keine eindeutigen Nutzer; die eindeutige Zahl steht in `total`.
- `registeredUsers` ist Bestand zum Abfragezeitpunkt, nicht zum Fensterende.
- Bei großen Mandanten zuerst nur `total` abfragen. `createdAt` und `tenantId` sind laut Schema einzeln indiziert, nicht als Kombination.
- Vor Ausführung ein passendes `maxTimeMS` für jede Aggregation, Suche und Zählung setzen. Das Muster oben ist dafür anzupassen; Timeout oder fehlende Env-Weitergabe sind Fehler, keine Nullnutzung. Den festen Beispielpfad `/tmp/usage-q.js` durch einen eindeutigen eigenen Pfad ersetzen und nur die eigene Datei entfernen, auch bei Abbruch. `firstUsage` durchsucht die ganze Historie und gehört nur zu einem Auftrag nach dem Nutzungsbeginn; sonst weglassen.

## Mehrere Instanzen

Für mehrere Slugs dieselbe Abfrage je Context ausführen und die Ergebnisse lokal zusammenführen. Nicht erreichbare Contexte (gestoppte oder archivierte VMs) als Lücke aufführen. Flottenweite Ledger-Sweeps sind teuer und erfassen nur laufende VMs. Für Flottenfragen die CP-Historie bevorzugen.
