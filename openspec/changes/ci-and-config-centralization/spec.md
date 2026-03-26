# Specification: CI and Config Centralization

## Overview

This specification defines the requirements for centralizing configuration data and establishing automated CI. The goal is to eliminate duplicated `CONTEXT_DATA` and `COUNTRY_RECOMMENDATIONS` dictionaries and add automated linting and testing.

---

## Requirement 1: src/config.py Exports

### Scenario 1.1: config.py defines all required constants

**Given** the project has a `src/` directory  
**When** the developer creates `src/config.py`  
**Then** the module MUST export the following constants:

| Constant | Type | Description |
|----------|------|-------------|
| `COUNTRIES` | list[str] | List of European and Asian countries for analysis |
| `INDICATORS_DICT` | dict[str, str] | Mapping of indicator names to World Bank API codes |
| `INDICATORS` | list[str] | List of indicator names (values from INDICATORS_DICT) |
| `CONTEXT_DATA` | dict[str, list] | Dictionary with country names and maternity scores |
| `DEFAULT_WEIGHTS` | dict[str, float] | Default weight configuration for scoring algorithm |
| `DATA_RAW_PATH` | str | Path to raw World Bank data directory |
| `DATA_EXTERNAL_PATH` | str | Path to external data directory (e.g., HDI) |
| `DATA_PROCESSED_PATH` | str | Path to processed output directory |
| `COUNTRY_RECOMMENDATIONS` | dict[str, str] | Country name to recommendation text mapping |

### Scenario 1.2: config.py uses public exports

**Given** `src/config.py` has been created  
**When** other modules import from `src.config`  
**Then** all required constants MUST be directly importable using `from src.config import <CONSTANT>`  
**And** constants MUST NOT require accessing private attributes (e.g., `_COUNTRIES`)

---

## Requirement 2: main.py Imports from src.config

### Scenario 2.1: main.py removes local CONTEXT_DATA definition

**Given** `main.py` contains a local `context_data` dictionary (lines 64-70)  
**When** the developer updates `main.py` to import from `src.config`  
**Then** the local `context_data` definition MUST be removed  
**And** `main.py` MUST import `CONTEXT_DATA` from `src.config`

**Given** `main.py` contains a local `weights` dictionary (lines 74-82)  
**When** the developer updates imports  
**Then** the local `weights` definition MUST be replaced with `DEFAULT_WEIGHTS` from `src.config`

### Scenario 2.2: main.py uses DATA paths from config

**Given** `main.py` uses hardcoded paths like `"data/raw/"` and `"data/processed"`  
**When** the developer updates `main.py`  
**Then** the code MUST import and use `DATA_RAW_PATH` and `DATA_PROCESSED_PATH` from `src.config`

### Scenario 2.3: main.py imports INDICATORS from config

**Given** `main.py` defines `INDICATORS = list(INDICATORS_DICT.values())` (line 30)  
**When** the developer updates imports  
**Then** the code MUST import `INDICATORS` directly from `src.config`

---

## Requirement 3: streamlit_app/app.py Imports from src.config

### Scenario 3.1: streamlit_app/app.py removes local CONTEXT_DATA

**Given** `streamlit_app/app.py` contains a local `CONTEXT_DATA` dictionary (lines 32-38)  
**When** the developer updates imports  
**Then** the local `CONTEXT_DATA` definition MUST be removed  
**And** the module MUST import `CONTEXT_DATA` from `src.config`

### Scenario 3.2: streamlit_app/app.py removes local COUNTRY_RECOMMENDATIONS

**Given** `streamlit_app/app.py` contains a local `reco` dictionary (lines 125-134)  
**When** the developer updates imports  
**Then** the local `reco` definition MUST be removed  
**And** the module MUST import `COUNTRY_RECOMMENDATIONS` from `src.config`

### Scenario 3.3: streamlit_app/app.py imports INDICATORS from config

**Given** `streamlit_app/app.py` defines `INDICATORS` list locally (lines 27-30)  
**When** the developer updates imports  
**Then** the local `INDICATORS` definition MUST be replaced with import from `src.config`

### Scenario 3.4: streamlit_app/app.py uses config for weights defaults

**Given** `streamlit_app/app.py` initializes slider default values  
**When** the developer updates imports  
**Then** the default values SHOULD align with `DEFAULT_WEIGHTS` from `src.config`

---

## Requirement 4: CI Pipeline with GitHub Actions

### Scenario 4.1: CI workflow file exists

**Given** the project is a Git repository  
**When** the developer creates `.github/workflows/ci.yml`  
**Then** the workflow file MUST exist at `.github/workflows/ci.yml`

