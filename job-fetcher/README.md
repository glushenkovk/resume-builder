# Job Fetcher - LinkedIn Job Description Extractor

A Dockerized Node.js microservice using Playwright to extract job descriptions from LinkedIn URLs.

## Features

- Extracts job title, company, location, and full description text
- Handles LinkedIn blocking gracefully (login walls, CAPTCHAs, rate limits)
- In-memory rate limiting per IP
- Concurrency control for browser instances
- Resource-efficient (blocks images/fonts/media)
- Health check endpoint

## Quick Start

### Standalone (for testing)

```bash
cd job-fetcher
docker compose up -d
```

Service will be available at `http://localhost:3001`

### With n8n (full stack)

From the project root:

```bash
docker compose up -d
```

This starts:
- n8n on `http://localhost:5678`
- Gotenberg on `http://localhost:3000`
- job-fetcher on `http://localhost:3001`

Inside the Docker network, n8n can reach job-fetcher at `http://job-fetcher:3000`

## API Endpoints

### GET /health

Health check endpoint.

**Response:**
```json
{
  "ok": true,
  "concurrency": {
    "current": 0,
    "max": 2,
    "queued": 0
  }
}
```

### POST /fetch

Fetch job description from LinkedIn URL.

**Request:**
```json
{
  "url": "https://www.linkedin.com/jobs/view/1234567890/",
  "options": {
    "timeoutMs": 45000,
    "headless": true
  }
}
```

**Success Response:**
```json
{
  "ok": true,
  "blocked": false,
  "jobId": "1234567890",
  "canonicalUrl": "https://www.linkedin.com/jobs/view/1234567890/",
  "title": "Software Engineer",
  "company": "Acme Corp",
  "location": "San Francisco, CA",
  "descriptionText": "We are looking for...",
  "applyUrl": "https://example.com/apply",
  "debug": {
    "finalUrl": "https://www.linkedin.com/jobs/view/1234567890/",
    "httpStatus": 200,
    "timingsMs": {
      "launch": 500,
      "goto": 2000,
      "extract": 1500
    }
  }
}
```

**Blocked Response:**
```json
{
  "ok": false,
  "blocked": true,
  "reason": "LOGIN_REQUIRED",
  "jobId": "1234567890",
  "canonicalUrl": "https://www.linkedin.com/jobs/view/1234567890/",
  "applyUrl": "https://example.com/apply",
  "debug": {
    "finalUrl": "https://www.linkedin.com/login",
    "httpStatus": null
  }
}
```

**Block Reasons:**
- `LOGIN_REQUIRED` - Redirected to login page
- `CAPTCHA` - CAPTCHA challenge detected
- `RATE_LIMIT` - LinkedIn rate limiting
- `SELECTOR_TIMEOUT` - Job content not found
- `UNKNOWN` - Unknown block type

## curl Examples

### Health check
```bash
curl http://localhost:3001/health
```

### Fetch a job
```bash
curl -X POST http://localhost:3001/fetch \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.linkedin.com/jobs/view/1234567890/"}'
```

### With custom timeout
```bash
curl -X POST http://localhost:3001/fetch \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.linkedin.com/jobs/view/1234567890/", "options": {"timeoutMs": 60000}}'
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `3000` | Server port |
| `HEADLESS` | `true` | Run Chromium in headless mode |
| `DEFAULT_TIMEOUT_MS` | `45000` | Default page load timeout |
| `MAX_CONCURRENCY` | `2` | Max concurrent browser instances |
| `RATE_LIMIT_MAX` | `30` | Max requests per window per IP |
| `RATE_LIMIT_WINDOW_MS` | `600000` | Rate limit window (10 minutes) |
| `REQUEST_TIMEOUT_MS` | `120000` | Global request timeout |

## Integration with n8n

In your n8n workflow, call the job-fetcher service:

**HTTP Request Node:**
- Method: `POST`
- URL: `http://job-fetcher:3000/fetch`
- Body (JSON):
```json
{
  "url": "={{$json.jobUrl}}",
  "options": { "timeoutMs": 45000 }
}
```

## Fallback Strategy

When LinkedIn blocks the request:

1. The service returns `blocked: true` with a reason
2. If available, `applyUrl` is still extracted (even if description blocked)
3. n8n workflow can detect this and prompt user for manual input

## Development

### Local development (without Docker)

```bash
cd job-fetcher
npm install
npx playwright install chromium
npm run dev
```

### Build TypeScript
```bash
npm run build
```

### Run production
```bash
npm start
```

## Troubleshooting

### Service not starting
- Check if port 3001 is available
- Ensure Docker has enough memory (2GB recommended)

### All requests blocked
- LinkedIn may be detecting automated traffic
- Try reducing concurrency to 1
- Wait and retry (rate limits typically clear in 10-30 minutes)

### Memory issues
- Reduce `MAX_CONCURRENCY` to 1
- Increase Docker memory limit

## License

MIT
