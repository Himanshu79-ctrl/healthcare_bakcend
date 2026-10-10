# Healthcare Backend

Backend for a healthcare application built with Django, Django REST Framework, PostgreSQL and JWT authentication.

## Tech Stack

- Python 3.11+
- Django 6
- Django REST Framework
- djangorestframework-simplejwt
- PostgreSQL
- python-decouple for environment variables

## Project Structure

```
healthcare_backend/
├── config/        project settings and root urls
├── accounts/      registration and login
├── patients/      patient records
├── doctors/       doctor records
├── mappings/      patient and doctor assignments
├── manage.py
├── requirements.txt
└── .env.example
```

## Setup

```bash
git clone <repo-url>
cd healthcare_backend

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

Create the database in PostgreSQL:

```sql
CREATE DATABASE healthcare_db;
```

Update `.env` with your credentials, then run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Run tests:

```bash
python manage.py test
```

## Environment Variables

| Variable | Description |
|---|---|
| SECRET_KEY | Django secret key |
| DEBUG | True or False |
| ALLOWED_HOSTS | Comma separated hosts |
| DB_NAME | PostgreSQL database name |
| DB_USER | PostgreSQL user |
| DB_PASSWORD | PostgreSQL password |
| DB_HOST | PostgreSQL host |
| DB_PORT | PostgreSQL port |
| ACCESS_TOKEN_MINUTES | Access token lifetime |
| REFRESH_TOKEN_DAYS | Refresh token lifetime |

## API Endpoints

All endpoints except register and login need the header `Authorization: Bearer <access_token>`.

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/auth/register/ | Register with name, email, password |
| POST | /api/auth/login/ | Login and get JWT tokens |

### Patients

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/patients/ | Add a patient |
| GET | /api/patients/ | List patients created by the logged in user |
| GET | /api/patients/<id>/ | Patient details |
| PUT | /api/patients/<id>/ | Update patient |
| DELETE | /api/patients/<id>/ | Delete patient |

### Doctors

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/doctors/ | Add a doctor |
| GET | /api/doctors/ | List all doctors |
| GET | /api/doctors/<id>/ | Doctor details |
| PUT | /api/doctors/<id>/ | Update doctor (creator only) |
| DELETE | /api/doctors/<id>/ | Delete doctor (creator only) |

### Mappings

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/mappings/ | Assign a doctor to a patient |
| GET | /api/mappings/ | List mappings of the user's patients |
| GET | /api/mappings/<patient_id>/ | Doctors assigned to a patient |
| DELETE | /api/mappings/<id>/ | Remove a doctor from a patient |

## Sample Requests

Register

```json
POST /api/auth/register/
{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "password": "StrongPass@123"
}
```

Login

```json
POST /api/auth/login/
{
  "email": "rahul@example.com",
  "password": "StrongPass@123"
}
```

Add patient

```json
POST /api/patients/
{
  "name": "Amit Kumar",
  "age": 34,
  "gender": "male",
  "phone": "9876543210",
  "address": "Hoshiarpur, Punjab",
  "medical_history": "Diabetes"
}
```

Add doctor

```json
POST /api/doctors/
{
  "name": "Neha Verma",
  "email": "neha@clinic.com",
  "phone": "9123456780",
  "specialization": "Cardiology",
  "experience_years": 8
}
```

Assign doctor

```json
POST /api/mappings/
{
  "patient": 1,
  "doctor": 1
}
```
