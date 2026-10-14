# Phase 1 Summary — Aerial Person Detection Pipeline

**Status:** ✅ COMPLETE  
**Branch:** `sujal-detection`  
**Commits:** `0c2609e` (schemas), `fde65e1` (inference engine + tests)  
**Date:** 2026-10-14

---

## What Was Built

### 1. Shared Schema Contract — `shared/schemas/detection.py`
- `BoundingBox` (Pydantic v2): x1, y1, x2, y2 with float validation
- `DetectionItem`: bbox + label + confidence + class_id
- `DetectionResult`: top-level output with source_image, timestamp, detections list, and detection_count computed field
- `shared/schemas/__init__.py` exports all three models

### 2. Inference Engine — `detection/infer.py`
- `run_detection(source, weights, conf_threshold, iou_threshold)` → `DetectionResult`
  - Auto-resolves weights: scans `detection/weights/*.pt` first, falls back to `yolov8n.pt` pretrained
  - Filters COCO classes to `[0]` (person) when using pretrained weights; all classes when custom SARD weights loaded
  - Tensor-safe coordinate extraction (`hasattr` guards for `.tolist()` / `.item()`)
- `save_annotated_image(source, result, output_path)`: draws bounding boxes via OpenCV, saves JPEG
- CLI entry point: `python detection/infer.py --source <img> [--weights <.pt>] [--conf 0.25] [--save-json <path>] [--save-img <path>]`

### 3. Test Fixture — `detection/samples/`
- `generate_sample.py`: creates a synthetic 640×480 gray aerial image with subtle gradient and text annotation
- `reference_aerial.jpg`: the generated fixture committed to repo

### 4. CLI Demo Outputs — `detection/output/`
- `demo_detections.json`: JSON output from CLI run on reference_aerial.jpg (0 detections — expected on synthetic fixture with pretrained weights)
- `demo_annotated.jpg`: OpenCV-annotated preview image

### 5. Test Suite — `tests/test_detection.py`
- 8 tests covering:
  - Schema construction and `detection_count` computed field
  - `BoundingBox` field validation
  - `run_detection()` return type, field presence, and non-negativity
  - `save_annotated_image()` file creation
  - CLI smoke test via `subprocess.run`
- **All 8 tests passed** ✅

### 6. Documentation — `detection/README.md`
- Updated with CLI usage examples, weight resolution logic, and output format

---

## Verification Results

| Check | Result |
|---|---|
| `pytest tests/test_detection.py` | 8/8 passed ✅ |
| `demo_detections.json` exists | ✅ |
| `demo_annotated.jpg` exists | ✅ |
| CLI exits with code 0 | ✅ |
| Schema contract importable from `shared.schemas` | ✅ |

---

## Key Decisions & Gotchas

1. **Tensor guard for xyxy coords:** `box.xyxy[0]` returns a PyTorch tensor in GPU context but a list in CPU-only environments. Used `hasattr(x, "tolist")` and `hasattr(x, "item")` for safe extraction.
2. **Class filter for pretrained weights:** COCO `yolov8n.pt` contains 80 classes. Filtered to `classes=[0]` (person only) at inference time to prevent false positives on vehicles, animals, etc. Custom SARD weights skip this filter.
3. **Synthetic fixture produces 0 detections:** This is correct behavior — a blank aerial gradient image has no discernible human figures. Real SARD_YOLO dataset images should yield detections when custom weights are provided.

---

## Downstream Contract

All Phase 2 (RAG), Phase 3 (Dashboard), and Phase 4 (Route Planning) modules **must** consume:

```python
from shared.schemas.detection import DetectionResult, DetectionItem, BoundingBox
```

The `DetectionResult` JSON schema is the single source of truth for inter-module data exchange.
