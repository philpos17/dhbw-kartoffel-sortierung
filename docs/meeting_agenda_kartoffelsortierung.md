# Gesprächsagenda für heute Abend

Stand: 27.06.2026

Ziel dieses Gesprächs ist nicht, schon alles perfekt zu lösen, sondern die wichtigsten fachlichen und methodischen Entscheidungen festzuziehen, damit wir das Projekt danach sauber aufsetzen können.

## 1. Zielbild der Anwendung klären

Zuerst sollten wir festlegen, für welchen realen Arbeitsschritt die Lösung überhaupt gebaut werden soll.

Zu klären:

- An welcher Prozessstufe soll die Lösung später eingesetzt werden?
- Findet die Sortierung vor oder nach Reinigung bzw. Vorseparation statt?
- Sollen wir einen realen Förderbandprozess nachbilden oder eher einen Labor-Prototypen für eine ähnliche Situation?
- Ist die spätere Zielumgebung ein einzelnes Kamerabild von oben oder sind langfristig mehrere Kameras bzw. eine Wendevorrichtung denkbar?
- Soll das System nur Objekte erkennen oder später auch eine tatsächliche Sortierentscheidung unterstützen?

Entscheidung heute:

- Exakte Prozessstufe definieren
- Zielumgebung grob festlegen
- Festlegen, ob wir im Projekt nur visuelle Erkennung bewerten oder schon eine Sortierlogik mitdenken

## 2. Zielklassen und Labeldefinitionen festlegen

Wir müssen die Klassen so definieren, dass sie fachlich sinnvoll und mit unseren Daten realistisch lernbar sind.

Zu klären:

- Welche Klassen sollen im Hauptmodell unterschieden werden?
- Soll `cut` eine eigene Klasse bleiben oder in `bad` aufgehen?
- Welche Defekttypen sind in der Praxis tatsächlich aussortierrelevant?
- Gehören Erdkluten fachlich zu `stone` oder brauchen wir dafür eigentlich eine eigene Kategorie?
- Welche weiteren Fremdobjekte kommen in der Praxis vor?
- Soll das Modell nur sichtbare Oberflächendefekte bewerten?

Entscheidung heute:

- Finale Hauptklassen für das Projekt festlegen
- Entscheiden, ob `bad` und `cut` zusammengeführt werden
- Klären, was genau unter `defective potato` bzw. `bad` fällt

Empfehlung:

- Wenn `bad` und `cut` dieselbe betriebliche Konsequenz haben, sollten wir sie für das Hauptmodell zusammenführen und den Defekttyp nur als Zusatzinformation behalten.

## 3. Reale Klassenverteilung und Repräsentativität verstehen

Wir brauchen ein Gefühl dafür, wie die reale Welt aussieht. Das ist wichtiger als ein künstlich schön ausbalanciertes Datenset.

Zu klären:

- Wie ist ungefähr die natürliche Verteilung von guten Kartoffeln, schlechten Kartoffeln und Steinen?
- Schwankt diese Verteilung stark zwischen Chargen, Sorten oder Tagen?
- Wie oft kommen seltene Defekte real vor?
- Wie hoch ist typischerweise der Anteil von Schmutz, Erdauflage oder teilverdeckten Kartoffeln?
- Wie oft treten Steine auf und wie ähnlich sehen sie Kartoffeln in der Praxis?

Entscheidung heute:

- Eine grobe Zielverteilung für den späteren Praxistest festhalten
- Einschätzen, wie weit das aktuelle Datenset davon entfernt ist

Wichtig:

- Das Trainingsset darf angereichert werden, aber Validation und Test sollten später die reale Verteilung möglichst gut widerspiegeln.

## 4. Aufnahme- und Datenerhebungsstrategie festlegen

Die Literatur spricht klar dafür, nicht nur mehr Daten zu sammeln, sondern vor allem realistischere Daten.

Zu klären:

- Können wir zusätzliche Bilder aufnehmen?
- Können wir mehrere getrennte Aufnahmesessions machen?
- Können wir nicht vorsortierte oder zumindest weniger künstlich arrangierte Szenen aufnehmen?
- Können wir verschiedene Dichten, Lichtbedingungen und Verschmutzungsgrade abdecken?
- Können wir Daten aus mehreren Chargen, Sorten oder Tagen bekommen?

Entscheidung heute:

- Ob und wie zusätzliche reale Daten aufgenommen werden
- Welche Situationen zwingend zusätzlich erfasst werden sollen
- Ob das aktuelle Setup nur ein Startdatensatz ist oder schon die Hauptdatenbasis

Empfehlung:

