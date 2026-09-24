# API Gateway Project — Day 1 Journal

**Date:** 17 August 2026
**Sprint:** Sprint 1 — API Gateway Foundation
**Status:** In Progress

---

## 1. Project Goal

We are building a **production-style API Gateway**, not a tutorial project.

The main goal is to build the system in a way that could eventually be deployed, while understanding every architectural decision and concept through the actual implementation.

The project will eventually include:

* API Gateway
* Request routing
* Reverse proxy
* Rate limiting
* Redis
* Authentication / JWT
* Request validation
* Timeouts
* Retries
* Circuit breaker
* Logging
* Metrics and monitoring
* Docker
* Testing and load testing
* CI/CD
* Cloud deployment

The project will be developed progressively rather than implementing everything at once.

---

## 2. Technology Stack

### Current

* **Language:** Python
* **Framework:** FastAPI
* **ASGI Server:** Uvicorn
* **Database:** SQLite initially
* **Virtual environment:** Python `venv`

### Later

* **Redis:** Rate limiting and shared distributed state
* **PostgreSQL:** Potential production database
* **Docker:** Containerization
* **Prometheus:** Metrics
* **Grafana:** Monitoring dashboard
* **GitHub Actions:** CI/CD

Important understanding:

**SQLite and Redis have different responsibilities.**

SQLite is a persistent database for application data.

Redis will later be used for fast shared/temporary state such as distributed rate-limit information.

---

## 3. Initial Architecture

Our initial system is:

```text
Client
   ↓
API Gateway
   ↓
User Service
   ↓
SQLite
```

For Sprint 1, we are temporarily keeping the User Service simple and are not using SQLite yet.

The immediate goal is:

```text
Client
   ↓
API Gateway :8000
   ↓
User Service :8001
   ↓
Response
```

---

## 4. API Gateway Concept

We learned that an API Gateway acts as a **single entry point** between clients and backend services.

A useful mental model is:

> API Gateway = security guard + traffic controller + entry point for backend services.

However, it is not only a security component.

It can eventually handle:

* Authentication
* Authorization
* Rate limiting
* Routing
* Request validation
* Logging
* Monitoring
* Timeouts
* Retries
* Circuit breaking

The gateway helps prevent clients from needing to communicate directly with every internal microservice.

---

## 5. Why a Single Entry Point?

Without a gateway:

```text
Client
 ├──→ User Service
 ├──→ Product Service
 └──→ Order Service
```

With a gateway:

```text
Client
   ↓
API Gateway
   ├──→ User Service
   ├──→ Product Service
   └──→ Order Service
```

The gateway becomes the controlled entry point to the backend system.

---

## 6. Reverse Proxy Concept

We learned that the API Gateway will initially behave as a **reverse proxy**.

A reverse proxy sits between the client and backend services:

```text
Client
   ↓
Reverse Proxy / API Gateway
   ↓
Backend Service
```

The client does not need to know the internal address of every service.

For example:

```text
Client
   ↓
api.example.com/api/users
   ↓
API Gateway
   ↓
User Service
```

The gateway knows where the User Service is located.

---

## 7. Routing Concept

The gateway needs to answer two questions:

### Question 1

**Which service should handle this request?**

### Question 2

**Where is that service located?**

Example:

```text
/api/users
      ↓
User Service
      ↓
http://127.0.0.1:8001
```

A future routing table could look like:

```text
/api/users      → User Service      → :8001
/api/products   → Product Service   → :8002
/api/orders     → Order Service     → :8003
```

We learned that the **path** can be used by the gateway to determine the target service.

For example:

```text
/api/products/25
        ↓
Product Service
```

The gateway does not need to understand the product's business logic. Its job is primarily to determine where the request should go.

---

## 8. Project Structure

We created a production-oriented target structure:

