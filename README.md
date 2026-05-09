# Personal Knowledge Base API

A FastAPI backend for a personal knowledge base with JWT-based authentication and user-scoped note management.

## Features
- User registration and login
- JWT access token generation
- Bearer-token authentication (`Authorization: Bearer <token>`)
- Current user endpoint
- Notes CRUD (create, update, list, get by ID, delete)
- Note search endpoint
- PostgreSQL + SQLAlchemy ORM

## Tech Stack
- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL (`psycopg2-binary`)
- Pydantic v2
- `python-jose` for JWT
- `bcrypt` for password hashing

## Project Structure
```text
Personal-knowledge-base/
|-- app/
|   |-- app.py
|   |-- JWT.py
|   |-- config/
|   |   `-- app_config.py
|   |-- database/
|   |   |-- db.py
|   |   |-- models/
|   |   |   `-- models.py
|   |   |-- schemas/
|   |   |   |-- auth.py
|   |   |   |-- note.py
|   |   |   `-- user.py
|   |   `-- CRUD/
|   |       |-- auth.py
|   |       `-- note.py
|   `-- routing/
|       |-- auth.py
|       |-- note.py
|       `-- user.py
|-- main.py
|-- requirements.txt
`-- .env.example
```

## Environment Variables
Create a `.env` file (you can copy from `.env.example`) and set values similar to:

```env
APP_NAME=Personal Knowledge Base
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/pkb
SECRET_KEY=your_super_secret_key
ALGORITHMS=HS256
ACCESS_TOKEN_EXPIRE_MINUTE=30
```

## Installation
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

If install fails due to pinned versions in `requirements.txt`, install minimum runtime deps:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose pydantic pydantic-settings passlib bcrypt python-multipart email-validator httpx
```

## Run the App
```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn app.app:app --reload
```

## API Docs
After startup:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication Flow
1. Register with `POST /auth/register`
2. Login with `POST /auth/login`
3. Copy `access_token` from response
4. Send header: `Authorization: Bearer <access_token>` for protected endpoints
5. In Swagger, click `Authorize` and paste the bearer token

## Main Endpoints

### Auth
- `POST /auth/register`
- `POST /auth/login`

### User
- `GET /users/me`

### Notes
- `POST /notes`
- `GET /notes`
- `GET /notes/{note_id}`
- `PUT /notes/{note_id}`
- `DELETE /notes/{note_id}`
- `GET /notes/search?q=...`

## Request Examples

### Register
```http
POST /auth/register
Content-Type: application/json

{
  "name": "aniket",
  "email_id": "aniket@example.com",
  "password": "Test12345",
  "confirm_password": "Test12345"
}
```

### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=aniket@example.com&password=Test12345
```

### Add Note
```http
POST /notes
Content-Type: application/json
Authorization: Bearer <jwt>

{
  "title": "My first note",
  "content": "Learning FastAPI",
  "tags": "fastapi,notes",
  "is_archived": false
}
```

### Update Note
```http
PUT /notes/7
Content-Type: application/json
Authorization: Bearer <jwt>

{
  "title": "Updated title",
  "content": "Updated content"
}
```

## Notes
- Login uses `OAuth2PasswordRequestForm`, so send `username` and `password` as form data, not JSON.
- Notes are user-scoped: you can access/update/delete only your own notes.
- If you changed the `Note.updated_at` model to nullable, make sure DB schema matches:

```sql
ALTER TABLE notes ALTER COLUMN updated_at DROP NOT NULL;
```

## Status
Core auth + note create/update flow is functional after dependency and schema alignment.
