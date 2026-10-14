<!-- GSD:project-start source:PROJECT.md -->
## Project

### AEGIS — Aerial Extraction & Guided Intelligent Search (Mid-Term Prototype)
AEGIS is an AI-driven decision-support system designed to locate isolated or injured personnel via aerial imagery, retrieve pertinent emergency medical and extraction procedures, and visualize operational tactical recommendations. This milestone targets a demonstrable mid-term prototype connecting aerial person detection, dashboard visualization, and grounded tactical RAG retrieval within a 1-day review deadline.

**Core Value:** A reliable, working end-to-end demonstration connecting aerial person detection on reference SARD_YOLO images, interactive dashboard visualization of actual detection outputs, and a grounded search-and-rescue RAG pipeline that answers queries with source citations.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

- **Language:** Python 3.11.x
- **Core AI/ML:** PyTorch, Ultralytics YOLO, Gymnasium, Stable-Baselines3, LangChain, LangGraph
- **Retrieval & DB:** ChromaDB, Sentence-Transformers
- **Application & Dashboard:** FastAPI, Uvicorn, Streamlit
- **Algorithms:** NumPy, OpenCV, NetworkX / SciPy (Dijkstra, A*)
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

- **Branching Policy:** Never push directly to `main`. Develop on designated feature branches (`sujal-detection`, `vedant-rag-pipeline`, `manan-agentic-layer`, `aryan-route-dashboard`) and open PRs against `testing`.
- **Integrity:** Do not fabricate training loss or detection metrics; preserve working modules and accurately represent progress.
- **Style:** Python `snake_case.py` files, `PascalCase` Pydantic models, type annotations on public signatures, structured `logging`.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Modular AI Decision-Support Pipeline connecting:
1. `detection/` (YOLO Aerial Target Detection)
2. `search_planning/` (RL Search Grid Exploration)
3. `rag_agentic/` (`rag_pipeline` ChromaDB retrieval + `agentic_layer` LangGraph multi-agent decision nodes)
4. `route_dashboard/` (FastAPI backend, A* pathfinding & Streamlit interactive dashboard)
5. `shared/` (Pydantic contracts & schemas)
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No custom external project skills found.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-plan-phase` to create detailed execution plans
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` — do not edit manually.
<!-- GSD:profile-end -->
