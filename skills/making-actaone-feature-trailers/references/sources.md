# Herkunft, geprüfter Stand und Grenzen

Stand: 2026-11-17. Nur Quellen gelesen; keine Skripte, kein Blender, kein Capture, kein Render ausgeführt. Weder Trailer-Workspace noch aktive Installation verändert.

## Ausgangsskill

Persönlicher Claude-Skill `making-actaone-feature-trailers` (Ordner enthält nur `SKILL.md`, Änderungsdatum 24.09.2026). Kein Git-Stand, keine Lizenzdatei; vom Nutzer für actago-Arbeit geschrieben. Hash des Ausgangsstands: [source-manifest.json](source-manifest.json).

## Trailer-Workspace

Der Skill ist ein Ablauf über einen separaten Arbeitsordner. Beim Nutzer liegt er unter einem persönlichen Projektpfad; der Skill nennt ihn jetzt `<trailer>`. Befund vom 17.11.2026:

- **Kein Git-Repository**, kein Remote, keine README, keine Lizenzdatei. Herkunft, Versionsstand und Weitergaberechte sind damit nicht belegt. Er enthält unter anderem staging-Aufnahmen und Renderergebnisse.
- Nicht in den Skill übernommen: Er ist ein Projekt mit Assets und Renderausgaben, keine Skill-Ressource, und es fehlt eine geklärte Weitergabe. Für gemeinsame Nutzung muss er erst als Repository mit Herkunft und Lizenz bereitgestellt werden.
- Vorhanden und mit den Angaben des Skills übereinstimmend (gelesen, nicht ausgeführt): `storyboard.md` (Stand 23.09.2026), `scripts/trailer.sh` mit Modi `stills|preview|final|music`, `_template.py` (900 Frames, Schnitte auf Vielfachen von 15), `make_music.py` (120 BPM), `grab.py --burst/--interval`, `chat_take.py`, `cua.py` mit `max_elements`-Wiederholung, `prep_lib.py` mit `still`, `seq`, `retime`, `first_change`, `first_match`, `typing_frames`, `ring`, `greeting_patcher`, `clean()` in `prep_control.py`/`prep_studio.py`, `release.py` mit `FRAME_END`, `DROP`, `RENDER_RANGES`, `CLIPS`, `assemble_release.py`, `style_loop.py`, `trailers/_selftest.py`.
- `kit.py` bestätigt den 46-px-Browserbalken.

Laufzeitannahmen in den Skripten (vorher implizit, jetzt im Skill als Vorprüfung):

- `cua.py`, `staging_window.py`: cua-driver unter `~\AppData\Local\Programs\Cua\cua-driver\bin\cua-driver.exe`. Beim Nutzer existiert zusätzlich ein persönlicher Skill `cua-driver` (Version 0.28.2); der Trailer-Ablauf hängt nur am Programm, nicht am Skill.
- `staging_window.py`: Edge unter `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`, Standard-URL `https://staging.ki.actago.de/c/new`, Windows-API über `ctypes.windll`.
- `trailer.sh`: `BLENDER` mit Default auf den Windows-Standardpfad von Blender 5.2; ffmpeg auf `PATH`.
- `style_loop.py`: liest Downloads aus `~\Downloads`.

## Weitere Quellprüfung

- `NON_BROWSER_VIOLATION_SCORE`: im LibreChat-Fork (`api/server/middleware/uaParser.js`, Blob `d7d38f1023d9`, `origin/main` `f29a7aafa2dc`) mit Default 20 belegt. Die konkrete Sperrdauer von zwei Stunden auf Staging ist nicht geprüft und stammt aus dem Ausgangsskill.
- Erfahrungswerte (3,3 s/Frame, ~25/~50 min, iGPU, „Luna“ macht ohne „nach unserer …“ eine Websuche, Pixelumrechnung `0.98`/`+30`) stammen aus dem Ausgangsskill und sind hardware- bzw. modellabhängig; nicht nachgemessen.

## JAST-Änderungen (für spätere Updates)

- Beschreibung ohne persönlichen Pfad; Workspace als `<trailer>`-Parameter.
- Neuer Abschnitt „Before the first step“: Workspace finden, Laufzeit prüfen statt Vorinstallation vorauszusetzen, Capture mit dem Nutzer abstimmen.
- `greeting_patcher` seinem Modul `prep_lib` zugeordnet (war als eigenständiges Skript lesbar).
- Alle fachlichen Regeln, Tabelle „Rules that bite“ und Quick reference unverändert.
- `references/sources.md`, `source-manifest.json`, `evaluation.md`: neu.

## Grenzen

- Kein Render-, Capture- oder Selbsttest; Strukturprüfung ersetzt keine Abnahme.
- Ohne Zugriff auf den Workspace ist der Skill nicht anwendbar. Das ist eine bewusste Lücke, kein Defekt der Übernahme.
