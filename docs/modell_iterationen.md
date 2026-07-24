# Modell-Iterationen & Design-Entscheidungen — Kartoffelsortierung

Dieses Dokument fasst die Verbesserungen und Design-Entscheidungen der YOLO-Modellentwicklung
für den Kartoffel-Sortierer zusammen — inklusive der Begründung für jede Entscheidung.

Klassen: `potato`, `stone`, `bad`, `cut`
Zielplattform: NVIDIA Jetson (daher Fokus auf kleine, schnelle Modelle)
Training: Google Colab (Tesla T4), Ultralytics YOLO, Datensatz via Roboflow

---

## 1. Ausgangslage (Iteration 1)

**Setup:** YOLOv8n, 50 Epochen, `imgsz=640`, Standard-Augmentierung, lineare LR.

**Ergebnis:**

| Metrik | Wert |
|---|---|
| mAP@50 (gesamt) | 0.636 |
| mAP@50-95 (gesamt) | ~0.53 |
| `potato` / `stone` mAP@50 | 0.994 / 0.977 |
| `bad` Recall (normiert) | 0.09 |
| `cut` Recall (normiert) | 0.25 |

**Diagnose:** Gute Kartoffeln und Steine wurden nahezu perfekt erkannt, aber die
**reject-kritischen Defektklassen `bad` und `cut` wurden praktisch übersehen**
(0.91 bzw. 0.75 als Hintergrund klassifiziert).

**Ursache:** Extreme Klassen-Unausgewogenheit — `potato` 23.504 Instanzen, `bad` 1.913,
`stone` 1.222, `cut` nur **46**. Das Problem war die **Datenlage**, nicht die Architektur.

---

## 2. Zentrale Erkenntnis: Augmentierung ≠ Klassenbalance

Standard-Augmentierung (Flip, HSV, Mosaic) **vervielfacht nur die vorhandenen wenigen
Objekte** — sie erzeugt keine neue Information über die Erscheinungsvielfalt von Defekten.
`mosaic=1.0` verdünnt seltene Klassen sogar zusätzlich. Deshalb waren gezielte Maßnahmen nötig.

---

## 3. Maßnahmen & Begründungen

### 3.1 Offline Copy-Paste-Augmentierung (Hauptmaßnahme für Defekte)
- **Was:** Echte `bad`/`cut`-Ausschnitte werden ausgeschnitten und in vielen Positionen,
  Größen und Rotationen (mit weichen Kanten) auf Trainingsbilder kopiert. Neue YOLO-Labels
  werden automatisch erzeugt.
- **Warum:** Erhöht die **Instanz- und Positionsvielfalt** der seltenen Klassen gezielt —
  der stärkste Hebel bei nur 46 `cut`-Instanzen. Wird nur auf das **Trainings-Set** angewendet
  (das Val-Set bleibt echt → saubere Methodik).
- **Verfeinerung (Iteration 4):** Gewichtung **bad:cut = 70:30**, da `bad` visuell deutlich
  variantenreicher ist als `cut` und mehr Beispiele braucht.

### 3.2 Zusätzliche echte, handgelabelte Daten
- **Was:** Passende öffentliche Bilder gesucht und **im Roboflow-Projekt selbst handgelabelt**
  (neue Datensatz-Version 8).
- **Warum:** Handlabeln stellt sicher, dass die **Klassen-IDs korrekt** zum eigenen Schema
  (`bad/cut/potato/stone`) passen — kein fehlerhaftes Remapping fremder Taxonomien.

### 3.3 Dynamische Lernrate (Cosine-Annealing)
- **Was:** `cos_lr=True` statt linearer LR-Abnahme.
- **Warum:** Konvergiert in den letzten Epochen sauberer/schneller. Die Trainingskurven
  zeigten, dass das Modell noch nicht auskonvergiert war.

### 3.4 `mixup=0.15`
- **Warum:** Mischt Bildpaare und hilft erfahrungsgemäß **Minderheitsklassen** (bad, cut).

### 3.5 `cls=0.7` (höheres Klassifikations-Gewicht)
- **Warum:** Legt mehr Gewicht auf die (schwierige) Klassifikation der harten Klassen.

