# Municipal Waste Billing System (MVP)

CSE 3206 – Software Engineering Sessional, Lab 2
Group #06, Section C (1st 30) | Team members: 2203136, 2203137, 2203138
Process model: **Waterfall**

## About

A minimum viable product for a municipal waste collection billing system.
Staff can register residents, generate monthly waste-collection bills, and
track payment status from a simple dashboard.

Built as a standard web application: a Flask REST API backend and a static
HTML/CSS/JS frontend that talks to it over `fetch()`.

## Team contribution / module ownership

| Member    | Module                              | Feature branch              |
|-----------|--------------------------------------|-------------------------------|
| 2203136   | Authentication API (`backend/auth/`) | `feature/auth-module`         |
| 2203138   | Backend REST API (`backend/api/`)    | `feature/backend-module`      |
| 2203137   | Frontend (`frontend/`), repo setup, README, merges | `feature/frontend-module` |

## Tech stack

- Backend: Python 3, Flask (REST API, session-based auth), Flask-SQLAlchemy (SQLite)
- Frontend: plain HTML, CSS, and vanilla JavaScript (`fetch`) — no build step needed for the MVP

## Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` — Flask serves the frontend pages directly and
exposes the API under `/api/...`.

Default login: `admin` / `admin123` (or register a new staff account).

## Project structure

```
municipal-waste-billing-system/
├── backend/
│   ├── app.py              # application factory, blueprint registration, serves frontend
│   ├── extensions.py       # shared SQLAlchemy instance
│   ├── models.py            # User, Resident, Bill models
│   ├── requirements.txt
│   ├── auth/                 # 2203136 - /api/auth/* (login, register, logout, session)
│   └── api/                   # 2203138 - /api/residents, /api/bills, /api/dashboard/summary
├── frontend/                  # 2203137
│   ├── index.html, register.html
│   ├── dashboard.html, residents.html, bills.html
│   ├── css/style.css
│   └── js/ (api.js, nav.js, auth.js, dashboard.js, residents.js, bills.js)
├── docs/
│   └── Requirement_Report.pdf
├── assets/
├── screenshots/
```

## API summary

| Endpoint                              | Method | Description                     |
|----------------------------------------|--------|----------------------------------|
| `/api/auth/register`                   | POST   | Create a staff account           |
| `/api/auth/login`                      | POST   | Log in, starts a session         |
| `/api/auth/logout`                     | POST   | Ends the session                 |
| `/api/auth/session`                    | GET    | Check current login state        |
| `/api/residents`                       | GET/POST | List / register residents      |
| `/api/residents/<id>`                  | GET/PUT/DELETE | Read / update / delete a resident |
| `/api/bills`                           | GET/POST | List / generate bills          |
| `/api/bills/<id>/toggle-status`        | PATCH  | Toggle Paid / Unpaid             |
| `/api/bills/<id>`                      | DELETE | Delete a bill                    |
| `/api/dashboard/summary`               | GET    | Stats for the dashboard page     |

## Git workflow

```
main
 ├── feature/auth-module        (2203136)
 ├── feature/backend-module     (2203138)
 └── feature/frontend-module    (2203137)
```

Each member worked on their own branch, opened a Pull Request against `main`,
had it reviewed by a teammate, resolved any conflicts, and merged once
approved.

## Note

This is Lab 2 of a semester-long project — an MVP only, not a complete
production system.
