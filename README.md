# AI Document Classification & Routing System

Classifies documents into Application, Complaint, Invoice, Contract, Request or Correspondence, and recommends a department.

## Project Structure

```text
frontend/       Browser interface
tests/          Automated tests
SECURITY.md     Security policy and review checklist
TEST_REPORT.md  Test execution template
```

## Setup
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
pip install pytest httpx
```

## Run the backend (from the project root)
```bash
uvicorn backend.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

## Run the frontend
```bash
python -m http.server 5500 --directory frontend
```
Open http://localhost:5500

## Tests
```bash
python -m pytest tests/ -v
```