### Scenario 4.2: CI runs ruff linter

**Given** the CI workflow is configured  
**When** the workflow runs on any push or pull request to `main` branch  
**Then** the job MUST execute `ruff check src/`  
**And** the job MUST fail if ruff reports any errors

### Scenario 4.3: CI runs pytest tests

**Given** the CI workflow is configured  
**When** the workflow runs  
**Then** the job MUST execute `pytest tests/`  
**And** the job MUST fail if any test fails

### Scenario 4.4: CI triggers on appropriate events

**Given** the CI workflow exists  
**When** a push or pull request occurs  
**Then** the workflow MUST trigger on:
- Push to `main` branch
- Pull requests to `main` branch

---

## Requirement 5: Config Module Tests

### Scenario 5.1: test_config.py exists

**Given** the project has a `tests/` directory  
**When** the developer creates `tests/test_config.py`  
**Then** the test file MUST exist at `tests/test_config.py`

### Scenario 5.2: Tests verify COUNTRIES constant

**Given** `tests/test_config.py` is created  
**When** tests run  
**Then** there MUST be a test verifying `COUNTRIES` is a non-empty list  
**And** the test MUST verify `COUNTRIES` contains expected countries (e.g., Germany, Spain, Norway)

### Scenario 5.3: Tests verify INDICATORS_DICT structure

**Given** `tests/test_config.py` is created  
**When** tests run  
**Then** there MUST be a test verifying `INDICATORS_DICT` is a dictionary  
**And** the test MUST verify the dictionary contains expected keys (e.g., "gdp", "gini", "education")

### Scenario 5.4: Tests verify CONTEXT_DATA structure

**Given** `tests/test_config.py` is created  
**When** tests run  
**Then** there MUST be a test verifying `CONTEXT_DATA` is a dictionary  
**And** the test MUST verify it contains "country" and "maternity_score" keys

### Scenario 5.5: Tests verify DEFAULT_WEIGHTS values

**Given** `tests/test_config.py` is created  
**When** tests run  
**Then** there MUST be a test verifying `DEFAULT_WEIGHTS` is a dictionary  
**And** the test MUST verify all weight values are floats between 0 and 1  
**And** the test MUST verify the sum of weights equals 1.0

### Scenario 5.6: Tests verify DATA path constants

**Given** `tests/test_config.py` is created  
**When** tests run  
**Then** there MUST be tests verifying `DATA_RAW_PATH`, `DATA_EXTERNAL_PATH`, and `DATA_PROCESSED_PATH` are non-empty strings

### Scenario 5.7: Tests verify COUNTRY_RECOMMENDATIONS

**Given** `tests/test_config.py` is created  
**When** tests run  
**Then** there MUST be a test verifying `COUNTRY_RECOMMENDATIONS` is a dictionary  
**And** the test MUST verify it contains entries for countries in `COUNTRIES`

### Scenario 5.8: Tests run successfully

**Given** `tests/test_config.py` is created  
**When** the developer runs `pytest tests/test_config.py`  
**Then** all tests MUST pass without errors

---

## Integration Tests

### Scenario 6.1: main.py runs without errors

**Given** the config centralization changes are complete  
**When** the developer runs `python main.py`  
**Then** the script MUST execute without ImportError  
**And** the script MUST produce expected output

### Scenario 6.2: Streamlit app runs without errors

**Given** the config centralization changes are complete  
**When** the developer runs `streamlit run streamlit_app/app.py`  
**Then** the app MUST start without ImportError  
**And** the app MUST render correctly with imported config

### Scenario 6.3: ruff check passes

**Given** the code changes are complete  
**When** the developer runs `ruff check src/`  
**Then** there MUST be no linting errors

### Scenario 6.4: pytest passes

**Given** the code changes are complete  
**When** the developer runs `pytest tests/`  
**Then** all tests MUST pass

---

## Acceptance Criteria Summary

| ID | Criterion | Verification |
|----|-----------|--------------|
| AC1 | `src/config.py` exports all 9 constants | Import each constant in Python shell |
| AC2 | `main.py` imports from `src.config` | Check no local CONTEXT_DATA definition |
| AC3 | `streamlit_app/app.py` imports from `src.config` | Check no local CONTEXT_DATA or COUNTRY_RECOMMENDATIONS |
| AC4 | `.github/workflows/ci.yml` runs ruff and pytest | View workflow file and verify jobs |
| AC5 | `tests/test_config.py` has comprehensive tests | Run pytest and verify coverage |
| AC6 | All CI checks pass | Run `ruff check` and `pytest` locally |
