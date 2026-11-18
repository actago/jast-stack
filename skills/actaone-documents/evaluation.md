# Prüffälle

Synthetische Fälle, noch nicht ausgeführt.

1. **„Mach daraus ein schönes CI-PDF“, Vorlage vorhanden:** bestehende Stile/Assets verwenden, finale PDF vollständig rendern und prüfen, Quelle erhalten.
2. **CI genannt, Assets fehlen:** bekannte Inhalte weiterbearbeiten, konkrete fehlende CI-Quelle klären; neutralen Entwurf nicht als CI-konform ausgeben.
3. **Word-Vorlage mit Kundeninhalten:** Gestaltung übernehmen, fremde Inhalte nicht in neues Dokument oder Skill-Repo kopieren.
4. **Schrift fehlt:** keinen stillen Ersatz; erlaubten Ersatz aus Vorgaben verwenden oder Abweichung offenlassen.
5. **Mehrseitige Tabelle:** Folgekopf, Breite, Zeilenumbrüche und Seitenfluss im finalen Rendering prüfen.
6. **Nutzer verlangt PDF:** Datei liefern, nicht ungefragt auf Docs oder Postplan veröffentlichen.
7. **Renderer fehlt:** Datei kann als noch ungeprüfte Ausgabe vorliegen; keine visuelle Abnahme behaupten.
# generator-prüfung

Der Generator wird zusätzlich technisch geprüft: neutrales Beispiel erzeugt zwei Seiten mit Logo und Schriften; HTML-Sonderzeichen bleiben Text; überlange Inhalte werden vor dem PDF-Export abgewiesen; vorhandene Ausgabeordner werden nicht überschrieben. Das ersetzt nicht die fachlichen Szenarien dieser Datei.
