# Einen konkreten Chat untersuchen

Nur lesen, wenn der Nutzer eine bestimmte Unterhaltung (Chat-URL `/c/<conversationId>` oder Share-URL `/share/<shareId>`) mit konkretem Supportanlass untersuchen lässt. Kundenchats sind Kundendaten: Der Umfang ist genau diese eine Unterhaltung, nur die Felder, die die Frage beantworten.

## Umfang und Datenschutz

- Lesen, nicht schreiben. Keine Nachrichten ändern, keine Testnachrichten in fremde Unterhaltungen, keine Anmeldung als der betroffene Nutzer.
- Standard sind Metadaten: Zeitstempel, Endpoint, Modell, `error`/`unfinished`, Tool-Namen und Status, Token-Zahlen, Datei-IDs und -Typen. Nachrichtentext nur lesen, wenn die Frage ohne ihn nicht zu beantworten ist und der Nutzer das für diesen Fall verlangt; dann nicht zitieren.
- In Berichte, Tickets, PRs, Memories oder Wissensbasis: keine Chatinhalte, keine Dateiinhalte, keine personenbezogenen Angaben über das Nötige hinaus. IDs bei Bedarf gekürzt oder gehasht.
- Andere Unterhaltungen desselben Nutzers oder Mandanten nur, wenn der Auftrag sie ausdrücklich nennt. Eigene Staging-Testchats sind weniger sensibel; Chats von Kollegen auf Staging gelten wie Kundenchats.
- Ergibt sich ein Fix, ist er ein eigener Schritt (Release, Vault, Code-PR); Nachstellen geschieht mit eigenen Testkonten auf Staging oder lokal, nicht in der Kundenunterhaltung.

## Ablauf

1. **Zuordnen:** Host `<slug>.ki.actago.de` → Context `customer-<slug>` (Staging: `staging`). Kein passender Context → melden, nicht raten.
2. **Share auflösen:** Collection `sharedlinks` nach `shareId` → `conversationId` (Feldnamen gegen das aktuelle Fork-Schema `packages/data-schemas/src/schema/share.ts` prüfen).
3. **Metadaten lesen** in der Instanz-DB (Mongo-Container der Instanz) mit Projektion, z. B.
   `db.conversations.findOne({conversationId}, {endpoint:1, model:1, createdAt:1, updatedAt:1, tenantId:1})`
   `db.messages.find({conversationId}, {messageId:1, parentMessageId:1, createdAt:1, endpoint:1, model:1, error:1, unfinished:1, tokenCount:1, 'content.type':1, 'content.tool_call.name':1}).sort({createdAt:1})`.
   Feldnamen vorher gegen `packages/data-schemas/src/schema/{message,convo}.ts` des laufenden Tags prüfen. Nach `createdAt` sortieren; `updatedAt` ändert sich durch spätere Verarbeitung. Tool-Argumente können gekürzt gespeichert sein.
4. **Zeitfenster korrelieren:** api-Logs der Instanz um die Zeitstempel, dazu je nach Pfad Upstream: Gateway/Provider (503, 4xx), CodeAPI (`[CodeApiInfra]`), RAG/KB, Websuche. Logs können Tenant-/User-IDs, Nachrichten und Secrets enthalten. Vor jeder Tool-Ausgabe auf Fehlerklasse, Zeitstempel und nötige technische Metadaten reduzieren; keine Rohzeilen weiterreichen. Bei Dokumenten die Datei-Metadaten in `files`, nicht den Inhalt.
5. **Stand abgleichen:** Live-Tag der Instanz und relevante Konfiguration (siehe [config-drift.md](config-drift.md)); bei Code-Verdacht gegen den Fork-Commit dieses Tags, nicht gegen `main`.
6. **Nachstellen**, wenn nötig, auf Staging oder lokal mit eigenem Konto.

## Bericht

```
Instanz: <slug> (Tag <tag>), Unterhaltung <id gekürzt>, Zeitraum <von–bis>
Befund: <was technisch passierte: Fehlercode, betroffener Dienst, Schritt>
Beleg: <Logklasse + Zeitstempel, Metadatenfelder>
Ursache: <…> | Vermutung (nicht belegt): <…>
Nächster Schritt: <Fix-Weg, Zuständigkeit>
Nicht geprüft / bewusst nicht gelesen: <…>
```

Wertungen über Antwortqualität („zu weitgehend", „falsch") nur mit technischem Beleg; sonst als Einschätzung kennzeichnen.
