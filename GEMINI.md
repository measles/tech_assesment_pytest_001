# Project Instructions

## API Specification
- The OpenAPI description is located at `http://54.226.15.13:8000/openapi.json`.
- **Mandate:** At the start of every session, read the updated version of the OpenAPI description from this URL to ensure the latest API state is known.

## Checklist
- The checklist for API testing is located at `docs/CHECKLIST.md`.

## Test Location
- All code must be placed in `src/tech_assesment_001`.
- Tests must be placed in `src/tech_assesment_001/test`.
- Utility functions and classes must be placed in `src/tech_assesment_001/utils`.

## Workflow
- The user will handle all commits. Do not stage or commit changes unless explicitly requested, and even then, prefer providing the changes for the user to review and commit themselves.
- Make changes as atomic as possible. Implement one check from the checklist at a time, including any directly related and necessary library changes.
- **Mandate:** Before providing changes for review, always run `uv run nox -s lint` to ensure code quality and formatting.
