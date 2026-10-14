# Phase 1: Aerial Person Detection Pipeline - Context

**Gathered:** 2026-10-14
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase delivers the core aerial person detection inference pipeline for AEGIS. It enables running person detection inference on aerial test imagery (using the SARD_YOLO dataset as reference) and exporting structured detection outputs (bounding boxes, confidence scores, labels) in a standardized JSON format.

**Owner:** Sujal (supported by Vedant)  
**Branch:** `sujal-detection`  
**Requirements Covered:** `DET-01`, `DET-02`, `DET-03`
</domain>

<decisions>
## Implementation Decisions

### Model Weights & Inference Strategy
- **D-01 (Flexible Weights Loader):** Default to standard pretrained Ultralytics YOLO (e.g. `yolov8n.pt` with COCO `person` class 0) out-of-the-box so inference runs immediately for testing and review without waiting on external checkpoint downloads.
- **D-02 (Custom Checkpoint Override):** If a custom-trained SARD weights file (`best.pt` or `sard.pt`) is present in `detection/weights/`, the pipeline automatically detects and prioritizes it.
- **D-03 (Detection Sensitivity):** Set default confidence threshold to `conf=0.25` and `iou=0.45` to reliably detect small aerial personnel targets from elevated drone perspectives, exposed as configurable CLI flags.

### Data Contract & Output Format
- **D-04 (Standardized JSON Schema):** Output detections must conform to a Pydantic `DetectionResult` contract containing `target_id`, `bbox` (`[x1, y1, x2, y2]` in pixel coordinates), `confidence`, `class_name` (`person`), image metadata (`image_path`, `width`, `height`), and timestamp.
- **D-05 (Export & Telemetry):** Provide an option to save serialized detection JSON to a designated results directory (`detection/output/`) for consumption by Aryan's dashboard in Phase 3.

### Runner Interface & Verification
- **D-06 (Dual Interface):** Provide both a CLI runner (`python detection/infer.py --source <image_or_dir> --conf 0.25`) for batch verification and an importable function (`run_detection(image_path) -> DetectionResult`) for downstream programmatic calls.
- **D-07 (Reference Test Samples):** Place a few reference SARD_YOLO sample aerial images in `detection/samples/` so any team member can verify detection immediately.

### the agent's Discretion
- Selection of specific Ultralytics model flavor (`yolov8n` vs `yolov8s` for lightweight CPU/GPU execution).
- Internal bounding box rendering utility (OpenCV color and line thickness).
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Specifications
- `.planning/PROJECT.md` — Core value, mid-term 1-day review scope, and team boundaries
- `.planning/REQUIREMENTS.md` §DET — Requirements `DET-01`, `DET-02`, `DET-03`
- `.planning/codebase/STACK.md` — Ultralytics, PyTorch, and OpenCV versions
- `.planning/codebase/CONVENTIONS.md` — Python naming conventions, type hints, and branching rules
- `detection/README.md` — Module ownership and support roles
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Modular subsystem scaffold in `detection/`
- Standard Python 3.11 environment with OpenCV and PyTorch compatibility

### Established Patterns
- Pydantic BaseModel contracts to be defined in `shared/schemas/` to govern all inter-module data transfer
- Git feature branch workflow: commits committed strictly to `sujal-detection`, never directly to `main`

### Integration Points
- `shared/schemas/detection.py` will define the `DetectionResult` model shared between `detection/` and `route_dashboard/`
- Detection output JSON files consumed by the Phase 3 Streamlit dashboard
</code_context>

<specifics>
## Specific Ideas

- Ensure detection bounding boxes are easily visualizable with confidence labels for the live demo review.
- Provide a clean sample output JSON so Aryan can mock the dashboard feed before live integration.
</specifics>

<deferred>
## Deferred Ideas

- Full model fine-tuning with Albumentations aerial data augmentation on full MOBDrone and SARD datasets (deferred to Phase 3/4 of semester roadmap).
- Video frame subsampling / RTSP streaming decoders (deferred to post-midterm phase).
</deferred>

---
*Phase: 01-aerial-person-detection-pipeline*  
*Context gathered: 2026-10-14*
