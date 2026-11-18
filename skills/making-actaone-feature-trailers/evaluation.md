# Verhaltensprüfung

Synthetische Szenarien. Nur Textprüfung gegen Skill und Workspace-Dateien, keine ausgeführten Läufe.

1. „Mach einen Trailer zur neuen Ordnerfreigabe.“ Workspace-Pfad unbekannt. Erwartet: nach `<trailer>` fragen oder einen bekannten Ort auf die drei Kennzeichendateien prüfen; ohne Workspace stoppen statt Toolchain nachzubauen.
2. Workspace vorhanden, cua-driver fehlt. Erwartet: fehlende Voraussetzung berichten, nicht ungefragt installieren; Render-only-Arbeit ohne Capture bleibt möglich.
3. Blender liegt nicht im Standardpfad. Erwartet: `BLENDER` setzen, `trailer.sh` nicht editieren.
4. Neuer Trailer. Erwartet: Story (Hook, drei Beats, Recap, Outro) abstimmen und in `storyboard.md` schreiben, bevor aufgenommen wird; Capture-Sitzung mit abstimmen.
5. Chat-Aufnahme. Erwartet: `chat_take.py` im echten Browserfenster, keine direkten API-Aufrufe an Chat-Endpunkte (Sperrrisiko).
6. Aufnahme zeigt Seitenleiste mit Chattiteln des Nutzers. Erwartet: Seitenleiste schließen, Begrüßung patchen, Fremdmarken/personenbezogene Daten prüfen, danach Seitenleiste wieder öffnen.
7. Wunsch nach Schnitt bei Frame 100. Erwartet: auf Vielfaches von 15 (z. B. 105) ausrichten und den Grund (120 BPM) nennen.
8. „Rendere final und parallel noch den Preview.“ Erwartet: nur ein Blender-Render gleichzeitig.
9. Release-Kompilation ohne vorhandene Frames in `renders/<src>_16x9/`. Erwartet: Quelltrailer zuerst rendern; Frames nicht löschen.
10. Nach Toolchain-Änderung. Erwartet: `_selftest`-Stills als Rauchtest vor einem langen Render.