### 3.6 Höhere Auflösung `imgsz=768`
- **Warum:** Defekte sind **kleine Objekte**; die Recall kleiner Objekte skaliert stark mit
  der Eingangsauflösung. Empfehlung: In Roboflow **"Fit" statt "Stretch"** exportieren,
  um die längliche Kartoffelform nicht zu verzerren.

### 3.7 Early Stopping großzügiger (`patience=20`, `epochs=100`)
- **Warum:** Iteration 2 stoppte bei Epoche 23, während die Recall noch stieg — zu früh.

---

## 4. Ergebnis-Verlauf der Iterationen

| Iteration | Wesentliche Änderung | mAP@50 | `bad` Recall | `cut` Recall | Early Stop |
|---|---|---|---|---|---|
| 1 | Baseline (YOLOv8n, 50 ep) | 0.636 | 0.09 | 0.25 | – |
| 2 | + handgelabelte Daten (v8); **cos_lr/mixup NICHT aktiv** | ~0.64 | 0.04 | 0.00 | ep 23 |
| 3 | + Copy-Paste + cos_lr + mixup **aktiv** (YOLOv8n) | **0.72** | **0.245** | **0.741** | ep 59 |
| 4 | Benchmark-Sieger **YOLO11s**, imgsz=768, cls=0.7, bad-gewichtetes Copy-Paste | **0.746** | **0.878** | **0.875** | ep 96 |

**Wichtigste Lektion (Iteration 3):** Die Copy-Paste-Augmentierung + aktivierte LR/mixup-Hebel
haben **`cut` von 0.00 auf 0.74 Recall** gebracht und `bad` etwa verdreifacht. Damit ist die
Kernhypothese bestätigt: Defekterkennung war ein **Daten-/Instanzproblem**.

**Wichtigste Lektion (Iteration 4):** Mit `YOLO11s` + höherer Auflösung + gezielter
Augmentierung stieg die **`bad`-Recall auf 0.878** (vorher 0.245) — der größte Sprung des
Projekts. Allerdings zu **Lasten der `bad`-Precision** (massive False Positives, siehe 5.2).

---

## 5. Modellvergleich (Iteration 4)

- **Was:** Mehrere Architekturen mit identischer Konfiguration im Benchmark:
  `yolov8n`, `yolov8s`, `yolo11n`, `yolo11s` (neuere Generation).
- **Warum:** Nachdem Nano auf der reicheren Datenbasis plateauartig auskonvergierte, könnte
  ihm schlicht **Kapazität** für die harten Klassen fehlen. `s`-Modelle und YOLO11 werden
  fair gegen die Baseline getestet.
- **Auswahlkriterium:** Sortierung nach **`bad`-Recall** (reject-kritischste Klasse), dann mAP@50.
- **Hinweis:** Auf einer einzelnen T4-GPU laufen die Modelle **nacheinander** (nicht echt
  parallel). Empfehlung: für einen schnellen Vergleich zunächst wenige Epochen, dann nur den
  Gewinner voll austrainieren.

### 5.1 Evaluierung zwischen den Trainings
- **Was:** Jedes Modell wird **direkt nach seinem Training** validiert, mit sofortiger
  Per-Klassen-Ausgabe und laufender Bestenliste.
- **Warum:** Frühes Feedback; defekte Läufe fallen sofort auf, statt erst nach Stunden.
  Die Vergleichszelle nutzt die gesammelten Ergebnisse weiter (keine doppelte Validierung).

### 5.2 Ergebnis-Detail: Sieger YOLO11s (Iteration 4)

**Konfiguration:** `yolo11s.pt`, `imgsz=768`, `epochs=100` (Early Stop bei **96**,
`patience=20`), `batch=0.85`, `cache=True`, `cos_lr=True`, `mixup=0.15`, `cls=0.7`, Datensatz v8.

**Per-Klassen-Auswertung (bestes Modell ≈ Epoche 76):**