- Wenn möglich sollten neue Daten in Aufnahmeblöcken gesammelt werden, damit wir später sinnvoll nach Sessions oder Chargen splitten können.

## 5. Definition eines repräsentativen Validation- und Test-Sets

Das ist einer der wichtigsten methodischen Punkte im ganzen Projekt.

Zu klären:

- Was wäre für uns ein realistisches Validation-Set?
- Soll das Validation-Set die natürliche Klassenverteilung abbilden oder absichtlich ausgeglichener sein?
- Welche Daten sollen als späterer Haupttest dienen?
- Wollen wir zusätzlich ein separates Challenge-Set für seltene oder schwierige Fälle aufbauen?

Entscheidung heute:

- Ob wir zwei getrennte Testlogiken verwenden:
- ein realitätsnahes Set mit natürlicher Verteilung
- ein Challenge-Set mit seltenen und schwierigen Fällen

Empfehlung:

- Ja, diese Trennung wäre methodisch sehr stark.

## 6. Split-Strategie für Train, Validation und Test

Wir sollten vermeiden, dass sehr ähnliche Bilder aus derselben Aufnahmesession in mehreren Splits landen.

Zu klären:

- Aus wie vielen Aufnahmeblöcken oder Sessions bestehen unsere aktuellen Daten eigentlich?
- Lassen sich bestehende Bilder rückwirkend nach Session, Tag oder Aufbau gruppieren?
- Können wir bei neuen Daten eine `session_id` oder `sequence_id` mitführen?

Entscheidung heute:

- Ob wir künftig nach Aufnahmegruppen statt rein zufällig splitten
- Welche Metadaten wir ab sofort unbedingt mitprotokollieren

Empfehlung:

- Ganze Sessions oder Blöcke sollten jeweils nur in einem Split liegen.

## 7. Was genau als Projekterfolg zählt

Wir sollten früh festlegen, welche Fehler im Use Case am kritischsten sind.

Zu klären:

- Was ist schlimmer: einen Stein übersehen oder eine gute Kartoffel fälschlich aussortieren?
- Welche Fehler wären in der Praxis noch tolerierbar?
- Ist hoher Recall bei `stone` wichtiger als eine gute Gesamt-mAP?
- Welche Zielgröße ist fachlich am wichtigsten: Sicherheit, Ausbeute, Geschwindigkeit oder ein Kompromiss daraus?

Entscheidung heute:

- Priorität der Fehlertypen festlegen
- Definieren, welche betriebliche Metrik für euch am wichtigsten ist

Empfehlung:

- Für den Use Case sollten wir nicht nur globale Modellmetriken betrachten, sondern explizit `stone recall`, `defect recall` und die Fehlablehnung guter Kartoffeln.

## 8. Modellvergleich sinnvoll eingrenzen

Wir haben schon erste Roboflow-Ergebnisse, aber der finale Vergleich muss fair und überschaubar bleiben.

Zu klären:

- Welche Modelle wollen wir im eigentlichen Projekt wirklich vergleichen?
- Reicht ein kompakter YOLO-Vertreter plus ein oder zwei RF-DETR-Varianten?
- Wollen wir eher maximale Genauigkeit vergleichen oder auch Laufzeit auf realistischer Hardware?
- Trainieren wir final lokal, in Colab oder teilweise weiter in Roboflow?

Entscheidung heute:

- Kleine finale Modellliste festlegen
- Haupttrainingsumgebung festlegen

Empfehlung:

- Ein sinnvoller Minimalvergleich wäre:
- ein kompaktes YOLO-Modell
- RF-DETR Small
- optional RF-DETR Medium

## 9. Umgang mit Roboflow im Projekt

Wir müssen festlegen, wie Roboflow in den eigentlichen Projektworkflow eingebunden wird.

Zu klären:

- Wofür nutzen wir Roboflow weiterhin konkret?
- Nur für Annotation und Dataset-Verwaltung oder auch für Vortraining und Baselines?
- Exportieren wir den Datensatz in YOLO- oder COCO-Format?
- Wollen wir Modellgewichte aus Roboflow als Vergleich mitnehmen?
- Wie dokumentieren wir Dataset-Versionen, Klassen und Augmentierungen so, dass es in GitHub und im Notebook nachvollziehbar bleibt?

Entscheidung heute:

- Rolle von Roboflow verbindlich festlegen
- Exportformat festlegen
- Entscheiden, ob Roboflow-Modelle nur Vorversuche bleiben oder Teil des finalen Vergleichs werden

Empfehlung:

- Roboflow als Annotation- und Baseline-Tool nutzen, aber die finale reproduzierbare Analyse in GitHub und Jupyter Notebook abbilden.

