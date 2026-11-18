# Lokale Besonderheiten (Windows-Entwicklungsrechner)

Lesen, wenn auf Windows gestartet wird, ein Worktree geteilte `node_modules` nutzt oder der Start trotz Rezept scheitert. Alle Punkte stammen aus Memories eines Entwicklerrechners (Stand jeweils angegeben) und sind **nicht** für diese Fassung erneut geprüft. Unter macOS/Linux ungetestet. Erst prüfen, ob der Punkt auf dem aktuellen Rechner zutrifft.

## Belegte Ports und fremde Stacks (Stand 11/2026)

Auf dem Rechner lief ein Docker-Desktop-LibreChat-Stack, der 27017 (Mongo) und 3080 (LibreChat-Container mit Restart-Policy `always`) belegte. Er gehört nicht zur Aufgabe. Ausweichen auf eigenes Port-Paar (z. B. Mongo 27018, Backend 3082, Vite 3092) statt ihn zu stoppen; Stoppen nur nach Rückfrage. Andere Agenten nutzten parallel eigene Paare (z. B. 3083, 3087/3097, 3088/3098). Port deshalb immer dem Prozess und Checkout zuordnen.

## Mongo ohne Docker

`mongodb-memory-server` liegt in den `node_modules` des Forks; ein kleines Startskript mit festem Port und Datenordner genügt. Alternativ ein vorhandener Mongo-Container mit Port-Forward. Fremde Datenbanken darin (andere Tenants/Testdaten) nicht verändern; eigene DB-Namen verwenden.

## Prozesse überleben lassen

Hintergrundaufgaben des Agenten-Harness enden nach Neustart oder Zeitlimit; Mongo und nodemon starben dabei, ein Kind-`node` hielt den Port weiter. Für längere Sitzungen per PowerShell `Start-Process` (versteckt, Logs in Datei) starten. Hängende Ports: PID mit `netstat -ano` finden, nur eigene Prozesse mit `taskkill /F /PID <pid>` beenden. Ein `cloudflared`-Prozess unter dem T3-Verzeichnis gehört T3 Code, nicht anfassen.

## Git-Bash-Fallen

- `MSYS_NO_PATHCONV=1` setzen, wenn Argumente mit `/` beginnen (`/api/...`, `git show origin/main:pfad`), sonst werden sie zu Windows-Pfaden.
- PowerShell: `$p` und `$P` sind dieselbe Variable.
- `git status --ignored` in Worktrees mit Junctions läuft minutenlang; abgebrochen hinterlässt es `index.lock`. Ohne `--ignored` arbeiten; Lock nur löschen, wenn kein git-Prozess läuft.

## Worktrees mit geteilten `node_modules` (Stand 09–11/2026)

Mehrere Worktrees teilten `node_modules` per NTFS-Junction mit einem anderen Checkout. Folgen:

- Pakete wie `librechat-data-provider`, `@librechat/api`, `@librechat/data-schemas` lösen auf den **anderen** Checkout auf; Änderungen im eigenen Worktree sind unsichtbar. Prüfen: `node -e "console.log(require.resolve('librechat-data-provider'))"` aus `packages/api`.
- Zwei Kopien von `@librechat/data-schemas` → zwei Tenant-Kontexte → 500 „…require an active tenant context". Kein Codefehler.
- Zwei `winston`-Kopien → „DailyRotateFile is not a constructor".
- Fehlt der Repo-Postinstall-Patch (`config/patch-langchain-openai-reasoning-summary.mjs`), meldet die Laufzeit „Tool … not found". Prüfen, dann den Patch aus dem Worktree ausführen (idempotent); nicht als Code-Bug „fixen".
- Junctions mit `[IO.Directory]::Delete(pfad, $false)` entfernen; rekursives Löschen läuft in das Ziel.

Eine eigene `npm ci`-Installation im Worktree vermeidet diese Klasse; sie kostet Zeit und Platz.

## Sonstiges

- `scripts/sort-imports.mts` nie ohne Dateiliste aufrufen (schreibt sonst über alle Quellwurzeln).
- Vite-Logs wachsen durch HMR stark; Logdateien regelmäßig kürzen.
- Erster Vite-Compile dauert über eine Minute; Headless-Screenshots erst danach.
- PDF-Parsing unter Windows stürzte vor Fix `ce9ebab2c` (11/2026) sporadisch mit Exit 139 ab; seitdem gilt ein Segfault dort als Regressionssignal.