```text
api_gateway/
│
├── gateway/
│   ├── main.py
│   ├── core/
│   ├── middleware/
│   ├── routing/
│   ├── resilience/
│   ├── services/
│   └── schemas/
│
├── services/
│   ├── user_service/
│   ├── product_service/
│   └── order_service/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── load/
│
├── infrastructure/
│   ├── docker/
│   ├── prometheus/
│   └── grafana/
│
├── docs/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

We decided not to implement every folder immediately.

The structure represents the **final direction of the project**, while implementation will grow as new engineering problems appear.

---

## 9. Important Python Structure Lesson

Initially, the microservice folder was created as:

```text
user-service
```

This caused an import problem.

Python module/package names should use:

```text
user_service
```

instead of:

```text
user-service
```

We also learned that Uvicorn uses the format:

```text
module.path:app
```

For example:

```bash
python -m uvicorn services.user_service.main:app --port 8001
```

This means:

```text
services
   ↓
user_service
   ↓
main.py
   ↓
app
```

---

## 10. First User Service

We created our first independent backend microservice:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users():
    return {
        "service": "User Service",
        "users": ["Alice", "Bob"]
    }
```

The current endpoint is:

```text
GET /users
```

It returns:

```json
{
    "service": "User Service",
    "users": ["Alice", "Bob"]
}
```

This is intentionally simple.

The purpose is to have a real backend service that the Gateway can communicate with.

---

## 11. Running the User Service

We successfully started it with:

```bash
python -m uvicorn services.user_service.main:app --port 8001
```

The service started successfully at:

```text
http://127.0.0.1:8001
```

We tested the endpoint and received:

```text
GET /users → 200 OK
```

Therefore:

```text
Client → User Service
```

is currently working.

---

## 12. Understanding the Uvicorn Logs

We observed:

```text
GET / HTTP/1.1" 404 Not Found
```

This was expected because we did not create a `/` endpoint.

We also saw:

```text
GET /favicon.ico HTTP/1.1" 404 Not Found
```

This was caused by the browser automatically requesting a favicon.

These are not application failures.

The important request was:

```text
GET /users HTTP/1.1" 200 OK
```

`200 OK` means the endpoint successfully handled the request.

---

## 13. Virtual Environment

We created a Python virtual environment so that this project has isolated dependencies.

We decided to use:

```bash
python -m pip
```

instead of directly calling:

```bash
pip
```

because `python -m pip` explicitly uses the pip associated with the Python interpreter/environment we're working with.

Packages installed so far:

* FastAPI
* Uvicorn

---

## 14. Current System State

Currently:

```text
Client
   │
   │ GET /users
   ▼
User Service :8001
   │
   │ 200 OK
   ▼
Client
```

This works.

But our actual goal is:

```text
Client
   │
   │ GET /api/users
   ▼
API Gateway :8000
   │
   │ route + forward
   ▼
User Service :8001
   │
   │ response
   ▼
API Gateway
   │
   ▼
Client
```

The Gateway → User Service connection is **the next implementation milestone**.

---

## 15. Engineering Lesson From Today

We learned an important development principle:

> Build and verify individual components before connecting them together.

We first verified:

```text
User Service works independently
```

Only after that will we introduce:

```text
Gateway → User Service
```

This makes debugging easier because if the Gateway fails later, we already know the User Service itself works.

---

## 16. Current Interview Knowledge

### What is an API Gateway?

An API Gateway is a single entry point between clients and backend services. It can centralize concerns such as routing, authentication, rate limiting, logging, and resilience.

### What is a reverse proxy?

A reverse proxy sits between clients and backend servers and forwards client requests to the appropriate backend service.

### Why use an API Gateway?

It provides a controlled entry point to backend services and centralizes common concerns instead of requiring every client to communicate directly with every microservice.

### How does the Gateway know where to send a request?

It can use routing rules based on the request path and map that path to an upstream service and its location.

Example:

```text
/api/users → User Service → 127.0.0.1:8001
```

---

## 17. Next Step

The next task is to build the first actual Gateway behavior:

```text
GET /api/users
       ↓
API Gateway :8000
       ↓
User Service :8001/users
       ↓
Response
```

This will be our first real **reverse-proxy/routing implementation**.

### **Sprint 1 status: Foundation completed; Gateway-to-service forwarding is next.**


