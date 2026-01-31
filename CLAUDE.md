# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered resume optimization system that transforms a resume PDF + job description into a complete job application package (optimized resume, cover letter, interview prep, etc.). Uses n8n for workflow orchestration, Gotenberg for PDF generation, and a custom Playwright-based LinkedIn scraper.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    n8n Workflow (Port 5678)             │
│  27 nodes: validation → resume parsing → job analysis  │
│            → fit scoring → artifact generation         │
│            → quality check → PDF output                │
└────────────────┬──────────────────┬────────────────────┘
                 │                  │
        ┌────────▼────────┐  ┌──────▼──────┐
        │   job-fetcher   │  │  Gotenberg  │
        │  (Port 3001)    │  │ (Port 3000) │
        │ LinkedIn scraper│  │  HTML→PDF   │
        └─────────────────┘  └─────────────┘
```

**Data Flow:**
1. Resume PDF read from `/data/input/`
2. Job description: manual text OR scraped from LinkedIn via job-fetcher
3. 6 OpenAI API calls using prompts from `/prompts/`
4. HTML→PDF via Gotenberg
5. Output written to `/data/output/JobApplications/{Company}/{Role}-{Date}/{request_id}/`

## Build and Run Commands

```bash
# Start all services (n8n, gotenberg, job-fetcher)
cd "c:/Users/Kons/resume builder"
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f n8n
docker-compose logs -f job-fetcher

# Rebuild job-fetcher after code changes
docker-compose up -d --build job-fetcher
```

### Job-Fetcher Development

```bash
cd job-fetcher
npm install        # Install dependencies (generates package-lock.json)
npm run build      # Compile TypeScript → dist/
npm run dev        # Watch mode with nodemon
npm start          # Production mode
```

### Tests

```bash
python tests/test_runner.py           # Main test suite
python tests/test_mcp_integration.py  # MCP integration tests
```

## Key Configuration Files

| File | Purpose |
|------|---------|
| `.env` | API keys (OpenAI, n8n), service URLs, defaults |
| `.mcp.json` | n8n-mcp server config for Claude integration |
| `docker-compose.yml` | Full stack: n8n + gotenberg + job-fetcher |
| `job-fetcher/tsconfig.json` | TypeScript config (requires `"dom"` in lib for Playwright) |

## n8n Workflow Structure

**Main workflow:** `workflow/workflow.json` (27 nodes, 6 OpenAI calls)

The workflow has a single **User Input** node that accepts JSON:
```json
{
  "job_url": "https://www.linkedin.com/jobs/view/123456789",
  "jd_text": "",
  "resume_path": "/data/input/master_resume.pdf",
  "language": "en",
  "tone": "professional",
  "pages": 1,
  "scrape_enabled": false
}
```

**Node Pipeline:**
1. Input validation
2. Resume PDF extraction
3. Job description (manual or scraped)
4. OpenAI: Parse Resume → Analyze Job → Fit Analysis → Enhance Resume → Generate Artifacts → Quality Check
5. HTML generation → Gotenberg PDF → Write files

## Important Directories

| Directory | Purpose |
|-----------|---------|
| `prompts/` | 13 AI prompt templates (01-13) with CRITICAL RULES preventing fabrication |
| `workflow/` | n8n workflow JSON variants |
| `job-fetcher/src/` | LinkedIn scraper (Express + Playwright) |
| `data/input/` | Input resume PDFs (mounted read-only in container) |
| `data/output/` | Generated application packages |
| `docs/` | Architecture docs, quickstart, troubleshooting |

## Job-Fetcher Service

Express server with Playwright browser automation for LinkedIn scraping.

**Endpoints:**
- `GET /health` - Health check with concurrency stats
- `POST /fetch` - Scrape LinkedIn job: `{ url: "..." }` → `{ title, company, descriptionText, ... }`

**Key constraints:**
- Max 2 concurrent browser instances (`MAX_CONCURRENCY=2`)
- Rate limit: 30 requests per 10 minutes per IP
- 45-second navigation timeout
- Detects login walls, CAPTCHAs, rate limits

## Docker Volume Mounts

```yaml
volumes:
  - n8n_data:/home/node/.n8n           # n8n persistent data
  - ./data/input:/data/input:ro        # Resume PDFs (read-only)
  - ./data/output:/data/output         # Generated files
```

**File access restriction:** n8n only allows reading from paths in `N8N_RESTRICT_FILE_ACCESS_TO=/data/input,/data/output`

## MCP Integration

The `.mcp.json` configures n8n-mcp for Claude to interact with n8n workflows:
- List/create/update/delete workflows
- Validate workflow configurations
- Test workflow execution

Requires `N8N_API_KEY` from n8n Settings → API.

## Troubleshooting

**"Access to file is not allowed"**: The `N8N_RESTRICT_FILE_ACCESS_TO` environment variable requires **semicolon-separated paths** (not commas). Example:
```yaml
- N8N_RESTRICT_FILE_ACCESS_TO=/data/input;/data/output;/home/node/.n8n
```
After changing, you must **recreate** the container (not just restart):
```bash
docker-compose up -d --force-recreate n8n
```

**Job-fetcher build fails**: Ensure `package-lock.json` exists (`npm install`) and `tsconfig.json` has `"dom"` in lib array.

**MCP authentication fails**: Generate new API key in n8n, update both `.env` and `.mcp.json`, restart VS Code.

**Wrong docker-compose running**: Check container names with `docker ps`. Use `docker-compose down` in correct directory before `docker-compose up -d`.
