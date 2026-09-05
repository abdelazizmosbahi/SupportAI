# Developer Rules — SupportAI

These rules are mandatory. Read before every task.

---

## Rule 1 — One task at a time

Work on only ONE task at a time. The current task must always be identified in `PROJECT_PROGRESS.md`.

## Rule 2 — Read progress before coding

Before beginning a task:
- Read `PROJECT_PROGRESS.md`
- Read the current task file
- Read the previous task's completion report (if exists)
- Inspect only relevant source files

## Rule 3 — Do NOT repeatedly reread the entire specification

After initial analysis, use `PROJECT_PROGRESS.md` and task files as primary context. Only return to `roadmap.md` when:
- A requirement is unclear
- An architectural decision needs verification
- A requirement appears contradictory

## Rule 4 — Focused repository navigation

Do NOT repeatedly scan the entire repository. For each task, identify the relevant module, inspect specific files, modify only what is necessary, run tests, update progress, commit.

## Rule 5 — No endless recapitulation

Do NOT spend time repeatedly explaining what the project is, the entire architecture, everything already implemented, every previous task, or the entire technology stack. Use the Markdown progress system.

## Rule 6 — Task lifecycle

Every task follows: `TODO` → `IN PROGRESS` → `IMPLEMENTATION` → `TESTING` → `VERIFICATION` → `DONE` → `COMMIT`

If something prevents completion: `IN PROGRESS` → `BLOCKED`. Document the blocker.

## Rule 7 — Before starting a task

Update `PROJECT_PROGRESS.md` with current task info. Update the task file status to `IN PROGRESS`.

## Rule 8 — During implementation

Keep changes focused on the current task. Do not implement future tasks. If a required task is discovered, document it and add to TODO.

## Rule 9 — Installing dependencies

Install necessary dependencies using the appropriate package manager. Do not ask the user to manually install something when you can safely install/configure it yourself.

## Rule 10 — Prefer free/open-source technologies

The project must remain free to develop and run. Do NOT introduce paid infrastructure or proprietary services. Prefer: PostgreSQL, pgvector, Redis, Celery, MinIO, Ollama, Docker, Docker Compose, Prometheus, Grafana, Loki, Jaeger, OpenTelemetry, Nginx, GitHub Actions, Terraform.

## Rule 11 — Do not add technologies just for the CV

Every technology must have a legitimate architectural purpose. Prefer simple, maintainable, testable, documented, production-oriented over unnecessary complexity.

## Rule 12 — Code quality

Write production-quality code. Follow: clear naming, separation of concerns, SOLID principles, type safety, dependency injection, reusable services, small functions, meaningful error handling, consistent formatting. Avoid: duplicated code, giant functions, hard-coded configuration, magic numbers, unnecessary abstractions.

## Rule 13 — Security

Security is mandatory at every layer. Always consider: authentication, authorization, tenant isolation, input validation, file validation, SQL injection, XSS, CSRF, CORS, rate limiting, secrets, secure headers, password hashing, token handling. Never commit secrets. Never expose secrets in frontend code. Never put passwords or tokens in logs.

## Rule 14 — Multi-tenant security

Every tenant-owned resource must be protected. Always verify: `current_user`, `organization_id`, resource ownership, permissions. Do not trust `organization_id` provided directly by the client without server-side verification. Tenant isolation must be tested.

## Rule 15 — Testing is part of implementation

A task is NOT complete simply because the code works manually. Add appropriate tests depending on the task. Critical business logic must have automated tests.

## Rule 16 — Run tests before completion

Before marking a task DONE: run relevant tests, run linting, run type checking where applicable, verify the application starts, verify the feature manually if appropriate. Do not mark a task complete based solely on "the code looks correct."

## Rule 17 — Database changes

Any database schema change must use migrations (Alembic). Do NOT manually modify the database schema without a migration. Workflow: SQLAlchemy model → Alembic migration → Migration test → Application test.

## Rule 18 — API changes

When adding/changing APIs: update Pydantic schemas, update routes, update validation, add tests, update API documentation if necessary, consider backward compatibility. FastAPI OpenAPI documentation should remain accurate.

## Rule 19 — Frontend changes

When modifying React: maintain feature-based structure, keep components small and focused, use Tailwind + MUI for styling, use TanStack Query for server state, keep auth state in React Context, use axios for API calls, use React Router protected routes, handle loading/error/empty states, maintain responsive behavior.

## Rule 20 — AI/RAG changes

When modifying the AI system, always consider: retrieval quality, hallucination, prompt injection, citation correctness, latency, failure handling, evaluation. RAG changes should be evaluated where appropriate. Do not assume an AI response is correct simply because the model generated it.

## Rule 21 — LLM provider abstraction

Do not couple application business logic directly to a specific LLM implementation. Keep LLM functionality behind an abstraction/provider layer. The application should be able to use local models without changing business logic.

## Rule 22 — Observability

