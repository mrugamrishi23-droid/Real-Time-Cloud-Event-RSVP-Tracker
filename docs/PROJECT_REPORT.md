# Project Report: Real-Time Cloud-Based Event Planning & RSVP Tracker

## Abstract
This project implements a cloud-oriented event planning platform where organizers publish events and attendees respond in real time. The system combines REST APIs, authentication, role-based authorization, a relational database, WebSockets, capacity management, announcements, notifications and analytics.

## Introduction
Traditional event coordination can rely on spreadsheets, messages and manual counting. This project centralizes the workflow in a browser-based application.

## Problem Statement
Organizers need a reliable way to publish events, manage capacity and observe attendee responses while attendees need a simple way to discover events and update their RSVP.

## Objectives
- Centralize event information.
- Provide secure registration and login.
- Support organizer and attendee roles.
- Store RSVP records.
- Push live RSVP updates.
- Enforce capacity.
- Provide analytics.
- Demonstrate cloud deployment and scalability.

## Existing System
A basic manual process may use spreadsheets, chat messages and separate communication channels. Such a process makes live counting and access control harder.

## Proposed System
The proposed system uses a browser frontend, FastAPI REST backend, relational database and WebSocket real-time channel.

## Cloud Computing Concepts
The application demonstrates SaaS through the browser application, PaaS through managed hosting, cloud database usage through PostgreSQL, environment-based secret management, cloud deployment, scalability concepts, logging and failure handling.

## Real-Time Computing
WebSockets allow the server to push RSVP changes to connected clients. This reduces the need for manual refresh.

## Database Design
Main entities:
- USERS
- EVENTS
- RSVPS
- WAITLIST
- ANNOUNCEMENTS
- NOTIFICATIONS

The `(event_id, user_id)` pair is unique for RSVPs.

## Authentication and Authorization
JWT identifies a logged-in user. Role-based checks distinguish attendees, organizers and administrators. Event ownership is checked for event modifications.

## RSVP Workflow
1. User selects an RSVP.
2. JWT is validated.
3. Event is checked.
4. Deadline and capacity are checked.
5. RSVP is inserted or updated.
6. Notification is generated.
7. WebSocket event is broadcast.

## Capacity and Concurrency
A simple read-then-write check can have a race condition. A production implementation should use a database transaction or atomic conditional update for final-seat allocation.

## Testing
The test plan covers registration, login, event CRUD, RSVP updates, capacity, unauthorized operations, WebSocket updates, analytics and failure scenarios.

## Security
The system uses password hashing, JWT, RBAC, ownership checks, database constraints, environment variables, configurable CORS and HTTPS/WSS for production.

## Scalability
A larger deployment can add load balancing, multiple stateless API instances, managed PostgreSQL, caching, queues, shared pub/sub and CDN delivery.

## Results
The local application demonstrates event creation, RSVP updates and real-time dashboard updates. Cloud deployment demonstrates remote access and managed infrastructure.

## Limitations
The starter does not include production email/SMS, distributed WebSocket fan-out or a full transaction-based capacity allocator.

## Future Scope
- Supabase/Firebase managed authentication.
- Managed real-time subscriptions.
- Email and push notifications.
- Redis-based distributed locks/pub-sub.
- Queue-based notification service.
- Advanced analytics.
- CI/CD tests and observability.

## Conclusion
The project demonstrates how a conventional event application can be redesigned around cloud computing principles, real-time communication, managed data services, security and scalability.
