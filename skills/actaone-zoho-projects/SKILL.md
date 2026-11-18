---
name: actaone-zoho-projects
description: Plane, recherchiere und pflege actaOne-Aufgaben in Zoho Projects über den bereitgestellten MCP-Server, einschließlich Status, Verantwortlichen, Terminen und Ticketbezügen. Verwende bei größeren Vorhaben einen vorhandenen oder neuen Postplan-Tracker, wenn verfügbar und geeignet; zeige konkrete Aufgabenänderungen vor dem Schreiben und lösche nichts.
---

# actaOne-Arbeit in Zoho Projects

MCP-Server `zoho-projects` verwenden; Tools und aktuelle Schemas entdecken. Portal **actago**, numerische ID als String **`20077052774`**, Standardprojekt **Künstliche Intelligenz**, ID **`131604000008451668`**. Ein ausdrücklich anderes Projekt im selben Portal zuerst auflösen. Nicht mit Portalnamen oder geratenen Projekt-IDs arbeiten.

## Lesen und planen

1. Umfang bestimmen: Aufgabenübersicht, eigenes Backlog, neues Vorhaben oder konkrete Änderung. Bei bekanntem Projekt `get_tasks_by_project` statt portalweiter Liste verwenden.
2. Vor Neuanlage nach bestehender Aufgabe anhand Titel, Beschreibung und vorhandener Ticket-/Paketzuordnung suchen. Pagination über `page_info.has_next_page` verfolgen; die erste Seite ist keine vollständige Bestandsprüfung.
3. „Meine Aufgaben“: ZPUID des Nutzers ermitteln oder im zulässigen Ergebnis nach Owner-E-Mail filtern. `${me}` und `current_login_user` nicht als Owner verwenden. Ein leerer Filtertreffer beweist bei ungeklärter Identität nicht, dass keine Aufgaben existieren.
4. Filter immer mit `pattern`, selbst bei einem Kriterium. Werte, Status-IDs und Zeitformate aus [MCP-Vertrag](references/mcp.md) beachten.
5. Arbeitspakete mit Ergebnis, Abnahmekriterien, vorhandenen Abhängigkeiten und nötigen Terminen beschreiben. Unbekannte Verantwortliche oder Termine nicht erfinden. Aus einem Plan nicht automatisch ein neues Zoho-Projekt erzeugen.

## Änderungen zeigen, ausführen, rücklesen

**Niemals etwas löschen. Vor jedem Erstellen oder Ändern von Aufgaben dem Nutzer die konkreten Änderungen zeigen.** Eine kompakte Vorschau reicht: Zielprojekt/-aufgabe, Aktion, Feld vorher → nachher, Grund. Bei mehreren Aufgaben einen zusammenhängenden Änderungssatz zeigen.

Ist dieser konkrete Umfang bereits beauftragt, nach der Vorschau fortfahren; diese Regel verlangt keine zusätzliche pauschale Bestätigung. Nicht beauftragte Entscheidungen erst klären. Unmittelbar vor Schreiben aktuellen Stand lesen und bei inzwischen geänderten Feldern die Vorschau aktualisieren, statt fremde Änderungen zu überschreiben.

- Nur geänderte Felder senden; keine ganze gelesene Aufgabe zurückschreiben.
- Status per ID, nicht per Anzeigename. Erledigt nur bei erfüllter vereinbarter Abnahme, nicht allein wegen Merge oder Trackerhäkchen.
- Verantwortliche mit der ausdrücklich additiven Updateform ergänzen; bestehende Mitverantwortliche und Arbeitsaufteilung erhalten. Details und Create-/Update-Unterschied: [MCP-Vertrag](references/mcp.md).
- Beschreibungen und Links gezielt ergänzen, vorhandenen Kontext erhalten. Keinen Tasklisten-/Projektwechsel über normale Task-Updates vortäuschen.
- Nach jeder Mutation Details rücklesen: ID, Projekt, betroffene Felder und unverändert zu erhaltende Verantwortliche prüfen. Bei Teilfehlern erfolgreiche und offene Änderungen getrennt melden; nach Timeout vor Wiederholung nach dem tatsächlichen Ergebnis suchen.

## Postplan und Ticketbezüge

Für größere Vorhaben mit mehreren Paketen, Abhängigkeiten oder Sitzungen den [Postplan-Ablauf](references/postplan.md) nutzen. Zoho bleibt führend für Aufgabenstatus, Verantwortliche und Termine; Postplan erklärt Zusammenhang, Entscheidungen und Fortschritt. Keine automatische bidirektionale Synchronisierung behaupten.

Ticketkontext nur über den Desk-Skill und dessen Abteilungsgrenze lesen. Ein Ticketbezug ist keine Erlaubnis zum Kundenkontakt. Kein automatisches Schließen von Tickets beim Abschluss einer Aufgabe.

## Abschluss

Aufgabenlinks aus Toolantworten, tatsächliche Änderungen, geprüften Endzustand, offene Blocker und gegebenenfalls Postplan-Link liefern. Fehlende MCP-Fähigkeit als konkrete Lücke nennen; keinen neuen API-Zugang oder Schreibweg improvisieren.

Herkunft und Grenzen: [sources.md](references/sources.md).
