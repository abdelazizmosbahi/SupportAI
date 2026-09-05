# SupportAI — AI Customer Support Platform

> A production-oriented, multi-tenant AI customer-support platform built with React, FastAPI, PostgreSQL/pgvector, local open-source LLMs, Docker, CI/CD, observability, and infrastructure automation.

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Goals](#2-project-goals)
3. [Core Features](#3-core-features)
4. [Architecture](#4-architecture)
5. [Technology Stack](#5-technology-stack)
6. [System Components](#6-system-components)
7. [User Roles](#7-user-roles)
8. [Multi-Tenancy](#8-multi-tenancy)
9. [Authentication and Authorization](#9-authentication-and-authorization)
10. [Frontend Architecture](#10-frontend-architecture)
11. [Backend Architecture](#11-backend-architecture)
12. [Database Architecture](#12-database-architecture)
13. [Document Management](#13-document-management)
14. [RAG Pipeline](#14-rag-pipeline)
15. [LLM Architecture](#15-llm-architecture)
16. [Conversation System](#16-conversation-system)
17. [Human Handoff](#17-human-handoff)
18. [AI Evaluation](#18-ai-evaluation)
19. [Analytics](#19-analytics)
20. [Background Jobs](#20-background-jobs)
21. [Caching](#21-caching)
22. [File Storage](#22-file-storage)
23. [API Design](#23-api-design)
24. [Error Handling](#24-error-handling)
25. [Security](#25-security)
26. [Rate Limiting](#26-rate-limiting)
27. [Logging](#27-logging)
28. [Observability](#28-observability)
29. [Testing Strategy](#29-testing-strategy)
30. [Docker](#30-docker)
31. [Local Development](#31-local-development)
32. [CI/CD](#32-cicd)
33. [Infrastructure as Code](#33-infrastructure-as-code)
34. [Deployment](#34-deployment)
35. [Networking](#35-networking)
36. [Monitoring](#36-monitoring)
37. [Backup and Recovery](#37-backup-and-recovery)
38. [Environment Management](#38-environment-management)
39. [Project Structure](#39-project-structure)
40. [Database Migrations](#40-database-migrations)
41. [Development Workflow](#41-development-workflow)
42. [Git Strategy](#42-git-strategy)
43. [Documentation](#43-documentation)
44. [Performance](#44-performance)
45. [Scalability](#45-scalability)
46. [AI Safety](#46-ai-safety)
47. [RAG Failure Handling](#47-rag-failure-handling)
48. [Definition of Done](#48-definition-of-done)
49. [Implementation Roadmap](#49-implementation-roadmap)
50. [CV Description](#50-cv-description)
51. [Interview Topics](#51-interview-topics)
52. [Final Architecture](#52-final-architecture)

---

# 1. Project Overview

## 1.1 What is SupportAI?

SupportAI is a full-stack AI customer-support platform designed to help companies manage customer conversations using an AI assistant backed by their own internal knowledge base.

The system allows organizations to:

- Create an organization/workspace
- Invite users
- Assign roles
- Upload company documentation
- Build a searchable knowledge base
- Automatically process documents
- Generate embeddings
- Store vectors in PostgreSQL
- Ask questions about company documentation
- Generate AI responses using RAG
- Display citations/sources
- Maintain conversation history
- Escalate conversations to human agents
- Evaluate AI response quality
- Monitor system performance
- View analytics
- Audit important actions

The platform is designed as a realistic SaaS-style application.

---

# 2. Project Goals

The project is intended to demonstrate knowledge of:

## Frontend

- React
- TypeScript
- TanStack Query
- Component architecture
- State management
- Forms
- Authentication
- Protected routes
- HTTP client interceptors (axios)
- Error handling
- Responsive UI
- Real-time interfaces

## Backend

- Python
- FastAPI
- REST APIs
- WebSockets/SSE
- SQLAlchemy
- Pydantic
- Dependency injection
- Authentication
- Authorization
- Background processing
- API security

## Database

- PostgreSQL
- Relational database design
- Indexing
- Transactions
- Foreign keys
- Query optimization
- pgvector
- Vector similarity search

## AI

- LLMs
- RAG
- Embeddings
- Chunking
- Retrieval
- Prompt engineering
- Context management
- Hallucination mitigation
- AI evaluation
- Local model serving

## DevOps

- Linux
- Docker
- Docker Compose
- CI/CD
- GitHub Actions
- Infrastructure as Code
- Terraform
- Reverse proxy
- Monitoring
- Logging
- Metrics
- Distributed tracing

## Software Engineering

- Clean architecture
- SOLID principles
- Design patterns
- Automated testing
- Documentation
- Git workflows
- Security
- Observability

---

# 3. Core Features

The application should contain the following modules:

```text
Authentication
    |
    +-- Login
    +-- Registration
    +-- Logout
    +-- Password management
    +-- Token refresh
    +-- Session management

Organizations
    |
    +-- Create organization
    +-- Organization settings
    +-- Members
    +-- Roles
    +-- Invitations

Knowledge Base
    |
    +-- Upload documents
    +-- Document processing
    +-- Document status
    +-- Delete documents
    +-- Search documents
    +-- View document metadata

AI Assistant
    |
    +-- New conversation
    +-- Ask questions
    +-- Streaming responses
    +-- Source citations
    +-- Conversation history
    +-- Feedback

Support
    |
    +-- Human handoff
    +-- Tickets
    +-- Agent dashboard
    +-- Conversation assignment
    +-- Ticket status

Evaluation
    |
    +-- Test datasets
    +-- RAG evaluation
    +-- Answer quality
    +-- Retrieval quality
    +-- Performance metrics

Analytics
    |
    +-- Conversations
    +-- Resolution rate
    +-- AI usage
    +-- Escalations
    +-- Response time

Administration
    |
    +-- Users
    +-- Roles
    +-- Permissions
    +-- Audit logs
    +-- System configuration

4. Architecture

High-level architecture:

                         INTERNET
                            |
                            v
                    +---------------+
                    |     Nginx     |
                    | Reverse Proxy |
                    +-------+-------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
       +-------------+             +-------------+
        |    React    |             |   FastAPI   |
       |   Frontend  |             |   Backend   |
       +-------------+             +------+------+ 
                                           |
              +----------------------------+--------------------+
              |              |             |                    |
              v              v             v                    v
        +----------+   +----------+   +----------+       +----------+
        |PostgreSQL|   |  Redis   |   |  MinIO   |       |  Ollama  |
        |+ pgvector|   | Cache/Q  |   | Storage  |       | Local LLM|
        +----------+   +----+-----+   +----------+       +----------+
                             |
                             v
                       +-----------+
                       |  Celery   |
                       |  Workers  |
                       +-----------+

                     OBSERVABILITY
                           |
              +------------+------------+
              |            |            |
              v            v            v
        +----------+  +----------+  +----------+
        |Prometheus|  |   Loki   |  |  Jaeger  |
        +----+-----+  +----------+  +----------+
             |
             v
        +----------+
        | Grafana  |
        +----------+

5. Technology Stack
5.1 Frontend
React
TypeScript
TanStack Query
MUI Material
Tailwind CSS

5.2 Backend
Python
FastAPI
Pydantic
SQLAlchemy 2
Alembic
Celery
Redis

5.3 AI
Ollama
LlamaIndex
Hugging Face
Sentence Transformers
Open-source LLMs


Possible local models:

Qwen
Llama
Mistral


The exact model should depend on the available hardware.

5.4 Database
PostgreSQL
pgvector


PostgreSQL stores both relational information and embeddings.

5.5 Storage
MinIO


MinIO provides S3-compatible object storage while remaining self-hosted.

5.6 Infrastructure
Docker
Docker Compose
Nginx
Terraform

5.7 CI/CD
GitHub
GitHub Actions

5.8 Observability
Prometheus
Grafana
Loki
OpenTelemetry
Jaeger

5.9 Testing
Pytest
Playwright
React Testing Library

6. System Components

The platform consists of:

frontend
backend
database
redis
celery-worker
minio
ollama
nginx
prometheus
grafana
loki
jaeger


Each component has one responsibility.

7. User Roles

The application supports:

OWNER

Full access.

Permissions:

organization.read
organization.update
members.read
members.create
members.update
members.delete
documents.read
documents.create
documents.delete
conversations.read
conversations.create
conversations.assign
evaluations.read
analytics.read
audit.read

ADMIN

Administrative access except ownership operations.

AGENT

Can manage support conversations.

VIEWER

Read-only access.

8. Multi-Tenancy

SupportAI is multi-tenant.

Each organization represents an isolated tenant.

Example:

Organization A

Users
Documents
Conversations
Tickets
Evaluations
Audit logs


Organization B has completely separate data.

Every tenant-owned database record should contain:

organization_id


Example:

documents
---------
id
organization_id
filename
status
created_at


Every query must enforce tenant isolation.

Bad:

session.query(Document).all()


Better:

session.query(Document).filter(
    Document.organization_id == current_user.organization_id
).all()


Tenant isolation must also exist in:

documents
conversations
messages
tickets
evaluations
analytics
audit logs
9. Authentication and Authorization

Authentication should use:

JWT
OAuth2-compatible flows


Access token:

short-lived


Refresh token:

longer-lived


The backend validates tokens.

React uses an HTTP client interceptor (axios) to attach:

Authorization: Bearer <token>

9.1 Password Security

Never store plaintext passwords.

Use:

Argon2


for password hashing.

9.2 React Route Guards

Example protected routes:

/dashboard
/conversations
/knowledge-base
/evaluations
/analytics
/settings
/admin


Unauthenticated users are redirected to:

/login

9.3 RBAC

Authorization must happen on the backend.

Frontend hiding a button is not security.

Example:

Agent
  |
  +-- Can read conversations
  +-- Can respond
  +-- Cannot manage organization

10. Frontend Architecture

Recommended React structure:

frontend/src/
├── api/
│   ├── client.ts
│   └── auth.ts
├── auth/
│   ├── AuthContext.tsx
│   └── ProtectedRoute.tsx
├── features/
│   ├── dashboard/
│   ├── conversations/
│   ├── knowledge-base/
│   ├── evaluations/
│   ├── analytics/
│   ├── tickets/
│   └── settings/
├── layout/
│   ├── AppLayout.tsx
│   ├── Sidebar.tsx
│   └── Header.tsx
├── pages/
│   ├── Login.tsx
│   └── Register.tsx
├── App.tsx
└── main.tsx

10.1 Main Pages
Login
Email
Password
Login
Forgot password

Dashboard

Show:

Total conversations
Open tickets
AI resolution rate
Average response time
Documents
AI evaluation score

Conversations

Two-panel layout:

+-------------------+------------------------+
| Conversations     | Conversation           |
|                   |                        |
| John              | Customer message       |
| Sarah             | AI response            |
| Ahmed             | Source citations       |
|                   |                        |
|                   | Message input         |
+-------------------+------------------------+

Knowledge Base
Upload document

Documents
-------------------------------
filename
type
size
status
chunks
created
actions

Evaluation

Show:

Faithfulness
Answer relevance
Context precision
Context recall
Latency

Analytics

Display:

Conversation volume
AI resolution
Escalation rate
Average response time
Top questions

11. Backend Architecture

Use a layered architecture.

API
 |
 v
Services
 |
 v
Repositories
 |
 v
Database


Recommended structure:

backend/
└── app/
    ├── main.py
    │
    ├── api/
    │   ├── auth.py
    │   ├── users.py
    │   ├── organizations.py
    │   ├── conversations.py
    │   ├── documents.py
    │   ├── tickets.py
    │   ├── evaluations.py
    │   ├── analytics.py
    │   └── admin.py
    │
    ├── core/
    │   ├── config.py
    │   ├── security.py
    │   ├── database.py
    │   └── logging.py
    │
    ├── models/
    │
    ├── schemas/
    │
    ├── repositories/
    │
    ├── services/
    │
    ├── rag/
    │
    ├── llm/
    │
    ├── evaluation/
    │
    ├── workers/
    │
    └── utils/

12. Database Architecture

Main entities:

User
Organization
Membership
Role
Permission
Document
DocumentChunk
Conversation
Message
Ticket
Evaluation
EvaluationResult
AuditLog
RefreshToken

12.1 Entity Relationships
Organization
     |
     +---- Users
     |
     +---- Documents
     |       |
     |       +---- Chunks
     |
     +---- Conversations
     |       |
     |       +---- Messages
     |
     +---- Tickets
     |
     +---- Evaluations
     |
     +---- AuditLogs

12.2 Users
users
-----
id
email
password_hash
first_name
last_name
is_active
created_at
updated_at

12.3 Organizations
organizations
-------------
id
name
slug
created_at
updated_at

12.4 Membership
memberships
-----------
id
user_id
organization_id
role_id
created_at

12.5 Documents
documents
---------
id
organization_id
filename
mime_type
storage_key
size
status
error_message
created_by
created_at
updated_at


Statuses:

UPLOADED
PROCESSING
PROCESSED
FAILED
DELETED

12.6 Document Chunks
document_chunks
---------------
id
document_id
organization_id
content
chunk_index
embedding
metadata
created_at


The embedding column uses pgvector.

12.7 Conversations
conversations
-------------
id
organization_id
customer_id
assigned_agent_id
status
priority
created_at
updated_at


Statuses:

OPEN
IN_PROGRESS
WAITING
RESOLVED
CLOSED

12.8 Messages
messages
--------
id
conversation_id
sender_type
content
model
tokens
latency_ms
created_at


Sender types:

CUSTOMER
AI
AGENT
SYSTEM

12.9 Tickets
tickets
-------
id
organization_id
conversation_id
assigned_agent_id
status
priority
reason
created_at
updated_at

12.10 Audit Logs
audit_logs
----------
id
organization_id
user_id
action
resource_type
resource_id
ip_address
metadata
created_at


Example:

USER_LOGIN
DOCUMENT_UPLOADED
DOCUMENT_DELETED
CONVERSATION_ASSIGNED
ROLE_CHANGED

13. Document Management

Supported formats:

PDF
TXT
DOCX


Future:

HTML
CSV
Markdown

13.1 Upload Flow
React
   |
   | multipart/form-data
   v
FastAPI
   |
   v
Validate file
   |
   v
Store in MinIO
   |
   v
Create DB record
   |
   v
Queue Celery task
   |
   v
Return response


The user should not have to wait for document processing.

13.2 File Validation

Validate:

extension
MIME type
file size
filename
content


Never trust the extension alone.

13.3 Document Processing

Pipeline:

Download from MinIO
        |
        v
Extract text
        |
        v
Normalize text
        |
        v
Remove unnecessary content
        |
        v
Split into chunks
        |
        v
Generate embeddings
        |
        v
Store chunks + vectors

14. RAG Pipeline

RAG means:

Retrieval-Augmented Generation


The AI does not rely exclusively on its pretrained knowledge.

It retrieves relevant company documents first.

14.1 Query Flow
Customer question
       |
       v
Normalize query
       |
       v
Generate embedding
       |
       v
Search pgvector
       |
       v
Retrieve Top-K chunks
       |
       v
Optional metadata filtering
       |
       v
Build context
       |
       v
Prompt LLM
       |
       v
Generate answer
       |
       v
Return citations

14.2 Chunking

Documents should be split into meaningful chunks.

Example:

chunk_size = 500-1000 tokens
overlap = 50-150 tokens


These values should be configurable.

14.3 Metadata

Each chunk should contain metadata:

{
  "document_id": "...",
  "page": 4,
  "filename": "refund-policy.pdf",
  "organization_id": "...",
  "document_type": "policy"
}

14.4 Retrieval

Retrieve:

Top K = 5


initially.

Then experiment with:

K = 3
K = 5
K = 8
K = 10


Evaluate which configuration performs best.

14.5 Similarity Search

pgvector can perform vector similarity search.

Conceptually:

question embedding
        |
        v
compare with chunk embeddings
        |
        v
similarity score
        |
        v
Top K

14.6 Citations

The AI response should contain citations.

Example:

Your refund request can be submitted within 30 days
of the original purchase.

Sources:
- Refund Policy — Page 4
- Customer Terms — Section 3.2


The frontend should make citations clickable.

15. LLM Architecture

Do not couple the application directly to one model.

Create an abstraction.

LLMProvider
    |
    +-- OllamaProvider


Future providers could be added:

OpenAIProvider
AnthropicProvider
GeminiProvider


The application should not need to change.

15.1 LLM Interface

Conceptually:

class LLMProvider:

    async def generate(
        self,
        prompt: str,
        system_prompt: str
    ) -> str:
        ...


Streaming:

async def stream(
    self,
    prompt: str,
    system_prompt: str
):
    ...

15.2 Local AI

Use:

Ollama


to serve local models.

Possible models:

Qwen
Llama
Mistral


The model can be configured using environment variables.

Example:

LLM_MODEL=qwen

16. Conversation System

Every conversation contains:

Customer
Messages
Status
Priority
Assigned agent
Created date
Updated date


Messages contain:

sender
content
timestamp
model
latency
token usage
sources

16.1 Streaming

AI responses should stream to the frontend.

Flow:

React
   |
   | POST message
   v
FastAPI
   |
   v
RAG
   |
   v
Ollama
   |
   | streaming tokens
   v
FastAPI
   |
   | SSE
   v
React


This creates a real-time ChatGPT-style experience.

17. Human Handoff

The AI should not attempt to answer every question.

If:

retrieval confidence is low


or:

user explicitly requests human


the conversation can be escalated.

Flow:

Customer
   |
   v
AI
   |
   v
Low confidence
   |
   v
Create ticket
   |
   v
Assign agent

17.1 Agent Dashboard

Agents should see:

Customer
Conversation
AI summary
Relevant documents
AI answer
Customer messages
Ticket priority


The agent can:

Reply
Assign
Change priority
Resolve
Close
Escalate

18. AI Evaluation

Evaluation is a major component of the project.

The system should measure:

Faithfulness
Answer relevance
Context precision
Context recall
Latency

18.1 Evaluation Dataset

Create a dataset:

Question
Expected answer
Relevant document
Expected source


Example:

{
  "question": "How long do refunds take?",
  "expected_answer": "Refunds are processed within 5 business days.",
  "source": "refund-policy.pdf"
}

18.2 Evaluation Pipeline
Evaluation dataset
       |
       v
Run RAG
       |
       v
Generate answer
       |
       v
Compare result
       |
       v
Calculate metrics
       |
       v
Store results
       |
       v
React dashboard

18.3 Evaluation Dashboard

Display:

Faithfulness             92%
Answer relevance         90%
Context precision        88%
Context recall            94%

Average retrieval       180ms
Average generation      2.4s

18.4 Regression Testing

Every important RAG change should be testable against the evaluation dataset.

Example:

Before change
Faithfulness: 92%

After change
Faithfulness: 87%

=> Regression detected


CI can optionally fail when quality drops below a configured threshold.

19. Analytics

The platform should provide:

Total conversations
Open conversations
Resolved conversations
Escalated conversations
AI resolution rate
Average response time
Average resolution time
Messages per conversation

19.1 AI Analytics

Track:

Model
Request count
Latency
Token usage
Errors
Fallbacks

19.2 Knowledge Base Analytics

Track:

Documents
Processing failures
Number of chunks
Most retrieved documents
Documents with no retrieval hits

20. Background Jobs

Use:

Celery
Redis


for asynchronous work.

Jobs include:

Document processing
Embedding generation
Evaluation
Analytics aggregation
Cleanup

20.1 Job Flow
FastAPI
   |
   v
Redis queue
   |
   v
Celery worker
   |
   v
Process task
   |
   v
Update database


This prevents long-running operations from blocking API requests.

21. Caching

Use Redis for:

rate limiting
temporary data
cached responses
job queues


Do not cache sensitive information carelessly.

Cache keys should include tenant context.

Example:

org:{organization_id}:question:{hash}

22. File Storage

Use:

MinIO


Buckets:

documents
avatars
exports


Files should not be stored directly inside PostgreSQL.

PostgreSQL stores:

storage_key
filename
mime_type
size


MinIO stores the actual file.

23. API Design

Use REST APIs.

Base path:

/api/v1

23.1 Authentication
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/me

23.2 Organizations
GET    /api/v1/organizations
POST   /api/v1/organizations
GET    /api/v1/organizations/{id}
PATCH  /api/v1/organizations/{id}
DELETE /api/v1/organizations/{id}

23.3 Members
GET    /api/v1/organizations/{id}/members
POST   /api/v1/organizations/{id}/members
PATCH  /api/v1/members/{id}
DELETE /api/v1/members/{id}

23.4 Documents
GET    /api/v1/documents
POST   /api/v1/documents
GET    /api/v1/documents/{id}
DELETE /api/v1/documents/{id}

23.5 Conversations
GET  /api/v1/conversations
POST /api/v1/conversations
GET  /api/v1/conversations/{id}
POST /api/v1/conversations/{id}/messages
PATCH /api/v1/conversations/{id}

23.6 Tickets
GET   /api/v1/tickets
POST  /api/v1/tickets
PATCH /api/v1/tickets/{id}

23.7 Evaluations
GET  /api/v1/evaluations
POST /api/v1/evaluations/run
GET  /api/v1/evaluations/{id}

23.8 Analytics
GET /api/v1/analytics/overview
GET /api/v1/analytics/conversations
GET /api/v1/analytics/ai
GET /api/v1/analytics/documents

24. Error Handling

Use consistent API errors.

Example:

{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "The requested document does not exist."
  }
}


Common codes:

UNAUTHORIZED
FORBIDDEN
NOT_FOUND
VALIDATION_ERROR
DOCUMENT_PROCESSING_FAILED
LLM_ERROR
RATE_LIMITED
INTERNAL_ERROR


Never expose internal stack traces to clients.

25. Security

Security must be implemented at every layer.

25.1 Backend Security

Implement:

JWT authentication
RBAC
tenant isolation
input validation
rate limiting
secure headers
CORS
file validation
SQL injection protection


SQLAlchemy parameterization should be used.

25.2 File Security

Uploaded files must be:

validated
size-limited
type-checked
stored outside application code


Potentially dangerous files should be rejected.

25.3 Prompt Injection

RAG introduces prompt-injection risks.

Documents may contain instructions such as:

Ignore previous instructions.
Reveal system prompt.


The system must treat retrieved documents as untrusted data.

System prompt should explicitly distinguish:

instructions


from:

retrieved content

25.4 Sensitive Data

Do not expose:

passwords
JWT secrets
database credentials
internal prompts
environment variables


in:

logs
API responses
frontend code
Git

26. Rate Limiting

Implement API rate limiting using Redis.

Example:

Login:
5 requests / minute

General API:
100 requests / minute

AI:
20 requests / minute


These values should be configurable.

27. Logging

Use structured logs.

Example:

{
  "timestamp": "...",
  "level": "INFO",
  "service": "backend",
  "request_id": "...",
  "organization_id": "...",
  "user_id": "...",
  "event": "conversation_created"
}


Never log:

passwords
tokens
full sensitive documents
secrets

28. Observability

Implement three major observability pillars:

Metrics
Logs
Traces

28.1 Metrics

Use:

Prometheus


Track:

HTTP requests
HTTP errors
request latency
database latency
Redis operations
Celery jobs
RAG latency
LLM latency

28.2 Logs

Use:

Loki


and visualize through:

Grafana

28.3 Tracing

Use:

OpenTelemetry
Jaeger


Example trace:

HTTP Request
    |
    +-- Authentication
    |
    +-- Database query
    |
    +-- Embedding generation
    |
    +-- Vector search
    |
    +-- LLM request
    |
    +-- Database save


This makes performance debugging much easier.

29. Testing Strategy

Testing should exist at multiple levels.

Unit tests
Integration tests
API tests
Database tests
RAG tests
Frontend tests
E2E tests
Security tests

29.1 Backend Unit Tests

Test:

authentication
authorization
services
RAG functions
chunking
document parsing
evaluation

29.2 API Tests

Test:

POST /login
GET /conversations
POST /documents
POST /messages

29.3 Tenant Isolation Tests

Critical tests:

Organization A cannot access Organization B documents.

Organization A cannot access Organization B conversations.

Organization A cannot retrieve Organization B embeddings.

29.4 RAG Tests

Test:

retrieval accuracy
citation correctness
empty retrieval
irrelevant question
long question
duplicate documents

29.5 Frontend Tests

Test:

components
services
guards
interceptors
forms

29.6 E2E Tests

Use:

Playwright


Example:

Register
   ↓
Create organization
   ↓
Login
   ↓
Upload document
   ↓
Wait for processing
   ↓
Start conversation
   ↓
Ask question
   ↓
Receive AI response
   ↓
Verify citation

30. Docker

Every service should be containerized.

Services:

frontend
backend
postgres
redis
celery
minio
ollama
nginx
prometheus
grafana
loki
jaeger

30.1 Development Docker Compose

Conceptual:

services:

  frontend:
    build: ./frontend

  backend:
    build: ./backend

  postgres:
    image: postgres

  redis:
    image: redis

  celery:
    build: ./backend

  minio:
    image: minio/minio

  ollama:
    image: ollama/ollama

  nginx:
    image: nginx

  prometheus:
    image: prometheus

  grafana:
    image: grafana/grafana

  loki:
    image: grafana/loki

  jaeger:
    image: jaegertracing/all-in-one


Exact image versions should be pinned in the actual project.

30.2 Health Checks

Every important service should expose or support health checks.

Backend:

GET /health


Database:

PostgreSQL health check


Redis:

Redis health check

31. Local Development

Prerequisites:

Git
Docker
Docker Compose
Node.js
Python
Vite


Optional:

NVIDIA GPU


for faster local LLM inference.

31.1 Start Project
git clone <repository>

cd supportai

docker compose up -d


Then:

Frontend:
http://localhost

Backend:
http://localhost/api

API documentation:
http://localhost/docs

Grafana:
http://localhost/grafana

MinIO:
http://localhost/minio


Actual ports should be documented in the project.

31.2 Environment Variables

Example:

APP_ENV=development

DATABASE_URL=postgresql://...

REDIS_URL=redis://...

MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=...
MINIO_SECRET_KEY=...

JWT_SECRET=...

LLM_PROVIDER=ollama
LLM_MODEL=...

EMBEDDING_MODEL=...

LOG_LEVEL=INFO


Never commit:

.env


to Git.

Commit:

.env.example


instead.

32. CI/CD

Use GitHub Actions.

Pipeline:

Pull Request
     |
     v
Lint
     |
     v
Type checking
     |
     v
Unit tests
     |
     v
Integration tests
     |
     v
E2E tests
     |
     v
Security scan
     |
     v
Docker build
     |
     v
RAG evaluation

32.1 Backend CI

Run:

ruff
mypy
pytest

32.2 Frontend CI

Run:

npm ci
npm run lint
npm test
npm run build

32.3 Docker CI

Build:

frontend image
backend image
worker image


Run containers and perform health checks.

32.4 Security Scanning

Use free/open-source scanners such as:

Trivy
Bandit
pip-audit
npm audit


Scan:

dependencies
Docker images
source code

33. Infrastructure as Code

Use:

Terraform


Infrastructure should be reproducible.

Example:

infrastructure/
├── main.tf
├── variables.tf
├── outputs.tf
├── providers.tf
└── modules/


Possible modules:

network
compute
database
storage
monitoring

33.1 Why Terraform?

It demonstrates:

Infrastructure as Code
reproducible infrastructure
configuration management
environment consistency

34. Deployment

The application should support deployment to a Linux server.

Architecture:

Internet
   |
   v
Nginx
   |
   +----------------+
   |                |
   v                v
React             FastAPI
                     |
          +----------+----------+
          |          |          |
          v          v          v
      PostgreSQL   Redis      MinIO
                     |
                     v
                  Celery
                     |
                     v
                   Ollama


Everything runs through Docker.

34.1 HTTPS

Production should use HTTPS.

Nginx terminates TLS.

Certificates can be managed using:

Let's Encrypt

34.2 Domain

Example:

supportai.example.com


The actual domain is optional for local development.

35. Networking

Containers should communicate through private Docker networks.

Example:

frontend-network
backend-network
database-network
observability-network


The database should not be publicly accessible.

Bad:

Internet -> PostgreSQL


Good:

Internet
   |
   v
Nginx
   |
   v
Backend
   |
   v
PostgreSQL

36. Monitoring

Grafana dashboards should include:

API
Requests/sec
Error rate
P50 latency
P95 latency
P99 latency

Database
Connections
Query latency
CPU
Memory

Redis
Memory
Commands
Connections

Celery
Queued jobs
Running jobs
Failed jobs
Execution time

AI
LLM latency
Embedding latency
RAG latency
Errors

37. Backup and Recovery

PostgreSQL should have regular backups.

Example strategy:

Daily database dump


Store backups separately from the running database.

Documents stored in MinIO should also be backed up.

Recovery should be tested.

A backup that has never been restored is not a proven backup.

37.1 Recovery Procedure
1. Stop affected services
2. Restore PostgreSQL
3. Restore MinIO data
4. Verify database integrity
5. Start backend
6. Start workers
7. Verify health endpoints
8. Run smoke tests

38. Environment Management

Support:

development
testing
production


Example:

.env.development
.env.test
.env.production


Production secrets should never be committed.

39. Project Structure

Recommended repository:

supportai/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── vite.config.ts
│   ├── package.json
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── rag/
│   │   ├── llm/
│   │   ├── evaluation/
│   │   ├── workers/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── alembic/
│   ├── pyproject.toml
│   └── Dockerfile
│
├── infrastructure/
│   └── terraform/
│
├── docker/
│   ├── nginx/
│   ├── postgres/
│   ├── prometheus/
│   ├── grafana/
│   └── loki/
│
├── evaluation/
│   ├── datasets/
│   ├── scripts/
│   └── results/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── deployment/
│   └── decisions/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── .env.example
├── .gitignore
├── Makefile
└── README.md

40. Database Migrations

Use:

Alembic


Never manually modify production tables.

Development workflow:

Modify SQLAlchemy model
        |
        v
Generate migration
        |
        v
Review migration
        |
        v
Run migration


Example:

alembic revision --autogenerate -m "add tickets"
alembic upgrade head

41. Development Workflow

Feature development:

Create issue
    |
    v
Create branch
    |
    v
Implement feature
    |
    v
Write tests
    |
    v
Run locally
    |
    v
Open Pull Request
    |
    v
CI
    |
    v
Code review
    |
    v
Merge

42. Git Strategy

Use:

main
develop
feature/*
bugfix/*


Example:

feature/rag-retrieval
feature/document-upload
feature/agent-dashboard
feature/evaluation
bugfix/tenant-isolation


Commit messages:

feat: add document ingestion pipeline
fix: enforce tenant isolation
test: add RAG retrieval tests
refactor: introduce LLM provider interface
docs: add deployment documentation

43. Documentation

The repository should contain:

README
Architecture documentation
API documentation
Database diagram
ER diagram
Deployment guide
Local development guide
Testing guide
RAG documentation
Security documentation
ADR documents

43.1 Architecture Decision Records

Create ADRs for important decisions.

Examples:

ADR-001: PostgreSQL as primary database
ADR-002: pgvector instead of dedicated vector database
ADR-003: MinIO for object storage
ADR-004: Ollama for local LLM inference
ADR-005: Celery for background jobs
ADR-006: Docker Compose for deployment


This demonstrates architectural thinking.

44. Performance

Performance goals:

API P95 < 500ms


excluding long-running LLM generation.

RAG retrieval:

< 500ms


Document processing:

asynchronous


AI responses:

streamed

44.1 Database Optimization

Use:

indexes
foreign-key indexes
vector indexes
pagination
connection pooling


Never return thousands of records to the React frontend at once.

Use:

limit
offset
cursor pagination


where appropriate.

45. Scalability

The system should be designed so components can scale independently.

Example:

                 Load Balancer
                      |
          +-----------+-----------+
          |           |           |
       FastAPI     FastAPI     FastAPI
          |           |           |
          +-----------+-----------+
                      |
                 PostgreSQL


Celery workers can scale separately:

worker x1
worker x2
worker x3


This is particularly useful for document processing.

45.1 Stateless Backend

FastAPI instances should be stateless.

State should live in:

PostgreSQL
Redis
MinIO


This allows horizontal scaling.

46. AI Safety

The assistant should have explicit rules.

It should:

Use retrieved context when available
Avoid inventing company policies
State uncertainty
Provide sources
Escalate when appropriate


If no relevant context exists:

"I don't have enough information in the company's knowledge base to answer that confidently."


rather than hallucinating.

47. RAG Failure Handling

Possible failures:

No documents
No relevant chunks
Embedding failure
LLM failure
Database failure
Document parsing failure

47.1 No Relevant Documents

Return:

I couldn't find enough relevant information in the knowledge base to answer this question confidently.


Offer:

Contact a human agent

47.2 LLM Failure

Implement fallback behavior:

LLM unavailable
      |
      v
Return friendly error
      |
      v
Offer human handoff


Never expose:

stack traces
internal URLs
credentials

48. Definition of Done

A feature is considered complete when:

Code implemented
Tests written
API documented
Frontend implemented
Error handling implemented
Security reviewed
Logging added
Metrics added if relevant
Docker tested
CI passes
Documentation updated

49. Implementation Roadmap

The project should NOT be built all at once.

Phase 1 — Project Setup

Implement:

Git repository
React
FastAPI
PostgreSQL
Docker Compose
Basic CI


Deliverable:

React -> FastAPI -> PostgreSQL

Phase 2 — Authentication

Implement:

Registration
Login
JWT
Refresh tokens
Password hashing
React protected routes
HTTP client interceptor (axios)


Deliverable:

Authenticated application

Phase 3 — Organizations

Implement:

Organizations
Members
Roles
RBAC
Tenant isolation


Deliverable:

Multi-tenant backend

Phase 4 — Knowledge Base

Implement:

MinIO
File uploads
PDF extraction
Document records
Celery
Redis


Deliverable:

Upload PDF
    |
    v
MinIO
    |
    v
Celery
    |
    v
Extract text

Phase 5 — Embeddings

Implement:

Chunking
Embedding generation
pgvector
Vector indexes


Deliverable:

PDF
 ↓
Chunks
 ↓
Embeddings
 ↓
PostgreSQL

Phase 6 — RAG

Implement:

Query embedding
Vector retrieval
Context building
Prompt construction
Ollama
Citations


Deliverable:

Question
 ↓
RAG
 ↓
AI answer
 ↓
Sources

Phase 7 — Chat

Implement:

Conversation creation
Messages
Conversation history
SSE streaming
AI responses


Deliverable:

ChatGPT-style support interface

Phase 8 — Human Handoff

Implement:

Tickets
Agent dashboard
Assignment
Priority
Status
AI summary


Deliverable:

AI -> Human workflow

Phase 9 — Evaluation

Implement:

Evaluation datasets
RAG metrics
Evaluation runs
Evaluation dashboard
Regression detection


Deliverable:

AI quality monitoring

Phase 10 — Analytics

Implement:

Conversation analytics
AI analytics
Knowledge base analytics

Phase 11 — Security

Perform:

Tenant isolation testing
RBAC testing
Rate limiting
File validation
Security headers
Dependency scanning

Phase 12 — Observability

Implement:

Prometheus
Grafana
Loki
OpenTelemetry
Jaeger

Phase 13 — Testing

Complete:

Unit tests
Integration tests
API tests
RAG tests
E2E tests


Target:

High coverage of business-critical code

Phase 14 — CI/CD

Implement:

Lint
Tests
Security scans
Docker builds
RAG evaluation
Deployment pipeline

Phase 15 — Production Deployment

Implement:

Linux server
Docker Compose
Nginx
HTTPS
Backups
Monitoring
Alerting

50. CV Description
Short Version

SupportAI — AI Customer Support Platform

Built a multi-tenant AI customer-support platform using React, FastAPI,
PostgreSQL/pgvector and locally hosted open-source LLMs, implementing
RAG-based document retrieval, streaming conversations, human handoff,
RBAC, automated AI evaluation, background processing and audit logging.
Containerized the complete system with Docker and implemented CI/CD,
infrastructure automation, monitoring, logging and distributed tracing.

50.1 Technology Keywords

The project demonstrates:

React
TypeScript
TanStack Query
Python
FastAPI
REST
SSE
PostgreSQL
pgvector
SQLAlchemy
Alembic
Redis
Celery
RAG
LLM
Ollama
Embeddings
LlamaIndex
Hugging Face
MinIO
Docker
Docker Compose
Nginx
GitHub Actions
Terraform
Prometheus
Grafana
Loki
OpenTelemetry
Jaeger
Pytest
Playwright
JWT
RBAC
Multi-tenancy
CI/CD

51. Interview Topics

This project should allow you to discuss:

Frontend
React architecture
TanStack Query
HTTP interceptors
route guards
component design
state management
Backend
FastAPI
dependency injection
REST architecture
async programming
SSE
background workers
Database
PostgreSQL
indexes
transactions
normalization
pgvector
query optimization
AI
RAG
embeddings
chunking
vector search
prompt injection
hallucinations
evaluation
DevOps
Docker
Docker Compose
CI/CD
Terraform
Nginx
Linux
deployment
Observability
Prometheus
Grafana
Loki
OpenTelemetry
Jaeger
Security
JWT
RBAC
tenant isolation
rate limiting
secure file uploads
secrets
52. Final Architecture

The complete system:

                           INTERNET
                              |
                              v
                     +----------------+
                     |     NGINX      |
                     | Reverse Proxy  |
                     +-------+--------+
                             |
              +--------------+--------------+
              |                             |
              v                             v
      +---------------+             +---------------+
       |    React      |             |    FastAPI    |
       |  TypeScript   |             |    Backend    |
      +---------------+             +-------+-------+
                                            |
              +-----------------------------+-------------------------+
              |              |              |              |           |
              v              v              v              v           v
       +-----------+   +-----------+   +-----------+   +---------+  +---------+
       |PostgreSQL |   |   Redis   |   |   MinIO   |   | Ollama  |  | Celery  |
       | + pgvector|   | Cache/Queue|  |  Storage  |   | Local AI|  | Workers |
       +-----------+   +-----------+   +-----------+   +---------+  +---------+
             |                                             |
             |                                             |
             +-------------------+-------------------------+
                                 |
                                 v
                          +-------------+
                          | RAG Engine  |
                          +-------------+
                                 |
                +----------------+----------------+
                |                |                |
                v                v                v
             Chunking       Embeddings        Retrieval
                |                |                |
                +----------------+----------------+
                                 |
                                 v
                              LLM
                                 |
                                 v
                         Answer + Sources
                                 |
                                 v
                             React


                       OBSERVABILITY LAYER

        +-------------+       +-------------+       +-------------+
        | Prometheus  |       |    Loki     |       |   Jaeger    |
        |   Metrics   |       |    Logs     |       |   Tracing   |
        +------+------+       +------+------+       +------+------+
               |                     |                     |
               +---------------------+---------------------+
                                     |
                                     v
                               +-----------+
                               |  Grafana  |
                               +-----------+


                         DEVELOPMENT / DEVOPS

     Developer
        |
        v
      Git
        |
        v
     GitHub
        |
        v
  GitHub Actions
        |
        +---- Lint
        |
        +---- Unit tests
        |
        +---- Integration tests
        |
        +---- E2E tests
        |
        +---- Security scanning
        |
        +---- RAG evaluation
        |
        +---- Docker build
        |
        v
     Deployment
        |
        v
   Linux Server
        |
        v
   Docker Compose

Project Principles

The project should follow these principles:

1. Production over demo

Do not build a simple chatbot.

Build a complete support platform.

2. Security by design

Tenant isolation and authorization belong in the backend.

3. AI is a subsystem

The application should not be tightly coupled to a single LLM.

4. Everything important is observable

Logs, metrics and traces should make failures diagnosable.

5. Everything important is tested

Especially authentication, tenant isolation, RAG retrieval and critical business logic.

6. Everything should be reproducible

A new developer should be able to run:

docker compose up


and obtain the complete development environment.

7. Prefer free and open-source infrastructure

The core application should not require:

OpenAI API
Anthropic API
Gemini API
AWS
Pinecone
paid database
paid object storage
paid monitoring


The system should be capable of running locally or on infrastructure you control.

Final Target

The finished project should feel like a small production SaaS company built by one engineer:

                    SUPPORTAI
                       |
       +---------------+---------------+
       |               |               |
    SUPPORT         KNOWLEDGE       ANALYTICS
       |               |               |
       v               v               v
    Tickets         Documents       Metrics
    Agents          RAG             Reports
    Chat            Embeddings
    AI              Vector Search
       |               |
       +-------+-------+
               |
               v
          Local LLM
               |
               v
          AI Responses
               |
               v
       Evaluation System
               |
               v
        Quality Metrics


Infrastructure:

Docker
    |
Docker Compose
    |
Nginx
    |
FastAPI
    |
PostgreSQL + pgvector
Redis + Celery
MinIO
Ollama

DevOps:

GitHub
    |
GitHub Actions
    |
Tests
    |
Security Scans
    |
Docker
    |
Deployment

Observability:

Prometheus
Grafana
Loki
OpenTelemetry
Jaeger


The end result is not merely an AI chatbot.

It is a:

Full-stack, multi-tenant, AI-powered customer-support SaaS platform with RAG, local LLM inference, asynchronous document processing, human-agent workflows, automated AI evaluation, security, observability, Docker-based infrastructure and CI/CD.

That is the level of project that can serve as a flagship portfolio project and give you substantial material to discuss in full-stack, backend, AI engineering, and DevOps interviews.


### A small but important recommendation

Don't try to implement all 52 sections simultaneously. The **roadmap inside the document is the order I'd actually follow**. Start with React → FastAPI → PostgreSQL → auth → multi-tenancy, then progressively add RAG, local LLMs, workers, evaluation, observability and DevOps.

The final project should be **deep rather than merely having a huge technology list**. A working tenant-isolated RAG pipeline with tests, monitoring, CI/CD and a polished React dashboard is far more valuable on your CV than 20 technologies that are only superficially integrated.