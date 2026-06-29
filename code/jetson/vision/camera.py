import cv2
import threading
import time
import base64
import sys
import os

# Add backend and hardware to path to allow imports if run standalone
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend import main
from backend import database
from detector import PotatoDetector
from logic import SortingLogic

class CameraProcess:
    def __init__(self, camera_id=0, ejector_queue=None):
        self.camera_id = camera_id
        self.cap = self._open_camera()
        self.detector = PotatoDetector()
        self.logic = SortingLogic()
        self.ejector_queue = ejector_queue
        
        self.running = False
        self.thread = None
        
        # Stats
        self.stats = {
            "total_good": 0,
            "total_bad": 0
        }
        self.active_model_name = "yolov8n.pt"
        self.counting_line_y = 80.0
        self.counting_orientation = 'horizontal'

    def _open_camera(self):
        import sys
        
        # Helper to test a camera source
        def try_cam(source, apiPreference=cv2.CAP_ANY):
            print(f"Versuche Kameraquelle: {source} (API: {apiPreference})...", flush=True)
            cap = cv2.VideoCapture(source, apiPreference)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    print(f"-> ERFOLG! Kamera {source} liefert Bilder.", flush=True)
                    return cap
                else:
                    print(f"-> FEHLER: Kamera {source} laesst sich oeffnen, liefert aber kein Bild.", flush=True)
                    cap.release()
            else:
                print(f"-> FEHLER: Konnte Kamera {source} nicht oeffnen.", flush=True)
            return None

        # 1. Standard USB Camera (often video0 or video1)
        cap = try_cam(0, cv2.CAP_V4L2)
        if cap: return cap
        
        cap = try_cam(1, cv2.CAP_V4L2)
        if cap: return cap
        
        cap = try_cam(0) # without explicit V4L2
        if cap: return cap
        
        cap = try_cam(1)
        if cap: return cap

        # 2. Try CSI Camera with GStreamer Pipeline (Raspberry Pi Camera)
        gstreamer_pipeline = (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! "
            "nvvidconv flip-method=0 ! "
            "video/x-raw, width=(int)640, height=(int)480, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
        )
        cap = try_cam(gstreamer_pipeline, cv2.CAP_GSTREAMER)
        if cap: return cap
            
        print("KRITISCHER FEHLER: Keine Kamera konnte geoeffnet werden!", flush=True)
        return cv2.VideoCapture(self.camera_id) # Fallback to default behavior

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_loop)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if self.cap:
            self.cap.release()

    def _run_loop(self):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # To avoid saving to DB on every frame, save periodically
        last_db_save = time.time()
        frame_count = 0
        prev_time = time.time()
        
        while self.running:
            frame_count += 1
            if frame_count % 30 == 0:
                current_settings = database.get_settings()
                if current_settings and 'model_path' in current_settings:
                    model_path = current_settings['model_path']
                    mapping = database.get_model_mapping(model_path)
                    self.counting_line_y = current_settings.get('counting_line_y', 80.0)
                    self.counting_orientation = current_settings.get('counting_orientation', 'horizontal')
                    
                    if self.detector.update_model_and_mapping(model_path, mapping):
                        self.active_model_name = model_path
                    # Fallback update mapping if model didn't change but mapping did
                    self.detector.class_mapping = mapping

            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
                
            # Process frame with YOLO
            annotated_frame, detections, inf_time = self.detector.process_frame(frame)
            
            # Apply logic and add to ejector queue if needed
            if self.ejector_queue:
                frame_height, frame_width = frame.shape[:2]
                crossed_good, crossed_bad = self.logic.update(
                    detections, self.ejector_queue, self.counting_line_y, 
                    frame_height, frame_width, self.counting_orientation
                )
                self.stats["total_good"] += crossed_good
                self.stats["total_bad"] += crossed_bad
                self.logic.cleanup()
                
            # Draw counting line
            h, w = annotated_frame.shape[:2]
            line_pos = self.counting_line_y / 100.0
            
            if self.counting_orientation == 'horizontal':
                line_y = int(h * line_pos)
                cv2.line(annotated_frame, (0, line_y), (w, line_y), (255, 255, 0), 2)
                cv2.putText(annotated_frame, f"Zaehllinie ({self.counting_line_y}%)", (10, line_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            else:
                line_x = int(w * line_pos)
                cv2.line(annotated_frame, (line_x, 0), (line_x, h), (255, 255, 0), 2)
                cv2.putText(annotated_frame, f"Zaehllinie ({self.counting_line_y}%)", (line_x + 10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            
            # Calculate FPS
            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time + 1e-6)
            prev_time = curr_time
            
            # Encode frame to jpg for websocket
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            base64_frame = base64.b64encode(buffer).decode('utf-8')
            
            # Broadcast via websocket
            try:
                if hasattr(main, 'main_loop') and main.main_loop:
                    import asyncio
                    asyncio.run_coroutine_threadsafe(
                        main.broadcast_frame(base64_frame, self.stats, self.active_model_name, fps, inf_time),
                        main.main_loop
                    )
            except Exception as e:
                print(f"Websocket Broadcast Fehler: {e}", flush=True)
                
            # Save stats periodically
            if time.time() - last_db_save > 10.0:
                database.log_stats(self.stats["total_good"], self.stats["total_bad"])
                last_db_save = time.time()
                
            # Cap framerate to save CPU if needed
            time.sleep(0.01)

if __name__ == "__main__":
    # Test run
    cam = CameraProcess()
    cam.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cam.stop()
