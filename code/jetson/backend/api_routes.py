from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
import database
import os
import shutil
from ultralytics import YOLO

router = APIRouter()

MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

class SettingsUpdate(BaseModel):
    model_path: str
    belt_speed_delay: float
    threshold_bad_area: float
    counting_line_y: float = 80.0
    counting_orientation: str = 'horizontal'

@router.get("/api/settings")
def get_settings():
    settings = database.get_settings()
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings

@router.post("/api/settings")
def update_settings(settings: SettingsUpdate):
    database.update_settings(
        settings.model_path,
        settings.belt_speed_delay,
        settings.threshold_bad_area,
        settings.counting_line_y,
        settings.counting_orientation
    )
    return {"status": "success"}

@router.get("/api/stats")
def get_stats():
    # Fetch today's aggregated stats
    conn = database.get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT 
            SUM(good_count) as total_good,
            SUM(bad_count) as total_bad
        FROM stats
        WHERE date(timestamp) = date('now')
    ''')
    row = c.fetchone()
    conn.close()
    
    # Drop stone_count here as well
    if not row or row['total_good'] is None:
        return {"total_good": 0, "total_bad": 0}
        
    return dict(row)

@router.get("/api/models")
def list_models():
    models = []
    if os.path.exists(MODELS_DIR):
        for f in os.listdir(MODELS_DIR):
            if f.endswith('.pt') or f.endswith('.engine'):
                models.append(f)
    # Wenn noch keine Modelle hochgeladen wurden, zeige zumindest yolov8n.pt an
    if 'yolov8n.pt' not in models:
        models.append('yolov8n.pt')
    return {"models": models}

@router.post("/api/models/upload")
async def upload_model(file: UploadFile = File(...)):
    if not (file.filename.endswith('.pt') or file.filename.endswith('.engine')):
        raise HTTPException(status_code=400, detail="Only .pt or .engine files are allowed")
        
    file_path = os.path.join(MODELS_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"status": "success", "filename": file.filename}

@router.get("/api/models/{model_name}/classes")
def get_model_classes(model_name: str):
    file_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(file_path):
        # Fallback to current dir if default model
        if os.path.exists(model_name):
            file_path = model_name
        else:
            raise HTTPException(status_code=404, detail="Model not found")
            
    try:
        model = YOLO(file_path)
        names = model.names # Dict of {id: "name"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    # Get current mapping from DB
    current_mapping = database.get_model_mapping(model_name)
    
    classes = []
    for class_id, class_name in names.items():
        class_mapping = current_mapping.get(class_id, {})
        classes.append({
            "id": class_id,
            "name": class_name,
            "action": class_mapping.get("action", "ignore") if isinstance(class_mapping, dict) else class_mapping,
            "confidence": class_mapping.get("confidence", 0.5) if isinstance(class_mapping, dict) else 0.5
        })
        
    return {"model_name": model_name, "classes": classes}

@router.post("/api/models/{model_name}/mapping")
def save_model_mapping(model_name: str, mapping: dict):
    # mapping is dict of {class_id: "action"}
    database.save_model_mapping(model_name, mapping)
    return {"status": "success"}
