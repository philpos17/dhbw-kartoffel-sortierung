# dhbw-kartoffel-sortierung

## Projektüberblick

Dieses Projekt entsteht im Rahmen eines Abschlussprojekts einer Vorlesung. Ziel ist es, einen realen Anwendungsfall aus der Landwirtschaft mit Methoden des Machine Learning bzw. Computer Vision zu bearbeiten.

Der Use Case stammt von einem Kartoffelbauernhof. Dort werden Kartoffeln aktuell manuell sortiert. Unterschieden werden dabei verwertbare Kartoffeln, beschädigte oder schlechte Kartoffeln sowie Steine bzw. Fremdkörper. Die manuelle Sortierung ist zeitaufwendig und personalintensiv. Ziel des Projekts ist es, diesen Prozess durch ein bildbasiertes System zu unterstützen oder teilweise zu automatisieren.

## Problemstellung

Untersucht wird, ob sich Kartoffeln und unerwünschte Objekte auf einem Förderbandbild zuverlässig mit Computer Vision erkennen und klassifizieren lassen.

Aktuell betrachten wir ein Object-Detection-Setup mit den Klassen:

- `potato`
- `bad`
- `cut`
- `stone`

Eine offene fachliche Frage ist noch, ob `cut` langfristig als eigene Klasse bestehen bleibt oder als Unterkategorie von `bad` behandelt werden sollte.

## Zielsetzung

Das Projektziel ist die Entwicklung und Bewertung eines Prototyps zur automatischen Erkennung und Sortierung von Kartoffeln und Fremdkörpern auf Bildern eines fließbandähnlichen Aufbaus.

Dazu sollen insbesondere folgende Fragen beantwortet werden:

- Ist Object Detection für diesen Use Case geeignet?
- Welche Modellarchitektur liefert auf dem vorhandenen Datensatz die besten Ergebnisse?
- Wie repräsentativ ist der aktuelle Datensatz für den späteren realen Einsatz?
- Welche Schwächen, Verzerrungen und Grenzen besitzt der Datensatz?
- Welche Metriken eignen sich zur Bewertung des Systems?

## Datensatz

Der aktuelle Datensatz wurde in Roboflow verwaltet und enthält derzeit:

- `773` Bilder
- `16.481` Annotationen
- `4` Klassen
- durchschnittlich `21,3` Objekte pro Bild
- Bildformat überwiegend `1920 x 1080`

Aktuelle Klassenverteilung laut bisherigem Stand:

- `potato`: 16.197
- `bad`: 1.978
- `stone`: 732
- `cut`: 32

Wichtiger Hinweis:
Der Datensatz ist vermutlich noch nicht vollständig repräsentativ für den realen späteren Einsatz. Nach aktuellem Stand wurden Kartoffeln auf ein Band gelegt, während Steine und beschädigte Beispiele teilweise künstlich ergänzt wurden. Die Repräsentativität des Datensatzes und insbesondere des Validation Sets muss im Projekt kritisch reflektiert werden.

## Bisherige Experimente in Roboflow

Bisher wurden in Roboflow mehrere Object-Detection-Modelle getestet.

### Ergebnisse

| Modell | Typ | Datum | mAP@50 | Precision | Recall | F1 |
|---|---|---|---:|---:|---:|---:|
| My First Project 6 | RF-DETR Small | 31.05.2026 | 75.1% | 84.2% | 76.1% | 80.0% |
| My First Project 4 | YOLOv11 Nano | 31.05.2026 | 72.2% | 68.3% | 76.4% | 72.1% |
| My First Project 3 | RF-DETR Medium | 17.05.2026 | 74.6% | 85.3% | 75.8% | 80.3% |
| My First Project 2 | RF-DETR Medium | 16.05.2026 | 66.7% | 66.3% | 65.7% | 66.0% |
| My First Project 1 | RF-DETR Small | 16.05.2026 | 50.4% | 48.5% | 50.0% | 49.3% |

Erste Beobachtung:
Die bisherigen Ergebnisse zeigen, dass der Use Case grundsätzlich lernbar ist. Gleichzeitig deuten die Werte darauf hin, dass Datensatzqualität, Klassenbalance und Repräsentativität einen starken Einfluss auf die Modellleistung haben.

## Geplanter Projektansatz

Das Projekt soll in mehreren Schritten bearbeitet werden:

1. Problemstellung und Zielbild fachlich präzisieren
2. Datensatz dokumentieren und kritisch bewerten
3. Related Work zu Agrar-Object-Detection recherchieren
4. Daten exportieren und reproduzierbare Trainingspipeline außerhalb von Roboflow aufbauen
5. Baseline-Modell im Jupyter Notebook trainieren bzw. evaluieren
6. Modelle vergleichen
7. Ergebnisse diskutieren und Grenzen des Ansatzes reflektieren

## Tools und Arbeitsumgebung

Geplant ist folgende Arbeitsumgebung:

- `Roboflow` für Annotation, Datensatzversionierung und erste Experimente
- `Jupyter Notebook` für dokumentierte und reproduzierbare Analyse
- `GitHub` für Zusammenarbeit und Versionsverwaltung
- `Google Colab` oder lokale Rechner für Training und Auswertung

## Reproduzierbarkeit

Ein wichtiger Teil des Projekts ist die Überführung der bisher in Roboflow geleisteten Arbeit in eine nachvollziehbare Projektstruktur. Dafür sollen insbesondere folgende Punkte dokumentiert werden:

- verwendete Datensatzversion
- Klassen und Labeldefinitionen
- Preprocessing- und Augmentierungsentscheidungen
- trainierte Modellarchitekturen
- verwendete Hyperparameter
- Evaluationsergebnisse

## Offene Fragen

Die folgenden Punkte müssen noch geklärt oder geschärft werden:

- Soll das Zielsystem 3 oder 4 Klassen unterscheiden?
- Ist `cut` eine eigene Klasse oder Teil von `bad`?
- Wie sieht die reale Klassenverteilung im Feld bzw. auf dem Band aus?
- Wie sollte ein repräsentatives Validation- und Test-Set aussehen?
- Können zusätzliche echte Daten aufgenommen werden?
- Soll das Endziel eher Erkennung, Zählung oder tatsächliche Sortierentscheidung sein?

## Vorläufiges Fazit

Der Anwendungsfall ist praxisnah und eignet sich gut für ein Computer-Vision-Projekt. Die bisherigen Roboflow-Ergebnisse sind ein guter Ausgangspunkt. Der wichtigste nächste Schritt besteht darin, Problemdefinition, Datensatzqualität und Evaluationsstrategie sauber zu schärfen, damit die spätere Modellbewertung fachlich belastbar ist.