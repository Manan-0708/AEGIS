# Architecture

**Analysis Date:** 2026-10-14

## Pattern Overview

**Overall:** Modular AI Decision-Support Pipeline & Multi-Agent Orchestration

**Key Characteristics:**
- **Pipeline Architecture:** Sequential and asynchronous stages connecting aerial perception, autonomous search coverage, tactical procedure retrieval, multi-agent validation, and terrain pathfinding.
- **Contract-Driven Boundaries:** Inter-module communication governed by shared Pydantic schemas in `shared/`.
- **Hybrid AI Core:** Blends Deep Learning (Computer Vision), Reinforcement Learning (PPO Search Planning), Symbolic/Heuristic Graph Search (A* Pathfinding), and Multi-Agent LLMs (LangGraph).
- **Stateless Services with Persistent Vector Index:** Core computation modules execute statelessly per scenario while knowledge bases persist in ChromaDB.

## Layers

**Perception Layer (`detection/`):**
- Purpose: Detect isolated, injured, or stranded personnel in aerial drone video feeds
- Contains: Model inference wrappers, YOLO fine-tuning scripts, frame preprocessing, confidence thresholding
- Depends on: Pretrained/fine-tuned weights (`*.pt`) from external storage
- Used by: Pipeline coordinator and Agentic Layer

**Search Planning Layer (`search_planning/`):**
- Purpose: Optimize aerial search trajectories over unmapped or partially observed search grids
- Contains: Custom Gymnasium search environment, reward functions, PPO agent policy, baseline fixed-pattern search comparisons
- Depends on: Gymnasium, Stable-Baselines3, NumPy
- Used by: Autonomous mission planner when targets are not yet located

**Knowledge & Retrieval Layer (`rag_agentic/rag_pipeline/`):**
- Purpose: Retrieve relevant search-and-rescue SOPs, first aid protocols, and terrain evacuation guidelines
- Contains: Document ingestion parsers, semantic chunkers, embedding generators, ChromaDB vector store interface, and cross-encoder rerankers
- Depends on: ChromaDB, Sentence-Transformers, raw rescue doctrine documents
- Used by: Multi-agent orchestration layer

**Agentic Decision Layer (`rag_agentic/agentic_layer/`):**
- Purpose: Orchestrate automated triage assessment, protocol verification, and human-in-the-loop mission reporting
- Contains: LangGraph `StateGraph`, Assessment Agent, Verification Agent, and Reporting Agent
- Depends on: LangGraph, LangChain, RAG pipeline, and detection outputs
- Used by: Route planning and dashboard layer

**Pathfinding Layer (`route_dashboard/`):**
- Purpose: Compute safe ground extraction routes to reach located targets across hazardous terrain
- Contains: Terrain cost grid models, Dijkstra baseline, A* pathfinding algorithm, waypoint generators
- Depends on: NumPy, NetworkX / SciPy, coordinates from detection layer
- Used by: Mission Dashboard and field responders

**Presentation & API Layer (`route_dashboard/`):**
- Purpose: Deliver interactive visualization for rescue teams and serve backend REST endpoints
- Contains: FastAPI REST routes (`/api/v1/*`), Streamlit operational dashboard components (video player, tactical map, action checklist)
- Depends on: FastAPI, Streamlit, and downstream module wrappers
- Used by: Field operators and ground rescue commanders

**Shared Utilities & Schemas (`shared/`):**
- Purpose: Provide common data schemas, coordinate converters, and utility functions
- Contains: Pydantic models for `DetectionResult`, `SearchPlan`, `RAGQuery`, `ExtractionRoute`, `MissionReport`
- Depends on: Pydantic, Python standard library
- Used by: All modules

## Data Flow

**End-to-End Rescue Mission Execution Flow:**

```
1. Aerial Video Frame / Coordinates
                │
                ▼
      [ Detection (CV) ] ──────── (Target not found) ──► [ Search Planning (RL) ]
                │                                                    │
         (Target detected)                                  (Optimal search grid)
                │                                                    │
                ▼                                                    ▼
      [ Assessment Agent ] ◄─────────────────────────────────────────┘
                │
                ▼
      [ RAG Retrieval (ChromaDB) ] ── (Fetch SOPs / medical guidelines)
                │
                ▼
      [ Verification Agent ] ───────── (Contradiction / sanity check)
                │
                ▼
      [ Reporting Agent ] ──────────── (Synthesize tactical brief)
                │
                ▼
      [ Route Planning (A*) ] ──────── (Compute safe ground path)
                │
                ▼
      [ Dashboard (Streamlit) ] ────── (Display map, feed & rescue brief)
```

