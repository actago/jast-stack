# Arbeit am JAST-Stack

Zielgruppe sind Entwickler und Betreiber von actaOne, die mit KI-Agenten arbeiten. Aggregiere vorhandene Custom Skills und Wissensquellen. Erfinde keine Ersatz-Skills für vorhandene Abläufe. Endanwender-Skills innerhalb von actaOne gehören derzeit nicht zum Umfang.

Bei neuen oder geänderten Skills lies [CONTRIBUTING.md](CONTRIBUTING.md). Jeder Skill muss als einzelner Ordner nutzbar bleiben; benötigte Referenzen gehören in seinen Ordner. Vermeide Abhängigkeiten von persönlichen lokalen Skills oder nicht verfügbaren Tools.

Beginne mit [catalog.md](catalog.md). Prüfe Aussagen über actaOne gegen maßgebliche Repository-Dokumente oder Wissensquellen. Halte Quellenprüfung und tatsächlichen Produkttest getrennt fest.

Übernimm in dieses Repo nur wiederverwendbares Arbeitswissen und erfundene oder anonymisierte Beispiele. Interne Betriebsdaten, Zugangsdaten und echte Gesprächs- oder Kundendokumente gehören nicht in die Beispielsammlung.

## Zoho Desk

- Nur actaOne, departmentId `68034000021139364`; diese ID bei Listen und Suchen immer mitgeben. Tickets anderer Abteilungen erst lesen, wenn der Nutzer die andere Abteilung ausdrücklich beim Namen angefordert hat.
- Niemals Kunden-E-Mails senden; `ZohoDesk_sendReply` ist gesperrt.
- Antwortentwürfe ausschließlich als internen Kommentar über `ZohoDesk_createTicketComment` mit `isPublic: false` und Kennzeichnung `Antwortentwurf:` speichern. Der Nutzer versendet selbst.

## Zoho Projects

- Portal-ID `20077052774` verwenden, nicht den Portalnamen `actago`.
- Hauptprojekt „Künstliche Intelligenz“: `131604000008451668`.
- Filter brauchen `pattern`, auch bei einem Kriterium. `${me}` ist kein gültiger Owner-Wert; ZPUID verwenden oder clientseitig nach Owner-E-Mail filtern.
- Niemals löschen. Vor Erstellen oder Ändern von Aufgaben dem Nutzer die konkreten Änderungen zeigen.
