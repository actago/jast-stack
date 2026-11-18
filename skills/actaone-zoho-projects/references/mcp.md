# MCP-Vertrag und bekannte Fallen

Am 17.11.2026 aus den aktuellen Toolschemas gelesen. Keine Live-Aufgaben abgefragt. Die detaillierte Operationsbeschreibung geht verkürzten, teils widersprüchlichen Feldkommentaren vor.

## Lesen und filtern

`ZohoProjects_get_tasks_by_project` mit `path_variables.portal_id: "20077052774"` und `project_id: "131604000008451668"`. Ohne Filter/View enthält die Liste offene und geschlossene Aufgaben. `per_page` explizit setzen und `page_info.has_next_page` beachten.

`query_params.filter` ist ein JSON-String, beispielsweise für einen bereits aufgelösten Owner:

```json
{"criteria":[{"field_name":"owner","criteria_condition":"is","value":["<ZPUID>"]}],"pattern":"1"}
```

- Immer `pattern`, bei mehreren Kriterien 1-basierte Indizes mit `AND`/`OR` in Großbuchstaben.
- `owner` benötigt ZPUID, nicht ZUID; keine `${me}`-Abkürzung. IDs aus verfügbaren Benutzer-Metadaten eindeutig zuordnen.
- Statusfilter verwenden Option-IDs; für alle offenen ist laut Schema `value:["${ALL_OPEN}"]` mit `criteria_condition:"is"` möglich.
- Datumsfilter: `YYYY-MM-DD`, keine ISO-Uhrzeit. Schreibfelder haben einen eigenen Vertrag: Date-only-Portal oder ISO-Zeit gemäß Portalmodus.
- Aufgabenliste über `tasklist_id` filtern, nicht `tasklist`; `milestone`/`milestone_id` sind laut gelesener Filterbeschreibung nicht unterstützt.
- Unbekannte Custom Fields/Optionen nur über verfügbare Metadaten auflösen. Fehlendes Metadatentool melden, keinen Namen als ID einsetzen.

## Erstellen und ändern

`create_a_task`: Pflichtfeld `body.name`; keine Taskliste vorgegeben bedeutet Standardliste des Projekts. `tasklist:{"id":"..."}` nur bei bekanntem Ziel. Phase wird von der Liste abgeleitet. Status `status:{"id":"..."}`, sonst Layoutdefault. Custom Fields sind API-Feldnamen auf oberster Ebene, kein `custom_fields`-Wrapper.

Owner beim **Erstellen**:

```json
{"owners_and_work":{"owners":[{"zpuid":"<ZPUID>"}]}}
```

Owner beim **Ergänzen einer bestehenden Aufgabe**:

```json
{"owners_and_work":{"owners":[{"add":[{"zpuid":"<ZPUID>"}]}]}}
```

Kein `remove:[]`: laut Toolschema entfernt das andere Owner. Auch die Create-Form ersetzt beim Update die gesamte Ownerliste und kann Arbeitsaufteilung zurücksetzen. Gezielt andere Owner entfernen/ersetzen nur bei entsprechendem Auftrag und mit eigener Vorschau, nicht als Nebeneffekt eines „hinzufügen“.

`update_a_task` kann Taskliste oder Projekt nicht ändern. Falls ein Move beauftragt ist, passende verfügbare Operation separat suchen und deren Auswirkungen prüfen. Closed-Status setzt `is_completed`/100 % selbst; diese Felder nicht zusätzlich widersprüchlich setzen. Nur notwendige Felder schreiben.
