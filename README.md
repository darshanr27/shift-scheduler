# Staff Shift Scheduler
A RESTful API for managing staff shifts with role based permission, built with FastAPI and PostgreSQL.

---

## Live API

**Base URL:** `https://shift-scheduler-9g44.onrender.com`
**Swagger UI:** [https://shift-scheduler-9g44.onrender.com/docs](https://shift-scheduler-9g44.onrender.com/docs)

### How to Test

1. **Signup** — `POST /auth/signup` with email, password, role, first_name and last_name
2. **Login** — `POST /auth/login`, copy the `access_token` from the response
3. **Authorize** — Click the 🔒 **Authorize** button in Swagger UI, paste the token
4. **Test routes** — All protected endpoints are now accessible

---

## Tech Stack

- **FastAPI** — API framework
- **SQLAlchemy** — ORM for database operations
- **Alembic** — Database migrations
- **PostgreSQL** (Supabase) — Database
- **Pydantic** — Request/response validation
- **JWT** (python-jose) — Authentication
- **Passlib + bcrypt** — Password hashing

---

## Folder Structure

```
shift-scheduler/
├── alembic/
├── models/
│   ├── user.py
│   ├── shift.py
│   └── assignment.py
├── routers/
│   ├── auth.py
│   ├── shifts.py
│   ├── assignments.py
│   └── export.py
├── schemas/
│   ├── user.py
│   ├── shift.py
│   └── assignment.py
├── services/
│   ├── auth_service.py
│   ├── shift_services.py
│   └── assignment_service.py
├── database.py
├── main.py
├── requirements.txt
└── .env
```

---

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/darshanr27/shift-scheduler
cd shift-scheduler
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi sqlalchemy alembic pydantic python-jose passlib bcrypt==4.0.1 passlib==1.7.4 python-dotenv psycopg2-binary uvicorn
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://postgres:yourpassword@db.xxxx.supabase.co:6543/postgres
SECRET_KEY=your_random_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRY_MINUTES=30
```

Generate a secure `SECRET_KEY`:
```bash
openssl rand -hex 32
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
fastapi dev main.py
```

API runs at `http://localhost:8000`
Swagger UI at `http://localhost:8000/docs`

---

## API Endpoints

### Auth
| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| POST | /auth/signup | Register a new user | No |
| POST | /auth/login | Login and get JWT token | No |

### Shifts
| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| POST | /shifts | Create a new shift | Admin |
| GET | /shifts | Get all shifts | Yes |
| GET | /shifts/{id} | Get shift by ID | Yes |
| PUT | /shifts/{id} | Update a shift | Admin |
| DELETE | /shifts/{id} | Delete a shift | Admin |
| GET | /shifts/by-date | Get shifts by date range | Yes |

### Assignments
| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| POST | /shifts/{shift_id}/assign/{user_id} | Assign staff to shift | Admin |
| DELETE | /shifts/{shift_id}/unassign/{user_id} | Unassign staff from shift | Admin |
| GET | /shifts/{shift_id}/assignments | Get all assignments for a shift | Yes |
| GET | /users/{user_id}/shifts | Get all shifts for a staff member | Yes |

### Export
| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| GET | /export/shifts | Download shift roster as CSV | Admin |

---

## Database Migrations

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# Check current version
alembic current
```