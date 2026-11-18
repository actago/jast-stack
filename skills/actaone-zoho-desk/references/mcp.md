# MCP-Vertrag

Am 17.11.2026 aus den verfügbaren Tooldefinitionen gelesen, keine Live-Tickets abgefragt. Vor Nutzung tatsächliches Schema erneut beachten.

- `ZohoDesk_searchTickets`: `query_params.departmentId`, bei ID-Zuordnung zusätzlich `id: ["<ticket-id>"]`; `from`/`limit` für Pagination. Betreffsuche über `subject`.
- `ZohoDesk_getTickets`: `query_params.departmentId` ausdrücklich setzen; keine Liste über alle Departments. `fields` kann benötigte Felder begrenzen.
- `ZohoDesk_getTicket`: `path_variables.ticketId`; kein departmentId-Parameter. Nur nach erlaubter Zuordnung verwenden.
- Threads/Kommentare erst für zugeordnete Tickets mit den bereitgestellten `getThreads`, `getThread`, `getTicketComments` oder `getTicketConversations` lesen. Pagination und Ausgabeumfang begrenzen.

Interner Antwortentwurf, nur nach beauftragtem Speichern:

```json
{
  "path_variables": {"ticketId": "<zugeordnete-ticket-id>"},
  "body": {
    "content": "Antwortentwurf:\n<geprüfter Entwurf>",
    "contentType": "plainText",
    "isPublic": false
  }
}
```

Eine erforderliche Organisations-ID aus der bestehenden MCP-Zuordnung bzw. freigegebenen Organisationsmetadaten ermitteln, nicht mit der Department-ID verwechseln. Fehlende Toolfähigkeit melden statt eine unbegrenzte generische Suche einzusetzen.
