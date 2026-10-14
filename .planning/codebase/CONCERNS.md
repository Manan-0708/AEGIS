# Codebase Concerns

**Analysis Date:** 2026-10-14

## Tech Debt

**Lack of Formalized Data Contracts in Code:**
- Issue: Inter-module contracts are documented conceptually in READMEs and checklists, but concrete Pydantic schemas in `shared/` are not yet committed.
- Files: `shared/README.md`, `rag_agentic/README.md`, `detection/README.md`, `route_dashboard/README.md`
- Why: Project is transitioning from Phase 1 (foundations & setup) to Phase 2 (MVP modules).
- Impact: Team members developing on independent branches (`sujal-detection`, `vedant-rag-pipeline`, `aryan-route-dashboard`, `manan-agentic-layer`) risk implementing diverging coordinate systems, bounding box formats (xyxy vs xywh), and JSON structures.
- Fix approach: Implement core Pydantic DTOs (`DetectionResult`, `SearchPlan`, `RAGQuery`, `ExtractionRoute`, `MissionReport`) in `shared/schemas.py` immediately and merge to `main`.

**Manual Asset & Weights Retrieval from Google Drive:**
- Issue: Datasets (SARD, MOBDrone) and model checkpoints (`*.pt`, `*.pth`) are hosted on external Google Drive (`https://drive.google.com/drive/folders/10CpW4MUXdUUGAECRarOE9qn1lQKXlFLo`) without automated download or verification scripts.
- Files: `README.md`, `.gitignore`
- Why: File size limits in GitHub prohibit committing multi-gigabyte video datasets and neural network weights.
- Impact: Inconsistent model versions across developer environments, broken paths, and friction during local testing.
- Fix approach: Create a helper script (`scripts/download_assets.py`) using `gdown` or Google Drive API with MD5 checksum verification.

**Absence of Root Dependency Manifest:**
- Issue: No root `requirements.txt` or `pyproject.toml` exists in the repository.
- Files: Project root
- Why: Module owners have been running independent "hello world" scripts in their own virtualenvs during Week 1-2.
- Impact: Dependency version conflicts (e.g. PyTorch CUDA build compatibility vs LangGraph vs NumPy 2.x breaking changes).
- Fix approach: Establish a unified `requirements.txt` pinning tested versions for PyTorch, Ultralytics, Gymnasium, LangGraph, ChromaDB, FastAPI, and Streamlit.

## Known Bugs

*(None currently active in committed code — repository is in foundational setup stage with clean directory scaffolds).*

## Security Considerations

**API Key Exposure Risk in Multi-Branch Collaboration:**
- Risk: Developers writing exploratory RAG/agent scripts may accidentally hardcode `OPENAI_API_KEY` or Hugging Face tokens in test scripts.
- Files: `rag_agentic/`, `.env`
- Current mitigation: `.gitignore` contains rules for `.env` and `.env.*`.
- Recommendations: Add pre-commit hooks (`detect-secrets`) and ensure all agent code exclusively reads credentials via `os.environ` or Pydantic `BaseSettings`.

**Unbounded User Inputs on FastAPI / Streamlit Endpoints:**
- Risk: Passing arbitrarily large grid dimensions or malformed aerial image payloads could trigger out-of-memory (OOM) crashes or Denial of Service on edge machines.
- Files: `route_dashboard/api/` (planned), `route_dashboard/app.py` (planned)
- Recommendations: Enforce strict Pydantic payload size validation and timeout caps on pathfinding and CV inference requests.

## Performance Bottlenecks

**High-Resolution Video Inference Latency:**
- Problem: Aerial drone video streams (1080p / 4K) processed at 30 FPS will overwhelm standard CPU or modest GPU runtimes if every frame undergoes full YOLO inference.
- Files: `detection/`
- Impact: Video playback stutter and laggy detection alerting in dashboard.
- Improvement path: Implement frame-skipping / temporal subsampling (e.g., inferencing 2-5 FPS), frame resizing, and batch inference.