| Klasse | #Val | Recall | AP@0.5 | ggü. Iteration 3 |
|---|---|---|---|---|
| `bad` | 49 | **0.878** | **0.441** | Recall 0.245 → 0.878 (**3.6×**), AP 0.214 → 0.441 |
| `cut` | 8 | **0.875** | 0.559 | Recall 0.741 → 0.875 |
| `potato` | 1504 | 0.995 | 0.995 | ~gleich |
| `stone` | 35 | 0.800 | 0.989 | Recall 1.00 → 0.80 (Regression) |
| **gesamt** | 1596 | — | **0.746** | mAP@0.5 0.72 → 0.746 |

**Trainingsdynamik:** glatte Konvergenz; bestes mAP@0.5:0.95 bei Epoche 76 (0.611). Der
scharfe Abfall des `train/box_loss` bei Epoche 91 (0.44 → 0.37) stammt von `close_mosaic=10`
(Mosaic wird für die letzten 10 Epochen deaktiviert). Rechenkosten: ~90 s/Epoche →
~2.4 h für dieses eine Modell (yolo11s + 768 px), vs. ~23 s/Epoche für die Nano-Baseline bei 640.

**Warum YOLO11s gewann:** Das Benchmark sortiert nach **`bad`-Recall**; die höhere Kapazität
gegenüber Nano half der visuell heterogenen `bad`-Klasse deutlich.

#### 5.2.1 ⚠️ Kritischer Trade-off: `bad`-Precision bricht ein
- Die **rohe** Konfusionsmatrix (Betriebspunkt conf=0.25) zeigt **1391 False-Positive-`bad`-Boxen**
  auf Hintergrundregionen (zusätzlich 167 `potato`, 109 `cut`, 57 `stone`). Damit liegt die
  `bad`-Precision am Standard-Betriebspunkt bei ≈ **0.03** — das Modell „ruft" überall `bad`.
- **Ursache:** `cls=0.7` + `mixup` + **70/30-Gewichtung des Copy-Paste zugunsten `bad`** haben
  das Modell zu sehr aggressiver `bad`-Vorhersage erzogen.
- **Kein hoffnungsloser Fall, sondern ein Schwellen-Problem:** Die PR-Kurve zeigt für `bad`
  eine Precision von ~0.9 bei niedriger Recall und ~0.5 um Recall 0.37–0.5. Ein brauchbarer
  Betriebspunkt existiert bei **höherem Confidence-Schwellenwert** (siehe Schwellen-Analyse, Abschnitt 6).
- **Konsequenz:** Recall allein ist irreführend; für die Bewertung/Deployment muss der
  **`bad`-Confidence-Schwellenwert bewusst gewählt** werden (Recall vs. Fehlauswurfrate).

#### 5.2.2 Regressionen / Vorbehalte
- **`stone`-Recall 1.00 → 0.80:** 7 von 35 Steinen werden als `potato` vorhergesagt — kleine,
  aber echte Regression (beobachten).
- **`cut` AP scheinbar gesunken (0.688 → 0.559):** bei nur **8** Val-Instanzen statistisches
  Rauschen; die Recall stieg.
- **Konfundiertes Experiment:** Iteration 4 änderte Modell (`yolo11s`), Auflösung (768),
  `cls` (0.7) und Copy-Paste-Gewichtung gleichzeitig → der `bad`-Sprung ist **keinem einzelnen
  Faktor** zuzuordnen (für eine saubere Ablation separat testen).

---

## 6. Evaluierungs-Strategie

- **Per-Klassen-Metriken statt nur Gesamt-mAP:** Die Gesamtwerte werden von `potato`/`stone`
  dominiert und **verschleiern** die schwache Defekterkennung. Eine explizite Tabelle je Klasse
  (inkl. Anzahl echter Val-Instanzen) macht `bad`/`cut` sichtbar.
- **Warnung bei zu kleinem Val-Set:** Bei < 30 echten Instanzen einer Defektklasse ist die
  Recall/mAP **statistisch unzuverlässig** (z. B. nur 8 echte `cut`-Instanzen). → Mehr echte
  Defekte auch ins **Val-Set** labeln (Ziel: ~30–50 je Klasse).
