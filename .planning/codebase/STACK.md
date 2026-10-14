# Technology Stack

**Analysis Date:** 2026-10-14

## Languages

**Primary:**
- Python 3.11.x - All core system modules, AI/ML pipelines, backend services, and dashboard

**Secondary:**
- Markdown - System documentation, module specs, API schemas, and checklists (`docs/`, `README.md`)
- Shell / PowerShell - Environment setup, automation scripts, and workflow execution

## Runtime

**Environment:**
- Python 3.11.8 (Standard CPython Runtime)
- OS: Cross-platform (Windows, Linux, macOS target support)
- Hardware acceleration: CUDA-enabled GPU (NVIDIA PyTorch runtime for YOLO fine-tuning & RL PPO training)

**Package Manager:**
- pip / venv (standard Python virtual environment)
- Lockfile: `requirements.txt` / `pyproject.toml` (standard virtual environment setup specified in `.gitignore`)

## Frameworks

**Core AI / ML:**
- PyTorch (>=2.0.0) - Core deep learning runtime for CV model training and RL tensor operations
- Ultralytics YOLO (v8/v9/v11) - Object detection model for aerial human and survivor identification
- Gymnasium (>=0.29.0) - Standard RL environment interface for aerial search simulation
- Stable-Baselines3 (>=2.0.0) - Proximal Policy Optimization (PPO) agent implementation for search planning
- LangChain / LangGraph (>=0.1.0) - Multi-agent orchestration, state graphs, and autonomous node transitions

**Information Retrieval & Embeddings:**
- ChromaDB - Vector database for embedded SOPs, rescue manuals, and medical triage doctrine
- Sentence-Transformers / Hugging Face Transformers - Local embeddings generation and cross-encoder reranking

**Application & Web Server:**
- FastAPI (>=0.100.0) - High-performance asynchronous REST API backend for module dispatch and telemetry
- Uvicorn (>=0.20.0) - ASGI web server implementation
- Streamlit (>=1.30.0) - Interactive operational mission dashboard (drone video feeds, map plots, tactical briefs)

**Algorithm & Computation:**
- NumPy (>=1.24.0) - Grid computations, array manipulations, and matrix operations
- OpenCV (cv2) - Imagery preprocessing, video frame extraction, and bounding box rendering
- NetworkX / SciPy - Graph representations, distance matrices, and Dijkstra / A* route planning

## Key Dependencies

**Critical:**
- `ultralytics` - Deep-learning aerial target detection pipeline in `detection/`
- `gymnasium` & `stable-baselines3` - Reinforcement learning simulation environment in `search_planning/`
- `chromadb` - Persistent vector database storage for tactical retrieval in `rag_agentic/rag_pipeline/`
- `langgraph` & `langchain-core` - StateGraph multi-agent flow (Assessment, Verification, Reporting) in `rag_agentic/agentic_layer/`
- `pydantic` (v2) - Strict data validation contracts across module boundaries in `shared/`
- `fastapi` - Microservice API bridging route planning, detection results, and dashboard in `route_dashboard/`
- `streamlit` - Field operator dashboard UI in `route_dashboard/`

**Infrastructure & Utilities:**
- `python-dotenv` - Environment variable loading (.env management)
- `albumentations` - Data augmentation for aerial camera angles, lighting conditions, and occlusions
- `pytest` - Automated unit and integration testing suite

## Configuration

**Environment:**
- `.env` files (excluded via `.gitignore`, template in `.env.example`)
- Key configurations:
  - `OPENAI_API_KEY` / `LOCAL_LLM_URL` - Model inference provider credentials
  - `CHROMA_PERSIST_DIR` - Storage path for vector database index
  - `MODEL_WEIGHTS_DIR` - Path to external weights downloaded from shared drive
  - `LOG_LEVEL` - Logging verbosity (DEBUG, INFO, WARNING, ERROR)

**Build & Tooling:**
- `.gitignore` - Standardized filters for virtualenvs (`.venv/`), weights (`*.pt`, `*.pth`, `*.onnx`), datasets, and cache files

## Platform Requirements

**Development:**
- Python 3.10+ / 3.11+
- CUDA-compatible GPU recommended for training YOLO and running local LLM embeddings/rerankers
- Minimum 16GB RAM for running local vector store and image inference simultaneously

**Production / Field Deployment:**
- Containerized Linux environment (Docker) or Edge Compute Unit on UAV ground control station
- External model weights and datasets downloaded from Google Drive: `https://drive.google.com/drive/folders/10CpW4MUXdUUGAECRarOE9qn1lQKXlFLo`

---

*Stack analysis: 2026-10-14*
*Update after major dependency changes*