**Large Terrain Grid Pathfinding Latency:**
- Problem: Standard A* on high-resolution terrain grids (e.g., 1000x1000 or greater) experiences exponential search tree expansion without efficient heuristics.
- Files: `route_dashboard/pathfinding/`
- Impact: Delayed extraction route computation for field rescue personnel.
- Improvement path: Use NumPy-accelerated distance matrices, bidirectional A*, or hierarchical graph abstraction (HPA*).

**Local Cross-Encoder Reranking Latency:**
- Problem: Running deep Transformer rerankers on CPU for every RAG retrieval step can add 1-3 seconds to agent response times.
- Files: `rag_agentic/rag_pipeline/`
- Improvement path: Cache frequent query embeddings and use lightweight cross-encoders (e.g., `ms-marco-MiniLM-L-6-v2`) or limit reranking pool to top 5 candidates.

## Fragile Areas

**Coordinate System Alignment Across Pipeline Boundaries:**
- Files: `detection/`, `shared/schemas/`, `route_dashboard/`
- Why fragile: Aerial imagery detection operates in 2D image pixel space `(u, v)`. Ground search planning operates in discrete grid cells `(row, col)`. Route planning and GIS maps operate in GPS coordinates `(lat, lon)`.
- Common failures: Off-by-one errors, inverted axes (x/y vs lat/lon vs row/col), scale factor distortions sending rescue teams miles off target.
- Safe modification: Centralize all coordinate transformations into tested utility functions in `shared/coordinates.py`.

**LangGraph Multi-Agent Contradiction Verification:**
- Files: `rag_agentic/agentic_layer/`
- Why fragile: LLM prompt sensitivity can lead to false positives (falsely blocking valid rescue plans) or false negatives (passing contradictory/hazardous evacuation advice).
- Safe modification: Enforce structured JSON schema outputs with explicit reasoning fields, and maintain deterministic safety check rules before relying on LLM judgment.

## Scaling Limits

**Local Vector Store (ChromaDB):**
- Current capacity: In-memory / SQLite-backed ChromaDB suitable for thousands of documents.
- Limit: Performance degrades if millions of chunks are indexed without distributed vector clustering.
- Status for AEGIS: Entirely adequate for the targeted rescue manuals, SOPs, and triage documentation.

**Hardware Concurrency on Single Developer Machine:**
- Current capacity: Running YOLO inference, PyTorch PPO training, local embedding models, and Streamlit concurrently will exceed single-GPU VRAM (especially on 6GB/8GB laptops).
- Scaling path: Isolate training to offline cloud GPU runs (Google Colab / external compute) while local development runs inference using lightweight checkpoints or ONNX runtime.

## Dependencies at Risk

**PyTorch & CUDA Version Fragmentation:**
- Risk: Different team members running Windows vs Linux with different CUDA drivers (CUDA 11.8 vs 12.1 vs 12.4).
- Impact: "Torch not compiled with CUDA enabled" errors when running teammate branches.
- Mitigation plan: Document the exact supported PyTorch/CUDA installation command in `docs/README.md`.

**LangChain / LangGraph Fast API Drift:**
- Risk: LangGraph undergoes frequent minor version releases with changing state graph syntax.
- Impact: Deprecation warnings or broken graph compilations across updates.
- Migration plan: Pin exact version `langgraph==0.2.*` in dependencies.

## Missing Critical Features (To be built in Phases 2-5)

**Pydantic Data Contracts:**
- Status: Missing in `shared/`
- Blocks: Cross-module pipeline verification
- Complexity: Low (1-2 days effort)

**Automated Test Suite:**
- Status: No tests currently exist
- Blocks: Safe continuous integration
- Complexity: Medium (build unit tests alongside Phase 2 MVPs)

**FastAPI Dispatch Gateway:**
- Status: Not yet implemented
- Blocks: Programmatic pipeline execution between detection and dashboard
- Complexity: Medium

## Test Coverage Gaps

**Entire Codebase:**
- What's not tested: No automated test files currently exist in the repository (`tests/` directory missing).
- Risk: Regression bugs and interface mismatches will remain undetected until manual testing.
- Priority: High.
- Plan: Stand up `tests/test_shared_schemas.py` and module-level unit tests during Phase 2 MVP development.

---

*Concerns audit: 2026-10-14*
*Update as issues are fixed or new ones discovered*