- **Schwellenwert-Analyse (Betriebspunkt):** Für einen Sorter ist eine **verpasste schlechte
  Kartoffel (False Negative) schlimmer als ein Fehlauswurf**. Precision/Recall über Confidence
  je Klasse zeigen, welcher Confidence-Schwellenwert das Ziel-Recall erreicht. Da YOLOs `conf`
  **global** ist, wird die klassenspezifische Feinsteuerung (z. B. `bad` niedrig) in der
  Nachverarbeitung umgesetzt (`code/jetson/vision/logic.py`).

---

## 7. Roboflow Preprocessing / Augmentierung — Hinweise

- **Resize „Stretch to 512x512"**: verzerrt die längliche Kartoffelform → besser **„Fit"**.
- **Auto-Adjust Contrast (Contrast Stretching)**: wird ins Training „eingebacken" → die
  **Jetson-Kamera-Pipeline muss dieselbe Vorverarbeitung** replizieren, sonst Domain-Mismatch.
- **„Outputs per training example: 3"** (inkl. 90°-Rotationen): vervielfacht **alle** Klassen
  gleichmäßig → ändert das Ungleichgewicht **nicht**.

---

## 8. Workflow & Infrastruktur

- **Ursache verzögerter Verbesserungen:** „Open in Colab" lädt das Notebook aus **GitHub**,
  nicht die lokale Kopie. Änderungen müssen daher **committet und gepusht** werden, bevor sie
  in Colab wirken. (Erklärte, warum cos_lr/mixup in Iteration 2 nicht aktiv waren.)
- **Sicherheit:** Der hartkodierte Roboflow-API-Key wurde entfernt und durch **Colab-Secrets**
  (`userdata.get('ROBOFLOW_API_KEY')`) ersetzt. Der bereits exponierte Key sollte **rotiert**
  werden (öffentliche Git-Historie).

### 8.1 GPU-Auslastung / Ressourcennutzung
- **Beobachtung:** Während des Iteration-4-Benchmarks war die T4 unterausgelastet
  (~4.6/15 GB GPU-RAM, ~31 %). Ursache: `batch=-1` (AutoBatch) zielt nur auf **~60 %**
  GPU-RAM, und die Nano-Modelle sind sehr klein.
- **Maßnahmen:**
  - `batch=0.85` — AutoBatch als **Bruchteil** zielt auf ~85 % GPU-RAM → größere Batches,
    bessere Durchsatzrate (v. a. die `s`-Modelle profitieren).
  - `cache=True` — Bilder in RAM/Disk cachen (Reserven vorhanden) → schnelleres Laden,
    I/O ist kein Flaschenhals mehr.
- **Grenzen:** Bei den winzigen Nano-Modellen ist oft die **Compute**-Leistung (nicht der
  Speicher) der Flaschenhals — sie füllen die GPU-RAM ggf. trotzdem nicht. Und auf **einer**
  GPU bleiben die Modelle **sequenziell**; echte Parallelität bräuchte mehrere GPUs.

---

## 9. Offene Punkte / Nächste Schritte

- [ ] Mehr echte `bad`- und besonders `cut`-Bilder labeln (Train **und** Val).
- [ ] Val-Set auf ~30–50 echte Instanzen je Defektklasse bringen (verlässliche Metriken).
- [ ] Roboflow-Export auf **„Fit"** umstellen; ggf. native/höhere Auflösung.
- [x] Iteration-4-Benchmark ausgewertet → Sieger **YOLO11s** (bad-Recall 0.878).
- [ ] **`bad`-Precision-Problem lösen:** Betriebspunkt/Confidence-Schwelle für `bad` bewusst
      wählen (1391 False Positives bei conf=0.25); ggf. Copy-Paste-Gewichtung entschärfen.
- [ ] `stone`-Regression (Recall 0.80) im Auge behalten.
- [ ] Klassenspezifische Confidence-Schwellen in der Jetson-Nachverarbeitung umsetzen.
- [ ] Gewinner-Modell für den Jetson exportieren (z. B. TensorRT/FP16).
- [ ] Sicherstellen, dass die Jetson-Vorverarbeitung das Roboflow-Preprocessing repliziert.
