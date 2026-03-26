# Tasks: CI and Config Centralization

## Phase 1: Infrastructure (Foundation)

- [x] 1.1 Create `src/config.py` with all 9 constants (COUNTRIES, INDICATORS_DICT, INDICATORS, CONTEXT_DATA, DEFAULT_WEIGHTS, DATA_RAW_PATH, DATA_EXTERNAL_PATH, DATA_PROCESSED_PATH, COUNTRY_RECOMMENDATIONS)
- [x] 1.2 Create `.github/workflows/ci.yml` with ruff lint and pytest test jobs

## Phase 2: Core Implementation (Import Updates)

- [x] 2.1 Update `main.py` imports: remove local CONTEXT_DATA (lines 64-70), weights (lines 74-82), and hardcoded paths; import from `src.config`
- [x] 2.2 Update `main.py` to use `DEFAULT_WEIGHTS` instead of local `weights` dict
- [x] 2.3 Update `main.py` to use `DATA_RAW_PATH` and `DATA_PROCESSED_PATH` from config
- [x] 2.4 Update `streamlit_app/app.py` imports: remove local CONTEXT_DATA (lines 32-38), INDICATORS (lines 27-30), COUNTRY_RECOMMENDATIONS (lines 125-134); import from `src.config`
- [x] 2.5 Align `streamlit_app/app.py` slider defaults with DEFAULT_WEIGHTS

## Phase 3: Testing

- [x] 3.1 Create `tests/test_config.py` with tests for COUNTRIES (non-empty list, contains expected countries)
- [x] 3.2 Create tests for INDICATORS_DICT (dict with expected keys: gdp, gini, education)
- [x] 3.3 Create tests for CONTEXT_DATA (dict with "country" and "maternity_score" keys)
- [x] 3.4 Create tests for DEFAULT_WEIGHTS (values 0-1, sum equals 1.0)
- [x] 3.5 Create tests for DATA_*_PATH constants (non-empty strings)
- [x] 3.6 Create tests for COUNTRY_RECOMMENDATIONS (dict with entries for COUNTRIES)
- [x] 3.7 Create `pytest.ini` with pytest configuration
- [x] 3.8 Create `ruff.toml` with ruff configuration

## Phase 4: Verification & Polish

- [x] 4.1 Update `requirements.txt` to include pytest and ruff (if not already present)
- [x] 4.2 Run `ruff check src/` and fix any linting errors
- [x] 4.3 Run `pytest tests/` and ensure all tests pass
- [x] 4.4 Verify `python main.py` runs without ImportError
- [x] 4.5 Verify `streamlit run streamlit_app/app.py` starts without ImportError

(End of file - total 33 lines)
