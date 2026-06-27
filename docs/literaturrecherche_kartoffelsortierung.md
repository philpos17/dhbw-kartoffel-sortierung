# Literaturrecherche: visuelle Kartoffelsortierung

Stand: 27. Juni 2026  
Projekt: RGB-Object-Detection für `good_potato`, `defective_potato` und `stone`

## Kurzfazit

Visuelle Kartoffelsortierung ist kein unbearbeitetes Feld. Es existieren RGB-Arbeiten zu Oberflächendefekten und seit Juni 2026 auch ein integriertes Förderbandsystem für Kartoffeln, Steine und Erdkluten. Die Studien verwenden jedoch überwiegend kontrollierte Beleuchtung, inszenierte oder ausgewogene Proben, zufällige Bildsplits und nur eine Detektorfamilie.

Eine tragfähige Forschungslücke lautet daher:

> Existing evidence is limited regarding fair comparisons of compact CNN/YOLO and real-time transformer detectors on densely populated RGB conveyor images of unsorted potatoes, using grouped data splits, natural operational prevalence, and a separately reported rare-case evaluation.

Nicht vertretbar wäre dagegen die Behauptung, es gebe noch keine RGB-Förderbandarbeit zu Kartoffeln und Steinen.

## A. Priorisierte Shortlist

### [1] Wang et al. (2026): Kartoffeln, Steine und Erdkluten

