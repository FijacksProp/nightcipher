# Dream Journal AI — Project TODO (Django Stack)

Use this as a living checklist. Keep tasks small, mark progress, and add notes as you learn.

Legend: [ ] todo  |  [~] in progress  |  [x] done

---

## 0) Project Setup & Decisions
- [x] Project name: NightCipher
- [ ] Repo structure (monolith vs split apps)
- [ ] Define MVP scope (features list + non-goals)
- [x] Decide on UI approach: Django templates + HTMX + Tailwind
- [x] Decide on hosting: Render
- [ ] Write a short product brief (1 page)

---

## 1) Tech Stack (Best-fit for Django)
- Backend: Django + Django REST Framework
- DB: PostgreSQL
- Async: Celery + Redis (or start synchronous for MVP)
- Auth: Django auth (email+password) or magic link later
- Frontend: Django templates + HTMX + Tailwind (sleek + low JS)
- AI: LLM API (OpenAI / Anthropic / other)
- Storage: local for dev, S3-compatible for prod
- Logging/Monitoring: Sentry (optional)

---

## 2) Environment & Repo Setup
- [x] Create virtualenv + install dependencies
- [ ] Add `.env` support (python-dotenv or django-environ)
- [ ] Add `.gitignore` for Python/Django/Node
- [x] Initialize Django project + `journal` app
- [ ] Configure Postgres local DB
- [x] Configure static + media files
- [ ] Basic CI: lint + tests (GitHub Actions)

---

## 3) Data Model & Migrations
- [x] Define models:
  - UserProfile
  - DreamEntry
  - Symbol
  - Tag
  - DreamSymbol (through table)
  - Interpretation
  - ClarifyingQuestion
- [x] Add indexes for search (date, user, tags)
- [x] Create migrations
- [ ] Seed common symbols (admin command or fixture)

---

## 4) Admin + Basic UX
- [ ] Register all models in Django admin
- [ ] Add search + filters in admin
- [ ] Create minimal UI layout (header, nav, container)
- [ ] Auth pages: login, logout, register

---

## 5) Dream Entry CRUD
- [ ] Dream create form (title, narrative, date, emotions, symbols, tags)
- [ ] Dream list page (filters by date / tag / symbol)
- [ ] Dream detail page
- [ ] Dream edit + delete
- [ ] Privacy field handling

---

## 5.1) MVP Pages (NightCipher)
- [ ] Professional chatbot page (input + response, clean layout)
- [ ] Social/feedback page (simple feed + likes + comments)
- [ ] Light moderation tools (report/flag + hide)

---

## 6) Interpretation Flow (Core AI)
- [ ] Create prompt templates (psych + spiritual)
- [ ] Build interpretation service layer
- [ ] Add clarifying question step
- [ ] Store questions + answers
- [ ] Generate interpretation and save to DB
- [ ] UI to display layered interpretation
- [ ] Add disclaimers (non-clinical, suggestive only)

---

## 7) Insights & Patterns
- [ ] Calculate top symbols/emotions
- [ ] Recurring themes (simple text summary)
- [ ] Weekly/monthly summary page
- [ ] Trend charts (optional)

---

## 8) Search & Filters
- [ ] Full-text search on narrative/title
- [ ] Filter by date range, tags, symbols, emotions
- [ ] Save filter presets (optional)

---

## 9) API (DRF) — Best Practices Checklist

Core rules:
- Use DRF serializers for validation
- Avoid exposing internal model fields directly
- Use pagination for lists
- Add throttling to AI endpoints
- Use token auth or session auth (keep it simple)

Endpoints (example):
- [ ] `POST /api/dreams/` create dream
- [ ] `GET /api/dreams/` list dreams (filters)
- [ ] `GET /api/dreams/:id/` detail
- [ ] `PATCH /api/dreams/:id/` update
- [ ] `DELETE /api/dreams/:id/` delete
- [ ] `POST /api/dreams/:id/interpret/` generate interpretation
- [ ] `GET /api/symbols/` list symbols

Security:
- [ ] Only allow access to own dreams
- [ ] Validate content length to avoid prompt abuse
- [ ] Log AI requests + responses (store safely)

Documentation:
- [ ] Add schema (drf-spectacular or drf-yasg)
- [ ] Add API README with curl examples

---

## 10) Async Jobs (Optional but Recommended)
- [ ] Add Celery + Redis
- [ ] Run interpretation in background
- [ ] Add job status field to dream
- [ ] Add retry + timeout handling

---

## 11) UI/UX Polish
- [ ] Empty state for new users
- [ ] Loading states for interpretation
- [ ] Microcopy + friendly tone
- [ ] Mobile responsive layout

---

## 12) Testing
- [ ] Model tests
- [ ] API tests (dream CRUD + interpret)
- [ ] Permission tests (user isolation)
- [ ] Basic integration test for full flow

---

## 13) Deployment
- [ ] Dockerfile
- [ ] Render/Railway config
- [ ] Set env vars (DB, secret key, AI API)
- [ ] Migrate + collectstatic
- [ ] Create admin user

---

## 14) Post‑launch
- [ ] Usage analytics (simple event logging)
- [ ] Feedback form
- [ ] Bug triage checklist

---

## Notes
- Start with Django templates + HTMX for speed.
- Add DRF once the core UX is working.
- Keep AI prompts versioned for repeatability.
