# Proposal: CI and Config Centralization

## Intent

Eliminate code duplication and establish automated CI to improve code quality and maintainability. `CONTEXT_DATA` (maternity scores) and `COUNTRY_RECOMMENDATIONS` are duplicated in `main.py` (lines 64-70) and `streamlit_app/app.py` (lines 32-38, 125-134), creating maintenance risk. Additionally, the project lacks automated testing and linting infrastructure.

## Scope

### In Scope
- Extract `CONTEXT_DATA` dict to `src/config.py`
- Extract `COUNTRY_RECOMMENDATIONS` dict to `src/config.py`
- Update `main.py` to import from `src/config.py`
- Update `streamlit_app/app.py` to import from `src/config.py`
- Create `.github/workflows/ci.yml` with ruff linting and pytest
- Create `tests/test_config.py` with basic tests for the config module

### Out of Scope
- Refactoring of other duplicated code (HDI loading logic)
- Additional test coverage beyond config module
- Deployment pipeline (CI only)

## Approach

1. Create `src/config.py` with `CONTEXT_DATA` and `COUNTRY_RECOMMENDATIONS` constants
2. Update imports in `main.py` and `streamlit_app/app.py` to use centralized config
3. Create GitHub Actions workflow with ruff (linting) and pytest (tests)
4. Write basic tests verifying config module exports correct data structures

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/config.py` | New | Centralized config module |
| `main.py` | Modified | Import from src.config |
| `streamlit_app/app.py` | Modified | Import from src.config |
| `.github/workflows/ci.yml` | New | CI pipeline |
| `tests/test_config.py` | New | Config module tests |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Streamlit reload issues with config changes | Low | Use st.cache_data appropriately |
| CI failures if dependencies missing | Low | Add pytest/ruff to requirements if needed |

## Rollback Plan

1. Revert import changes in `main.py` and `streamlit_app/app.py`
2. Restore inline `CONTEXT_DATA` and `COUNTRY_RECOMMENDATIONS` definitions
3. Delete `src/config.py`, `.github/workflows/ci.yml`, `tests/test_config.py`

## Dependencies

- `pytest` and `ruff` packages (verify in requirements.txt or add)

## Success Criteria

- [ ] `main.py` runs without errors using imported config
- [ ] Streamlit app renders correctly with imported config
- [ ] `ruff check src/` passes with no errors
- [ ] `pytest tests/` passes with no errors
- [ ] GitHub Actions workflow runs on push/PR