## Day 1
 Project structure created
 User Service created and running
 .env configuration
 config.py reads service URL
 Gateway running on port 8000
 User Service running on port 8001
 Basic Gateway → User Service proxy
 httpx communication
 Generic service routing
 Unknown service → 404
 Service down handling → 503
 Dynamic path forwarding
 Tested /api/users
 Tested /api/users/25
all are completeed

## Day3

GET requests
✅ Dynamic paths like /api/users/25
✅ POST requests
✅ Forward JSON request bodies
✅ Return responses from the microservice
✅ Handle unavailable services with errors

## day 4

✅ Created middleware/
✅ Created logging_middleware.py
✅ Moved logging logic out of main.py
✅ Imported it into main.py
✅ Registered it with FastAPI
✅ Tested GET and POST successfully

Client
  ↓
logging_middleware.py
  ↓
Gateway route
  ↓
User Service
  ↓
Response
  ↓
logging middleware logs status

✅ Generate unique Request ID
✅ Store it in request.state
✅ Use it in logging
✅ Add it to the response header
✅ Tested successfully

Request ID middleware is now complete

## day 5

✅ API Gateway routing
✅ User microservice
✅ Request forwarding / proxy
✅ GET and POST requests
✅ Service error handling
✅ Request logging middleware
✅ Production logger
✅ Exception logging
✅ Request ID middleware
✅ Request ID in logs
✅ X-Request-ID response header
✅ Console logging
✅ File logging
✅ Log rotation

✅ Dynamic routing (service_name + path)
✅ GET + POST forwarding (with body + headers)
✅ Error handling (404, 502, 503)
✅ Middleware for logging
✅ Request ID tracking
✅ Proper logger (console + file + rotation)
✅ Exception logging
The 3 new files, one-line each
File	Job
core/logger.py	Sets up HOW/WHERE logs are saved (console + file, with rotation)
middleware/request_id_middleware.py	Gives every request a unique ID
middleware/logging_middleware.py	Uses that ID + logger to record what happened
The connection, in order
1. logger.py        → creates the logging system + gateway/logs/ folder
2. request_id_middleware.py → generates unique ID per request
3. logging_middleware.py    → logs using that ID + the logger
4. main.py                   → connects both middleware to the app
Middleware order (important detail you learned)

Last added = runs first. So add_request_id was added LAST but runs FIRST — generating the ID before log_requests needs to use it.

The full request journey
Client → add_request_id (creates ID) → log_requests (logs "incoming")
       → Gateway routes → proxy_service forwards → User Service
       → log_requests (logs "response status") → add_request_id (adds header)
       → Client (gets response + X-Request-ID header)
Where to SEE proof it's working
Terminal → shows logs live
gateway/logs/gateway.log → same logs, saved permanently
Response headers (in /docs or curl -i) → shows X-Request-ID
Why each piece exists (one-liners)
Request ID → so you can trace ONE specific request in messy, mixed-up logs
Logger (not print) → timestamps, severity levels, saves to file
Log rotation → prevents log file from growing forever
Middleware → runs automatically for every request, no manual repeating

### day 6

✅ Docker is running
✅ Redis container is running
✅ Redis can store data
✅ Redis can retrieve data

## day 7
✅ Request ID middleware
✅ Logging middleware
✅ Rate limiting middleware
✅ Redis request counting
✅ 60-second expiry
✅ 429 responses
✅ 429 responses logged

✅ Redis-based counting
✅ 10 requests per 60 seconds
✅ 429 Too Many Requests
✅ retry_after using Redis TTL
✅ Configuration values
✅ Request ID and logging
✅ Blocked requests also logged

✅ Redis request counting
✅ Configurable limit and window
✅ 10 requests / 60 seconds
✅ Allowed requests return remaining count
✅ Blocked requests return 429
✅ retry_after from Redis TTL
✅ Rate-limit headers
✅ Request ID
✅ Logging for 200 and 429
✅ complete file logging and terminal logging

