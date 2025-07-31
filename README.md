# Patient Management API

A modern FastAPI backend for patient and provider onboarding, authentication, and management. Supports:
- Patient self-registration and login
- Provider registration and login
- JWT-based authentication
- MongoDB for data storage
- Dockerized deployment

## Features
- **Patient onboarding:** Patients can register themselves with detailed demographic and contact info.
- **Provider onboarding:** Providers can be registered with role, NPI, work locations, and more.
- **Authentication:** Separate login endpoints for patients and providers, both using JWT.
- **API documentation:** Interactive Swagger UI at `/docs`.

## Folder Structure
- `patient_management_backend/` — Main backend code
- `Seesion Screenshots/` — UI reference screenshots

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd python-ai-suit-14
```

### 2. Run with Docker (Recommended)
```bash
cd patient_management_backend
docker-compose up --build
```
- The API will be available at `http://localhost:8000/api`
- MongoDB will run at `localhost:27017`

### 3. Manual Setup (Without Docker)
#### Prerequisites
- Python 3.11+
- MongoDB running locally or remotely

#### Install dependencies
```bash
cd patient_management_backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Set environment variables (example)
```bash
export MONGODB_URL=mongodb://localhost:27017/
export JWT_SECRET_KEY=supersecretkey
export JWT_ALGORITHM=HS256
export ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Run the app
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Authentication Flows

### Patient
- **Register:** `POST /api/auth/register` — All fields from the Add Patient screen
- **Login:** `POST /api/auth/login` — Email & password

### Provider
- **Register:** `POST /api/provider/register` — All fields from the Add Provider screen
- **Login:** `POST /api/provider/login` — Email & password

## Main API Endpoints

### Patient Endpoints (`/api/patients`)
- `GET /` — List all patients (auth required)
- `GET /{patient_id}` — Get patient details (auth required)
- `POST /` — Create patient (admin/provider only)
- `PUT /{patient_id}` — Update patient
- `DELETE /{patient_id}` — Delete patient

### Provider Endpoints (`/api/provider`)
- `GET /` — List all providers (auth required)
- `GET /{provider_id}` — Get provider details (auth required)
- `POST /register` — Register provider
- `POST /login` — Provider login

### Auth Endpoints (`/api/auth`)
- `POST /register` — Patient self-registration
- `POST /login` — Patient login

## API Documentation
- Swagger UI: [http://localhost:8000/api/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/api/redoc](http://localhost:8000/redoc)

---
