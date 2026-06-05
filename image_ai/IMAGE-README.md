# ReMIND — Image Enhancement Module

## Author

M. Talha Faizan

## Responsibility

This module handles all image-related AI services in ReMIND, including:

- Image enhancement
- Face restoration
- Resolution upscaling
- AI-based caption generation
- Pipeline optimization
- Temporary file management
- Logging system
- Cache system
- Evaluation tracking

---

# Technologies Used

## GFPGAN

Used for:

- face restoration
- facial enhancement
- repairing damaged faces

## Real-ESRGAN

Used for:

- image upscaling
- image sharpening
- quality enhancement

## VIT-GPT2 Captioning

Used for:

- generating image captions
- contextual image understanding

---

# Pipeline Overview

Input Image -> Decision Engine -> GFPGAN (optional) -> Real-ESRGAN (optional) -> Caption Generation -> Final Output

---

# Features

- Modular enhancement pipeline
- AI-based decision engine
- Session-based temp management
- Automatic cache system
- Logging system
- JSON-based evaluation reports
- Caption generation
- Automatic cleanup of unnecessary folders

---

# Folder Structure

```txt
backend/
│
├── app/
│   ├── ai_services/
│   ├── evaluation/
│   ├── tests/
│   └── utils/
│
├── cache/
├── evaluation_results/
├── logs/
├── temp/
│
└── requirements.txt
```
