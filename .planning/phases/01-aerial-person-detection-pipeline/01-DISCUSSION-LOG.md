# Discussion Log: Phase 1 — Aerial Person Detection Pipeline

**Date:** 2026-10-14  
**Phase:** 1 of 4 (Aerial Person Detection Pipeline)  
**Status:** Completed  

---

## Areas Discussed

### 1. Model Weights & Inference Strategy
- **Question:** How should detection inference load its model weights given the 1-day deadline?
- **Options Presented:**
  1. Flexible YOLO loader (default to pretrained YOLO COCO person class with custom SARD override) [Selected]
  2. Strict SARD checkpoint only (require downloading *.pt from Google Drive)
- **Selection & Rationale:** Flexible loader selected. Prevents blocking review demo on missing or multi-hour training checkpoint downloads while allowing immediate override if weights are placed in `detection/weights/`.

### 2. Detection Sensitivity Thresholds
- **Question:** What confidence threshold should be the default for aerial imagery?
- **Options Presented:**
  1. Configurable threshold default conf=0.25, iou=0.45 [Selected]
  2. High confidence filter conf=0.50
- **Selection & Rationale:** `conf=0.25` selected because aerial drone imagery features small person targets with lower native confidence scores compared to eye-level photography.

---

## Key Decisions Captured
- **D-01:** Pretrained YOLO default with optional custom SARD weights override.
- **D-02:** Configurable CLI flags for `--conf` (default 0.25) and `--iou` (default 0.45).
- **D-03:** Structured JSON export adhering to shared `DetectionResult` schema for downstream Phase 3 dashboard integration.
- **D-04:** Dual interface: CLI runner `python detection/infer.py` and importable `run_detection()` function.
