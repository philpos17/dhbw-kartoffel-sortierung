# Potato Sorter - AI Vision Backend

This repository contains the backend and computer vision pipeline for the AI-powered Potato Sorter. It uses FastAPI for the web server, WebSockets for real-time video streaming, and YOLOv8 accelerated via NVIDIA TensorRT for real-time object detection on Jetson hardware.

## System Architecture
* **Hardware:** NVIDIA Jetson Orin Nano
* **Backend:** Python 3.10 (FastAPI, Uvicorn)
* **Vision Pipeline:** OpenCV (Video Capture), Ultralytics YOLOv8 (Detection), ByteTrack (Object Tracking)
* **Acceleration:** TensorRT (.engine models)

## Environment Compatibility Matrix
To ensure the system works seamlessly with the Jetson architecture, specific versions of core libraries are required. Do not blindly update these packages without verifying compatibility against the NVIDIA JetPack version.

| Component | Required Version | Notes |
| :--- | :--- | :--- |
| **OS** | Ubuntu 22.04 LTS | Standard for JetPack 6 |
| **JetPack** | 6.1 (r36.4) | Must match L4T version |
| **Python** | 3.10 | OS Default |
| **PyTorch** | `2.5.0a0+872d972e41.nv24.08` | NVIDIA custom aarch64 wheel |
| **Torchvision**| `0.20.0` | Must be built from source locally |
| **TensorRT** | `10.3.0` | Installed via `apt`, symlinked to venv |
| **Ultralytics**| `8.4.80` or newer | Handles YOLOv8 logic |

## Setup Instructions (Fresh Jetson Install)

The provided setup script automates the entire installation process, including virtual environment creation, system dependencies, and compiling required C++ extensions.

1. **Clone the Repository:**
   Ensure this project directory is placed in the home folder of the Jetson (e.g., `~/potato-sorter/`).

2. **Run the Setup Script:**
   The script does NOT require `sudo` to execute (it will request `sudo` permissions internally when installing system packages).
   ```bash
   cd ~/potato-sorter
   chmod +x setup_jetson_cuda.sh
   ./setup_jetson_cuda.sh
   ```
   > [!WARNING]
   > The setup script compiles `torchvision` from source. This process will take approximately 10-20 minutes on a Jetson Nano. Do not interrupt the process.

3. **Start the Application:**
   Once setup is complete, run the backend server:
   ```bash
   sudo .venv/bin/python3 run.py
   ```
   *Note: `sudo` is required to access hardware GPIO pins via the `Jetson.GPIO` library.*

## Model Management & TensorRT Conversion

For maximum inference speed (e.g., 20+ FPS), models must be exported to TensorRT (`.engine` format).

> [!CAUTION]
> TensorRT models (`.engine`) are strictly tied to the hardware architecture they were compiled on. You **cannot** export a model to TensorRT in Google Colab and run it on the Jetson. The conversion must happen locally on the Jetson.

**Workflow for Custom Models:**
1. Train your model in Google Colab or locally on a standard GPU.
2. Download the resulting `.pt` weights file (e.g., `kartoffel_modell_best.pt`).
3. Place the `.pt` file into the `models/` directory on the Jetson.
4. Run the export command directly on the Jetson:
   ```bash
   .venv/bin/yolo export model=models/kartoffel_modell_best.pt format=engine half=True workspace=4
   ```
5. Restart the backend. The UI will automatically detect the new `.engine` file and allow you to select it for inference.

## Known Jetson Workarounds (Architecture Hacks)

This codebase includes specific workarounds for known NVIDIA/PyTorch aarch64 compatibility bugs. If you encounter issues during future updates, reference these patches:

1. **Torchvision NMS Runtime Crash:**
   The compiled C++ extension of `torchvision` on JetPack 6.1 fails to register the `torchvision::nms` operator, causing the camera thread to crash silently.
   *Fix:* A pure-PyTorch NMS fallback is monkeypatched into `torchvision.ops.nms` at the top of `vision/detector.py`.
2. **Torchvision Meta Registrations Import Error:**
   Due to PyTorch 2.5 API changes, importing `torchvision` fails entirely due to missing meta registrations.
   *Fix:* The setup script explicitly empties `.venv/lib/python3.10/site-packages/torchvision/_meta_registrations.py` to bypass the fatal import error.
3. **ONNX Runtime Missing Wheel:**
   During TensorRT export, Ultralytics attempts to validate the model by installing `onnxruntime-gpu`, which does not exist for ARM64 on standard PyPI.
   *Fix:* The setup script installs the CPU `onnxruntime` and uses `sed` to patch the Ultralytics exporter to accept it.
