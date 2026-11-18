# katalog

hier sind die 51 skills aus dem repo, nach aufgabe sortiert. jeder link führt direkt zur anleitung. quellen, voraussetzungen und anpassungen stehen im jeweiligen skill-ordner.

## planen, entwickeln und prüfen

| skill | wofür |
| --- | --- |
| [grilling](skills/grilling/SKILL.md) | einen plan oder eine idee gründlich hinterfragen. gerade dann, wenn man schon sehr überzeugt davon ist. |
| [to-spec](skills/to-spec/SKILL.md) | aus dem besprochenen vorhaben eine konkrete spezifikation machen. |
| [to-tickets](skills/to-tickets/SKILL.md) | einen plan in umsetzbare tickets mit abhängigkeiten zerlegen. |
| [implement](skills/implement/SKILL.md) | arbeit anhand einer spezifikation oder vorhandener tickets umsetzen. |
| [triage](skills/triage/SKILL.md) | issues und externe prs einordnen, prüfen und für die bearbeitung vorbereiten. |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | fehler und performanceprobleme systematisch eingrenzen. |
| [tdd](skills/tdd/SKILL.md) | features und fixes mit dem red-green-testzyklus entwickeln. |
| [code-review](skills/code-review/SKILL.md) | änderungen getrennt gegen projektregeln und die spezifikation prüfen. |
| [codebase-design](skills/codebase-design/SKILL.md) | module, schnittstellen und testbare grenzen entwerfen. |
| [domain-modeling](skills/domain-modeling/SKILL.md) | begriffe, fachmodell und architekturentscheidungen schärfen und festhalten. |
| [research](skills/research/SKILL.md) | eine frage anhand von primärquellen recherchieren und die ergebnisse dokumentieren. |
| [writing-for-agents](skills/writing-for-agents/SKILL.md) | anleitungen und dokumentation schreiben, mit denen agenten arbeiten können. |
| [resolving-merge-conflicts](skills/resolving-merge-conflicts/SKILL.md) | merge- und rebase-konflikte anhand der absicht beider änderungen lösen. |

## prs und reviews mit mehreren agenten

| skill | wofür |
| --- | --- |
| [full-send](skills/full-send/SKILL.md) | eine änderung durch umsetzung, review, pr und checks bis zum merge bringen. |
| [full-stop](skills/full-stop/SKILL.md) | denselben ablauf bis zum mergebereiten pr durchführen und dort stoppen. |
| [council](skills/council/SKILL.md) | reviews mit drei modellen verschiedener anbieter durchführen und findings abgleichen. |
| [sol-loop](skills/sol-loop/SKILL.md) | eine änderung wiederholt mit einem sol-reviewer prüfen und findings auflösen. |
| [file-pr](skills/file-pr/SKILL.md) | einen pr mit verständlicher beschreibung und passenden belegen anlegen. |
| [babysit-pr](skills/babysit-pr/SKILL.md) | ci und reviews eines prs verfolgen und relevante probleme bearbeiten. |
| [takeover](skills/takeover/SKILL.md) | bestehende arbeit an einem pr, branch oder agenten-thread übernehmen. |
| [modernize](skills/modernize/SKILL.md) | ältere prs auf den aktuellen stand bringen. |
| [leaving-pr-comments](skills/leaving-pr-comments/SKILL.md) | klare, korrekt formatierte kommentare auf github schreiben. |

## actaone entwickeln und betreiben

| skill | wofür |
| --- | --- |
| [actaone-local-dev](skills/actaone-local-dev/SKILL.md) | den librechat-fork lokal starten, ports und dienste zuordnen und ein testkonto einrichten. |
| [actaone-infra](skills/actaone-infra/SKILL.md) | den richtigen dienst, die umgebung, den zugangsweg und das runbook finden. |
| [actaone-ansible](skills/actaone-ansible/SKILL.md) | playbooks und persistente konfiguration ändern, applies vorbereiten und ergebnisse prüfen. |
| [keyvault-edit](skills/keyvault-edit/SKILL.md) | konfiguration über den vorgesehenen vault-scope ändern und ihre wirksamkeit prüfen. |
| [sudo-window](skills/sudo-window/SKILL.md) | administrative zugänge und temporäre rechte für beauftragte systemänderungen handhaben. |
| [diagnose-instance](skills/diagnose-instance/SKILL.md) | instanzfehler, deployprobleme, konfigurationsabweichungen und konkrete chatfehler untersuchen. |
| [cut-release](skills/cut-release/SKILL.md) | releases vorbereiten, stable freigeben und auf den beauftragten zielumfang ausrollen. |
| [babysit-release](skills/babysit-release/SKILL.md) | neue features und aktivierung aus git ableiten, den kandidaten auf staging begleiten und nach einem konkreten testplan abnehmen. |
| [babysit-deploy](skills/babysit-deploy/SKILL.md) | rollout begleiten, wirksamen stand aller ziele prüfen und neue features auf canaries, risikobasierten stichproben und beim recheck testen. |
| [actaone-vm-lifecycle](skills/actaone-vm-lifecycle/SKILL.md) | zustandswechsel von instanzen begleiten: branch-ttl, hotseats, archivierung, wiederaufnahme und abbau. |
| [actaone-provision-customer](skills/actaone-provision-customer/SKILL.md) | kundeninstanzen anlegen, hotseats übernehmen und onboarding sowie lebenszyklus prüfen. |
| [actaone-provisioning-webhook](skills/actaone-provisioning-webhook/SKILL.md) | den provisioning-webhook, seinen payload-vertrag und integrationsfehler bearbeiten. |
| [actaone-service-rollout](skills/actaone-service-rollout/SKILL.md) | zentrale dienste über canary und wellen einführen und den abbau alter ressourcen vorbereiten. |

