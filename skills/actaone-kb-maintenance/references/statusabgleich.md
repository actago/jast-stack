# Statusabgleich (Vault-Refresh)

Zusammengeführt aus `vault-refresh` Schritte 1–6 und `actaone-updates`. Dauer je nach Rückstau 5–30 Minuten. Harvest ist ein eigener Teil: [harvest.md](harvest.md).

## 1. Sync und Bestandsaufnahme

`00 Meta/sync-memories.ps1` spiegelt die eigenen Claude-Memories nach `20 Team/<Kürzel>/Memories/`, ruft `apply-tags-<Kürzel>.ps1` auf (falls vorhanden) und aktualisiert die Harvest-Ampel. Neue Memories ohne Tags in Schritt 5 einpflegen.

## 2. GitHub-Abgleich

Für `actago/actaOne`, `actago/LibreChat`, `actago/KB_RAG`:

```text
gh pr list -R <repo> --state all --limit 150 --json number,title,state,mergedAt
```

Unter Windows PowerShell 5.1: `(... | Out-String) | ConvertFrom-Json`. Ohne `gh` GitHub im Browser. Jede Notiz mit Status `aktuell`, `teilweise` oder `pruefen`, die PRs oder Branches behauptet, gegen den echten Stand prüfen; offene PRs in `10 actaOne/Offene Baustellen.md` bestätigen oder abhaken. Release-Aussagen gegen die Stable-Registry auf der Management-VM prüfen; Codeaussagen gegen die Quelle. Merge ≠ produktiver Rollout.

## 3. Nutzer-Häkchen verarbeiten

`- [x]` in `Offene Baustellen`, die noch nicht in der ✅-Sektion stehen, bedeuten „Nutzer sagt: erledigt“. Je Häkchen:

1. Wenn möglich verifizieren; sonst als „lt. Nutzer erledigt, <Datum>“ kennzeichnen.
2. Zeile oben ins `10 actaOne/Gelöst-Log.md` mit Datum und Lösungsweg.
3. Eintrag in die ✅-Sektion verschieben (durchgestrichen).
4. Status im Tag-Mapping auf `status/erledigt`.
5. Quell-Memory aktualisieren, dann erneut syncen.

Häkchen in fremden Bereichen nur nach Absprache verbuchen.

## 4. Fachnotizen nachziehen

Gesicherte Erkenntnisse in bestehende MOCs, Referenzen, `Offene Baustellen` und `Gelöst-Log`. Bei Systemseiten die Metadaten laut `Wissensseiten – Aufbau & Pflege` (`belegarten`, `quellenstand`, `pruefstatus` mit Umfang). Größere Statuswechsel: neue Notiz `10 actaOne/Wissens-Audit YYYY-MM-DD.md`, alten Audit auf `status/archiv`, Home-Links anpassen.

## 5. Neue Memories einpflegen

Je Memory ohne Tags: Eintrag im eigenen `apply-tags-<Kürzel>.ps1` (`Slug = @('memory, <themen>, status/<x>', 'Lesbarer Titel')`), in passende MOCs verlinken, ggf. Baustellen/Gelöst-Log. Sync erneut. Ohne eigenes Mapping-Skript bleiben Memories ungetaggt.

## 6. Sprint-Notiz

Nur im eigenen Bereich: Geliefert-Sektion der laufenden Sprint-Notiz aus seit dem letzten Refresh gemergten PRs nachführen. Sprints laufen vier Wochen ab Montag; am Ende Review ausfüllen, Unerledigtes zurück in `Offene Baustellen`, Status in `Sprint-Übersicht.md`, neue Sprint-Notiz aus Vorlage.

## Bericht

Was veraltet war, was als erledigt verbucht wurde (mit Belegart), was offen bestätigt ist und was ungeprüft blieb.
