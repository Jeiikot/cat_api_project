# 🐱 Cat API Project

[![CI](https://github.com/jeiikot/cat_api_project/actions/workflows/ci-docker.yml/badge.svg)](https://github.com/jeiikot/cat_api_project/actions/workflows/ci-docker.yml)
[![Docker Hub](https://img.shields.io/docker/pulls/jeiikot/cat_api_project)](https://hub.docker.com/r/jeiikot/cat_api_project)


Back-end service built with **FastAPI** and **MongoDB** (async Motor driver) following a clean, layered architecture.
> **Tip** You can try every **/breeds** endpoint without a database because they proxy TheCatAPI directly. **/users** routes do need MongoDB running.


* **Breeds** – read-only wrapper over [TheCatAPI](https://thecatapi.com)  
* **Users**  – CRUD + login persisted in MongoDB

---

## 🔧 Requirements

| Tool | Version |
|------|---------|
| Python | 3.11 |
| Docker & Docker Compose | 20.10+ |
| (Optional) local MongoDB | 6.x |

> **Tip** You can exercise all **/breeds** endpoints without MongoDB – they call TheCatAPI directly. **/users** routes need Mongo running.

---

## 🚀 Quick start


> **⏱️ Estimated time:** 1 min with the pre-built image, ~3 min if you build locally.

| Option | When to use |
|--------|-------------|
| **A. `docker compose up`** | Local development and end-to-end tests |
| **B. Pull the image from Docker Hub** | Quick evaluation without cloning or building |
| **C. Local virtual-env** | Fine-tuning or debugging outside Docker |



### Option A — Docker Compose (recommended)

```bash
docker compose up --build
```

Services started:

* **FastAPI** → <http://localhost:8000>  (docs at `/docs`)  
* **MongoDB**   → port `27017`

### Option B — Use the image published by CI

```bash
  docker pull jeiikot/cat_api_project:latest
  docker compose up -d
```

### Option C — Virtual environment

```bash
    python -m venv venv
    source venv/bin/activate       
    pip install -r requirements.txt
    uvicorn app.main:app --reload
```

Create a `.env` file first (see template below).

---

## 🗄️ Environment variables

Create **`.env`** (or use Docker-Compose defaults):

```env
# Database
MONGO_URL=mongodb://mongo:27017
DB_NAME=cat_api

# External API
CAT_API_URL=https://api.thecatapi.com/v1
CAT_API_KEY=replace-with-your-own-key
```

---

## 🗂️ Project layout

```
cat_api_project/
├── app/
│   ├── core/            # settings / env helpers
│   ├── db/              # MongoDB client
│   ├── models/          # Pydantic schemas
│   ├── routers/         # FastAPI routes (controllers)
│   ├── services/        # business logic
│   ├── tests/           # unit & integration tests
│   └── utils/           # helpers (e.g. hash_password)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 📚 HTTP API

### Breeds (proxy to TheCatAPI)

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/breeds?limit=10&page=0` | Paginated list of cat breeds |
| `GET`  | `/breeds/{breed_id}` | Retrieve breed by ID |
| `GET`  | `/breeds/search?query=siamese&limit=5&page=0` | Search breeds by name |

> All breed endpoints are **fully async** using `httpx.AsyncClient`.

### Users (Mongo-backed)

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/users?limit=10&page=0` | Paginated list of users |
| `POST` | `/users` | Create user – username auto-generated, password hashed |
| `POST` | `/users/login` | Validate credentials & return user data |

### Paginated response

```json
{
  "results": [
    { "username": "jdoe", "name": "John", "lastname": "Doe" }
  ],
  "limit": 10,
  "page": 0,
  "next": "/users?limit=10&page=1",
  "previous": null
}
```

---
## 🛠️ CI / CD 

A single GitHub Actions workflow—**ci-docker.yml**—runs automatically on every push to `main` and on merged pull-requests.

| Step | What happens |
|------|--------------|
| 🧪 **Test** | Installs dependencies and runs all unit tests with coverage-gate (≥ 90 %). |
| 🐳 **Build** | Builds the Docker image using the root `Dockerfile`. |
| 🚀 **Publish** | Pushes the image to Docker Hub `jeiikot/cat_api_project` with two tags:<br>• **latest** – always the most recent build<br>• **{commit-SHA}** – immutable pin to that revision |

```bash
  docker pull jeiikot/cat_api_project:latest
  docker compose up -d
```

Prefer to test a feature branch locally?

```bash
  docker compose build
  docker compose up
```
---

## 🧪 Running tests

```bash
  pytest
```

Unit tests cover user creation, unique-username generation, login flow, and one breed endpoint.

---
