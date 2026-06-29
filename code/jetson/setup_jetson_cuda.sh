#!/bin/bash
# ==============================================================================
# Jetson Orin Nano (JetPack 6.1) - Environment Setup & TensorRT Optimization
# ==============================================================================
set -e

LOG_FILE="setup_cuda_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -i "${LOG_FILE}")
exec 2>&1

echo "====================================================="
echo "Jetson CUDA Environment Setup"
echo "Log file: ${LOG_FILE}"
echo "====================================================="

# 1. Ensure working directory
if [ ! -f "requirements.txt" ]; then
    echo "[ERROR] requirements.txt not found. Please execute from the project root."
    exit 1
fi

# 2. System dependencies & Virtual Environment
echo "[INFO] Checking system dependencies and virtual environment..."
sudo apt-get update
sudo apt-get install -y python3.10-venv python3-pip libopenblas-base libopenmpi-dev \
    libomp-dev libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev \
    libavformat-dev libswscale-dev tensorrt python3-libnvinfer python3-libnvinfer-dev

if [ ! -d ".venv" ]; then
    echo "[INFO] Creating Python virtual environment (.venv)..."
    python3 -m venv .venv
fi

source .venv/bin/activate

# 3. Base requirements
echo "[INFO] Installing base requirements..."
pip install -r requirements.txt

# 4. Remove standard PyTorch to enforce NVIDIA Jetson optimized build
echo "[INFO] Purging standard PyTorch packages..."
pip uninstall -y torch torchvision tensorrt || true

# 5. NVIDIA PyTorch & cuSPARSELt
echo "[INFO] Installing NVIDIA PyTorch 2.5.0 for JetPack 6.1..."
pip install https://developer.download.nvidia.com/compute/redist/jp/v61/pytorch/torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whl
pip install nvidia-cusparselt-cu12

echo "[INFO] Linking cuSPARSELt..."
cp -P .venv/lib/python3.10/site-packages/nvidia/cusparselt/lib/* .venv/lib/python3.10/site-packages/torch/lib/ || true

# 6. Build torchvision from source
echo "[INFO] Building torchvision v0.20.0 from source (ETA: 10-20m)..."
pip install Pillow numpy requests

if [ ! -d "torchvision_src" ]; then
    git clone --branch v0.20.0 https://github.com/pytorch/vision torchvision_src
fi

cd torchvision_src
export BUILD_VERSION=0.20.0
export MAX_JOBS=2
# Force numpy<2 to prevent Jetson ABI mismatch
../.venv/bin/pip install "numpy<2" wheel
../.venv/bin/pip install .
cd ..
rm -rf torchvision_src

# 7. Link System TensorRT to venv
echo "[INFO] Linking system TensorRT to virtual environment..."
ln -sf /usr/lib/python3/dist-packages/tensorrt* .venv/lib/python3.10/site-packages/ || true
ln -sf /usr/lib/python3.10/dist-packages/tensorrt* .venv/lib/python3.10/site-packages/ || true

# 8. CUDA Verification
echo "[INFO] Verifying CUDA support..."
CUDA_AVAILABLE=$(python3 -c "import torch; print(torch.cuda.is_available())")
echo ">>> CUDA Available: $CUDA_AVAILABLE <<<"

# 9. Jetson-specific compatibility patches
echo "[INFO] Applying Jetson compatibility patches..."
# Bypass PyTorch 2.5 meta registration issue on aarch64
echo "" > .venv/lib/python3.10/site-packages/torchvision/_meta_registrations.py

# Install ONNX CPU runtime to bypass missing onnxruntime-gpu wheel
pip install onnx onnxslim onnxruntime
sed -i 's/"onnxruntime-gpu"/"onnxruntime"/g' .venv/lib/python3.10/site-packages/ultralytics/engine/exporter.py

# 10. Initial TensorRT Export
echo "====================================================="
echo "[INFO] Exporting yolov8n.pt to TensorRT (.engine)..."
yolo export model=models/yolov8n.pt format=engine half=True workspace=4

echo "====================================================="
echo "SETUP COMPLETE."
echo "Start the application: sudo .venv/bin/python3 run.py"
echo "====================================================="
