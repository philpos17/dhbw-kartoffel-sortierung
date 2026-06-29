import torch
import torchvision

# ==============================================================================
# Jetson Orin Nano Compatibility Patch: Pure PyTorch NMS Fallback
# ==============================================================================
# The compiled C++ extension of torchvision on JetPack 6.1 aarch64 often fails
# to register the `torchvision::nms` operator correctly, causing a fatal runtime
# crash in the camera thread. To ensure stability on the Jetson platform, we
# monkeypatch torchvision.ops.nms with a pure PyTorch implementation.
def pure_pytorch_nms(boxes, scores, iou_threshold):
    if boxes.numel() == 0:
        return torch.empty((0,), dtype=torch.int64, device=boxes.device)
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    _, order = scores.sort(0, descending=True)
    keep = []
    while order.numel() > 0:
        if order.numel() == 1:
            keep.append(order.item())
            break
        i = order[0].item()
        keep.append(i)
        xx1 = x1[order[1:]].clamp(min=x1[i])
        yy1 = y1[order[1:]].clamp(min=y1[i])
        xx2 = x2[order[1:]].clamp(max=x2[i])
        yy2 = y2[order[1:]].clamp(max=y2[i])
        inter = (xx2 - xx1).clamp(min=0) * (yy2 - yy1).clamp(min=0)
        iou = inter / (areas[i] + areas[order[1:]] - inter)
        idx = (iou <= iou_threshold).nonzero(as_tuple=False).squeeze(-1)
        if idx.numel() == 0:
            break
        order = order[idx + 1]
        # In case idx was a scalar, ensure order remains a 1D tensor
        if order.dim() == 0:
            order = order.unsqueeze(0)
    return torch.tensor(keep, dtype=torch.int64, device=boxes.device)

# Monkey-Patch: Ersetze die fehlerhafte C++ Funktion durch unsere reine PyTorch-Version
torchvision.ops.nms = pure_pytorch_nms
torchvision.ops.boxes.nms = pure_pytorch_nms
# ==========================================

from ultralytics import YOLO
import cv2
import numpy as np
import os

class PotatoDetector:
    def __init__(self, model_path='yolov8n.pt'):
        # Robust path resolution to the 'models' directory at project root
        self.models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
        
        # If only a filename was provided at startup, resolve it to the full path
        if not os.path.isabs(model_path) and not model_path.startswith('models/'):
            model_path = os.path.join(self.models_dir, os.path.basename(model_path))
            
        try:
            self.model = YOLO(model_path)
            self.model_path = model_path
            print(f"Loaded model {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            
        self.class_mapping = {}

    def update_model_and_mapping(self, model_path, mapping):
        self.class_mapping = mapping
        
        full_path = os.path.join(self.models_dir, model_path)
        engine_path = full_path.replace('.pt', '.engine')
        
        # Prioritize TensorRT (.engine) if it exists for huge FPS boost
        if os.path.exists(engine_path):
            full_path = engine_path
            print(f"CUDA Optimierung: Lade superschnelles TensorRT Modell -> {engine_path}", flush=True)
            
        if not os.path.exists(full_path):
            print(f"Fehler: Modell {full_path} nicht gefunden!", flush=True)
            return False
            
        model_changed = False
        if not hasattr(self, 'model_path') or self.model_path != full_path:
            try:
                print(f"Hot-swapping model to: {full_path}", flush=True)
                self.model = YOLO(full_path)
                self.model_path = full_path
                model_changed = True
            except Exception as e:
                print(f"Error swapping model: {e}")
                
        self.class_mapping = mapping
        return model_changed

    def process_frame(self, frame):
        if self.model is None:
            return frame, [], 0.0
            
        # Run YOLO tracking with very low global confidence so we can filter dynamically
        # tracker='bytetrack.yaml' can be specified, but default botsort/bytetrack works
        results = self.model.track(frame, persist=True, verbose=False, tracker="bytetrack.yaml", conf=0.05)
        
        detections = []
        inf_time = 0.0
        
        if results and len(results) > 0:
            result = results[0]
            
            if hasattr(result, 'speed') and 'inference' in result.speed:
                inf_time = result.speed['inference']
                
            if result.boxes is not None and result.boxes.id is not None:
                boxes = result.boxes.xyxy.cpu().numpy()
                track_ids = result.boxes.id.int().cpu().numpy()
                class_ids = result.boxes.cls.int().cpu().numpy()
                confidences = result.boxes.conf.cpu().numpy()
                
                for box, track_id, cls_id, conf in zip(boxes, track_ids, class_ids, confidences):
                    x1, y1, x2, y2 = map(int, box)
                    
                    original_name = self.model.names.get(int(cls_id), f"cls_{cls_id}")
                    mapping_data = self.class_mapping.get(int(cls_id), {})
                    
                    if isinstance(mapping_data, dict):
                        action = mapping_data.get("action", "ignore")
                        thresh = mapping_data.get("confidence", 0.5)
                    else:
                        action = mapping_data
                        thresh = 0.5
                        
                    if float(conf) < thresh:
                        continue
                    
                    detections.append({
                        "id": int(track_id),
                        "class_name": original_name,
                        "action": action,
                        "bbox": [x1, y1, x2, y2],
                        "conf": float(conf),
                        # center coordinate for tracking on belt
                        "center_x": int((x1 + x2) / 2),
                        "center_y": int((y1 + y2) / 2)
                    })
                    
                    # Draw on frame for visualization
                    if action == "bad":
                        color = (0, 0, 255) # Red
                    elif action == "good":
                        color = (0, 255, 0) # Green
                    else:
                        color = (128, 128, 128) # Gray for ignore
                        
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"ID:{track_id} {original_name} {conf:.2f}", (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame, detections, inf_time
