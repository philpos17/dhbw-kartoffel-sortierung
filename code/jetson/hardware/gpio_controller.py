import time
import logging

try:
    import Jetson.GPIO as GPIO
    HARDWARE_AVAILABLE = True
except Exception as e:
    print(f"Warning: Jetson.GPIO not available or failed to initialize ({e}). Using mock hardware mode.")
    HARDWARE_AVAILABLE = False

class ValveController:
    def __init__(self, pins=None):
        # Default Jetson Orin Nano GPIO pins for valves
        # Can be configured based on actual wiring
        self.pins = pins if pins else [11, 13, 15, 19, 21, 23, 29, 31]
        
        # Mapping from X-coordinate (0-1) to valve index
        self.num_valves = len(self.pins)
        
        self._setup_gpio()
        
    def _setup_gpio(self):
        if not HARDWARE_AVAILABLE:
            return
            
        GPIO.setmode(GPIO.BOARD)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW) # Initially off
            
    def get_valve_for_x(self, x_normalized):
        """Map a normalized X coordinate (0.0 to 1.0) to a valve index."""
        if x_normalized < 0: x_normalized = 0
        if x_normalized >= 1.0: x_normalized = 0.99
        return int(x_normalized * self.num_valves)
        
    def activate_valve(self, valve_index, duration=0.1):
        if valve_index < 0 or valve_index >= self.num_valves:
            return
            
        pin = self.pins[valve_index]
        
        if HARDWARE_AVAILABLE:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(pin, GPIO.LOW)
        else:
            logging.info(f"[MOCK] Activated valve {valve_index} (Pin {pin}) for {duration}s")
            
    def cleanup(self):
        if HARDWARE_AVAILABLE:
            GPIO.cleanup()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    vc = ValveController()
    vc.activate_valve(0)
    vc.cleanup()
