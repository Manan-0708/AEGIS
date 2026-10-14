# AEGIS — Aerial Extraction & Guided Intelligent Search

## What This Is

AEGIS is an AI-driven decision-support system designed to locate isolated or injured personnel via aerial imagery, retrieve pertinent emergency medical and extraction procedures, and visualize operational tactical recommendations. This milestone targets a demonstrable mid-term prototype connecting aerial person detection, dashboard visualization, and grounded tactical RAG retrieval within a 1-day review deadline.

## Core Value

A reliable, working end-to-end demonstration connecting aerial person detection on reference SARD_YOLO images, interactive dashboard visualization of actual detection outputs, and a grounded search-and-rescue RAG pipeline that answers queries with source citations.

## Requirements

### Validated

- ✓ Modular repository structure with 5 decoupled subsystem directories (`detection/`, `search_planning/`, `rag_agentic/`, `route_dashboard/`, `shared/`) — Phase 1 setup
- ✓ Complete codebase intelligence mapping documented in `.planning/codebase/` (922 lines across 7 files) — Phase 1 setup
- ✓ Git workflow and multi-branch team ownership established (`sujal-detection`, `vedant-rag-pipeline`, `manan-agentic-layer`, `aryan-route-dashboard`, `testing`, `main`) — Phase 1 setup

### Active

- [ ] **DET-01**: Working person detection inference pipeline running on aerial images using SARD_YOLO reference dataset (Sujal / Vedant)
- [ ] **DASH-01**: Operational dashboard UI displaying actual aerial detection results with bounding boxes, labels, and confidence scores (Aryan)
- [ ] **RAG-01**: Ingestion and chunking of emergency rescue doctrines, standard operating procedures, and medical triage documents into vector storage (Manan / Vedant)
- [ ] **RAG-02**: Grounded Q&A retrieval answering tactical rescue queries with direct source document references and citations (Manan)
- [ ] **ROUTE-01**: Basic search-priority or route visualization displayed on the dashboard interface if time allows (Aryan / Sujal — Stretch)
- [ ] **INT-01**: End-to-end integration walkthrough verifying detection-to-dashboard and query-to-RAG flows without fabrication (All)

### Out of Scope

- Full PPO Reinforcement Learning agent training in Gymnasium — deferred to Phase 3/4 final milestone; baseline simulation or static priority suffices for mid-term review
- Complex multi-agent contradiction-checking and self-correcting loops in LangGraph — deferred to Phase 4; simple grounded RAG with source verification is required for mid-term
- Real-time live drone hardware telemetry or RTSP stream decoders — pre-recorded test images/video from SARD_YOLO are used for the demo
- Direct pushes to `main` branch — all development must use feature branches with reviews
- Rebuilding existing scaffolding or fabricating mock results — preserve real progress and report status honestly

## Context

- **Team Ownership:**
  - Sujal: Computer Vision & Search Planning
  - Vedant: Dataset validation, CV support & integration testing
  - Manan: RAG pipeline & Agentic Layer (Project lead)
  - Aryan: Route planning & Dashboard
- **Dataset & Weights:** Hosted on external Google Drive (`https://drive.google.com/drive/folders/10CpW4MUXdUUGAECRarOE9qn1lQKXlFLo`). Local testing uses reference SARD_YOLO images.
- **Timeline:** Exactly 1 day remaining before the mid-term review.

## Constraints

- **Timeline**: 1 day hard deadline before mid-term review — demands smallest testable, working end-to-end slice.
- **Git Workflow**: Never push directly to `main`; develop on feature branches and merge through PRs.
- **Integrity**: Do not fabricate training loss or detection metrics; preserve working modules and accurately represent progress.
- **Simplicity**: Focus on testable, modular tasks that each assigned team member can complete and explain independently.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Focus on 3 core pillars for mid-term (Detection + Dashboard + RAG with citations) | 1-day timeline prevents full RL and deep multi-agent completion; a working vertical slice is far more valuable for review | ✓ Good |
| Treat search priority and route planning as stretch goals | Ensures team does not risk core detection and RAG deliverables | ✓ Good |
| Ground RAG answers strictly with source references | Prevents LLM hallucinations during live review and provides auditable advice | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-10-14 after initialization for Mid-Term Prototype*
