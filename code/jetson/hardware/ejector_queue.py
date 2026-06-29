import threading
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend import database
from hardware.gpio_controller import ValveController

class EjectorQueue:
    def __init__(self, image_width=640):
        self.queue = []
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
        self.image_width = image_width
        self.valve_controller = ValveController()
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._process_queue)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.valve_controller.cleanup()
            
    def add_eject_task(self, x_pixel, y_pixel, track_id, reason="bad_potato"):
        # Fetch current delay from DB settings
        settings = database.get_settings()
        delay = settings["belt_speed_delay"] if settings else 2.5
        
        execute_at = time.time() + delay
        x_normalized = x_pixel / self.image_width
        valve_idx = self.valve_controller.get_valve_for_x(x_normalized)
        
        with self.lock:
            self.queue.append({
                "execute_at": execute_at,
                "valve_idx": valve_idx,
                "track_id": track_id,
                "reason": reason
            })
            # Sort queue by execution time
            self.queue.sort(key=lambda item: item["execute_at"])
            
    def _process_queue(self):
        while self.running:
            current_time = time.time()
            task_to_execute = None
            
            with self.lock:
                if self.queue and self.queue[0]["execute_at"] <= current_time:
                    task_to_execute = self.queue.pop(0)
                    
            if task_to_execute:
                # Actuate the valve in a separate thread so we don't block the queue
                threading.Thread(
                    target=self.valve_controller.activate_valve, 
                    args=(task_to_execute["valve_idx"], 0.1),
                    daemon=True
                ).start()
                
                # Update stats via backend depending on reason
                if task_to_execute["reason"] == "stone":
                    # We might handle logic stats directly in camera.py, but this ensures it actually ejected
                    pass
            else:
                time.sleep(0.01) # Small sleep to prevent CPU hogging
