# AEGIS
### Aerial Extraction & Guided Intelligent Search

AEGIS (Aerial Extraction & Guided Intelligent Search) is an AI-driven decision-support system for locating isolated/injured personnel via aerial imagery, planning efficient search coverage, retrieving correct recovery procedures, and computing safe routes to reach them.

---

## Project Structure & Module Ownership

| Module | Description | Owner | Folder Path |
| :--- | :--- | :--- | :--- |
| **Detection** | Detection Model | Manan | [`detection/`](detection/) |
| **Search Planning** | Search Planning RL Model | Sujal | [`search_planning/`](search_planning/) |
| **RAG + Agentic** | RAG + Agentic Layer | Vedant | [`rag_agentic/`](rag_agentic/) |
| **Route & Dashboard** | Route Planning + Dashboard | Aryan | [`route_dashboard/`](route_dashboard/) |

---

## Datasets & Model Weights

> [!NOTE]
> All datasets and trained model weight files are hosted externally and maintained in a shared Google Drive (they are not tracked in this repository).
>
> **Google Drive Link:** `[INSERT_GOOGLE_DRIVE_LINK_HERE]`

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
