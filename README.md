# 🐱 Cat API Project

Back-end service built with **FastAPI**, **MongoDB** (Motor async driver) and a clean, layered architecture. The project exposes two resource domains:

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

### Option A — Docker Compose (recommended)

```bash
docker compose up --build
```

Services started:

* **cat-api** → <http://localhost:8000>  (docs at `/docs`)  
* **mongo**   → port `27017`

### Option B — Local virtual-env

```bash
python -m venv venv
source venv/bin/activate       # Windows ➜ venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create a `.env` file first (see template below).

---

## 🗄️ Environment variables

Create **`.env`** (or use Docker-Compose defaults):

```env
# Database
MONGO_URL=mongodb://mongo:27017         # use mongodb://localhost:27017 if running Mongo locally
DB_NAME=cat_api

# External API
THECATAPI_URL=https://api.thecatapi.com/v1
THECATAPI_KEY=replace-with-your-own-key
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

## 🧪 Running tests

```bash
pytest -q
```

Unit tests cover user creation, unique-username generation, login flow, and one breed endpoint.

---
