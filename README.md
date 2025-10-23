member 1: Backend
member 2:frontend
member 1 and member 2:devops

# flask-lab-project

Small sample Flask project with Docker and CI/CD (GitHub Actions).

This README shows how to add collaborators, build, test, and run the project locally, and how CI publishes the image to GHCR.

## Add collaborators (GitHub)
- Go to the repository on GitHub -> Settings -> Collaborators -> Invite collaborators by username or email.

## Local setup (Windows PowerShell)
Run these commands from the repository root (`C:\D\sem7\Devops\pre mid\flask-lab-project`).

1) Create and activate a virtual environment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2) Install runtime and dev dependencies
```powershell
python -m pip install --upgrade pip
pip install -r main/requirements.txt
pip install pytest
```

3) Run unit tests
```powershell
pytest -q main/tests
```

## Build and run with Docker (local)
Make sure Docker Desktop / daemon is running.

1) Build the image from `main/`
```powershell
# tag the image locally
docker build -t flask-lab-project:local ./main
```

2) Run the container (foreground)
```powershell
docker run --rm -p 5000:5000 --name flask-lab-local flask-lab-project:local
# open http://localhost:5000 or http://localhost:5000/health
```

3) Run the container (detached)
```powershell
docker run -d -p 5000:5000 --name flask-lab-local flask-lab-project:local
docker logs -f flask-lab-local
```

If the container fails because `gunicorn` is not found, ensure `gunicorn` is listed in `main/requirements.txt` and rebuild (`docker build ...`).

## CI/CD (GitHub Actions)
- Workflow file: `.github/workflows/ci-cd.yml`.
- Triggers: push to `main` and pull requests targeting `main`.
- What it does: installs dependencies, runs pytest, builds Docker image from `main/`, and pushes to GitHub Container Registry (GHCR) as `ghcr.io/<owner>/flask-lab-project:latest` and `...:<sha>`.

To manually run the workflow in GitHub: Actions -> CI/CD -> Run workflow (choose branch `main`).

## Pulling the image from GHCR
```powershell
# optionally authenticate to GHCR (if image is private)
# echo <PERSONAL_ACCESS_TOKEN> | docker login ghcr.io -u <GITHUB_USERNAME> --password-stdin

docker pull ghcr.io/<owner>/flask-lab-project:latest
docker run -p 5000:5000 ghcr.io/<owner>/flask-lab-project:latest
```

## Notes and tips
- Use branches for each member (backend, frontend, devops) and create PRs to merge into `main`.
- `main/requirements.txt` should contain runtime dependencies (Flask, gunicorn). Put `pytest` into `requirements-dev.txt` if you want separation.
- Add `.dockerignore` to speed up builds and exclude `.venv`, `tests`, etc.

If you want, I can add `requirements-dev.txt`, a `.dockerignore`, or a short CONTRIBUTING.md describing the branching workflow.