## 10. Umgang mit Data Augmentation und synthetischen Daten

Wir sollten hier bewusst vorgehen und nicht zu früh zu viel künstlich erzeugen.

Zu klären:

- Reichen Standardaugmentierungen zunächst aus?
- Wollen wir synthetische Daten überhaupt nutzen?
- Falls ja, für welche Klassen und in welchem Umfang?
- Wollen wir Copy-Paste für Steine testen?

Entscheidung heute:

- Ob synthetische Daten ein Kernelement oder nur ein Zusatzexperiment werden
- Welche konservativen Standardaugmentierungen wir als Startpunkt verwenden

Empfehlung:

- Zuerst echte Daten plus einfache realistische Augmentation.
- Synthetische Daten nur ergänzend und nie als Ersatz für reale Testdaten.

## 11. Grenzen des Kamerasetups realistisch festlegen

Ein Einzelkamerasystem kann nicht alles leisten. Das müssen wir fachlich sauber einordnen.

Zu klären:

- Soll ein nicht sichtbarer Defekt auf der Unterseite überhaupt als Fehler des Modells gelten?
- Welche Fälle sind aus einer einzigen Draufsicht grundsätzlich nicht entscheidbar?
- Reicht für das Projekt die sichtbare Oberflächenqualität aus?

Entscheidung heute:

- Bewertungsgrenze des Systems definieren
- Festlegen, dass nur visuell sichtbare Informationen der Einzelansicht beurteilbar sind

## 12. Praktische Metadaten, die wir ab jetzt sammeln sollten

Wenn wir weitere Daten aufnehmen, sollten wir gleich die richtigen Zusatzinformationen mitschreiben.

Sinnvolle Metadaten:

- Datum
- Session- oder Sequence-ID
- Charge
- Sorte
- Feld oder Lieferant, falls verfügbar
- Licht-Setup
- Kameraposition
- Bandgeschwindigkeit
- Belegungsdichte
- Verschmutzungsgrad
- Bemerkungen zu Besonderheiten der Aufnahme

Entscheidung heute:

- Welche Metadaten realistisch erfassbar sind
- Welche davon Pflichtfelder für neue Aufnahmen werden

## 13. Konkrete Entscheidungen, die wir am Ende des Gesprächs getroffen haben sollten

Am Ende des Gesprächs sollten wir idealerweise diese Punkte entschieden haben:

- reale Zielanwendung und Prozessstufe
- finale Hauptklassen
- Umgang mit `cut`
- grobe Zielverteilung für den Praxistest
- Plan für zusätzliche Datenaufnahme
- Split-Strategie nach Sessions oder Gruppen
- Trennung von realistischem Testset und Challenge-Set
- finale Modellkandidaten für den Hauptvergleich
- Rolle von Roboflow im Workflow
- Umgang mit Augmentation und synthetischen Daten
- wichtigste Erfolgsmetriken aus fachlicher Sicht

## 14. Empfohlene Kurzfassung für das Gespräch

Wenn wenig Zeit ist, sollten wir mindestens diese Kernfragen beantworten:

1. Für welche reale Prozessstufe bauen wir die Lösung?
2. Welche finalen Klassen wollen wir im Hauptmodell?
3. Ist `cut` eine eigene Klasse oder Teil von `bad`?
4. Wie sieht die reale Klassenverteilung ungefähr aus?
5. Können wir mehr reale, weniger künstliche Daten aufnehmen?
6. Wie sollen Validation und Test realistisch aufgebaut sein?
7. Wollen wir natürliches Testset und Challenge-Set trennen?
8. Welche Modelle vergleichen wir final?
9. Welche Fehler sind in der Praxis am kritischsten?
10. Welche Rolle spielt Roboflow im finalen Workflow?

## 15. Persönliche Empfehlung für eure Richtung

Wenn ich eurem Projekt jetzt eine klare Richtung geben müsste, würde ich heute Abend auf folgende Zielentscheidung hinarbeiten:

- Hauptaufgabe als `good potato` vs. `defective potato` vs. `stone`
- `cut` nicht als Hauptklasse, sondern als Defekt-Untertyp
- neue Daten möglichst in echten Aufnahmeblöcken sammeln
- Split nicht zufällig, sondern nach Sessions oder Gruppen
- ein realistisches Testset mit natürlicher Verteilung plus separates Challenge-Set
- fairer Vergleich von kleinem YOLO-Modell und RF-DETR unter identischen Bedingungen

Das wäre für euer Projekt fachlich sauber, praktisch machbar und methodisch deutlich stärker als nur ein weiterer isolierter Roboflow-Score.
