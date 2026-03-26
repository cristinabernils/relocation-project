# Design: CI and Config Centralization

## Technical Approach

Centralize all configuration constants (countries, indicators, weights, paths, recommendations) into a single `src/config.py` module, then update imports in `main.py` and `streamlit_app/app.py`. Add CI pipeline with ruff (linting) and pytest (testing) to enforce code quality.

## Architecture Decisions

### Decision: Single Config Module Location

**Choice**: `src/config.py` as the centralized configuration source
**Alternatives considered**: `config/settings.py`, `src/settings.py`, `.env` file
**Rationale**: Spec requires `src/config.py`. Using `src/` aligns with existing module structure (`src/data_fetching.py`, `src/scoring.py`, etc.). Direct module import (`from src.config import X`) is the simplest approach per spec Scenario 1.2.

### Decision: Include All 9 Constants in config.py

**Choice**: Export all 9 constants specified in Requirement 1
**Alternatives considered**: Lazy loading, dataclasses, Pydantic models
**Rationale**: Simplicity. The spec explicitly lists 9 constants to export. Using plain module-level constants allows direct `from src.config import COUNTRIES` as required by Scenario 1.2. No additional dependencies needed.

### Decision: CI Uses Separate Jobs for Lint and Test

**Choice**: Sequential jobs in GitHub Actions (install → lint → test)
**Alternatives considered**: Single job with all steps, parallel jobs
**Rationale**: Fail-fast pattern. If lint fails, don't waste CI time running tests. Clearer error messages. Sequential is standard practice.

### Decision: Test Coverage Focuses on Config Module Only

**Choice**: `tests/test_config.py` validates config structures only
**Alternatives considered**: Full test suite for all modules, integration tests only
**Rationale**: Spec Requirement 5 explicitly defines test scenarios for config. Other modules are out of scope per proposal.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/config.py` | Create | Centralized config exports (9 constants) |
| `tests/test_config.py` | Create | Unit tests for config module |
| `.github/workflows/ci.yml` | Create | CI pipeline with ruff + pytest |
| `main.py` | Modify | Replace inline CONTEXT_DATA, weights, paths with imports from src.config |
| `streamlit_app/app.py` | Modify | Replace inline CONTEXT_DATA, INDICATORS, COUNTRY_RECOMMENDATIONS with imports from src.config |

## Interfaces / Contracts

### src/config.py Exports

```python
# Countries: list of country codes for analysis
COUNTRIES = [
    "DEU", "FRA", "ITA", "ESP", "NLD", "SWE", "POL", "GRC", "PRT", "NOR",
    "GBR", "JPN", "KOR", "CHN", "IND", "SGP", "VNM"
]

# Indicators: mapping of names to World Bank API codes
INDICATORS_DICT = {
    "NY.GDP.PCAP.CD": "gdp_per_capita",
    "FP.CPI.TOTL.ZG": "inflation",
    "SL.UEM.TOTL.ZS": "unemployment",
    "SP.POP.TOTL": "population",
    "SI.POV.GINI": "gini_index",
    "SE.XPD.TOTL.GD.ZS": "education_spending_gdp"
}

# List of indicator names (derived from INDICATORS_DICT values)
INDICATORS = list(INDICATORS_DICT.values())

# Context data: maternity scores by country
CONTEXT_DATA = {
    "country": ["Germany", "Spain", "Norway", "United Kingdom", "Sweden", "Japan", "Portugal", "Greece"],
    "maternity_score": [4, 4, 5, 3, 5, 2, 4, 3]
}

# Default scoring weights (must sum to 1.0)
DEFAULT_WEIGHTS = {
    "gdp": 0.30,
    "gini": 0.20,
    "education": 0.15,
    "maternity": 0.10,
    "employment": 0.05,
    "stability": 0.05,
    "hdi": 0.15
}

# Data directory paths
DATA_RAW_PATH = "data/raw"
DATA_EXTERNAL_PATH = "data/external"
DATA_PROCESSED_PATH = "data/processed"

# Country recommendations (text by country name)
COUNTRY_RECOMMENDATIONS = {
    "Norway": "Norway excels in social support, high salaries, and egalitarian policies.",
    "Sweden": "Sweden is balanced in all aspects, with progressive policies and strong quality of life.",
    # ... etc
}
```

### main.py Import Changes

```python
# BEFORE (lines 30, 64-70, 74-82):
INDICATORS = list(INDICATORS_DICT.values())
context_data = {"country": [...], "maternity_score": [...]}
weights = {"gdp": 0.30, ...}

# AFTER:
from src.config import (
    INDICATORS, CONTEXT_DATA, DEFAULT_WEIGHTS,
    DATA_RAW_PATH, DATA_EXTERNAL_PATH, DATA_PROCESSED_PATH
)
context_df = pd.DataFrame(CONTEXT_DATA)
weights = DEFAULT_WEIGHTS
```

### streamlit_app/app.py Import Changes

```python
# BEFORE (lines 27-30, 32-38, 125-134):
INDICATORS = [...]
CONTEXT_DATA = {...}
reco = {...}

# AFTER:
from src.config import INDICATORS, CONTEXT_DATA, COUNTRY_RECOMMENDATIONS
context_df = pd.DataFrame(CONTEXT_DATA)
```

## Data Flow

```
                    ┌──────────────────┐
                    │   src/config.py  │
                    │   (9 constants) │
                    └────────┬─────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   main.py    │  │streamlit_app/│  │  CI Pipeline │
    │              │  │   app.py     │  │              │
    │              │  │              │  │ • ruff check │
    │              │  │              │  │ • pytest     │
    └──────────────┘  └──────────────┘  └──────────────┘
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | COUNTRIES is non-empty list with expected countries | `assert isinstance(COUNTRIES, list)` + `"DEU" in COUNTRIES` |
| Unit | INDICATORS_DICT is dict with expected keys | `assert isinstance(INDICATORS_DICT, dict)` + `"gdp" in INDICATORS_DICT.values()` |
| Unit | CONTEXT_DATA has "country" and "maternity_score" | `assert "country" in CONTEXT_DATA` |
| Unit | DEFAULT_WEIGHTS values are floats 0-1, sum=1.0 | Loop validation + `sum() == 1.0` |
| Unit | DATA_*_PATH are non-empty strings | `assert DATA_RAW_PATH` etc |
| Unit | COUNTRY_RECOMMENDATIONS is dict with COUNTRIES entries | `for c in COUNTRIES: assert c in COUNTRY_RECOMMENDATIONS` |
| Integration | main.py runs without ImportError | `python main.py` smoke test |
| Integration | streamlit_app/app.py runs without ImportError | `streamlit run streamlit_app/app.py` smoke test |

## CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install ruff
      - run: ruff check src/

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pip install pytest
      - run: pytest tests/
```

## Migration / Rollback

No data migration required. This is a refactoring change with new files.

**Rollback Plan** (per proposal):
1. Revert import changes in `main.py` and `streamlit_app/app.py`
2. Restore inline `CONTEXT_DATA`, `INDICATORS`, `DEFAULT_WEIGHTS`, `COUNTRY_RECOMMENDATIONS`
3. Delete `src/config.py`, `.github/workflows/ci.yml`, `tests/test_config.py`

## Open Questions

- [ ] Should `COUNTRIES` store country names or ISO codes? (Spec says "European and Asian countries" — using codes from data_fetching.py for consistency)
- [ ] Add pytest and ruff to requirements.txt? (Spec mentions verifying in requirements)

## Next Step

Ready for sdd-tasks to break down into implementable tasks.
