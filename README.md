# dhbw-kartoffel-sortierung (Potato Sorting)

## Project Overview

This project is part of a final university course project. The goal is to address a real-world agricultural use case using Machine Learning and Computer Vision methods.

The use case originates from a potato farm, where potatoes are currently sorted manually. The process involves distinguishing between usable potatoes, damaged or bad potatoes, and stones or foreign objects. Manual sorting is time-consuming and labor-intensive. The aim of this project is to support or partially automate this process using an image-based system.

## Problem Statement

The project investigates whether potatoes and unwanted objects on a conveyor belt can be reliably detected and classified using Computer Vision.

Currently, we are considering an Object Detection setup with the following classes:

- `potato`
- `bad`
- `cut`
- `stone`

An open technical question is whether `cut` should remain a separate class in the long run or be treated as a subcategory of `bad`.

## Objectives

The project goal is the development and evaluation of a prototype for the automatic detection and sorting of potatoes and foreign objects in images of a conveyor belt setup.

In particular, the following questions are to be answered:

- Is Object Detection suitable for this use case?
- Which model architecture delivers the best results on the available dataset?
- How representative is the current dataset for future real-world application?
- What are the weaknesses, biases, and limitations of the dataset?
- Which metrics are suitable for evaluating the system?

## Dataset

> **Detailed insights into the physical setup, camera angles, and the image acquisition process can be found in the [Project Preparations](docs/projekt_vorarbeiten.md#3-image-acquisition-setup)**

The current dataset was managed in Roboflow and currently contains:

- `855` images
- `17,511` annotations
- `4` classes
- an average of `20.5` objects per image
- image resolution predominantly `1920 x 1080`

Current class distribution:

- `potato`: 16,271
- `stone`: 778
- `bad`: 399
- `cut`: 63

Important note:
The dataset is likely not yet fully representative of the actual real-world application. As it stands, potatoes were placed on a belt, while stones and damaged examples were sometimes artificially added. The representativeness of the dataset, especially the validation set, must be critically reflected upon during the project.

### Optional External Data Sources (Kaggle etc.)

In addition, a public potato dataset could be obtained via Kaggle or similar platforms, for instance to enrich rare classes, cover defect types, or obtain additional examples of healthy potatoes. Examples:

- [Potato Disease Recognition Dataset](https://www.kaggle.com/datasets/sujaykapadnis/potato-disease-recognition-dataset)
- [Healthy Potato Image](https://www.kaggle.com/datasets/mehedihasanmridha/healthy-potato-image)

Important: Such datasets originate from different recording conditions (lighting, background, single object instead of a densely packed belt) and should therefore only be used as supplementary material during training. Validation and operational testing should continue to rely on our own, realistic conveyor belt data to avoid obscuring domain shifts. Licensing and terms of use of the respective source must be checked before use.

## Previous Experiments in Roboflow

Several object detection models have been tested in Roboflow so far.

### Results

| Model | Type | Date | mAP@50 | Precision | Recall | F1 |
|---|---|---|---:|---:|---:|---:|
| My First Project 7 | RF-DETR Small | Jul 13, 2026 | 92.2% | 92.9% | 90.4% | 91.6% |
| My First Project 6 | RF-DETR Small | May 31, 2026 | 75.1% | 84.2% | 76.1% | 80.0% |
| My First Project 4 | YOLOv11 Nano | May 31, 2026 | 72.2% | 68.3% | 76.4% | 72.1% |
| My First Project 3 | RF-DETR Medium | May 17, 2026 | 74.6% | 85.3% | 75.8% | 80.3% |
| My First Project 2 | RF-DETR Medium | May 16, 2026 | 66.7% | 66.3% | 65.7% | 66.0% |
| My First Project 1 | RF-DETR Small | May 16, 2026 | 50.4% | 48.5% | 50.0% | 49.3% |

Initial Observation:
The results so far show that the use case is fundamentally learnable. At the same time, the values indicate that dataset quality, class balance, and representativeness have a strong influence on model performance.

## Planned Project Approach

The project will be processed in several steps:

1. Technically specify the problem statement and target picture
2. Document and critically evaluate the dataset
3. Research related work on agricultural object detection
4. Export data and set up a reproducible training pipeline outside of Roboflow
5. Train and evaluate a baseline model in a Jupyter Notebook
6. Compare models
7. Discuss results and reflect on the limitations of the approach

## Tools and Workspace

The planned workspace is as follows:

- `Roboflow` for annotation, dataset versioning, and initial experiments
- `Jupyter Notebook` for documented and reproducible analysis
- `GitHub` for collaboration and version control
- `Google Colab` or local machines for training and evaluation

## Reproducibility

An important part of the project is transferring the work previously done in Roboflow into a comprehensible project structure. In particular, the following points must be documented:

- dataset version used
- classes and label definitions
- preprocessing and augmentation decisions
- trained model architectures
- hyperparameters used
- evaluation results

## Potential Target Hardware: Edge Deployment on NVIDIA Jetson (Optional)

As an additional, non-binding idea, there is the possibility of running the final implementation on an NVIDIA Jetson (e.g. Orin Nano / Orin NX) to enable inference directly at the conveyor belt without an external computer.

Whether this actually becomes part of the project remains open, as the setup effort (JetPack, TensorRT conversion, driver and camera integration) is high. Realistically, only a **feasibility assessment based on hardware specs** is expected initially, rather than a full production deployment.

Key aspects to consider would be:

- expected inference latency and throughput of candidate models (compact YOLO vs. RF-DETR) on Jetson-class hardware
- available memory and computing power (TOPS) relative to the required belt speed
- necessity of model optimization (quantization, TensorRT, model size)
- effort for the toolchain and integration compared to the project's benefit

This assessment can be a valuable project result even if a real Jetson deployment is ultimately not implemented.

## Open Questions

The following points still need to be clarified or refined:

- Should the target system distinguish 3 or 4 classes?
- Is `cut` a separate class or part of `bad`?
- What does the real class distribution look like in the field or on the belt?
- What should a representative validation and test set look like?
- Can additional real data be recorded?
- Should the final goal be detection, counting, or actual sorting decisions?
- Should an edge deployment on NVIDIA Jetson be part of the project, or only flow in as a feasibility assessment based on hardware specs?

## Preliminary Conclusion

The use case is practical and well-suited for a computer vision project. The Roboflow results so far provide a good starting point. The most important next step is to neatly refine the problem definition, dataset quality, and evaluation strategy so that the subsequent model evaluation is technically sound.