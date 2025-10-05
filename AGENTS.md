# Repository Guidelines

## Project Structure & Module Organization
The workspace is split into rontend/ (Vue 3 + Vite SPA), ackend/ (FastAPI microservice), DATASET/ (reference CSVs) and uploads/ produced by the API. Within rontend/src/, routes live in outer/, shared UI in components/, and page-level views in pages/; keep reusable assets under ssets/ and theme tokens in styles/. The backend entrypoint is ackend/api/api_routes.py; persistent files such as the SQLite stub exoplanet.db stay alongside it.

## Build, Test, and Development Commands
Run 
pm install once inside rontend/, then 
pm run dev to boot the Vite dev server on port 5173. Use 
pm run build for a production bundle and 
pm run preview to smoke-test the build. 
pm run lint (ESLint + Vuetify preset) and 
pm run type-check (vue-tsc) should be clean before committing. Backend dependencies install via pip install -r requirements.txt inside ackend/; start the API with uvicorn api.api_routes:app --reload --port 8000.

## Coding Style & Naming Conventions
Frontend code follows the repo's .editorconfig: two-space indentation, LF endings, UTF-8. Keep Vue single-file components in PascalCase under components/, route files in kebab-case, and TypeScript modules in camelCase. Prefer script setup syntax, centralized API calls under rontend/api/, and reuse Vuetify composables. Backend modules should remain PEP 8 compliant with snake_case functions and descriptive path prefixes.

## Testing Guidelines
Automated tests are not yet wired up; rely on 
pm run type-check plus targeted manual QA in the Vite preview. When adding tests, place component specs under rontend/tests/ using Vitest + Vue Test Utils, and cover FastAPI endpoints with pytest in ackend/tests/. Keep fixtures lightweight and document any dataset dependencies near the test.

## Commit & Pull Request Guidelines
Existing commits are short, imperative statements ("Upload Vue", "ADD Footer..."); follow that style and scope one concern per commit. For pull requests, include: 1) a concise summary of changes, 2) references to Jira/GitHub issues, 3) screenshots or recordings for UI updates, and 4) backend API curl examples when endpoints change. Mention required setup steps (e.g., seed files in DATASET/) and confirm lint/type-check status in the PR checklist.

## Environment & Configuration Tips
Store secrets in a local .env consumed by FastAPI; never commit credentials. Coordinate frontend to backend ports through the CORS allowlist in pi_routes.py, and keep large datasets out of Git by updating .gitignore as needed.
