# Bisherige Vorarbeiten: Datensammlung und Erste Schritte

## 1. Hintergrund und Motivation
**Der Weg der Kartoffel:**
Die Kartoffeln werden auf dem Feld mit einer Erntemaschine aus der Erde geholt, wobei direkt auf der Maschine eine erste grobe Sortierung stattfindet. In der Verarbeitungshalle angekommen, durchlaufen sie eine Rüttel- und Sortiermaschine, welche die Ernte in drei verschiedene Größenklassen unterteilt. 

**Das aktuelle Problem:**
An dieser Station stehen derzeit bis zu vier Personen an den Bändern, deren Aufgabe es ist, schlechte Kartoffeln, Steine und Dreck manuell auszusortieren. Die verbleibenden guten Kartoffeln werden anschließend im Kühlhaus eingelagert. Wenn sie später je nach Kundenbedarf verpackt und verschickt werden, erfolgt vor dem Verpacken noch eine weitere manuelle Kontrollstufe. Dieser Prozess ist aktuell enorm personal- und zeitintensiv.

**Zielsetzung des Projekts:**
Um diesen Personalbedarf zu reduzieren, soll der Sortierprozess automatisiert werden. Ein Kamerasystem soll die schlechten Kartoffeln sowie Fremdkörper (wie Steine) automatisch erkennen, um sie auszusortieren.

## 2. Projektkontext und Maschinenaufbau
- **Aufbau der Maschine:** Die Anlage nutzt ein Förderband mit rotierenden Rollen. Dadurch drehen sich die Kartoffeln während des Vorwärtstransports, sodass das Kamerasystem sie von allen Seiten erfassen kann.
- **Saisonale Unterschiede:**
  - **Sommer:** Die Kartoffeln kommen relativ sauber aus dem Kühlhaus. Der Fokus dieses Projekts liegt auf der Automatisierung der finalen Qualitätskontrolle beim Auslagern/Verpacken in dieser Phase.
  - **Herbst (Erntezeit):** Die frischen Kartoffeln direkt aus der Erde sind deutlich dreckiger, oft durch die Erntemaschine beschädigt und von vielen Erdklumpen begleitet. Dieser erschwerte Anwendungsfall ist ausdrücklich **nicht** Thema der aktuellen Arbeit.
- **Klassifizierung:** Die Bilderkennung konzentriert sich auf die Erkennung von Kartoffeln (`potato`), spezifischen Defekten (`bad`) und Fremdkörpern (`stone`).

## 3. Setup zur Bildakquise
- **Kamera-Setup:** Erste Tests wurden mit einer handelsüblichen Webcam durchgeführt, die an ein MacBook angeschlossen war.
- **Aufnahmeintervall:** Alle 0,5 Sekunden wurde automatisiert ein Bild ausgelöst und gespeichert.
- **Umgebungsbedingungen:**
  - Das Förderband wurde gut ausgeleuchtet.
  - Die Bandgeschwindigkeit wurde so langsam wie möglich eingestellt, um die Bildqualität zu maximieren.

## 4. Erste Erkenntnisse und Herausforderungen
- **Probleme bei der Fehlererkennung:** Es fiel auf, dass die Webcam spezifische Defekte wie schrumpelige Kartoffeln nicht gut abbilden und erkennen lässt.
- **Ursachen:** Die Auflösung der Webcam ist zu gering. Zudem führt die zu hohe Belichtungszeit/Verschlusszeit der Kamera bei den sich bewegenden Kartoffeln zu leicht verschwommenen Bildern (Motion Blur).
- **Lösungsansatz:** Für den zukünftigen Betrieb wird der Einsatz einer professionellen Industriekamera (vorzugsweise mit Global Shutter und höherer Auflösung) empfohlen, was voraussichtlich Abhilfe schaffen würde.

## 5. Datenverarbeitung und Modelltraining in Roboflow
- **Upload & Datensatz:** Alle gesammelten Bilder wurden in die Plattform **Roboflow** hochgeladen. Der finale Datensatz auf der Plattform umfasst:
  - **772 Bilder** (Median Auflösung: 1920x1080)
  - **16.427 Annotations** insgesamt (im Durchschnitt 21,3 Bounding Boxes pro Bild)
  - **Klassenverteilung der gelabelten Objekte:** 
    - 1106x *potato*
    - 774x *bad*
    - 74x *stone*
  *(Hinweis: Da schrumpelige Kartoffeln aufgrund der Kamera-Unschärfe schwer zu erkennen waren, wurden diese Defekte beim Labeling vermutlich nur teilweise erfasst).*
