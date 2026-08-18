# AEGIS — Semester Checklist & Timeline
*Tick boxes as items get completed. Works natively on GitHub (clickable checkboxes) — for a shared Google Doc version, this same list pastes in cleanly and Google Docs will auto-convert `[ ]` into checkboxes.*

---

## Phase 1 — Foundations & Setup (Weeks 1-2)

- [ ] Repo cloned and working locally (All)
- [ ] Dev environment set up (All)
- [ ] Datasets downloaded — SARD, MOBDrone (Sujal)
- [ ] Study: CNN/YOLO fundamentals (Sujal)
- [ ] Study: RL fundamentals (Sujal)
- [ ] Study: RAG fundamentals + ChromaDB basics (Vedant)
- [ ] Study: LangGraph + agentic patterns (Manan)
- [ ] Study: Dijkstra/A*, FastAPI, Streamlit basics (Aryan)
- [ ] Data-format contracts defined between all modules (Manan)
- [ ] Pretrained YOLO run on sample image, zero fine-tuning — baseline check (Sujal)
- [ ] "hello world" test in each person's own tooling done (All)

---

## Phase 2 — Core Module MVPs (Weeks 3-6)

- [ ] Baseline detection model fine-tuned on SARD only (Sujal)
- [ ] Baseline fixed-pattern search simulation working (Sujal)
- [ ] RAG: document collection done (Vedant)
- [ ] RAG: chunking pipeline working (Vedant)
- [ ] RAG: embeddings + basic retrieval working on small test set (Vedant)
- [ ] LangGraph skeleton — single retrieval node, hardcoded test question (Manan)
- [ ] Assessment / Verification / Reporting agent structure defined (Manan)
- [ ] Dijkstra working on small hand-made grid (Aryan)
- [ ] Basic FastAPI endpoint skeleton (Aryan)
- [ ] **Milestone check-in: all 4 modules have a rough working MVP**

---

## Phase 3 — Core AI Depth (Weeks 7-9)

- [ ] Augmentation added to detection training (Sujal)
- [ ] Detection evaluated — precision/recall/mAP (Sujal)
- [ ] Custom Gymnasium search environment built (Sujal)
- [ ] First PPO agent trained on search environment (Sujal)
- [ ] Hybrid/semantic search + reranking added to RAG (Vedant)
- [ ] Full doctrine/guidance knowledge base loaded (Vedant)
- [ ] Assessment Agent built — confidence-based decision logic (Manan)
- [ ] Verification Agent built — contradiction checking (Manan)
- [ ] A* implemented, upgraded from Dijkstra (Aryan)
- [ ] Terrain cost variation added to grid (Aryan)
- [ ] **Milestone check-in: real AI/ML depth demonstrated in every module**

---

## Phase 4 — Agentic & Integration Layer (Weeks 10-11)

- [ ] Reporting Agent built (Manan)
- [ ] Full LangGraph flow connected: Assessment → Retrieval → Verification → Reporting (Manan)
- [ ] PPO search agent compared vs. baseline (Sujal)
- [ ] Detection scaled up with MOBDrone, if time allows (Sujal)
- [ ] RAG-to-agent handoff refined (Vedant, supporting Manan)
- [ ] Chunking refined based on real retrieval test results (Vedant)
- [ ] Streamlit dashboard shell built — video/map/report panels, placeholder data (Aryan)
- [ ] **Milestone check-in: agentic layer works end to end; dashboard shell exists**

---

## Phase 5 — Full Pipeline Integration (Weeks 12-13)

- [ ] Detection → search-decision connected (Manan)
- [ ] Search-decision → RAG/agent connected (Manan)
- [ ] RAG/agent → route planning connected (Manan)
- [ ] Route planning → dashboard connected (Manan)
- [ ] Integration bugs fixed, data formats aligned (All)
- [ ] Full pipeline tested with real sample scenarios, start to finish (All)
- [ ] **Milestone check-in: one working, connected system runs end to end**

---

## Phase 6 — Evaluation (Week 14)

- [ ] Final detection metrics compiled — across terrain/altitude/occlusion (Sujal)
- [ ] Search-planning efficiency vs. baseline compiled (Sujal)
- [ ] RAG evaluation — retrieval precision/recall, faithfulness (Vedant)
- [ ] Route-planning evaluation — route quality vs. baseline (Aryan)
- [ ] End-to-end system evaluation — time-to-viable-route vs. naive baseline (Manan)
- [ ] All results compiled into comparison tables/plots (Manan)
- [ ] **Milestone check-in: real experimental results exist, not just screenshots**

---

## Phase 7 — Polish, Demo Prep, Documentation (Weeks 15-16)

- [ ] Bug fixes across all modules (All)
- [ ] UI polish on dashboard (Aryan)
- [ ] Live demo rehearsed at least twice, full run-through (All)
- [ ] Final project report written (Manan, with input from all)
- [ ] Everyone can explain their own module in depth (All)
- [ ] Everyone can explain the system as a whole, not just their part (All)
- [ ] **Final check: ready for demo, viva, and submission**

---

## Ongoing / Every Week (applies throughout)

- [ ] Pushed progress to own branch at least every 2-3 days
- [ ] Attended weekly team sync
- [ ] PRs opened against `testing`, not `main`
- [ ] Blockers flagged within 20-30 minutes of getting stuck, not sat on silently
