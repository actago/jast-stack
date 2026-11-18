# Herkunft und Prüfstand

Eigener JAST-Skill, 17.11.2026. Grundlage sind die ausdrücklichen Nutzerregeln in AGENTS.md: Portal-/Projekt-ID, Filter-pattern, Owner-ZPUID, niemals löschen und Aufgabenänderungen vorab zeigen. Ergänzt aus den aktuellen MCP-Operationsbeschreibungen von `get_tasks_by_project`, `create_a_task` und `update_a_task`: Pagination, Filtercodierung, Status-IDs und unterschiedliche Ownerformen.

Postplan-Anbindung auf ausdrücklichen Nutzerauftrag, passend zum vorhandenen JAST-Postplan-Skill. Herstellerunabhängige Auftrags-/Readback-Regeln sind eigene Aggregation. Kein behaupteter automatischer Sync.

Nur Schemas gelesen, keine Zoho-Datensätze oder Portalbenutzer abgefragt, keine Mutationen und kein Postplan-Upload. Die Team-IDs sind keine universellen Defaults. Keine praktische oder unabhängige Agentenabnahme erfolgt.