## day 8 (fixed window to token bucket )

 Redis-backed Token Bucket
 Per-client IP buckets
 Bucket capacity configuration
 Token refill rate configuration
 Gradual token refill
 429 Too Many Requests
 Retry-After header
 Rate-limit headers
 Request ID integration
 Logging integration
 Redis fail-open handling
 Race condition fixed
 Atomic Redis Lua script
 Tested blocked → refill → allowed behavior

 ### day 9

 Request validation       ✅
Email validation         ✅
Password hashing         ✅
SQLite database storage  ✅
SQLAlchemy model         ✅
Safe response schema    ✅
Duplicate check logic    ✅

Client
  ↓
POST /auth/register
  ↓
Validate UserRegister
  ↓
Check existing email
  ↓
Hash password
  ↓
Store in SQLite
  ↓
Return safe user data

---------------

What we completed
1. JWT setup
Created backend/.env
Added:
JWT_SECRET
JWT_ALGORITHM
JWT_EXPIRATION_MINUTES
Added separate configuration for Gateway and User Service.
Added fail-fast validation if JWT_SECRET is missing.
2. JWT utility

Created core/jwt.py with a stricter production-style approach.

Every token will contain:

sub → user ID
iat → issued time
exp → expiration time

Optional extra_data can be added when needed.

3. SQLite + SQLAlchemy setup

Created:

database/
├── database.py
└── models.py

Completed:

SQLite connection
SQLAlchemy engine
SessionLocal
Base
get_db() dependency
User database model

User fields:

id
name
email
hashed_password
4. Pydantic schemas

Created:

schemas/user.py

With:

UserRegister
UserLogin
UserResponse

This separates:

API validation ≠ Database model

And prevents hashed_password from being returned.

5. Password security

Created:

core/security.py

With:

hash_password()
verify_password()

Passwords are hashed with bcrypt — never stored as plain text. 🔐

6. Registration endpoint

Created:

POST /auth/register

Flow:

Validate input
↓
Check duplicate email
↓
Hash password
↓
Save user to SQLite
↓
Return safe response
🐛 Problems we solved
Problem 1 — 422 Unprocessable Entity

Cause:

Email

instead of:

email

FastAPI/Pydantic field names are case-sensitive.

✅ Fixed.

Problem 2 — 500 Internal Server Error

The error happened during password hashing.

Cause:

Passlib + bcrypt 5.0.0

compatibility issue.

We changed bcrypt to:

bcrypt==4.0.1

✅ Fixed.

🎉 Final result

Your User Service successfully returned:

POST /auth/register → 201 Created ✅

So today we built the foundation of a real authentication system.

⏭️ Next
POST /auth/login
        ↓
Find user
        ↓
Verify password
        ↓
Create JWT
        ↓
Return access token 🔐

At this point we have:

Feature	Status
User registration	✅
Password hashing	✅
Password verification	✅
JWT generation	✅
JWT expiration	✅ Tested
JWT verification	✅
Bearer authentication	✅
Current user dependency	✅
User database lookup	✅
User roles	✅
Admin authorization	✅
401 authentication errors	✅
403 authorization errors	✅
Alembic migrations	✅
Role migration	✅
Environment configuration	✅
Auth service layer	✅
Auth route layer	✅
Gateway rate limiting	✅
Redis token bucket	✅
Atomic Redis operation	✅
Old duplicate auth routes removed	✅


Completed Checklist — Today
🔐 Authentication
 User registration
 Email validation
 Password validation — 8–128 chars
 Password hashing with bcrypt
 Password verification
 User login
 JWT access token generation
 JWT expiration
 JWT verification
 Bearer token authentication
 /users/me protected endpoint
 get_current_user() dependency
👮 Authorization
 Added role to User model
 Default role = user
 Public registration cannot choose admin
 Created authorization.py
 Created require_admin()
 Admin endpoint protection
 Tested user → 403
 Tested admin → 200
🗄️ Database
 DATABASE_URL from .env
 Removed create_all()
 Added Alembic
 Created role migration
 Successfully ran alembic upgrade head
 Existing users safely received role=user
