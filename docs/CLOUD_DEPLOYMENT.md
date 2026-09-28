# Cloud Deployment

## Recommended student path

### 1. PostgreSQL

Create a free PostgreSQL project with a provider that supports student/hobby use. Supabase is one practical option because its free plan includes a PostgreSQL database and Realtime quota.

Copy the connection string into:

```text
DATABASE_URL=postgresql+psycopg://...
```

### 2. Backend

Deploy `backend/` as a Docker/Python web service.

Start command if not using Docker:

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set:
- DATABASE_URL
- JWT_SECRET
- CORS_ORIGINS

### 3. Frontend

Build:

```text
npm install
npm run build
```

Publish the `dist` directory.

Set:
```text
VITE_API_URL=https://YOUR-BACKEND/api
VITE_WS_URL=wss://YOUR-BACKEND/api/ws/events
```

### 4. Validate

- `/health`
- `/docs`
- login
- event creation
- RSVP
- WebSocket counter
- unauthorized action
- analytics

## Enterprise AWS mapping

```text
CloudFront
   |
S3 / frontend hosting
   |
API Gateway
   |
Lambda / ECS
   |
RDS PostgreSQL / DynamoDB
   |
API Gateway WebSocket
   |
Cognito
   |
SNS / SES
   |
CloudWatch
```

Azure equivalent:
- Azure Static Web Apps
- Azure Functions / Container Apps
- Azure Database for PostgreSQL
- Azure Web PubSub
- Microsoft Entra ID
- Application Insights

GCP equivalent:
- Cloud Storage / Firebase Hosting
- Cloud Run / Cloud Functions
- Cloud SQL / Firestore
- Firebase Realtime / WebSockets through application layer
- Identity Platform / Firebase Auth
- Cloud Monitoring

## Free-tier caution

Free tiers change. Verify the provider's current limits before deployment and avoid assuming that "free" means permanent or production-ready.