- **Labeling-Prozess:**
  1. Zunächst wurden die ersten 200 Bilder manuell gelabelt, um eine Datengrundlage zu schaffen.
  2. Basierend auf diesen 200 Bildern wurde ein erstes Objekt-Erkennungsmodell in Roboflow trainiert.
  3. Dieses vortrainierte Modell wurde anschließend genutzt, um die restlichen Bilder halbautomatisiert (Assisted Labeling) vorzulabeln. Dies hat den weiteren Labeling-Prozess deutlich beschleunigt.
- **Preprocessing & Data Augmentation:** 
  Um das Modell für das Training robuster zu machen, wurden in Roboflow folgende Schritte angewendet:
  - **Preprocessing:** Auto-Orient (angewendet), Resize (Stretch to 512x512)
  - **Augmentations (2 Outputs pro Trainingsbild):** Rotation (zwischen -15° und +15°), Blur (bis zu 1px).

## 6. Geplante Systemarchitektur und Hardware-Konzept (Aus bisherigen Planungen)
Aus vorherigen Evaluierungen ergeben sich folgende technische Rahmenbedingungen für das endgültige System:
- **Hardware-Zentrale:** Ein Nvidia Jetson Orin Nano (mit 500GB SSD) soll als Edge-Device (Standalone) dienen, um die Kamera auszulesen und die KI lokal auszuführen.
- **Künstliche Intelligenz:** Es ist der Einsatz eines vortrainierten **YOLOv8n-Modells** (YOLOv8 Nano) geplant. Dieses liefert Objekterkennungen (Bounding Boxes) für Kartoffeln, Steine sowie punktuelle Detektionen für schlechte Stellen und Schnitte.
- **Objekt-Tracking:** Da sich die Kartoffeln auf dem Band bewegen und drehen, muss jedes Objekt per Tracking-Algorithmus (z.B. ByteTrack) eine durchgängige ID erhalten, um es bis zum Auswurf nachzuverfolgen.
- **Aktorik (Sortierung):** Das Aussortieren von schlechten Kartoffeln und Steinen erfolgt über eine Ventilinsel. Die Ventile werden via Relaismodul direkt durch die GPIO-Pins des Jetson angesteuert, abhängig von der räumlichen Position der Kartoffel auf dem Förderband.
- **Software & UI:** 
  - Ein lokaler Webserver auf dem Jetson stellt eine Web-App (React/Vite) als Steuerungs-Dashboard bereit.
  - Das Dashboard zeigt den Live-Videostream der Kamera, aktuelle Statistiken und bietet Einstellungsmöglichkeiten.
  - Über eine Logik im Interface sollen sich Toleranzwerte definieren lassen (z. B. welche Größe an schlechten Stellen noch akzeptabel ist) und Modelle gewechselt werden können.
  - Produktionsdaten werden in einer lokalen Datenbank protokolliert.
- **Herausforderungen beim Setup:** Bei der initialen Einrichtung der CUDA- und PyTorch-Umgebung auf dem Nvidia Jetson zeigten sich bereits typische Edge-Deployment-Hürden (wie Konflikte mit `libcudnn`-Versionen), die sorgfältig dokumentiert und gelöst werden müssen.

## 7. Ausblick und Zukünftige Optimierungen
Aus den bisherigen Erkenntnissen ergeben sich folgende Ansätze für die Weiterentwicklung des Systems:
- **Zwei-Kamera-Setup:** Es hat sich gezeigt, dass Kartoffeln an den äußeren Rändern (Seiten) des Förderbands nicht immer optimal erfasst werden. Zukünftig könnte ein Setup mit zwei Kameras nötig sein, um tote Winkel zu vermeiden und die Seiten besser auszuleuchten und zu filmen.
- **Logik zur feingranularen Defekterkennung:** Die Erkennung von Defekten ist im Datensatz bereits verankert, da Kartoffeln allgemein (`potato`) und fehlerhafte Stellen (`bad`) separat gelabelt wurden. Zukünftig soll die Software-Logik so programmiert werden, dass Kartoffeln, in deren Bereich ein Defekt (`bad`) detektiert wird, dynamisch als "schlechte Kartoffel" gewertet werden können. Das bietet den großen Vorteil, dass im Interface später exakte Schwellenwerte (Thresholds) eingestellt werden können. So lässt sich je nach aktueller Produktionsanforderung flexibel entscheiden, ab welcher Größe oder Anzahl von Defekten eine Kartoffel als Ausschuss gilt (und nicht pauschal beim kleinsten Kratzer).
