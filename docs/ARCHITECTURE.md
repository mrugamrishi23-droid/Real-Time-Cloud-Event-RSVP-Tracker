# Architecture Notes

## Request path

```text
Attendee
  |
  +--> React UI
        |
        +--> POST /api/events/{id}/rsvp
                    |
                    v
                 FastAPI
                    |
              auth + validation
                    |
                    v
                PostgreSQL
                    |
             commit successful
                    |
                    v
              WebSocket Manager
                    |
          +---------+---------+
          |                   |
    Organizer browser    Attendee browser
```

## Why WebSockets?

Polling asks the server repeatedly whether something changed. WebSockets maintain a persistent connection so the server can push an event when an RSVP changes.

## Failure handling

If the WebSocket disconnects, the frontend should reconnect or refresh the selected event. REST remains the source of truth, so a missed WebSocket message does not corrupt the RSVP.

## Scaling path

For a larger deployment:

```text
CDN
 |
React static assets
 |
Load Balancer
 |
+--------+--------+
| FastAPI | FastAPI |
+--------+--------+
       |
   Redis / PubSub
       |
PostgreSQL primary
       |
read replicas / cache
```

Multiple FastAPI instances need shared pub/sub; an in-memory WebSocket manager alone only works within one process.