Important backend operations should be observable. Where appropriate add: structured logs, metrics, traces, request IDs, latency measurements, error information. Do not add excessive logging. Never log secrets or sensitive customer content unnecessarily.

## Rule 23 — Configuration

Configuration belongs in environment variables or configuration files. Never hard-code passwords, tokens, secrets, or database credentials. Provide `.env.example` when environment variables are introduced.

## Rule 24 — Docker

The application must remain reproducible. Whenever a dependency/service is introduced: update Docker configuration, update Docker Compose, update environment variables, verify startup, update documentation if necessary.

## Rule 25 — CI/CD

CI must eventually validate: lint, type checking, unit tests, integration tests, E2E tests, security scanning, Docker builds. Do not bypass CI failures just to mark a task complete.

## Rule 26 — Git rules

Git must be initialized during project setup. Every meaningful completed task must have its own commit. Do not accumulate dozens of unrelated tasks into one commit. Commit only after: implementation, testing, verification, progress documentation.

## Rule 27 — Commit message format

Every task completion commit must contain: task ID, meaningful title, date, time.
Format: `TASK-XXX: <meaningful description> — YYYY-MM-DD HH:MM`

## Rule 28 — Git commit workflow

After completing a task:
1. Run tests
2. Inspect `git diff`
3. Inspect `git status`
4. Update task Markdown
5. Update `PROJECT_PROGRESS.md`
6. Create completion report
7. Commit changes
8. Verify commit
9. Update `PROJECT_PROGRESS.md` with commit hash

## Rule 29 — Completion reports

When a task is completed, create a Markdown file in `project progress md/completed/`. Must contain: status, completed at, summary, implementation details, files changed, dependencies added, database changes, configuration changes, tests added, verification results, important decisions, known limitations, follow-up work, git commit info, notes for next task.

## Rule 30 — Progress file must be updated immediately

After every task, update `PROJECT_PROGRESS.md`. Move the task from IN PROGRESS to DONE. Update: Last Completed Task, Last Commit, Next Task, Current Phase.

## Rule 31 — Keep progress files concise

The progress system exists to reduce context consumption. Do NOT turn `PROJECT_PROGRESS.md` into another copy of the project specification. It should contain only current state and important decisions.

## Rule 32 — Completion reports must also be concise

Focus on: what changed, where it changed, why it changed, how it was tested, what the next task needs to know. Do NOT include entire source files or huge code blocks.

## Rule 33 — Before starting the next task

Read `PROJECT_PROGRESS.md`, identify the next task, read ONLY the previous task's completion report, read the next task's task file, inspect only relevant source files, start implementation. Do NOT reread all previous completion reports or the entire repository.

## Rule 34 — If you discover missing requirements

Do not silently invent major architecture. Determine the smallest reasonable solution. Document the decision. For major architectural changes, update `PROJECT_PROGRESS.md` and create an ADR.

## Rule 35 — If requirements conflict

Stop the affected task. Identify the conflict. Document it. Do not randomly choose an architecture. Resolve the conflict using the most coherent interpretation possible. Document the final decision.

## Rule 36 — Do not hide failures

If something fails, document: what failed, why it failed, what was attempted, current state, next action. Never mark a task DONE when acceptance criteria are not actually satisfied.

## Rule 37 — Do not fake tests

Never report PASS unless the test was actually executed. Never claim deployed/working/verified/secure without evidence.

## Rule 38 — Do not fake git commits

Never report a commit unless the commit actually exists. After committing, `git status` and `git log -1` must be used to verify the commit.

## Rule 39 — Keep the working tree clean

At the end of a completed task, `git status` should show no unintended changes. Generated files, temporary files, logs, caches, local databases, secrets, and IDE files must be appropriately ignored.

## Rule 40 — Documentation is part of the project

When behavior changes significantly, update documentation. Documentation should eventually cover: architecture, installation, local development, API, database, RAG, LLM, security, testing, Docker, deployment, CI/CD, monitoring, backup/recovery.

## Rule 41 — Do not overengineer early

Implement the simplest architecture that satisfies the specification. Do not build microservices, Kubernetes, complex event buses, or multiple databases unless the requirements justify them. The initial architecture should remain coherent and manageable.

## Rule 42 — Preserve architectural consistency

Before introducing a new technology, ask: Does this solve a real problem? Does the existing stack already solve it? Does it introduce unnecessary complexity? Does it violate the free/open-source requirement? Does it make the project harder to maintain? If yes, do not introduce it.

## Rule 43 — Current task must always be recoverable

At any moment, another developer should be able to open `PROJECT_PROGRESS.md` and understand: what has been completed, what is currently being worked on, what remains, what should happen next. This is a hard requirement.

## Rule 44 — Final rule

The Markdown progress system is your persistent project memory. Use it to avoid re-reading everything, re-explaining everything, re-scanning everything, repeating previous work, and losing track of the current task. Always remain focused on the current task.
