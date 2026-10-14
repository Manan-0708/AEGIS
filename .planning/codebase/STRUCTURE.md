# Codebase Structure

**Analysis Date:** 2026-10-14

## Directory Layout

```
AEGIS/
├── detection/                     # Computer Vision module (YOLO aerial target detection)
│   └── README.md                  # Module scope & ownership (Sujal / Vedant)
├── search_planning/               # Reinforcement Learning search trajectory optimization
│   └── README.md                  # Module scope & ownership (Sujal)
├── rag_agentic/                   # Knowledge retrieval and multi-agent decision system
│   ├── rag_pipeline/              # Document ingestion, chunking, embedding, ChromaDB
│   │   └── .gitkeep               # Directory placeholder
│   ├── agentic_layer/             # LangGraph multi-agent flow & decision agents
│   │   └── .gitkeep               # Directory placeholder
│   └── README.md                  # Module scope & ownership (Manan / Vedant)
├── route_dashboard/               # Extraction route planning (A*) and Streamlit dashboard
│   └── README.md                  # Module scope & ownership (Aryan)
├── shared/                        # Inter-module data contracts, schemas, and common utilities
│   └── README.md                  # Shared utilities overview
├── docs/                          # Project specifications, timelines, and architectural notes
│   ├── CHECKLIST.md               # Semester milestones, weekly deliverables & tickboxes
│   └── README.md                  # Documentation overview
├── .planning/                     # Project planning & codebase intelligence artifacts
│   └── codebase/                  # Codebase mapping documents (STACK, ARCHITECTURE, etc.)
├── .agent/                        # GSD automation workflows, skills, and tools
├── .gitignore                     # Git tracking exclusions (virtualenvs, datasets, weights)
└── README.md                      # Project root overview, team roles & Google Drive link
```

## Directory Purposes

**`detection/`:**
- Purpose: Houses the computer vision pipeline for aerial imagery target detection.
- Contains: Model definition, dataset loader routines, data augmentation pipelines (Albumentations), YOLO fine-tuning scripts, and inference wrappers.
- Key files: `detection/README.md` (module overview and ownership).
- Subdirectories (planned): `training/`, `models/`, `evaluation/`.

**`search_planning/`:**
- Purpose: Implements reinforcement learning agents for optimizing search trajectories in unmapped or partially observed sectors.
- Contains: Custom Gymnasium environments simulating aerial drone dynamics, reward functions, baseline fixed-pattern search algorithms, and PPO agent training loops.
- Key files: `search_planning/README.md` (module overview and ownership).
- Subdirectories (planned): `envs/`, `policies/`, `benchmarks/`.

**`rag_agentic/`:**
- Purpose: Houses the knowledge retrieval pipeline and LangGraph multi-agent orchestration layer.
- Contains:
  - `rag_pipeline/`: Knowledge base document parsers, chunking strategies, embedding wrappers, and ChromaDB vector store clients.
  - `agentic_layer/`: LangGraph `StateGraph` definition, Assessment Agent, Verification Agent, and Reporting Agent implementations.
- Key files: `rag_agentic/README.md`, `rag_agentic/rag_pipeline/.gitkeep`, `rag_agentic/agentic_layer/.gitkeep`.

**`route_dashboard/`:**
- Purpose: Computes safe ground extraction routes across terrain grids and serves the interactive operational dashboard.
- Contains: Dijkstra and A* pathfinding algorithms, elevation and terrain hazard cost matrices, FastAPI endpoints, and Streamlit visualization front-end.
- Key files: `route_dashboard/README.md` (module overview and ownership).
- Subdirectories (planned): `pathfinding/`, `api/`, `components/`.

**`shared/`:**
- Purpose: Central repository of shared data transfer objects, Pydantic data schemas, coordinate transformations, and configuration loaders.
- Contains: Standard data contracts linking detection outputs to agent inputs and pathfinding parameters.
- Key files: `shared/README.md` (shared utilities overview).
- Subdirectories (planned): `schemas/`, `utils/`.