🏗️ Clean Architecture
 Created routes/auth.py
 Created services/auth_service.py
 Separated routes from business logic
 Separated authentication from authorization
 Cleaned main.py
 Removed duplicate register/login routes
 Removed unused imports
🚦 Gateway
 Redis rate limiting
 Token bucket algorithm
 Atomic Lua operation
 429 Too Many Requests tested
 Gateway protects authentication requests
🧪 Testing
 Login → 200 OK
 /users/me → 200 OK
 Expired JWT → 401
 Invalid authentication → 401
 Normal user → admin endpoint 403
 Admin → admin endpoint 200
 Rate limit → 429


 ## day 10 

1. Timeout

 Gateway :8000
     ↓
User Service :8001
     ↓
waits 10 seconds
     ↓
Gateway waits only 5 seconds
     ↓
504 Gateway Timeout ✅


### day 11

Completed today:

✅ Added Retry mechanism to Gateway
✅ GET requests retry up to 3 total attempts
✅ POST requests are not retried
✅ Added exponential backoff
Retry 1 → 1 sec
Retry 2 → 2 sec
✅ Tested with User Service stopped
✅ Confirmed Gateway eventually returns 503 Service Unavailable
✅ Confirmed retry attempts in Gateway logs
✅ Timeout + Retry + Backoff are now working together

✅ Retry mechanism
✅ GET-only retry policy
✅ 3 total attempts with MAX_RETRIES=2
✅ Exponential backoff
✅ Configurable MAX_RETRIES
✅ Configurable RETRY_BACKOFF_BASE
✅ Verified that changing .env changes the actual retry behavior
Timeout configuration finish

### sprint 12

Timeout → ✅
Retry → ✅
Circuit Breaker → 🟡 almost complete
Locking → ⏳ next concept

### sprint 13

✅ Timeout — complete
✅ Retry + exponential backoff — complete
✅ Circuit Breaker state machine — complete
✅ Circuit Breaker integration with Gateway — complete
✅ Recovery probe — tested

### sprint 14

✅ Connection failure → Circuit Breaker failure
✅ 3 failures → Circuit opens
✅ OPEN → requests blocked immediately
✅ Recovery timeout → HALF-OPEN probe
✅ Failed probe → OPEN again
✅ Upstream HTTP 500 → counted as failure
✅ Normal 200 → Circuit CLOSED
✅ Temporary /test-error endpoint removed
✅ Normal /api/users still works

1. Circuit Breaker — Integration Testing
 Tested User Service completely unavailable
 Verified connection failures are counted
 Verified 3 consecutive failures → OPEN
 Verified OPEN circuit blocks new requests
 Verified blocked requests return 503 immediately
 Verified recovery timeout
 Verified OPEN → HALF-OPEN
 Verified recovery probe
 Verified failed probe → OPEN
 Verified successful request → CLOSED
2. Circuit Breaker — Debugging
 Added temporary debug output
 Identified why Failures=3, State=CLOSED appeared in the logs
 Confirmed the state transition was happening after the debug print
 Removed temporary debugging output
3. Upstream HTTP 5xx Handling
 Identified an important issue: httpx doesn't automatically treat HTTP 500 as an exception
 Updated proxy_service.py
 Added detection for upstream 5xx responses
 Made 5xx responses count as Circuit Breaker failures
 Kept 4xx responses from being treated as service failures
4. 5xx Testing
 Created temporary /users/test-error endpoint
 Tested Gateway → User Service → HTTP 500
 Verified repeated 500 responses eventually open the Circuit Breaker
 Verified subsequent requests are blocked with 503
 Removed the temporary test endpoint
 Verified normal /api/users still returns 200
🏁 Today's checkpoint

Your resilience layer is now:

                    API Gateway
                         │
                ┌────────▼────────┐
                │  Circuit Breaker│
                └────────┬────────┘
                         │
                     ┌───▼───┐
                     │ Retry │
                     └───┬───┘
                         │
                    ┌────▼─────┐
                    │ Timeout  │
                    └────┬─────┘
                         │
                         ▼
                   User Service

Completed today: Circuit Breaker integration + 5xx failure handling + full testing. ✅

