# Dataset

## Public Dataset on Roboflow Universe

The dataset used in this project is publicly available as an open-source project on Roboflow Universe:

**[Potato Sorting on Conveyor Dataset](https://universe.roboflow.com/ms-workspace-m1gci/potato-sorting-on-conveyor)**

It contains 855 source images with 17,511 bounding-box annotations across four classes:
`potato`, `bad`, `cut`, and `stone`.

## Downloading the Dataset (YOLOv11 Format)

To download the current dataset version (v8) in YOLOv11-compatible format, a valid
[Roboflow API key](https://docs.roboflow.com/api-reference/authentication) is required.

```bash
pip install roboflow
```

```python
from roboflow import Roboflow

rf = Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace("ms-workspace-m1gci").project("potato-sorting-on-conveyor")
version = project.version(8)
dataset = version.download("yolov11")
```

> **Note:** Do not hard-code your API key in shared notebooks or public repositories.
> In Google Colab, use `from google.colab import userdata; api_key = userdata.get('ROBOFLOW_API_KEY')` instead.
