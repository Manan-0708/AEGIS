# Coding Conventions

**Analysis Date:** 2026-10-14

## Naming Patterns

**Files & Directories:**
- `snake_case.py` for all Python modules (`inference.py`, `search_env.py`, `retriever.py`, `pathfinder.py`)
- `test_*.py` for automated test files (`test_detection.py`, `test_state_graph.py`)
- `UPPERCASE.md` for major repository documentation (`README.md`, `CHECKLIST.md`)
- `snake_case` for all Python packages and directory names (`rag_pipeline`, `agentic_layer`, `search_planning`, `route_dashboard`)

**Classes & Models:**
- `PascalCase` for all classes, agents, and Pydantic schemas (`DetectionResult`, `AssessmentAgent`, `TerrainGrid`, `VerificationResult`)
- Custom exceptions suffixed with `Error` (`PipelineIntegrationError`, `InvalidCoordinatesError`, `ModelInferenceError`)

**Functions & Methods:**
- `snake_case` for functions and methods (`detect_targets()`, `calculate_route()`, `retrieve_context()`, `format_mission_report()`)
- Descriptive verb-noun combinations (`get_bounding_boxes()`, `validate_safety_constraints()`)
- Async functions use standard `async def` without special prefixes

**Variables & Constants:**
- `snake_case` for local variables and parameters (`target_coordinates`, `confidence_threshold`, `terrain_map`)
- `UPPER_SNAKE_CASE` for global and module constants (`DEFAULT_IOU_THRESHOLD`, `MAX_SEARCH_STEPS`, `CHROMA_COLLECTION_NAME`)
- Private helper functions or class attributes prefixed with single underscore (`_extract_features()`, `_calculate_heuristic()`)

**Type Annotations:**
- Mandatory type hints on all public function signatures and class definitions (`def plan_route(start: Tuple[int, int], goal: Tuple[int, int], grid: np.ndarray) -> List[Tuple[int, int]]:`)
- Pydantic BaseModel utilized for all structured data passed across module interfaces

## Code Style

**Formatting:**
- Black / Ruff formatting standard
- Line length: 88 characters (Black standard) or maximum 100 characters
- Indentation: 4 spaces per indentation level (no tabs)
- Double quotes for strings, triple double quotes for docstrings (`"""..."""`)

**Linting & Quality:**
- Flake8 / Ruff linting for PEP 8 compliance
- No unused imports or variables permitted in merged code
- Type checking with `mypy` across `shared/` contracts

## Import Organization

**Order:**
1. Python standard library imports (`os`, `sys`, `time`, `typing`, `pathlib`, `logging`)
2. Third-party library imports (`torch`, `ultralytics`, `gymnasium`, `langchain`, `pydantic`, `fastapi`)
3. Internal application imports from `shared` or local packages (`from shared.schemas import DetectionResult`)

**Grouping:**
- Blank line separating standard library, third-party, and local module imports
- Alphabetical ordering within each section
- Absolute imports preferred over deep relative imports (`from shared.schemas import ...` rather than `from ...shared.schemas import ...`)

## Error Handling

**Strategy:**
- Fail-fast on configuration or contract mismatch; fail-safe during operational inference
- Use custom, descriptive exceptions defined in `shared/exceptions.py`
- Never use bare `except:` or catch-all `except Exception: pass` without logging

**Pattern:**
```python
import logging
from shared.exceptions import ModelInferenceError

logger = logging.getLogger(__name__)

def run_detection(frame: np.ndarray) -> DetectionResult:
    try:
        results = model(frame)
        return parse_results(results)
    except Exception as exc:
        logger.error(f"Inference failed on frame: {exc}", exc_info=True)
        raise ModelInferenceError(f"Detection pipeline failure: {exc}") from exc
```

## Logging

**Framework:**
- Standard Python `logging` module
- Structured logger instances initialized per module: `logger = logging.getLogger(__name__)`
- Log levels:
  - `DEBUG`: Detailed diagnostic output (tensor shapes, raw bbox coordinates)
  - `INFO`: Mission milestones (target detected, route generated, report synthesized)
  - `WARNING`: Non-fatal anomalies (low detection confidence, fallback protocol applied)
  - `ERROR`: Module execution failures requiring intervention

**Rule:**
- Avoid raw `print()` statements in production code; use `logger.info()` or `logger.debug()`

## Documentation & Docstrings

**Docstring Style:**
- Google-style or standard Sphinx docstrings for all public modules, classes, and functions:
```python
def compute_astar_route(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    cost_matrix: np.ndarray
) -> List[Tuple[int, int]]:
    """Compute the minimum-cost path from start to goal over a terrain grid.

    Args:
        start: Grid coordinate tuple (x, y) for starting location.
        goal: Grid coordinate tuple (x, y) for target extraction point.
        cost_matrix: 2D NumPy array representing traversal difficulty.

    Returns:
        List of grid coordinate tuples representing the optimal route.

    Raises:
        ValueError: If start or goal coordinates are outside grid bounds.
        NoPathFoundError: If all paths to goal are blocked by obstacles.
    """
```

## Git & Collaboration Workflow

**Branching & PR Rules (per `README.md` and `docs/CHECKLIST.md`):**
1. Never push directly to the `main` branch.
2. Develop features on designated module branches (`sujal-detection`, `sujal-search-planning`, `vedant-rag-pipeline`, `manan-agentic-layer`, `aryan-route-dashboard`).
3. Open PRs against `testing` for integration and regression testing.
4. Obtain peer review approval before merging into `main`.
5. Atomic commits with imperative, descriptive commit messages (`Add A* terrain cost weighting`, `Implement ChromaDB hybrid retriever`).

---

*Convention analysis: 2026-10-14*
*Update when patterns change*
