# Agentic AI Tender

A starter multi-service tender intelligence platform built from the provided architecture diagram.

## Key components
- `frontend/next-app`: Next.js 14 App Router dashboard
- `backend/fastapi_gateway`: API gateway with JWT validation, request logging, and service routing
- `backend/services/*`: Modular FastAPI microservices for auth, tender CRUD, analysis, and notifications
- `agents`: Multi-agent orchestration templates for discovery, PDF processing, eligibility, risk, matching, and recommendation
- `jobs`: Celery background job and task definitions
- `scrapers`: Web scraper scaffolding using Playwright and BeautifulSoup
- `docker-compose.yml`: Local development stack with PostgreSQL, Redis, MinIO, and service containers

## Getting started

1. Copy environment template:

```bash
cp .env.example .env
```

2. Start local services with Docker:

```bash
docker-compose up --build
```

3. Install frontend dependencies and run Next.js:

```bash
cd frontend/next-app
npm install
npm run dev
```

4. Visit the dashboard at `http://localhost:3000` and the API gateway at `http://localhost:8000/docs`.

## Development commands

- `docker-compose up --build` - start service stack
- `docker-compose down` - stop and remove containers
- `cd frontend/next-app && npm run dev` - run frontend locally
- `cd backend && uvicorn fastapi_gateway.main:app --reload --host 0.0.0.0 --port 8000` - run gateway locally
- `cd backend && celery -A jobs.celery_app worker --loglevel=info` - run worker locally

## Architecture

The gateway routes requests to microservices and performs centralized JWT validation.
The multi-agent layer coordinates discovery, PDF processing, analysis, eligibility, risk scoring, and recommendation.
Background jobs handle scraping, PDF ingestion, and AI pipelines.
Search and embeddings are prepared for future Elastic/pgvector integration.