**`docs/`:**
- Purpose: Semester project milestones, team task tracking, API specifications, and architectural documentation.
- Contains: Checklists, design specs, and progress tracking files.
- Key files: `docs/CHECKLIST.md` (semester timeline across 7 phases), `docs/README.md`.

**`.planning/codebase/`:**
- Purpose: Living system documentation capturing technology stack, architecture, conventions, testing, and tech debt.
- Contains: `STACK.md`, `ARCHITECTURE.md`, `STRUCTURE.md`, `CONVENTIONS.md`, `TESTING.md`, `INTEGRATIONS.md`, `CONCERNS.md`.

## Key File Locations

**Entry Points:**
- `route_dashboard/app.py` (planned) - Streamlit operational dashboard entry point
- `route_dashboard/api/main.py` (planned) - FastAPI backend server entry point
- `detection/inference.py` (planned) - Aerial frame inference entry point
- `search_planning/train_ppo.py` (planned) - RL agent training script

**Configuration:**
- `.gitignore` - Excluded files (virtualenvs, model checkpoints, raw video, datasets)
- `.env.example` (planned) - Environment variable definitions and provider keys
- `requirements.txt` / `pyproject.toml` (planned) - Project dependency definitions

**Core Logic:**
- `rag_agentic/agentic_layer/graph.py` (planned) - LangGraph orchestration pipeline
- `rag_agentic/rag_pipeline/retriever.py` (planned) - Hybrid search and reranking client
- `route_dashboard/pathfinding/astar.py` (planned) - A* terrain path calculation

**Testing & Evaluation:**
- `tests/` (planned) - Cross-module unit and integration tests
- `docs/CHECKLIST.md` - Phase-by-phase delivery and acceptance criteria

## Naming Conventions

**Files:**
- `snake_case.py` for Python modules and source files (`inference.py`, `train_ppo.py`, `state_graph.py`)
- `UPPERCASE.md` for major project reference files (`README.md`, `CHECKLIST.md`, `STACK.md`)
- `test_*.py` for automated test files (`test_retrieval.py`, `test_astar.py`)

**Directories:**
- `snake_case` for module subdirectories (`rag_pipeline`, `agentic_layer`, `search_planning`, `route_dashboard`)

**Classes & Types:**
- `PascalCase` for Python classes and Pydantic schemas (`DetectionResult`, `AssessmentAgent`, `TerrainCostGrid`)
- `UPPER_SNAKE_CASE` for constants (`DEFAULT_CONFIDENCE_THRESHOLD`, `MAX_GRID_DIMENSION`)

## Where to Add New Code

**New Detection Model or Preprocessing Logic:**
- Implementation: `detection/` (or `detection/models/`, `detection/training/`)
- Branch: `sujal-detection`
- Data contract schema: Update in `shared/schemas/`

**New Search Environment or Policy Algorithm:**
- Implementation: `search_planning/` (or `search_planning/envs/`)
- Branch: `sujal-search-planning`

**New RAG Pipeline Document or Embedder:**
- Implementation: `rag_agentic/rag_pipeline/`
- Branch: `vedant-rag-pipeline`

**New Decision Agent or LangGraph Node:**
- Implementation: `rag_agentic/agentic_layer/`
- Branch: `manan-agentic-layer`

**New Pathfinding Algorithm or Dashboard View:**
- Implementation: `route_dashboard/`
- Branch: `aryan-route-dashboard`

**New Shared Schema / Contract:**
- Implementation: `shared/schemas/`
- Coordination: Review across all module owners before merging into `testing`/`main`

## Special Directories

**External Data Directories (Local Only, Gitignored):**
- `data/` and `datasets/`: Local storage for SARD and MOBDrone images/videos
- Weights storage: Local storage for `*.pt`, `*.pth`, `*.onnx` model files
- Sourced from: Shared Google Drive (`https://drive.google.com/drive/folders/10CpW4MUXdUUGAECRarOE9qn1lQKXlFLo`)

---

*Structure analysis: 2026-10-14*
*Update when directory structure changes*