📌 Tomorrow's first task

Per-service Circuit Breakers

We'll solve this architectural issue:

/api/users    → User Service
/api/orders   → Order Service

❌ One global breaker

and move toward:

/api/users    → User Service    → User Circuit Breaker
/api/orders   → Order Service   → Order Circuit Breaker

We'll understand why first, then implement it cleanly.

Enjoy your break — don't change anything in the project tonight. 😄

## sprint - 15

Circuit Breaker: Per-Service Architecture
 Understood why a single global Circuit Breaker is problematic
 Designed separate Circuit Breaker state per upstream service
 Created gateway/resilience/circuit_manager.py
 Implemented CircuitBreakerManager
 Implemented dynamic get_breaker(service_name)
 Updated proxy_service.py to use the manager
 Passed service_name from main.py → forward_request()
 Kept breaker instances persistent across requests
Isolation Testing
 Tested separate users and orders breakers
 Simulated 3 User Service failures
 Confirmed users → OPEN
 Confirmed orders → CLOSED
 Confirmed users requests are blocked
 Confirmed orders requests remain allowed
Real Gateway Testing
 Tested healthy User Service → 200 OK
 Stopped User Service
 Tested repeated failures → 503
 Confirmed retry/timeout behavior
 Confirmed Circuit Breaker opened after threshold
 Confirmed subsequent requests were blocked almost immediately
 Restarted User Service
 Tested recovery after recovery timeout
 Confirmed successful recovery → 200 OK
 Confirmed Circuit Breaker returned to CLOSED

 Circuit Breaker

 Fixed HALF-OPEN race condition using asyncio.Lock
 Tested concurrent requests
 Confirmed 1 probe allowed / 9 blocked
 Confirmed circuit_manager.py does not need a lock

Health Checks

 Created User Service /health
 Added database health check
 Created Gateway health check
 Gateway shows actual service + database health
 Tested healthy service
 Tested User Service down → unhealthy
🎯 Today's result

Circuit Breaker → completed ✅
Health Checks → completed ✅

Next session: 
Gateway Authentication.

summary-
API Gateway — Checkpoint

Here is our current project checkpoint. Everything below is completed and tested unless marked otherwise.

1. Gateway Foundation ✅
FastAPI Gateway created
User Service created
Gateway runs on 8000
User Service runs on 8001
Environment-based configuration with .env
Gateway routing system created
2. Reverse Proxy ✅
Gateway forwards requests to User Service

Dynamic paths work:

/api/users/me → /users/me
Unknown service → 404
Upstream unavailable → 503
Upstream communication error → 502
Gateway preserves upstream status code, body and headers
3. Middleware ✅
Request ID middleware
Request logging middleware
Rate-limit middleware

Request IDs appear in logs:

[10d7a04a-550c-45d7-bab4-db1c03aa48d2]
4. Redis Rate Limiting ✅
Redis-based token bucket
Per-client/IP limiting
Configurable capacity/refill rate
Atomic Lua script
429 Too Many Requests
Rate-limit headers
Retry-After
Fail-open behavior if Redis has a problem
5. User Authentication ✅

User Service has:

Registration
Login
Password hashing
JWT creation
JWT verification
Bearer authentication
Current-user dependency
Role-based authorization
Admin authorization
Pydantic validation
Alembic migrations
6. Gateway Authentication ✅ JUST COMPLETED

This was our recent debugging task.

Architecture:

Client
   ↓
Gateway
   ↓ verify JWT
Gateway
   ↓ forward Authorization header
User Service
   ↓ verify JWT
Protected endpoint

Gateway has its own JWT verification code.

User Service has its own JWT code.

They only share:

JWT_SECRET
JWT_ALGORITHM

We confirmed the secret fingerprints match.

And the final test:

GET /api/users/me

returned:

{
  "id": 6,
  "name": "Test User",
  "email": "test@example.com",
  "role": "user"
}

with:

UPSTREAM STATUS: 200
GET /api/users/me HTTP/1.1" 200 OK

