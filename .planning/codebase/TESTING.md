# Testing Patterns

**Analysis Date:** 2026-10-14

## Test Framework

**Runner:**
- `pytest` (>=7.4.0)
- Config: `pytest.ini` or `pyproject.toml` in project root

**Plugins & Extensions:**
- `pytest-asyncio` - For testing asynchronous FastAPI endpoints and async LangGraph node executions
- `pytest-cov` - Test coverage measurement and reporting
- `pytest-mock` - Fixture-based mocking and monkeypatching

**Run Commands:**
```bash
pytest                                  # Run all unit and integration tests
pytest -v                               # Verbose test execution
pytest tests/test_pathfinding.py        # Run single test module
pytest -k "test_astar"                  # Run specific test function
pytest --cov=. --cov-report=term-missing # Generate test coverage report
```

## Test File Organization

**Location:**
- Dedicated `tests/` directory at the project root with subfolders mirroring system modules:
```
AEGIS/
├── tests/
│   ├── test_detection.py               # CV model loading, inference wrappers, bbox parsing
│   ├── test_search_planning.py         # Gymnasium environment, reward logic, observation spaces
│   ├── test_rag_pipeline.py            # Document chunking, embeddings, ChromaDB retrieval
│   ├── test_agentic_layer.py           # LangGraph node transitions, assessment/verification logic
│   ├── test_route_planning.py          # Dijkstra and A* pathfinding over terrain cost matrices
│   ├── test_shared_schemas.py          # Pydantic data contract validation
│   └── fixtures/                       # Test data, sample frames, mock documents, grid matrices
```

**Naming:**
- Test files prefixed with `test_*.py`
- Test functions prefixed with `test_*()`
- Test classes prefixed with `Test*`

## Test Structure

**Suite Organization:**
```python
import pytest
import numpy as np
from route_dashboard.pathfinding.astar import compute_astar_route
from shared.exceptions import NoPathFoundError

class TestAStarPathfinding:
    """Tests for the A* terrain pathfinding implementation."""

    @pytest.fixture
    def simple_grid(self) -> np.ndarray:
        """Create a 10x10 zero-cost traversal grid."""
        return np.ones((10, 10), dtype=float)

    def test_direct_line_path(self, simple_grid):
        # Arrange
        start = (0, 0)
        goal = (0, 5)

        # Act
        path = compute_astar_route(start, goal, simple_grid)

        # Assert
        assert len(path) == 6
        assert path[0] == start
        assert path[-1] == goal

    def test_obstacle_avoidance(self, simple_grid):
        # Arrange: create an impassable wall
        simple_grid[1:9, 5] = np.inf
        start = (4, 2)
        goal = (4, 8)

        # Act
        path = compute_astar_route(start, goal, simple_grid)

        # Assert
        assert (4, 5) not in path  # Must navigate around the wall
        assert path[-1] == goal

    def test_unreachable_goal_raises_error(self, simple_grid):
        # Arrange: completely enclose goal
        simple_grid[4:7, 4:7] = np.inf
        start = (0, 0)
        goal = (5, 5)

        # Act & Assert
        with pytest.raises(NoPathFoundError):
            compute_astar_route(start, goal, simple_grid)
```

## Mocking

**Framework:**
- `unittest.mock` / `pytest-mock` (`mocker` fixture)

**What to Mock:**
- External LLM API calls (OpenAI API / Anthropic endpoints) to avoid cost and latency in CI
- Heavy PyTorch / YOLO model weights during unit testing of downstream pipeline logic
- ChromaDB disk persistence for fast in-memory unit tests
- Video camera hardware feeds (use pre-recorded test clips or synthetic NumPy arrays)

**What NOT to Mock:**
- Pydantic schema validation (must test real contracts)
- Algorithm logic (A*, Dijkstra, heuristic cost calculations)
- Custom Gymnasium environment step and reset transitions

**Pattern for Mocking LLM Node:**
```python
def test_assessment_agent_decision(mocker):
    # Mock LLM response to simulate low confidence triage
    mock_llm = mocker.patch("rag_agentic.agentic_layer.agents.ChatOpenAI")
    mock_llm.return_value.invoke.return_value.content = '{"status": "CONFIRMED", "triage": "URGENT"}'

    # Run agent function and assert parsed state
    state = run_assessment_node({"detection_confidence": 0.92})
    assert state["triage"] == "URGENT"
```

## Fixtures and Factories

**Test Fixtures (`tests/fixtures/`):**
- `sample_frame.jpg` - Fixed resolution aerial test image with known coordinates
- `synthetic_terrain.npy` - 20x20 terrain cost matrix with known water bodies and elevation gradients
- `sample_sop.md` - Synthetic search-and-rescue manual used for chunking and retrieval tests
- `mock_detections.json` - Serialized `DetectionResult` objects for testing LangGraph ingestion

## Coverage

**Requirements:**
- Core algorithms (`shared/schemas/`, `route_dashboard/pathfinding/`, `rag_agentic/agentic_layer/state.py`): Target >= 80% line coverage
- AI/ML Model Training scripts: Monitored via training loss/mAP rather than unit test coverage
- Integration tests: End-to-end smoke test validating pipeline connection across all 5 modules

## Test Types

**1. Unit Tests:**
- Test individual functions in isolation (e.g., coordinate conversion, distance metrics, prompt formatting, Pydantic validator checks).
- Run time: < 100ms per test.

**2. Simulation & Environment Tests:**
- Gym environment sanity checking via `gymnasium.utils.env_checker.check_env(env)`.
- Verifies observation space bounds, action space validity, and episode termination triggers.

**3. Integration & Contract Tests:**
- Validates data exchange across module boundaries:
  - `DetectionResult` -> `AssessmentAgent`
  - `AssessmentAgent` -> `Retriever`
  - `VerificationAgent` -> `AStarPathfinder`
- Ensures JSON serialization and Pydantic validation succeed without runtime schema errors.

**4. End-to-End Smoke Tests:**
- Simulates complete pipeline flow: Feeding synthetic aerial frame -> Detection -> RAG -> Agents -> Route generation -> Response serialization.

---

*Testing analysis: 2026-10-14*
*Update when test patterns change*
