# TASK.dev.docker-compose-stack.md

## 🧩 Task: Dockerize the Development Stack (Frontend + Backend)

Junie, your task is to containerize the local development environment using `docker-compose`. This will allow us to run both the FastAPI backend and the Next.js frontend in hot-reloading containers.

---

## 🎯 Objectives

- Create a `docker-compose.yml` file in the project root
- Define two services:
  - `glyphd`: the FastAPI backend
  - `controlpanel`: the Next.js frontend

---

## 📦 Backend (glyphd)

- Base image: **Python 3.12-slim** or **python:3.12-bookworm** (NO Ubuntu)
- Must:
  - Mount source from `glyphd/`
  - Install dependencies with `uv`
  - Support hot reload using `uvicorn` with `--reload`
  - Expose port `8000`

Dockerfile example (inside `glyphd/`):

```Dockerfile
FROM python:3.12-bookworm
WORKDIR /app
COPY . .
RUN pip install uv && uv pip install --system .
CMD ["uvicorn", "glyphd.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## 📦 Frontend (controlpanel)

- Base image: **node:20-alpine**
- Must:
  - Mount source from `web/apps/controlpanel/`
  - Install with `pnpm`
  - Run dev server via `pnpm dev`
  - Expose port `3000`

Dockerfile example (inside `web/apps/controlpanel/`):

```Dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN corepack enable && corepack prepare pnpm@latest --activate
RUN pnpm install
CMD ["pnpm", "dev"]
```

---

## 🛠 docker-compose.yml (at project root)

```yaml
version: '3.9'
services:
  glyphd:
    build: ./glyphd
    ports:
      - "8000:8000"
    volumes:
      - ./glyphd:/app
    environment:
      - PYTHONUNBUFFERED=1

  controlpanel:
    build: ./web/apps/controlpanel
    ports:
      - "3000:3000"
    volumes:
      - ./web/apps/controlpanel:/app
    depends_on:
      - glyphd
```

---

## ✅ Completion Criteria

- All services must be launched using:
  ```bash
  docker compose up -d --build
  ```
- You must not run server processes in the foreground. Always use detached mode (`-d`) so your CLI remains responsive.
- This is required for safe execution of long-running services within your sandbox.

- Visiting `localhost:3000` opens the Next.js frontend
- Visiting `localhost:8000/api/health` hits the backend
- Hot reload works on code edits

---

## 📝 Notes

Do **not** use Ubuntu as a base image. Use Alpine for Node and Bookworm-slim for Python. This dev stack should remain minimal, fast, and observable in Docker Desktop.

You must also update your `.junie/guidelines.md` to document the proper way to run the stack using `docker compose up -d`. This ensures you do not block your terminal or crash your session when invoking services interactively.
