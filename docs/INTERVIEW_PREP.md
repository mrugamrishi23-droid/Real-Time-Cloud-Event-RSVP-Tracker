# Interview Preparation — 10 Questions + Strong Answers

## 1. Explain your project.
I built a Real-Time Cloud-Based Event Planning and RSVP Tracker. Organizers create and manage events, while attendees register and respond with Going, Maybe or Not Going. FastAPI exposes REST APIs, PostgreSQL stores the cloud data, JWT provides authentication, and WebSockets push RSVP changes to connected dashboards without a manual refresh.

## 2. Why did you use cloud computing?
The event data needs centralized access from different devices. Cloud hosting also provides managed databases, remote accessibility and a path to scaling the API and database when the number of attendees increases.

## 3. What does real-time mean here?
When an attendee changes an RSVP, the backend commits the change and broadcasts an event over WebSocket. The organizer dashboard receives it and updates the counters without polling or refreshing.

## 4. REST API vs WebSocket?
REST is request-response and is suitable for CRUD operations such as creating an event. WebSocket keeps a connection open and lets the server push changes, which is useful for live RSVP counters.

## 5. How is authentication different from authorization?
Authentication identifies the user after login. Authorization checks what that authenticated user is allowed to do. For example, an attendee can RSVP but cannot modify an organizer's event.

## 6. How do you prevent duplicate RSVPs?
The backend performs an upsert-style operation and the database has a unique constraint on `(event_id, user_id)`. Therefore the same user cannot have multiple active RSVP rows for one event.

## 7. How do you handle a full event?
Before accepting a GOING response, the backend checks the current Going count against capacity. If it is full, the request is rejected and the optional waitlist can store the attendee.

## 8. What is the race condition in capacity management?
If two users both see one remaining seat before either write commits, both could be accepted by a naive check. A production system should use a database transaction, row lock or atomic conditional update so the capacity allocation is decided by the database.

## 9. How would you scale it?
I would keep API servers stateless, put them behind a load balancer, use a managed PostgreSQL database with proper indexes and connection pooling, add Redis caching and shared pub/sub for WebSocket fan-out, and use a queue for notifications.

## 10. What security controls did you implement?
Passwords are hashed, APIs use JWT authentication, role checks protect privileged operations, event ownership is verified server-side, database uniqueness prevents duplicate RSVPs, secrets are environment variables, and production traffic should use HTTPS/WSS.