[Deep Learning-Based Intelligent Sorting of Potato Tubers and Mineral Impurities](https://doi.org/10.3390/foods15122070)

Die direkteste Arbeit nutzt eine RGB-Industriekamera über einem Förderband und 3.455 Originalbilder mit Kartoffeln, Steinen, Erdkluten und Mischszenen. YOLOv10n-PB erreichte nach einem 8:1:1-Split 98,9 % mAP@0.5; ein Systemtest mit 120 Objekten ergab 98,3 % Gesamtsortiergenauigkeit. Limitationen sind Dunkelbox, konstante Beleuchtung, definierte Objektabstände, nur 25 Steine im Systemtest und keine Kartoffeldefekte.

### [2] Li et al. (2025): Defekte auf einer Kartoffel-Sortierlinie

[Improved YOLO v5s-based detection method for external defects in potato](https://doi.org/10.3389/fpls.2025.1527508)

Auf 1.804 RGB-Bildern wurden healthy, greening, sprouting, scab, mechanical damage und rot erkannt. Das verbesserte YOLOv5s erreichte 85,1 % mAP, 86,6 % Recall und 30,7 FPS; zusätzlich wurden 150 gezielt ausgewählte Kartoffeln auf der Linie geprüft. Der zufällige Bildsplit, fehlende Steine und die künstlich zusammengesetzte Klassenverteilung begrenzen die Vergleichbarkeit.

### [3] Wang und Xiao (2021): Out-of-Sample-Prüfung

[Potato Surface Defect Detection Based on Deep Transfer Learning](https://doi.org/10.3390/agriculture11090863)

SSD, Faster R-CNN und R-FCN wurden auf 2.770 Bildern einzelner normaler, künstlich zerkratzter und gekeimter Kartoffeln getestet. Besonders wertvoll ist ein zusätzlicher Test mit 642 Kartoffeln aus einem anderen Markt und variierter Beleuchtung. Die sehr hohen Accuracy-Werte stammen jedoch aus ausgewogenen Einzelobjektbildern und sind keine COCO-mAP-Werte.

### [4] Zhu et al. (2025): Mehrseitiges Hochdurchsatzsystem

[Real-time detection method for potato surface defects based on YOLOv11-MML](https://doi.org/10.11975/j.issn.1002-6819.202504149)

YOLOv11-MML wurde in ein Zweikanalsystem mit Wendevorrichtung integriert. Berichtet werden 96,7 % mAP, 171,3 FPS, zwölf Kartoffeln pro Sekunde und 94,0 % Klassifikationsgenauigkeit. Das System zeigt den Nutzen mehrseitiger Sicht; die zugängliche englische Darstellung enthält aber zu wenige Split- und Prävalenzdetails für einen fairen Zahlenvergleich.

### [5] Yang et al. (2023): Multispektrale Defekterkennung

[Automatic detection of multi-type defects on potatoes using multispectral imaging](https://doi.org/10.1016/j.jfoodeng.2022.111213)

Ein 25-Band-System erfasste 428 Kartoffeln mit fünf Defekttypen; 128 Kartoffeln bildeten den Test. MDDNet erreichte 90,26 % mAP bei etwa 75 ms pro Bild. Wegen der zusätzlichen Spektralinformation und 409×216 Pixeln ist dies keine direkte RGB-Baseline.

### [6] Al-Mallahi et al. (2010): Kartoffel–Erdkluten-Trennung

[Detection of potato tubers using an ultraviolet imaging-based machine vision system](https://doi.org/10.1016/j.biosystemseng.2009.11.004)

Auf 1.171 Harvester-Videoframes wurden 2.233 Kartoffeln und 1.457 Erdkluten segmentiert. Berichtet werden 98,79 % beziehungsweise 98,28 % erfolgreiche Erkennung bei rund 94 ms pro Frame. Das UV-Verfahren nutzt Kontrast, der einer RGB-Kamera nicht zur Verfügung steht.

### [7] Korchagin et al. (2021): Reale Förderbandstörungen

[Development of an Optimal Algorithm for Detecting Damaged and Diseased Potato Tubers Moving along a Conveyor Belt](https://doi.org/10.3390/agronomy11101980)

Untersucht wurden ein 800-mm-Band bei bis zu 1 m/s, 4K-Kamera und gepulste Beleuchtung. Die Arbeit dokumentiert Überdeckung, Schmutz, Mehrfacherfassung und den Zielkonflikt zwischen Geschwindigkeit und Bewegungsunschärfe. Unklare Testtrennung und uneinheitliche Metriken verhindern die Nutzung als belastbare Modellbaseline.

### [8] Wosner et al. (2021): Agrarobjekte unter Überdeckung

[Object detection in agricultural contexts](https://doi.org/10.1016/j.compag.2021.106404)

Sieben RGB-Agrardatensätze wurden mit Mask R-CNN, RetinaNet und EfficientDet untersucht. Kleine Objekte, Größenvariation und Überdeckung waren zentrale Fehlerursachen; eine explizite Mehrfachauflösung verbesserte die meisten Aufgaben. Daraus folgt, Dichte, Überdeckung und Objektgröße als eigene Testslices auszuweisen.

### [9] Allmendinger et al. (2025): YOLO versus RT-DETR

[Assessing the capability of YOLO- and transformer-based object detectors for real-time weed detection](https://doi.org/10.1007/s11119-025-10246-0)

Auf 5.611 realen Feldbildern wurden YOLOv8–v10 und RT-DETR mit gemeinsamen Splits und fünf Trainings-/Validierungsfaltungen verglichen. YOLOv9e erreichte im Fünfklassen-Setting 79,86 % mAP50 und 72,36 % Recall, RT-DETR-l die höchste mittlere Precision von 81,46 %; kleine YOLOs waren am schnellsten. Die Autoren räumen ein, dass dieselbe Pflanze in verschiedenen Wachstumsstadien Splitgrenzen überschreiten kann.

### [10] Robinson et al. (2026): RF-DETR-Primärquelle

[RF-DETR: Neural Architecture Search for Real-Time Detection Transformers](https://openreview.net/forum?id=qHm5GePxTh)

RF-DETR verbindet einen vortrainierten Vision Transformer mit einer DETR-artigen Architektur und Architecture Search. RF-DETR-Nano erreicht 48,0 COCO AP; größere Varianten liefern starke Accuracy-Latency-Pareto-Punkte. Daraus folgt jedoch keine garantierte Überlegenheit auf kleinen Kartoffeldatensätzen.

### [11] David et al. (2021): Domänenvielfalt

[Global Wheat Head Detection 2021](https://doi.org/10.34133/2021/9846158)

GWHD 2021 umfasst 6.422 RGB-Bilder und rund 275.000 Bounding Boxes aus mehreren Ländern, Institutionen, Jahren und Aufnahmeplattformen. Konsistente Teilmengen werden als eigene Domänen behandelt. Für das Projekt entsprechen Liefercharge, Aufnahmelauf und Tag solchen Domänen.

### [12] Roberts et al. (2017): Strukturierte Splits

[Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure](https://doi.org/10.1111/ecog.02881)

Zufällige Cross-Validation kann bei abhängigen Beobachtungen den Vorhersagefehler deutlich unterschätzen. Der Split sollte die spätere Generalisierungsfrage abbilden. Daher müssen zusammengehörige Frames, Arrangements und Chargen innerhalb genau eines Splits bleiben.

### [13] Ghiasi et al. (2021): Copy-Paste

[Simple Copy-Paste Is a Strong Data Augmentation Method](https://doi.org/10.1109/CVPR46437.2021.00294)

Copy-Paste verbesserte auf COCO eine starke Baseline um 1,5 Box-AP und half besonders bei seltenen LVIS-Kategorien. Für Kartoffeln müssen Größe, Schatten, Kontakt und Überdeckung plausibel bleiben. Steine eignen sich besser für maskenbasiertes Copy-Paste als frei schwebende Defektpatches.

### [14] Hartley und French (2021): Synthetische Agrardaten

[Domain Adaptation of Synthetic Images for Wheat Head Detection](https://doi.org/10.3390/plants10122633)

Mehr als 5.000 gerenderte Bilder wurden mit realen Weizenbildern kombiniert. Die beste Real-plus-Synthetic-Variante verbesserte die Lokalisierungsmaße um knapp 5 %, während unkontrollierte GANs Objekte hinzufügten oder entfernten. Synthetische Daten können reale Trainingsdaten ergänzen, aber keinen realen Test ersetzen.

### [15] Saito und Rehmsmeier (2015): Imbalanced Evaluation

[The Precision-Recall Plot Is More Informative than the ROC Plot](https://doi.org/10.1371/journal.pone.0118432)

PR-Kurven bilden die Leistung einer seltenen positiven Klasse aussagekräftiger ab als ROC-Kurven oder globale Accuracy. Für `stone` und `defective_potato` sind daher eigene PR-Kurven, AP, Recall und Precision notwendig.

## B. Literaturmatrix

| Quelle | Umgebung/Sensor | Aufgabe und Größe | Split | Modell/Metrik | Hauptergebnis und Limitation |
|---|---|---|---|---|---|
| [1] Wang 2026 | RGB, Top-view-Laborband | potato/stone/clod; 3.455 Bilder | 8:1:1, Augmentation nur Train | YOLOv10n-PB; mAP50 und Systemmetriken | 98,9 % mAP50; kontrollierte Abstände und nur 25 Steine im Systemtest |
| [2] Li 2025 | RGB-CCD, Rollenlinie | sechs Kartoffelzustände; 1.804 Bilder | zufällig 3:1:1 | YOLOv5s; P/R/F1/mAP/FPS | 85,1 % mAP; keine Steine, kein Group Split |
| [3] Wang/Xiao 2021 | RGB, Einzelobjekte | normal/scratch/sprout; 2.770 Bilder plus 642 OOS-Kartoffeln | 3:1 plus neues Markt-Batch | SSD, Faster R-CNN, R-FCN; Accuracy/F1/FPS | nützlicher OOS-Test; künstliche Defekte und ausgewogene Klassen |
| [4] Zhu 2025 | RGB, Zweikanal/Wendemechanik | mehrere Defekttypen; N nicht ausreichend berichtet | nicht ausreichend berichtet | YOLOv11-MML; mAP/FPS/System-Accuracy | 12 Kartoffeln/s; andere Hardware und unklare Datensatzdetails |
| [5] Yang 2023 | 25-Band-MSI | fünf Defekte; 428 Kartoffeln | 128 Testkartoffeln | MDDNet; mAP/Zeit | 90,26 % mAP; nicht RGB |
| [6] Al-Mallahi 2010 | UV, Harvesterband | tuber/clod; 1.171 Frames, 3.690 Objekte | videobasierter Test | Schwellenwertsegmentierung | sehr hohe Raten; UV und binäre Aufgabe |
| [7] Korchagin 2021 | RGB, 1-m/s-Band | Tuber- und Defekterkennung | unabhängiger Split unklar | klassische Merkmale, SVM und CNN | dokumentiert Blur/Overlap/Dirt; Metrikqualität schwach |
| [8] Wosner 2021 | RGB, Feld/Obstgarten | sieben Agrardatensätze | datensatzspezifisch | Mask R-CNN, RetinaNet, EfficientDet | Scale und Occlusion zentrale Fehlerquellen |
| [9] Allmendinger 2025 | RGB-Feldbilder | 16 Arten bzw. fünf Gruppen; 5.611 Bilder | 68/17/15 plus 5-fold Train/Val | YOLOv8–10, RT-DETR; mAP50/95, Latenz | Modellranking hängt von Precision, Recall und Hardware ab |
| [10] Robinson 2026 | generische RGB-Benchmarks | COCO/RF100-VL | offizielle Splits | RF-DETR; COCO AP/Latenz | methodische Primärquelle, keine Kartoffelevidenz |
| [11] David 2021 | RGB, mehrere Länder/Plattformen | 6.422 Bilder, ca. 275.000 Ähren | Domänenmetadaten/OOD-Splits | Dataset-Benchmark | Vorlage für chargen-/laufbasierte Domänen |
| [12] Roberts 2017 | strukturierte Daten | methodische Arbeit | Block-/Group-CV | Vorhersagefehler | begründet Sequence Splitting |
| [13] Ghiasi 2021 | COCO/LVIS-RGB | Instance Segmentation/Detection | offizielle Splits | Copy-Paste; Box-/Mask-AP | Rare-Class-Gewinne; Agrarkontext nicht garantiert |
| [14] Hartley 2021 | reales und synthetisches RGB | >5.000 synthetische Bilder; realer Test mit 100 Bildern | reale Benchmark-Splits | Mask R-CNN/CycleGAN | Nutzen möglich, aber Artefakte und kleiner Test |
| [15] Saito 2015 | imbalanced classification | mehrere Simulationen/Datensätze | experimentelle Vergleiche | PR versus ROC | begründet klassenweise PR-Auswertung |

Zusätzlich bemerkenswert: [Wu et al. 2025](https://doi.org/10.3390/agronomy15040875) augmentierten 900 Originalbilder zunächst durch Spiegelung auf 2.700 Bilder und teilten erst danach zufällig 8:1:1. Dadurch können Varianten desselben Originals mehrere Splits erreichen – ein konkretes Beispiel für potenzielle Leakage.

## C. Synthese

### 1. Potato/food sorting

Die direkte Literatur bestätigt, dass RGB für sichtbare Defekte und mineralische Fremdkörper grundsätzlich geeignet ist. Sie zeigt zugleich, dass hohe Werte meist aus kontrollierten Einzelobjekt-, Dunkelbox- oder geordneten Förderbandbedingungen stammen. UV-, multispektrale und hyperspektrale Resultate dürfen nicht als erwartbare RGB-Leistung interpretiert werden.

Die reale Sortierleistung hängt außerdem von Bandgeschwindigkeit, Bewegungsunschärfe, Abstand, Tracking, Auswurfzeitpunkt und Defektsichtbarkeit ab. Detektions-mAP und physische Sortiergenauigkeit sind deshalb getrennt zu berichten.

### 2. Real-world agricultural detection

Überdeckung, Kontaktobjekte, kleine Defekte, ähnliche Farben und wechselnde Beleuchtung sind wiederkehrende Fehlerquellen. Diese Bedingungen sollten als annotierte Testslices behandelt werden:

- Belegungsdichte und Überdeckungsgrad
- Bewegungsunschärfe
- Verschmutzung beziehungsweise Erdbedeckung
- Beleuchtung
- Objekt- und Defektgröße
- Defektschwere
- Ähnlichkeit von Stein und Kartoffel

### 3. YOLO versus DETR

Die Evidenz unterstützt keine pauschale Rangfolge. In [9] hatte RT-DETR Vorteile bei Precision, größere YOLOs bei Recall/mAP und kleine YOLOs bei Latenz. Der Vergleich sollte deshalb sowohl task-level als auch unter einem gemeinsamen Ressourcenbudget erfolgen.

Alle Modelle benötigen dieselbe Dataset-Version, dieselben Splits und Testbilder. Latenz muss auf derselben Zielhardware einschließlich Resize, Datentransfer und Postprocessing gemessen werden.

### 4. Imbalance, augmentation und synthetische Daten

Nach Zusammenführung von `bad` und `cut` beträgt das aktuelle ungefähre Instanzverhältnis 14.464 : 1.285 : 732. Problematischer als dieses Verhältnis ist die interne Unterrepräsentation seltener Defekttypen; 30 `cut`-Instanzen erlauben keine belastbare subtype-spezifische Aussage.

Copy-Paste und synthetische Daten können helfen, müssen aber durch Real-only-Ablationen geprüft werden. Augmentation erfolgt ausschließlich nach dem Split und nur im Training. Validation, Operational Test und Challenge Set bleiben vollständig real und unverändert.

## Prüfung der Forschungslücke

Die Literatur deckt bereits ab:

- RGB-YOLO-Systeme für Kartoffeldefekte auf Sortierlinien;
- RGB-YOLO-Systeme für Kartoffeln, Steine und Erdkluten;
- UV- und multispektrale Kartoffelinspektion;
- YOLO–RT-DETR-Vergleiche in realen Agrarfeldern;
- RF-DETR als peer-reviewte Echtzeit-Transformerfamilie.

Nicht gemeinsam gezeigt wurde:

1. feste RGB-Einzelkamera;
2. dicht belegte, nicht manuell vorselektierte Mischbilder;
3. `good_potato` / `defective_potato` / `stone`;
4. fairer YOLO/CNN–RF-/RT-DETR-Vergleich;
5. gruppen- oder sequenzbasierter Split;
6. Operational Test mit natürlicher Prävalenz;
7. separat ausgewiesener Rare-Case-Test.

Empfohlene Formulierung:

> Existing studies demonstrate RGB-based potato defect detection and, more recently, dynamic separation of potato tubers from stones and soil clods. However, the available evidence is dominated by controlled acquisition, staged or balanced samples, image-level random splits, and evaluations within a single detector family. We found limited peer-reviewed evidence comparing compact CNN/YOLO and real-time transformer detectors on densely populated RGB conveyor images of unsorted potatoes while preserving operational class prevalence and reporting a separate rare-case evaluation.

Im Paper sollte „to the best of our literature search up to June 2026“ ergänzt werden.

## D. Related-Work-Entwurf

> Automated potato inspection has been studied using color, ultraviolet, multispectral, and hyperspectral imaging. Ultraviolet reflectance enabled tuber–clod separation on a harvester conveyor, but relies on spectral contrast unavailable to a standard RGB camera [6]. More recent multispectral work detected five potato-defect types using a compact detector [5], again using information that is not directly comparable to RGB-only inspection.
>
> RGB studies increasingly formulate potato quality control as object detection. Wang and Xiao compared SSD, Faster R-CNN, and R-FCN on normal, scratched, and sprouted potatoes and, importantly, added an out-of-sample batch collected from another market [3]. Li et al. evaluated an improved YOLOv5s model on images acquired from a potato grading line, covering six surface conditions [2]. Zhu et al. integrated a lightweight YOLOv11 variant into a multi-view conveyor system [4]. Most directly, Wang et al. developed a top-view RGB system for separating potato tubers from stones and soil clods and jointly evaluated visual recognition and pneumatic rejection [1]. However, these studies predominantly used controlled illumination, staged samples, constrained object spacing, balanced or manually selected class compositions, or image-level random splits. Their reported scores therefore cannot be transferred directly to densely populated, naturally composed conveyor streams.
>
> Related agricultural detection research identifies occlusion, small targets, scale variation, background similarity, and illumination changes as major failure modes [8]. The Global Wheat Head Dataset further demonstrates the importance of acquisition-domain diversity across locations, years, sensors, and growth stages [11]. For temporally or hierarchically structured data, random cross-validation may underestimate prediction error; blocking by the intended unit of generalization is therefore recommended [12]. In conveyor video, this implies keeping complete recording runs, arrangements, or delivery lots within a single split.
>
> Evidence comparing convolutional and transformer detectors in agriculture remains limited. A field study of YOLOv8–v10 and RT-DETR found that model rankings depended on the target criterion: RT-DETR achieved high precision, larger YOLO variants achieved stronger recall or mAP, and small YOLO variants provided the lowest latency [9]. RF-DETR reports competitive accuracy–latency trade-offs on generic multi-domain benchmarks [10], but has not established superiority for potato conveyor imagery.
>
> Class imbalance should be addressed without changing the operational test distribution. Copy-Paste can improve rare-category detection [13], while agricultural synthetic-data studies show both potential gains and risks from domain gap and generated artifacts [14]. Accordingly, augmentation should be applied only to training data and evaluated on unchanged real images. Evidence remains limited for a grouped, prevalence-preserving comparison of compact YOLO/CNN and real-time transformer detectors on dense RGB images of unsorted potatoes, complemented by a separately reported rare-case challenge set.

## E. Quellen für das finale Paper

Kernset:

1. Wang et al. 2026 [1] – direkteste Stone-/Conveyor-Arbeit.
2. Li et al. 2025 [2] – direkte RGB-Defektarbeit.
3. Wang und Xiao 2021 [3] – OOS-Evaluation.
4. Wosner et al. 2021 [8] – Occlusion, Scale und Metriken.
5. Allmendinger et al. 2025 [9] – YOLO–RT-DETR-Vergleich.
6. Robinson et al. 2026 [10] – offizielle RF-DETR-Quelle.
7. Roberts et al. 2017 [12] – Group Splitting.

Falls tatsächlich verwendet:

8. Ghiasi et al. 2021 [13] – Copy-Paste.
9. Hartley und French 2021 [14] – synthetische Daten und Domain Gap.

Bei extremem Platzmangel können [3] und [14] entfallen.

## F. Konsequenzen für das Experimentdesign

### Zielpopulation

Alle sichtbaren Objekte auf der späteren, noch nicht manuell vorsortierten Förderbandstufe – über relevante Sorten, Chargen, Bodenfeuchte, Verschmutzung, Bandgeschwindigkeit und Belegungsdichte hinweg.

`defective_potato` sollte nur visuell erkennbare, ausschleuserelevante Defekte umfassen. Ein Defekt auf der nicht sichtbaren Unterseite darf einer Einzelkamera nicht als Miss angelastet werden.

`bad` und `cut` können zusammengeführt werden, wenn sie dieselbe Betriebsentscheidung auslösen. Der ursprüngliche Defektsubtyp sollte als Metadatum erhalten bleiben.

### Datenerhebung

Fortlaufende, nicht vorselektierte Produktionsblöcke aufnehmen und dokumentieren:

- `sequence_id`, Datum und Charge
- Sorte und Feld/Lieferant
- Boden- beziehungsweise Feuchtezustand
- Bandgeschwindigkeit und Belegungsdichte
- Licht- und Kamerakonfiguration
- Reinigung beziehungsweise Vorseparation

Zusätzlich reale leere Bandframes und typische Nichtzielobjekte sammeln.

### Split

Alle benachbarten Frames, dieselbe physische Anordnung und möglichst dieselbe Charge bleiben in genau einem Split. Beispielsweise:

- 70 % Aufnahmegruppen Training
- 15 % Validation
- 15 % Development Test
- finaler Operational Test aus später aufgenommenen Chargen

Augmentation, Oversampling und Copy-Paste erfolgen erst nach dem Split.

### Operational Test

- fortlaufende natürliche Produktion
- unveränderte Klassenprävalenz
- keine Auswahl besonders einfacher oder schwieriger Frames
- primäre Quelle für reale Precision und Fehler pro 1.000 Objekte

### Rare-Case Challenge Set

Separat anreichern mit:

- seltenen Defekttypen
- Steinen und visuell ähnlichen Erdkluten
- starker Verschmutzung
- Kontakt und Überdeckung
- hoher Dichte
- Bewegungsunschärfe
- ungünstiger Beleuchtung

Challenge- und Operational-Ergebnisse dürfen nicht zu einer gemeinsamen mAP vermischt werden.

### Statistische Mindestmengen

Folgende Werte sind ausdrücklich Faustregeln unter vereinfachter unabhängiger Binomialannahme:

- Bei erwartetem Recall von 90 %: ungefähr 139 unabhängige positive Fälle für eine approximative 95-%-Genauigkeit von ±5 Prozentpunkten.
- Konservativ: ungefähr 385 unabhängige Fälle für ±5 Prozentpunkte bei unbekanntem Anteil.
- Bei null beobachteten Fehlern liegt die obere 95-%-Fehlergrenze näherungsweise bei `3/n` („rule of three“; [Hanley und Lippman-Hand](https://doi.org/10.1001/jama.1983.03330370053031)).

Empfehlung:

- 150–200 reale `stone`-Instanzen im Operational Test
- 150–200 reale `defective_potato`-Instanzen
- mindestens fünf unabhängige Aufnahmegruppen
- zusätzlich 100–150 Instanzen je kritischer Klasse im Challenge Set

Bei der aktuellen Stone-Prävalenz von etwa 4,4 % wären grob 3.400 natürliche Objekte nötig, um 150 Steine zu beobachten.

Da Boxen innerhalb derselben Sequenz korreliert sind, sollten Konfidenzintervalle per Cluster-Bootstrap über Sequenzen oder Chargen berechnet werden.

### Modellvergleich

Mindestens:

- YOLO11 Nano
- RF-DETR Small
- RF-DETR Medium
- optional ein zweites YOLO-Größenniveau

Regeln:

- eine eingefrorene Dataset-Version
- identische Splits und Annotationen
- dokumentiertes Pretraining
- vergleichbares Tuningbudget
- möglichst drei Seeds
- Schwellenwertwahl nur auf Validation
- Test erst nach Festlegung aller Konfigurationen
- End-to-End-Latenz p50/p95/p99 auf derselben Hardware

Die bisherigen Roboflow-Werte sind nur Vorversuche, solange Dataset-Version, Split und Klassenmapping nicht identisch sind.

### Augmentation

Konservative Standardaugmentation:

- Rotation und Spiegelung
- moderate Skalierung und Translation
- begrenzter Helligkeits-/Kontrast-/HSV-Jitter
- realistische Bewegungsunschärfe entlang der Bandrichtung
- Mosaic/MixUp nur als Ablation

Copy-Paste:

- Segmentmasken statt Rechtecken
- plausible Größe, Schatten und Überdeckung
- Steine auf reale Bandhintergründe
- Defektpatches nur auf Kartoffeloberflächen
- keine Quellen aus Validation oder Test

Synthetische Daten:

- ausschließlich Training
- Artefakt- und Labelprüfung
- Dosisstudie, etwa 0/25/50/100 %
- Anerkennung eines Nutzens nur auf unveränderten realen Tests

### Kennzahlen

Detection:

- AP50 und AP50–95 je Klasse
- Macro-mAP und Einzel-AP
- klassenweise PR-Kurven
- Precision, Recall und F1 am gewählten Betriebspunkt
- Konfusionsmatrix
- Condition-Slices

Betrieb:

- Stone-Recall beziehungsweise missed-stone rate
- Defect-Recall
- False-Reject-Rate guter Kartoffeln
- Fehler pro 1.000 Objekte
- End-to-End-Latenz und stabiler Durchsatz
- Detektions- und physische Ausschleusleistung getrennt

## G. Offene Fragen

Mit dem Landwirt klären:

1. Exakte Prozessstufe vor oder nach Reinigung/Vorseparation?
2. Zählen Erdkluten zu `stone`?
3. Welche weiteren Fremdobjekte treten auf?
4. Welche Defekttypen und Schweregrade sind ausschleuserelevant?
5. Ist `cut` ein natürlicher Schaden oder überwiegend inszeniert?
6. Welche Sorten, Felder, Böden und Jahreszeiten müssen abgedeckt werden?
7. Wie hoch sind natürliche Klassenprävalenzen pro Charge?
8. Welche Dichte, Überdeckung und Bandgeschwindigkeit treten real auf?
9. Wie werden übersehener Stein und falsch ausgeworfene Kartoffel kostenmäßig gewichtet?
10. Soll nur sichtbare Oberflächenqualität beurteilt werden?
11. Welche Zielhardware und maximale End-to-End-Latenz gelten?
12. Ist später eine Wendevorrichtung oder zweite Kamera möglich?

Durch neue Daten zu beantworten:

- Prävalenzschwankung zwischen Chargen
- Anteil erdbedeckter Kartoffeln
- Verteilung von Dichte und Überdeckung
- Häufigkeit einzelner Defektsubtypen
- Domain Shift zwischen Tagen und Sorten
- Labelübereinstimmung zwischen Annotierenden
- Anteil aus einer Einzelansicht nicht entscheidbarer Fälle

## H. BibTeX

```bibtex
@article{wang2026potatoimpurities,
  author  = {Wang, Qian and Chen, Ke and Li, Qiying and Xu, Qiuying and Deng, Weigang},
  title   = {Deep Learning-Based Intelligent Sorting of Potato Tubers and Mineral Impurities: System Development and Experimental Evaluation},
  journal = {Foods},
  year    = {2026},
  volume  = {15},
  number  = {12},
  pages   = {2070},
  doi     = {10.3390/foods15122070}
}

@article{li2025potatodefects,
  author  = {Li, XiLong and Wang, FeiYun and Guo, Yalin and Liu, Yijun and Lv, HuangZhen and Zeng, Fankui and Lv, Chengxu},
  title   = {Improved {YOLO} v5s-based detection method for external defects in potato},
  journal = {Frontiers in Plant Science},
  year    = {2025},
  volume  = {16},
  pages   = {1527508},
  doi     = {10.3389/fpls.2025.1527508}
}

@article{wang2021potatotransfer,
  author  = {Wang, Chenglong and Xiao, Zhifeng},
  title   = {Potato Surface Defect Detection Based on Deep Transfer Learning},
  journal = {Agriculture},
  year    = {2021},
  volume  = {11},
  number  = {9},
  pages   = {863},
  doi     = {10.3390/agriculture11090863}
}

@article{wosner2021agriculturaldetection,
  author  = {Wosner, Omer and Farjon, Guy and Bar-Hillel, Aharon},
  title   = {Object detection in agricultural contexts: A multiple resolution benchmark and comparison to human},
  journal = {Computers and Electronics in Agriculture},
  year    = {2021},
  volume  = {189},
  pages   = {106404},
  doi     = {10.1016/j.compag.2021.106404}
}

@article{allmendinger2025yolodetr,
  author  = {Allmendinger, Alicia and Saltik, Ahmet Oguz and Peteinatos, Gerassimos G. and Stein, Anthony and Gerhards, Roland},
  title   = {Assessing the capability of {YOLO}- and transformer-based object detectors for real-time weed detection},
  journal = {Precision Agriculture},
  year    = {2025},
  volume  = {26},
  number  = {3},
  pages   = {52},
  doi     = {10.1007/s11119-025-10246-0}
}

@inproceedings{robinson2026rfdetr,
  author    = {Robinson, Isaac and Robicheaux, Peter and Popov, Matvei and Ramanan, Deva and Peri, Neehar},
  title     = {{RF-DETR}: Neural Architecture Search for Real-Time Detection Transformers},
  booktitle = {International Conference on Learning Representations},
  year      = {2026},
  url       = {https://openreview.net/forum?id=qHm5GePxTh}
}

@article{roberts2017structuredcv,
  author  = {Roberts, David R. and Bahn, Volker and Ciuti, Simone and Boyce, Mark S. and Elith, Jane and Guillera-Arroita, Gurutzeta and Hauenstein, Severin and Lahoz-Monfort, Jose J. and Schroder, Boris and Thuiller, Wilfried and Warton, David I. and Wintle, Brendan A. and Hartig, Florian and Dormann, Carsten F.},
  title   = {Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure},
  journal = {Ecography},
  year    = {2017},
  volume  = {40},
  number  = {8},
  pages   = {913--929},
  doi     = {10.1111/ecog.02881}
}

@inproceedings{ghiasi2021copypaste,
  author    = {Ghiasi, Golnaz and Cui, Yin and Srinivas, Aravind and Qian, Rui and Lin, Tsung-Yi and Cubuk, Ekin D. and Le, Quoc V. and Zoph, Barret},
  title     = {Simple Copy-Paste Is a Strong Data Augmentation Method for Instance Segmentation},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  year      = {2021},
  pages     = {2918--2928},
  doi       = {10.1109/CVPR46437.2021.00294}
}

@article{hartley2021syntheticwheat,
  author  = {Hartley, Zane K. J. and French, Andrew P.},
  title   = {Domain Adaptation of Synthetic Images for Wheat Head Detection},
  journal = {Plants},
  year    = {2021},
  volume  = {10},
  number  = {12},
  pages   = {2633},
  doi     = {10.3390/plants10122633}
}
```

## Abschließende Empfehlung

Der stärkste Beitrag für ein fünfseitiges IEEE-Paper ist kein weiterer isolierter mAP-Wert, sondern ein sauberer Nachweis unter drei getrennten Ebenen:

1. fairer Architekturvergleich auf identischem gruppenbasiertem Split;
2. Operational Test mit natürlicher Prävalenz und betriebsbezogenen Fehlerraten;
3. Rare-Case Challenge Set mit separat berichteter Robustheit.
