# mit agenten arbeiten

## vom plan zur umsetzung

Wenn ein Plan schon überzeugend klingt, mit [grilling](../skills/grilling/SKILL.md) die offenen Entscheidungen herausarbeiten. [to-spec](../skills/to-spec/SKILL.md) hält das Ergebnis fest, [to-tickets](../skills/to-tickets/SKILL.md) zerlegt es in Arbeitspakete samt Abhängigkeiten. [implement](../skills/implement/SKILL.md) arbeitet auf dieser Grundlage. Kleine Änderungen brauchen nicht zwangsläufig alle vier Schritte.

## subagents und sparring

Jacob nutzt viel Subagent-Arbeit und Cross-Harness-Reviews in T3, etwa Astra und Opus im Sparring. Ein sinnvoller Auftrag nennt Ziel, erlaubte Dateien, vorhandene Quellen und den Nachweis, an dem das Ergebnis geprüft wird. Bei paralleler Umsetzung überschneidende Schreibbereiche vermeiden. Ein Reviewer braucht die Anforderung und den tatsächlichen Diff; die Zusammenfassung des Implementierers allein reicht nicht.

[code-review](../skills/code-review/SKILL.md) trennt Projektstandards und Spezifikation. [council](../skills/council/SKILL.md) nutzt mehrere Anbieter; [sol-loop](../skills/sol-loop/SKILL.md) ist der eigene Ablauf für einen Sol-Reviewer. Für Astra/Opus die tatsächlich verfügbaren Modelle in T3 wählen und nicht behaupten, ein nicht verfügbares Modell habe geprüft. Maßgeblich sind die Orchestrierungsregeln der laufenden Sitzung.

## findings und abschluss

Ein brauchbares Finding nennt Datei/Stelle, Auslöser, Folge und einen konkreten Fix. Widersprechende Reviews gegen Code oder Test auflösen; Zustimmung mehrerer Agenten ersetzt keinen Nachweis. Im Abschluss unterscheiden: implementiert, getestet, reviewt, gemergt und ausgerollt. Für größere Vorhaben diesen Stand im selben [Postplan](../skills/postplan/SKILL.md) pflegen.

[full-stop](../skills/full-stop/SKILL.md) endet am mergebereiten PR, [full-send](../skills/full-send/SKILL.md) schließt den Merge ein. In actaOne können gemergte Templates und Provisioner den nächsten Deploy beeinflussen, auch ohne neues Kunden-Release. Dafür den [Release-Ablauf](../skills/cut-release/SKILL.md) und den konkreten Auftrag berücksichtigen.

## release und deploy babysitten

[babysit-release](../skills/babysit-release/SKILL.md) begleitet einen konkreten Kandidaten auf Staging bzw. einer benannten Testinstanz. [babysit-deploy](../skills/babysit-deploy/SKILL.md) begleitet den beauftragten Rollout. Beide leiten zuerst aus Git-Deltas einen Feature- und Aktivierungsplan ab: Code allein reicht nicht, Template, Renderer, Vault und Migration müssen zur Zielinstanz passen.

Release-Abnahme prüft alle anwendbaren Änderungen auf dem kleinen Testzielumfang. Beim Flotten-Deploy bekommt jede Zielinstanz Basis-/Konfigurationsnachweise; funktionale Tests laufen risikobasiert auf Canary und Vertretern der betroffenen Profile sowie zeitversetzt nach dem Rollout. Ein Fehler erweitert die Prüfung. Jobstatus, Konfigurationsnachweis und Funktionstest bleiben getrennt sichtbar.

Die Skills verwenden verfügbare Beobachtungsmechanismen, Postplan und Hark nach Auftrag. Sie installieren keinen eigenen Watch-Dienst und können ohne laufenden Harness keine dauerhafte Überwachung versprechen.
