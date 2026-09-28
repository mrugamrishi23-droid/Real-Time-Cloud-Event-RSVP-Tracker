# Real-Time Cloud-Based Event Planning & RSVP Tracker

A student-friendly, industry-oriented cloud computing project that demonstrates event management, authentication, RBAC, REST APIs, WebSockets, RSVP capacity control, announcements, notifications, analytics, failure handling and cloud deployment.

## 1. Why this project?

The system centralizes event creation and RSVP tracking. Attendees can respond with GOING, MAYBE or NOT_GOING. The organizer can see RSVP counters update in real time without refreshing the page.

## 2. Architecture

```text
Browser / React
      |
      | HTTPS REST
      v
FastAPI Backend
      |
      +---- JWT Authentication / RBAC
      |
      +---- SQLAlchemy
      |
      v
SQLite (local) / PostgreSQL (cloud)
      |
      +---- RSVP transaction + uniqueness
      |
      +---- WebSocket broadcast
                    |
                    v
             Organizer Dashboard
```

For a managed cloud database, PostgreSQL can be hosted on a provider such as Supabase. The app's real-time channel is implemented with FastAPI WebSockets, so the same application works locally and in the cloud.

## 3. Main cloud concepts

| Concept | Project implementation |
|---|---|
| SaaS | Browser-based event application |
| PaaS | Hosted FastAPI + static frontend |
| Cloud database | PostgreSQL deployment |
| REST | `/api/events`, `/api/login`, RSVP APIs |
| WebSockets | Live RSVP counter updates |
| RBAC | ATTENDEE / ORGANIZER / ADMIN |
| Scalability | Stateless API, managed DB, load balancing strategy |
| Caching | Recommended for popular read-heavy event pages |
| CDN | Static frontend hosting/CDN |
| Secrets | Environment variables |
| Monitoring | `/health`, platform logs |
| CI/CD | Git-based deployment |
| Failure handling | reconnect, idempotent upsert, validation, graceful errors |

## 4. Local installation

### Backend - Windows PowerShell

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

API docs: `http://127.0.0.1:8000/docs`

### Frontend

Open another PowerShell:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open `http://localhost:5173`.

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## 5. Demo flow

1. Register an ORGANIZER account.
2. Create `Cloud Computing Workshop`, capacity 100.
3. Open the event.
4. Register an attendee in another browser/incognito window.
5. Select GOING.
6. Keep the organizer event open: the count changes through WebSocket.
7. Change GOING to MAYBE and observe the counter.
8. Create an announcement.
9. Test a full event and waitlist response.
10. Try modifying another organizer's event and verify `403`.

## 6. Cloud deployment

### Option A - Supabase + Render

- Supabase: managed PostgreSQL and optional managed Realtime/Auth.
- Render: FastAPI web service and static frontend.

For the first deployment, this repository keeps authentication in FastAPI JWT and uses PostgreSQL as the cloud database. A later enhancement can replace JWT auth with Supabase Auth.

### Render environment

Backend:
- `DATABASE_URL`
- `JWT_SECRET`
- `CORS_ORIGINS`

Frontend:
- `VITE_API_URL=https://YOUR-BACKEND.onrender.com/api`
- `VITE_WS_URL=wss://YOUR-BACKEND.onrender.com/api/ws/events`

### Important free-tier limitation

Free hosting is appropriate for a student demo, not production. Some free services sleep or have storage/usage limits. Keep a local SQLite copy for development and backups.

## 7. API summary

- `POST /api/register`
- `POST /api/login`
- `POST /api/logout`
- `POST /api/events`
- `GET /api/events`
- `GET /api/events/{id}`
- `PUT /api/events/{id}`
- `DELETE /api/events/{id}`
- `POST /api/events/{id}/rsvp`
- `DELETE /api/events/{id}/rsvp`
- `GET /api/events/{id}/rsvps`
- `GET /api/rsvps/me`
- `GET /api/events/{id}/analytics`
- `POST /api/events/{id}/announcements`
- `GET /api/events/{id}/announcements`
- `GET /api/notifications`
- `PUT /api/notifications/{id}/read`
- `WS /api/ws/events/{id}`

## 8. Concurrency

The important business rule is not just:

```python
if current_going < capacity:
    insert_rsvp()
```

Two requests can read the same value before either writes. The production-safe design is a database transaction/conditional write or row-level lock. This starter uses a database uniqueness constraint for one RSVP per user/event and performs capacity validation inside the write workflow. For a high-volume PostgreSQL deployment, upgrade the capacity operation to a PostgreSQL transaction with `SELECT ... FOR UPDATE` or an atomic conditional counter.

## 9. Security

- Passwords are hashed with bcrypt.
- JWT is used for API authentication.
- Role checks protect organizer/admin operations.
- Event ownership is checked server-side.
- RSVP uniqueness is enforced by the database.
- Secrets are loaded from environment variables.
- CORS is configurable.
- Frontend values are never treated as the source of truth for counts.
- Production deployment should use HTTPS/WSS.

## 10. Testing

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest -q
```

Recommended additional tests are listed in `docs/TEST_PLAN.md`.

## 11. GitHub proof strategy

Use meaningful commits:
- `Initialize cloud event platform architecture`
- `Implement authentication and roles`
- `Add event management module`
- `Implement RSVP workflow`
- `Add PostgreSQL cloud configuration`
- `Add real-time RSVP WebSocket`
- `Implement capacity and waitlist handling`
- `Build organizer dashboard`
- `Add announcements and notifications`
- `Add analytics`
- `Add automated tests`
- `Deploy application to cloud`
- `Complete documentation`

Never commit `.env`, credentials, API keys, database passwords or generated databases.

## 12. Project limitations

This student version intentionally keeps email/SMS/push integrations optional and does not claim production-grade distributed locking. For very high traffic, add Redis, a message queue, a managed WebSocket service, distributed rate limiting, database connection pooling, observability and a stronger transaction-based capacity allocator.

## 13. Learning outcomes

You can explain:
- cloud service models
- managed databases
- REST API design
- WebSockets
- authentication vs authorization
- RBAC
- database constraints
- race conditions
- scalability
- failure handling
- CI/CD
- secrets management
- cloud deployment