## modelle, suche und auswertung

| skill | wofür |
| --- | --- |
| [actaone-litellm](skills/actaone-litellm/SKILL.md) | modelle, freigaben, teams, keys und discovery im gateway bearbeiten. |
| [actaone-presidio](skills/actaone-presidio/SKILL.md) | pseudonymisierung, erkennerqualität und die anbindung der instanzen prüfen. |
| [actaone-websearch](skills/actaone-websearch/SKILL.md) | websuche, scraping, reranking und quellenqualität untersuchen. |
| [actaone-benchmarks](skills/actaone-benchmarks/SKILL.md) | modellvergleiche und messreihen auf der benchmark-instanz durchführen. |
| [actaone-usage-analysis](skills/actaone-usage-analysis/SKILL.md) | nutzungsaggregate je instanz lesend auswerten und kostenbegriffe auseinanderhalten. |

## tickets, projekte und wissen

| skill | wofür |
| --- | --- |
| [actaone-zoho-desk](skills/actaone-zoho-desk/SKILL.md) | actaone-tickets bearbeiten und antwortentwürfe als interne kommentare hinterlegen. keine kundenmails senden. |
| [actaone-zoho-projects](skills/actaone-zoho-projects/SKILL.md) | aufgaben, status, verantwortliche und termine pflegen. änderungen vorher zeigen, nichts löschen. |
| [postplan](skills/postplan/SKILL.md) | für größere vorhaben einen projektplan anlegen und unter derselben url weiterpflegen. |
| [actaone-kb-maintenance](skills/actaone-kb-maintenance/SKILL.md) | die obsidian-wissensbasis lesen, notizen pflegen und arbeitswissen aus sessions festhalten. |

zoho desk und projects nutzen die bereitgestellten mcp-server. postplan kommt bei größeren vorhaben dazu, wenn es verfügbar und sinnvoll ist; zoho bleibt für tickets und aufgaben maßgeblich.

## dokumente und kommunikation

| skill | wofür |
| --- | --- |
| [actaone-documents](skills/actaone-documents/SKILL.md) | dokumente, präsentationen und berichte mit den passenden ci-vorlagen gestalten. |
| [docx](skills/docx/SKILL.md) | word-dateien und vorlagen erstellen, lesen und bearbeiten. |
| [pdf](skills/pdf/SKILL.md) | pdfs erstellen, auslesen, zusammenfügen und bearbeiten. |
| [pptx](skills/pptx/SKILL.md) | powerpoint-präsentationen und vorlagen erstellen oder überarbeiten. |
| [xlsx](skills/xlsx/SKILL.md) | tabellen, formeln und auswertungen erstellen oder bearbeiten. |
| [actaone-release-notes](skills/actaone-release-notes/SKILL.md) | release-änderungen in belegte release notes und produkt-payloads übersetzen. |
| [making-actaone-feature-trailers](skills/making-actaone-feature-trailers/SKILL.md) | feature-trailer und kurze produktvideos erstellen oder überarbeiten. |

## skripte und wissen

für ci-pdfs gibt es den [generator](skills/actaone-documents/scripts/build_ci.py) mit gebündeltem konzeptlayout, logo, schriften und [beispiel-pdf](skills/actaone-documents/examples/report.pdf). die [startanleitung](skills/actaone-documents/references/ci-generator.md) beschreibt den aufruf.

die [dokumentübersicht](knowledge/documents.md) erschließt außerdem die office-/pdf-skripte: kommentare, konvertierung, formularfelder, folienvorschau und formelberechnung. im [wissensbereich](knowledge/README.md) stehen einstiege zu agenten-workflows, actaone-quellen und wissenspflege.

## was ihr dafür braucht

- die actaone-skills brauchen je nach aufgabe die privaten repos, runbooks, wissensbasis und eingerichteten zugänge.
- die pr-skills brauchen github-zugang und teilweise weitere skills aus dieser sammlung. council und sol-loop brauchen die passenden modelle und einen harness, der sie aufrufen kann.
- der trailer-skill braucht einen separaten arbeitsordner und seine werkzeuge. dieser ordner liegt nicht hier im repo.
- der ci-pdf-generator enthält logo, inter-schriften und das layout aus den actaone-konzeptdokumenten. andere vorlagen oder marken brauchen ihre eigenen assets; das paket ist keine vollständige firmenweite ci-richtlinie.
- formatwerkzeuge und hilfsskripte haben eigene abhängigkeiten. schaut vor dem einsatz in den jeweiligen skill, besonders unter windows.

quellen und lizenzen stehen in den skill-ordnern. die engineering-skills von matt pocock und tstack tragen mit-lizenzen, die vier office-skills apache-2.0-lizenzen. details und weitere hinweise stehen jeweils in `references/sources.md`.

## prüfen

```text
python -m pip install -r requirements-dev.txt
python scripts/validate.py
```

der validator prüft struktur und links. er führt die workflows nicht aus. die szenarien in `evaluation.md` beschreiben, wie sich ein skill verhalten soll; sie sind keine automatisch ausgeführten tests.

bei `implement`, `to-spec`, `to-tickets` und `triage` akzeptiert der codex-validator das claude-feld `disable-model-invocation` nicht. die passende installation und das aufrufverhalten müssen deshalb je harness geprüft werden.
