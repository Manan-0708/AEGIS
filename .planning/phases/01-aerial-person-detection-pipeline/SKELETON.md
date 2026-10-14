# Walking Skeleton — AEGIS Mid-Term Prototype

**Phase:** 1  
**Generated:** 2026-10-14  

## Capability Proven End-to-End

An operator can run person detection on an aerial reference image from the SARD_YOLO dataset via `detection/infer.py`, extracting detected target coordinates, confidence scores, and structured JSON telemetry that downstream dashboard and planning components can consume without schema divergence.

## Architectural Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Deep Learning Model | Ultralytics YOLO (v8n default with custom SARD override) | Fast inference on CPU/GPU without blocking review demo on long offline training cycles |
| Inter-Module Contract | Pydantic v2 `BaseModel` in `shared/schemas/detection.py` | Strict validation of coordinate formats across team branches |
| Detection Interface | Dual CLI + Importable API | Enables both standalone terminal verification and programmatic consumption by Streamlit dashboard |
| Storage & Weights | Local `detection/weights/` fallback with external Google Drive sourcing | Complies with repository size limits while preserving custom fine-tuned weights support |
| Branch Isolation | `sujal-detection` feature branch | Enforces branching policy; protects `main` and allows peer review by Vedant |

## Stack Touched in Phase 1

- [ ] Data Contract — `shared/schemas/detection.py` Pydantic models for `DetectionResult`
- [ ] Model Inference Engine — `detection/infer.py` with flexible YOLO weight resolution
- [ ] Reference Fixtures — `detection/samples/` reference aerial test imagery
- [ ] Output Serialization — `detection/output/` structured JSON export
- [ ] Test Verification — `tests/test_detection.py` test suite validating inference and contracts

## Out of Scope (Deferred to Later Slices)

- Multi-camera video frame streaming / RTSP decoders (deferred to post-midterm)
- Full Gymnasium PPO reinforcement learning search policy (deferred to Phase 4 / final semester review)
- Multi-agent contradiction checking in LangGraph (deferred to Phase 2/4)
- Complex multi-elevation 3D A* pathfinding (deferred to Phase 4)

## Subsequent Slice Plan

- **Phase 2:** Tactical Rescue RAG Knowledge Base (Manan / Vedant) — Ingest rescue SOPs and deliver cited answers
- **Phase 3:** Operations Dashboard UI (Aryan) — Render detections, mission summary, and RAG query panel
- **Phase 4:** End-to-End Integration & Stretch Visualization (All) — Connect detection to dashboard and optional route overlay
