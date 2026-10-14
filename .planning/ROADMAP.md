# Roadmap: AEGIS Mid-Term Prototype

## Overview

This roadmap drives AEGIS toward a demonstrable mid-term prototype within a 1-day timeline. Built around the Vertical MVP principle, each phase delivers a tangible, testable capability assigned to specific team members: aerial person detection on reference SARD_YOLO imagery (Sujal/Vedant), grounded tactical rescue RAG Q&A with citations (Manan/Vedant), interactive operations dashboard (Aryan), and end-to-end integration with search/route visualization as a stretch goal (All).

## Phases

- [x] **Phase 1: Aerial Person Detection Pipeline** - Run person detection on SARD_YOLO aerial test images with structured JSON output (Sujal / Vedant)
- [ ] **Phase 2: Tactical Rescue RAG Knowledge Base** - Ingest rescue SOPs and deliver grounded Q&A with traceable source citations (Manan / Vedant)
- [ ] **Phase 3: Operations Dashboard UI** - Interactive Streamlit UI displaying detections, telemetry, and RAG query panel (Aryan)
- [ ] **Phase 4: End-to-End Integration & Stretch Visualization** - Verify connected pipeline demo and add basic search/route overlay if time allows (All)

## Phase Details

### Phase 1: Aerial Person Detection Pipeline
**Goal**: Run person detection on aerial test images using SARD_YOLO reference dataset and export structured bounding box outputs.
**Mode**: mvp
**Depends on**: Nothing (first phase)
**Requirements**: DET-01, DET-02, DET-03
**Owner**: Sujal (supported by Vedant)
**Branch**: `sujal-detection`
**Success Criteria**:
  1. Operator can run detection inference on reference aerial images from SARD_YOLO via a Python script.
  2. Output bounding boxes, `person` class label, and confidence scores are correctly extracted.
  3. Detection outputs are formatted into standardized JSON data structures conforming to shared schemas.
**Plans**: 1 plan

Plans:
- [x] 01-01: Implement SARD_YOLO inference script and structured JSON detection exporter

---

### Phase 2: Tactical Rescue RAG Knowledge Base
**Goal**: Ingest emergency rescue procedures and provide grounded Q&A with direct source document citations.
**Mode**: mvp
**Depends on**: Nothing (can run in parallel)
**Requirements**: RAG-01, RAG-02, RAG-03, RAG-04
**Owner**: Manan (supported by Vedant)
**Branch**: `vedant-rag-pipeline` / `manan-agentic-layer`
**Success Criteria**:
  1. Search-and-rescue SOPs and emergency medical guidelines are chunked and indexed in local ChromaDB.
  2. Tactical query interface retrieves relevant doctrine chunks based on natural language rescue questions.
  3. Generated answers are strictly grounded in retrieved passages and display explicit source document citations.
**Plans**: 1 plan

Plans:
- [ ] 02-01: Build document chunker, ChromaDB vector store index, and cited query retriever

---

### Phase 3: Operations Dashboard UI
**Goal**: Provide an interactive dashboard displaying actual aerial detection results and an interactive tactical RAG query panel.
**Mode**: mvp
**Depends on**: Phase 1, Phase 2
**Requirements**: DASH-01, DASH-02, DASH-03
**Owner**: Aryan
**Branch**: `aryan-route-dashboard`
**Success Criteria**:
  1. Dashboard renders aerial images with overlay bounding boxes, labels, and confidence tags.
  2. Mission summary panel displays detection telemetry (count of detected targets, confidence scores).
  3. Interactive RAG query component allows operator to ask rescue questions and view cited recommendations.
**Plans**: 1 plan

Plans:
- [ ] 03-01: Build Streamlit operational dashboard with detection visualizer and RAG query panel

---

### Phase 4: End-to-End Integration & Stretch Visualization
**Goal**: Verify complete end-to-end integration walkthrough and display basic search-priority or route visualization if time allows.
**Mode**: mvp
**Depends on**: Phase 1, Phase 2, Phase 3
**Requirements**: INT-01, ROUTE-01
**Owner**: All team members (coordinated by Manan)
**Branch**: `testing`
**Success Criteria**:
  1. Complete end-to-end mission scenario runs successfully from detection loading to tactical brief generation.
  2. Basic search-priority grid or safe approach route visualization is rendered if time permits (Stretch).
  3. Verification checklist confirms all demonstrated outputs are real and testable without fabrication.
**Plans**: 1 plan

Plans:
- [ ] 04-01: Execute end-to-end integration smoke test and optional route/priority visualizer

## Progress

**Execution Order:**
Phases execute in numeric order: 1 & 2 (parallel) → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Aerial Person Detection Pipeline | 1/1 | ✅ Complete | 2026-10-14 |
| 2. Tactical Rescue RAG Knowledge Base | 0/1 | 🔄 Next | - |
| 3. Operations Dashboard UI | 0/1 | Not started | - |
| 4. End-to-End Integration & Stretch | 0/1 | Not started | - |
