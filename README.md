Title: TheWatsonxPrototypev2.0

Author: Costas Hadjineophytou

Overview:
A full‑stack Python prototype demonstrating programmatic use of IBM watsonx services (LLM, NLU, TTS, STT). The Tkinter frontend provides an intuitive UI (tabs, components, popups) and orchestrates a thin, testable backend of small services with standardised validation and error handling.

The architecture consciously emphasises clear separation of concerns: the Tkinter UI focuses on presentation and interaction, the logic layer (managers/factory) coordinates flows, and backend services encapsulate domain operations (LLM/NLU/STT/TTS, IAM, resources). Cross‑cutting concerns—validation, error handling and configuration—are centralised for consistency, reusability and testability.

Architecture at a glance:
- Frontend (Tkinter): `frontend/app.py`, tabs in `frontend/tabs/*`, reusable UI in `frontend/components/*`, popups in `frontend/pop_ups/*`, assets in `frontend/assets/*`.
- Logic layer: Managers/factory wiring the UI to backend services.
- Backend services: LLM/NLU/STT/TTS services plus IAM token and resource discovery in `backend/services/*`, wired by `backend/service_factory.py`.
- Validation: Shared `BaseValidator` + service‑specific validators in `backend/validators/*` (input, credentials, optional resource checks).
- Error handling: Typed exceptions and normalization in `backend/utils/errors.py`, `backend/utils/error_handling.py`, composed via `backend/utils/error_handler.py`.
- Config & utils: `.env` driven config in `backend/config/config.py` and helpers in `backend/utils/*` (token, files, audio, env).
- Tests: Unit and integration tests in `backend/tests/*`.

Testing:
- Backend: Unit and integration tests under `backend/tests/unit` and `backend/tests/integration`.
- Logic layer: Unit and integration tests under `logic/tests/unit` and `logic/tests/integration`.
- End‑to‑end: E2E tests live in the top‑level app tests directory (main app scope).

Key features:
- Text generation (LLM), NLU analysis, Text‑to‑Speech, Speech‑to‑Text.
- Centralised IAM token handling and optional IBM Cloud resource validation.
- Consistent error model with typed exceptions and contextual logging.
- Settings popup to edit API key and region; `.env` reload support.

Prerequisites:
- Python 3.10+ on Windows.
- IBM Cloud account + API key with access to required services.

Setup:
1) Create and activate a virtual environment.
2) Install dependencies:
   pip install -r requirements.txt
3) Copy `.env.template` to `.env` and set:
   - IBM_CLOUD_API_KEY=your-api-key
   - IBM_CLOUD_MODELS_URL=https://<region>.ml.cloud.ibm.com
   - IBM_CLOUD_PROJECTS_URL=https://api.<region>.dataplatform.cloud.ibm.com

Run:
python main.py
Then use Settings → watsonx to confirm API key/region. The “Home” tab provides large tiles to the four service tabs.

Troubleshooting:
- Invalid API key: The app launches and prompts you to update Settings; services remain unavailable until fixed.
- IAM/HTTP errors: Logged and normalised to typed errors; check console/logs for context.
- Region mismatch: Ensure models/projects URLs use the same region (e.g., eu-gb, us-south).



