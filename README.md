# AEGIS
### Aerial Extraction & Guided Intelligent Search

AEGIS (Aerial Extraction & Guided Intelligent Search) is an AI-driven decision-support system for locating isolated/injured personnel via aerial imagery, planning efficient search coverage, retrieving correct recovery procedures, and computing safe routes to reach them.

---

## Project Structure & Module Ownership

| Module | Owner | Support | Folder |
|---|---|---|---|
| Detection (CV) | Sujal | Vedant | detection/ |
| Search Planning (RL) | Sujal | — | search_planning/ |
| RAG Pipeline | Manan | Vedant | rag_agentic/rag_pipeline/ |
| Agentic Layer | Manan | — | rag_agentic/agentic_layer/ |
| Route Planning + Dashboard | Aryan | — | route_dashboard/ |

---

## Datasets & Model Weights

> [!NOTE]
> All datasets and trained model weight files are hosted externally and maintained in a shared Google Drive (they are not tracked in this repository).
>
> **Google Drive Link:** `https://drive.google.com/drive/folders/10CpW4MUXdUUGAECRarOE9qn1lQKXlFLo`

---

## Workflow & Contribution Guidelines

Follow this standard Git workflow for all development work:

1. **Create a branch:** Create a feature or fix branch off `main` (`git checkout -b feature/your-feature-name`).
2. **Work & Commit:** Implement changes locally and commit with clear, descriptive commit messages.
3. **Push:** Push your feature branch to remote (`git push origin feature/your-feature-name`).
4. **Pull Request (PR):** Open a Pull Request targeting `main`.
5. **Review & Merge:** Obtain code review approval, address feedback, and merge into `main`.

> [!IMPORTANT]
> **Never push directly to `main` branch.** Always submit a Pull Request for review.