So Gateway → JWT verification → forwarding → User Service authentication is working. ✅

7. Resilience ✅

Completed:

Request timeout
Retry mechanism
Exponential backoff
GET-only retry
Circuit breaker
CLOSED / OPEN / HALF-OPEN states
Per-service circuit breakers
Circuit recovery testing
HALF-OPEN race-condition protection
Concurrency test

We tested the race condition and got:

1 request allowed
9 requests blocked
8. Health Checks ✅

User Service:

GET /health

checks:

Service status
Database connection

Gateway:

GET /health/users

checks the actual User Service.

Tested:

User Service running → healthy
User Service stopped → unhealthy
📍 Where we are now

The project currently looks roughly like:

                         ┌─────────────────┐
                         │     Client      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   API Gateway   │
                         │                 │
                         │ Request ID      │
                         │ Logging         │
                         │ Rate Limiting   │
                         │ JWT Auth   ✅   │
                         │ Routing         │
                         │ Timeout         │
                         │ Retry            │
                         │ Circuit Breaker │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  User Service   │
                         │                 │
                         │ JWT Auth        │
                         │ Authorization   │
                         │ Database        │
                         │ Health Check    │
                         └─────────────────┘
🔜 Next major step

Before moving into more advanced features, we should finish the authentication integration properly:

Protect all appropriate Gateway routes, not just the GET routes.
Test no token → 401
Test invalid token → 401
Test expired token → 401
Test valid token → 200
Test role-based access through Gateway.
Remove temporary JWT debugging prints.

Then we can move forward to the next production concern.

Current checkpoint: Authentication through the Gateway is officially working. 🔐✅

## sprint 16

Reviewed and hardened proxy_service.py
 Forward only existing headers
 Added query-parameter forwarding
 Updated retry.py to support params
 Tested existing JWT /api/users/me → 200
 Tested query forwarding with ?limit=25 → {"limit":25}
 Confirmed the complete request flow: method, path, query params, headers, body
 Remove temporary /users/test endpoint
 Automated tests — next step

 ## sprint 17

 Authentication testing — COMPLETE
 No JWT → 401
 Invalid JWT → 401
 Valid JWT → 200
 Expired JWT → 401
2. Gateway routing — IN PROGRESS
 Unknown service without authentication → 401
 Unknown service with valid JWT → 404
 Dynamic route /api/users/25 → 200
 Test another dynamic ID, e.g. /api/users/99
3. User Service support

We discovered /users/25 didn't exist, so we added:

GET /users/{user_id}

and verified directly:

GET /users/25
→ 200
→ {"id":25,"name":"User 25"}

Then we verified the same request through the Gateway:

GET /api/users/25
→ 200
4. Important debugging lesson

Today we followed the correct debugging flow:

Gateway test failed
       ↓
Test upstream directly
       ↓
User Service returned 404
       ↓
Fix User Service route
       ↓
Test User Service directly → 200
       ↓
Test Gateway again → 200

This is exactly how we should debug the project instead of randomly changing Gateway code.

📌 Tomorrow's starting point

First:

/api/users/99

Then:

Request forwarding tests

Query parameters
Headers
Request body
POST
PUT
DELETE

After that we'll continue with the remaining integration tests.

## sprint 18

Today's checkpoint: Gateway dynamic routing is confirmed working for /api/users/25.

ested dynamic path forwarding
 Tested query parameter forwarding
 Tested Authorization header forwarding
 Tested JSON request-body forwarding
 Fixed test-file syntax error
 All related tests passed
 Committed/pushed request-forwarding test checkpoint

Concept learned: Gateway must preserve important parts of the incoming request — path, query params, headers, and body — when forwarding to the upstream service.

## sprint 19

 Made GET /users/{user_id} admin-only
 Added require_admin() authorization
 Verified normal user → 403
 Created admin user using scripts/create_admin.py
 Verified admin → 200
 Verified admin + nonexistent user → 404
 Understood authentication vs authorization
 Understood why API security matters
 Understood the Gateway → User Service → DB flow

Checkpoint: Admin authorization for the user-details API is complete.


