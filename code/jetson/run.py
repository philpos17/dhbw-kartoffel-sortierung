import uvicorn
import threading
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'vision'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'hardware'))

from hardware.ejector_queue import EjectorQueue
from vision.camera import CameraProcess
import backend.main as backend_app

def main():
    print("Starting Potato Sorter System...")
    
    # 1. Initialize Ejector Queue
    ejector_queue = EjectorQueue()
    ejector_queue.start()
    
    # 2. Initialize Camera and Vision Pipeline
    cam = CameraProcess(camera_id=0, ejector_queue=ejector_queue)
    cam.start()
    
    # 3. Start Web Backend
    try:
        uvicorn.run(backend_app.app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        pass
    finally:
        print("Shutting down...")
        cam.stop()
        ejector_queue.stop()

if __name__ == "__main__":
    main()
