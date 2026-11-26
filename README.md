# BBC News Classification & Routing System

Classifies BBC news articles into Business, Entertainment, Politics, Sport, or Tech and recommends a department.

## Project Structure

```text
backend/
  __init__.py
  main.py           FastAPI application
  requirements.txt  Backend dependencies
  .env.example      Example environment configuration
data/raw/           Local source dataset (not tracked)
models/             Local trained model artifacts (not tracked)
frontend/           Browser interface
  css/
  js/
notebooks/          Data exploration and project notebooks
reports/            Model and analysis reports
src/
  data/              Dataset loading
  models/            Training and evaluation scripts
  preprocessing/     Text preprocessing
tests/              Automated tests
SECURITY.md         Security policy
requirements-dev.txt Development and test dependencies
requirements-training.txt Additional training and notebook dependencies
```

## Setup

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install the development and test dependencies:

```bash
pip install -r requirements-dev.txt
```

## Train the model

The dataset and model artifacts are kept local and excluded from Git. If they
aren't present, place the BBC dataset at `data/raw/bbc_data.csv`, then run:

```bash
pip install -r requirements-training.txt
python src/models/train_baseline.py
```

The training workflow saves the selected scikit-learn pipeline to
`models/baseline_model.joblib`.

## Run the backend

Copy `backend/.env.example` to `backend/.env` and adjust its values if needed.
The local `.env` file is ignored by Git.

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
