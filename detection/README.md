# Detection Module (Computer Vision)

**Owner:** Sujal  
**Support:** Vedant (Dataset validation, CV support, and integration testing)  
**Feature Branch:** `sujal-detection`

---

## Overview

The AEGIS Detection Module runs object detection on aerial drone imagery to identify stranded or injured personnel in maritime and wilderness search-and-rescue scenarios.

It uses the **SARD_YOLO** reference dataset conventions and provides:
1. **Flexible Model Loader:** Automatically checks `detection/weights/` for custom fine-tuned weights (`best.pt`, `sard.pt`, `sard_yolo.pt`), with seamless fallback to pretrained Ultralytics YOLO (`yolov8n.pt` with class 0 `person` filter).
2. **Standardized Data Contract:** Emits structured JSON outputs adhering to `shared.schemas.DetectionResult`.
3. **Dual Interface:** Standalone CLI script for field testing and an importable Python function for dashboard integration.

---

## Quick Start & CLI Usage

### 1. Run Detection on an Aerial Image
```bash
python detection/infer.py --source detection/samples/reference_aerial.jpg --save-json detection/output/demo_detection.json --save-img detection/output/demo_annotated.jpg
```

### 2. Available CLI Arguments
- `--source` *(required)*: Path to an aerial image file or directory of images.
- `--weights` *(optional)*: Path to custom `.pt` model checkpoint.
- `--conf` *(default: 0.25)*: Confidence threshold (tuned for small aerial targets).
- `--iou` *(default: 0.45)*: Non-Maximum Suppression IoU threshold.
- `--save-json` *(optional)*: File path to save the serialized `DetectionResult` JSON.
- `--save-img` *(optional)*: File path to save the preview image with bounding box overlays.

---

## Programmatic Usage in Python

```python
from detection.infer import run_detection, save_annotated_image

# Run inference
result = run_detection("path/to/aerial_frame.jpg", conf=0.25)

print(f"Targets detected: {result.target_count}")
for target in result.detections:
    print(f"Target #{target.target_id}: bbox={target.bbox.to_xyxy_list()}, conf={target.confidence:.2f}")

# Render annotated image
save_annotated_image("path/to/aerial_frame.jpg", result, "detection/output/annotated.jpg")

# Export JSON
result.save_json("detection/output/result.json")
```

---

## Directory Structure
- `detection/infer.py` — Main inference engine and CLI runner
- `detection/samples/` — Reference aerial test images
- `detection/weights/` — Local drop-in directory for custom SARD model checkpoints (`best.pt`)
- `detection/output/` — Default export directory for annotated images and JSON results
