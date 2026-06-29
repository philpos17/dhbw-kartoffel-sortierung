import time

class SortingLogic:
    def __init__(self):
        # Maps track_id -> list of classifications
        self.history = {}
        # Maps track_id -> state (None, 'good', 'eject')
        self.decisions = {}
        # Time when object was last seen to clean up memory
        self.last_seen = {}
        # Has object been counted?
        self.counted = {}
        # Last known X or Y coordinate
        self.last_pos = {}

    def update(self, detections, ejector_queue, counting_line_pos_percent, frame_height, frame_width, counting_orientation='horizontal', current_time=None):
        if current_time is None:
            current_time = time.time()
            
        crossed_good = 0
        crossed_bad = 0
        counting_pos = (frame_height if counting_orientation == 'horizontal' else frame_width) * (counting_line_pos_percent / 100.0)
            
        for det in detections:
            track_id = det["id"]
            action = det["action"]
            
            if action == "ignore":
                continue
            
            self.last_seen[track_id] = current_time
            curr_pos = det["center_y"] if counting_orientation == 'horizontal' else det["center_x"]
            prev_pos = self.last_pos.get(track_id, curr_pos)
            
            if track_id not in self.history:
                self.history[track_id] = []
                self.decisions[track_id] = None
                
            self.history[track_id].append(action)
            
            # Evaluate history if no decision yet
            if self.decisions[track_id] is None:
                history = self.history[track_id]
                # If object has been seen enough times (e.g. 5 frames) to make a reliable decision
                if len(history) >= 5:
                    bad_count = history.count("bad")
                    # If more than 30% of detections are bad, eject it
                    if bad_count / len(history) > 0.3:
                        self.decisions[track_id] = "eject"
                        ejector_queue.add_eject_task(det["center_x"], det["center_y"], track_id, "bad")
                    else:
                        # Let it pass as good
                        self.decisions[track_id] = "good"
                        
            # Check line crossing
            if prev_pos < counting_pos and curr_pos >= counting_pos and not self.counted.get(track_id, False):
                self.counted[track_id] = True
                decision = self.decisions.get(track_id)
                
                # If it crossed but no decision yet (fast movement?), force decision based on current history
                if decision is None:
                    history = self.history[track_id]
                    if len(history) > 0 and (history.count("bad") / len(history) > 0.3):
                        decision = "eject"
                        # We might also want to trigger eject here if we didn't before, but 
                        # usually eject logic happens earlier (higher up the screen).
                        ejector_queue.add_eject_task(det["center_x"], det["center_y"], track_id, "bad")
                    else:
                        decision = "good"
                        
                if decision == "eject":
                    crossed_bad += 1
                else:
                    crossed_good += 1
                    
            self.last_pos[track_id] = curr_pos

        return crossed_good, crossed_bad

    def cleanup(self, current_time=None):
        if current_time is None:
            current_time = time.time()
            
        # Remove IDs not seen for more than 5 seconds
        to_remove = [tid for tid, t in self.last_seen.items() if current_time - t > 5.0]
        for tid in to_remove:
            del self.last_seen[tid]
            if tid in self.history: del self.history[tid]
            if tid in self.decisions: del self.decisions[tid]
            if tid in self.counted: del self.counted[tid]
            if tid in self.last_pos: del self.last_pos[tid]
            
        return len(to_remove)
