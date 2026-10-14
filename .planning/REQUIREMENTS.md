# Requirements: AEGIS Mid-Term Prototype

**Defined:** 2026-10-14
**Core Value:** A reliable, working end-to-end demonstration connecting aerial person detection on reference SARD_YOLO images, interactive dashboard visualization of actual detection outputs, and a grounded search-and-rescue RAG pipeline that answers queries with source citations.

## v1 Requirements

Requirements for the 1-day mid-term review prototype. Each maps directly to roadmap phases.

### Aerial Detection (CV)

- [ ] **DET-01**: Operator can execute person detection inference on aerial test images using the SARD_YOLO reference dataset
- [ ] **DET-02**: Detection pipeline extracts structured bounding boxes, target class (`person`), and confidence scores
- [ ] **DET-03**: Detection outputs are formatted into standardized JSON data structures conforming to shared schemas

### Tactical RAG Pipeline

- [ ] **RAG-01**: Pipeline ingests, parses, and chunks search-and-rescue SOPs, first-aid protocols, and evacuation doctrine
- [ ] **RAG-02**: Vector storage (ChromaDB) indexes chunked doctrine with traceable source metadata (document name, section)
- [ ] **RAG-03**: Retriever performs semantic similarity search to return top relevant context passages for rescue queries
- [ ] **RAG-04**: System generates answers to operational queries strictly grounded in retrieved context with explicit source citations

### Operations Dashboard

- [ ] **DASH-01**: Dashboard displays aerial imagery with overlaid detection bounding boxes, target labels, and confidence scores
- [ ] **DASH-02**: Dashboard displays mission summary telemetry (detected target count, confidence levels, scenario status)
- [ ] **DASH-03**: Dashboard provides an interactive RAG query panel displaying retrieved doctrine passages alongside cited answers

### Integration & Stretch

- [ ] **INT-01**: Verification smoke test confirms end-to-end flow from aerial image detection to tactical response generation
- [ ] **ROUTE-01**: Basic search-priority grid or route visualization displayed on the dashboard interface (Stretch goal)

## v2 Requirements

Deferred to subsequent semester phases (Phases 3–7). Tracked for roadmap continuity.

### Reinforcement Learning Search Planning

- **RL-01**: Custom Gymnasium environment simulating UAV aerial search dynamics
- **RL-02**: PPO agent trained on search environment outperforming fixed-pattern baseline

### Multi-Agent Cognitive Verification

- **AGENT-01**: Full LangGraph multi-agent flow: Assessment Agent → Retrieval → Verification Agent → Reporting Agent
- **AGENT-02**: Automated contradiction detection checking operational constraints against doctrine

### Advanced Route Planning

- **ROUTE-02**: Cost-weighted A* pathfinding incorporating elevation delta, hazard zones, and surface friction
- **ROUTE-03**: Dynamic rerouting around newly detected obstacles

### Production Readiness & Streaming

- **STREAM-01**: Live RTSP aerial video stream decoding and frame-by-frame inference
- **DEPLOY-01**: Containerized deployment for field ground control stations

## Out of Scope

| Feature | Reason |
|---------|--------|
| Full PPO RL model training | Requires days of training iterations; deferred to final semester milestone |
| Deep multi-agent reflection loops | High token latency and failure modes for 1-day deadline; single grounded RAG pass is reliable |
| Real-time live drone hardware integration | Physical drone unavailable for mid-term lab demo; pre-recorded SARD_YOLO data suffices |
| Direct git push to `main` | Strict project rule: all changes must go through feature branches and PRs |
| Fabricating benchmark metrics | Academic and engineering integrity: report genuine prototype capabilities only |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DET-01 | Phase 1 | Pending |
| DET-02 | Phase 1 | Pending |
| DET-03 | Phase 1 | Pending |
| RAG-01 | Phase 2 | Pending |
| RAG-02 | Phase 2 | Pending |
| RAG-03 | Phase 2 | Pending |
| RAG-04 | Phase 2 | Pending |
| DASH-01 | Phase 3 | Pending |
| DASH-02 | Phase 3 | Pending |
| DASH-03 | Phase 3 | Pending |
| INT-01 | Phase 4 | Pending |
| ROUTE-01 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 12 total
- Mapped to phases: 12
- Unmapped: 0 ✓

---
*Requirements defined: 2026-10-14*
*Last updated: 2026-10-14 after initial definition*
