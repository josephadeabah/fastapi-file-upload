
---

# File Upload API

A FastAPI-based REST API that allows authenticated users to upload files. Includes user registration, login (JWT authentication), secure file storage, and database migrations using Alembic. Fully containerized with Docker.

---

## Features

* **User Authentication**

  * Register new users
  * Login with JWT token
* **File Upload**

  * Upload files securely
  * Stores files in a dedicated `uploads/` directory
* **Database Integration**

  * SQLAlchemy ORM
  * PostgreSQL compatible
  * Alembic migrations for schema management
* **Dockerized**

  * Runs with Docker for easy setup
* **API Documentation**

  * Automatic Swagger UI and ReDoc via FastAPI

---

## Tech Stack

* Python 3.11
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication (`python-jose`)
* Alembic (database migrations)
* Docker & Docker Compose

---

## Project Structure

```text
file-upload-api/
│
├─ alembic/                # Alembic migration scripts
│  ├─ versions/            # Individual migration files
│  └─ env.py
│
├─ app/
│  ├─ routers/
│  │  ├─ auth.py
│  │  └─ files.py
│  ├─ models/
│  │  ├─ user.py
│  │  └─ file.py
│  ├─ services/
│  │  └─ file_service.py
│  ├─ utils/
│  │  ├─ dependencies.py
│  │  └─ security.py
│  ├─ database.py
│  └─ config.py
│
├─ uploads/                # Uploaded files directory
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml      # optional
├─ .dockerignore
├─ .gitignore
└─ README.md
```

---

## Getting Started

### Prerequisites

* Python 3.11+
* PostgreSQL
* Docker & Docker Compose (optional)

---

### Local Development

1. **Clone the repo**

```bash
git clone https://github.com/<your-username>/file-upload-api.git
cd file-upload-api
```

2. **Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Set up environment variables**

```bash
cp .env.example .env
```

Edit `.env` with your database credentials, JWT secret key, and other configurations.

4. **Run Alembic migrations**

```bash
alembic upgrade head
```

This will create the necessary tables (`users`, `files`) in your database.

5. **Start the FastAPI server**

```bash
uvicorn app.main:app --reload
```

6. **Open Swagger UI**

```text
http://localhost:8000/docs
```

---

### Docker Setup

1. **Build the Docker image**

```bash
docker build -t file-upload-api .
```

2. **Run the container**

```bash
docker run -d -p 8000:8000 --name file-upload-api \
  --env-file .env file-upload-api
```

3. **Verify**

```text
http://localhost:8000/docs
```

---

## API Endpoints

| Endpoint         | Method | Description                            |
| ---------------- | ------ | -------------------------------------- |
| `/auth/register` | POST   | Register a new user                    |
| `/auth/login`    | POST   | Login and receive JWT token            |
| `/files/upload`  | POST   | Upload a file (requires Authorization) |

---

## Environment Variables

| Variable     | Description                 |
| ------------ | --------------------------- |
| SECRET_KEY   | JWT signing key             |
| ALGORITHM    | JWT algorithm (e.g., HS256) |
| DATABASE_URL | SQLAlchemy database URL     |
| HOST         | App host (default: 0.0.0.0) |
| PORT         | App port (default: 8000)    |
| UPLOAD_DIR   | File upload directory       |

---

## Git & Docker Ignore

**.gitignore**

```text
__pycache__/
*.pyc
.env
uploads/
alembic/versions/
```

**.dockerignore**

```text
__pycache__/
*.pyc
.env
.git
alembic/versions/
uploads/
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push branch: `git push origin feature/my-feature`
5. Create a pull request

---

## License

MIT License

---
