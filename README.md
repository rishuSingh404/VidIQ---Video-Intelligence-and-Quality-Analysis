# Video Artifact Analysis and Model Training

## Project Overview

This project is designed to analyze various artifacts in videos, such as motion intensity, time differences, jerkiness, flickering, and mosquito noise. The data is then combined and used for machine learning model training with LSTM models using Keras, including a PCA feature selection model.

---

## File Structure

The project is organized as follows:

```
.
├── Frame Extraction (NOT INCLUDED IN THIS FOLDER)
│   ├── Video_List.py
│   └── Frame_by_Frame.py (Functions, not for running)
├── Artifact Extraction (NOT INCLUDED IN THIS FOLDER)
│   ├── Artifacts_Frame_List.py
│   └── Artifacts.py (Functions, not for running)
├── Jerkiness Extraction
│   ├── TimeDifference.py
│   ├── MotionIntensity.py
│   └── Jerkiness.py
├── Flickering Extraction
│   └── Flickering.py
├── Mosquito Noise Extraction
│   └── MosquitoNoise.py
├── Function Definitions (Not for running)
│   └── Functions.py
├── Artifact Combination
│   └── AllArtifactsCombine.py
├── Data Preparation
│   ├── DataCombine.py
│   └── DataCombine with Processing.py
├── Model Training
│   ├── LSTM model (keras).py
│   └── LSTM model (keras) with PCA feature selection.py
└── Model Loading (For testing)
    ├── LoadModel.py (all features)
    └── LoadModel (PCA).py (with PCA)
```

---

## Prerequisites

Make sure the following packages are installed:

```bash
pip install numpy pandas openpyxl opencv-python scikit-learn keras tensorflow
```

---

## Instructions to Run

### 1. Jerkiness Extraction

```bash
python TimeDifference.py
python MotionIntensity.py
python Jerkiness.py
```

### 2. Flickering Extraction

```bash
python Flickering.py
```

### 3. Mosquito Noise Extraction

```bash
python MosquitoNoise.py
```

### 4. Combine All Artifacts into a Single Excel File

```bash
python AllArtifactsCombine.py
```

### 5. Data Preparation

First, run the standard data combination:

```bash
python DataCombine.py
```

If normalization is needed, follow up with:

```bash
python "DataCombine with Processing.py"
```

### 6. Model Training

You can train the model using all features or with PCA feature selection:

```bash
python "LSTM model (keras).py"
# OR
python "LSTM model (keras) with PCA feature selection.py"
```

### 7. Model Testing

Load the model for testing using:

```bash
python LoadModel.py
# OR with PCA
python "LoadModel (PCA).py"
```

---

## Key Functions

- `YComponent()`: Extracts the Y component from a video file.
- `jerkiness()`: Calculates jerkiness using motion intensity and time difference.
- `blockshaped()`: Splits an image array into blocks.
- `AvgPixelIntensity()`: Computes the average pixel intensity of an image.
- `LaplacianEdge()`: Computes edge sharpness using the Laplacian method.

---

## Notes

- Ensure all input videos and excel files are in their respective folders as expected by the scripts.
- The `Functions.py` file contains helper functions and is not meant to be run directly.
- The processing sequence is crucial; follow the steps in order to avoid errors.

---