1. **Target Identification:** Aerial video feed streams into `detection/`. YOLO detects personnel, outputting bounding box, target class, and confidence score.
2. **Search Coverage (if needed):** If target is undetected, `search_planning/` RL agent computes the next optimal search trajectory over the operational sector.
3. **Context Assessment:** The `Assessment Agent` in `rag_agentic/agentic_layer/` evaluates detection confidence, environmental conditions, and situational urgency.
4. **Doctrine Retrieval:** `rag_agentic/rag_pipeline/` retrieves relevant rescue protocol and medical triage guidelines from ChromaDB.
5. **Verification & Contradiction Check:** The `Verification Agent` audits retrieved instructions against current constraints (e.g., forbidding helicopter hoist in high winds).
6. **Reporting:** The `Reporting Agent` compiles a standardized, actionable mission brief.
7. **Extraction Route Generation:** `route_dashboard/` takes target coordinates and terrain elevation/hazard matrices, running A* to plot the safest ground extraction corridor.
8. **Operational Display:** Results populate the `route_dashboard/` Streamlit UI for commanding officers.

**State Management:**
- Inter-agent state tracked in LangGraph `AgentState` TypedDict/Pydantic schema (holding image metadata, detection output, retrieved documents, validation flags, and final report).
- Persistent state saved to disk for ChromaDB vector indices; operational sessions remain stateless per scenario.

## Key Abstractions

**DetectionResult (`shared/`):**
- Purpose: Standardized representation of CV model inference
- Attributes: `target_id`, `bbox`, `confidence`, `timestamp`, `gps_coordinates`
- Pattern: Immutable Pydantic BaseModel

**MissionState (`rag_agentic/agentic_layer/`):**
- Purpose: Central state payload threaded through LangGraph nodes
- Attributes: `detection_data`, `triage_level`, `retrieved_docs`, `verification_passed`, `report_text`, `route_waypoints`
- Pattern: LangGraph StateGraph dictionary/model

**TerrainGrid (`route_dashboard/`):**
- Purpose: 2D representation of operational area with associated traversal cost weights
- Attributes: Elevation delta, water barriers, vegetation density, hazard zones
- Pattern: Cost Matrix / Weighted Graph for A* algorithm

**Retriever (`rag_agentic/rag_pipeline/`):**
- Purpose: Unified query interface for hybrid dense + reranked search
- Pattern: Strategy pattern wrapping ChromaDB collection queries and Cross-Encoder ranking

## Entry Points

**API Gateway:**
- Location: `route_dashboard/api/main.py` (planned)
- Triggers: HTTP REST requests from dashboard or external systems
- Responsibilities: Input validation, module dispatch, aggregating pipeline outputs

**Dashboard UI:**
- Location: `route_dashboard/app.py` (planned)
- Triggers: User launch (`streamlit run route_dashboard/app.py`)
- Responsibilities: Render map overlays, drone video feed, and tactical triage panels

**Batch Evaluation Scripts:**
- Location: `detection/evaluate.py`, `search_planning/train_ppo.py`, `rag_agentic/eval.py`
- Triggers: Command-line runs for model benchmarking and metrics compilation

## Error Handling

**Strategy:** Fail-safe defaults with structured fallback responses.
- In `detection/`: Low confidence detections trigger a "Search Area" recommendation rather than false alarms.
- In `rag_agentic/`: If RAG retrieval returns zero confident matches or the Verification Agent identifies direct contradictions, the system falls back to standard general triage rules and flags a human operator warning.
- In `route_dashboard/`: If A* cannot find a zero-risk path to the target, it identifies the nearest safe rendezvous point and calculates an approach corridor.

## Cross-Cutting Concerns

**Data Contracts:**
- All inter-module payload exchanges must adhere to Pydantic definitions in `shared/` to allow independent parallel development across team branches.

**Logging:**
- Python standard `logging` configured with timestamps, module names, and severity levels.

**Security & Secrets:**
- All sensitive credentials (`OPENAI_API_KEY`, tokens) loaded strictly via environment variables; never hardcoded in source.

---

*Architecture analysis: 2026-10-14*
*Update when major patterns change*
