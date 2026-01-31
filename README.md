# Resume Enhancer n8n

An n8n workflow that transforms your resume and LinkedIn job URL into a complete, ATS-optimized job application package.

## Features

- **Resume Parsing**: Extracts structured data from PDF resumes
- **Job Analysis**: Analyzes requirements from LinkedIn job postings
- **Fit Scoring**: Calculates match percentage and identifies gaps
- **ATS Optimization**: Enhances resume with relevant keywords
- **Complete Package**: Generates cover letter, interview prep, and more
- **Quality Assurance**: AI critic ensures no fabricated information

## Generated Files

| File | Description |
|------|-------------|
| `improved_resume.pdf` | ATS-optimized resume |
| `cover_letter.md` | Personalized cover letter |
| `interview_prep.md` | Interview questions & answers |
| `ats_keywords.md` | Keyword optimization guide |
| `gap_analysis.md` | Skills gap analysis |
| `stories_STAR.md` | STAR-format interview stories |
| `questions_to_recruiter.md` | Questions to ask |
| `30-60-90.md` | Onboarding plan |

## Quick Start

### 1. Prerequisites

- **n8n** running (self-hosted, Docker)
- **OpenAI API** key
- **Gotenberg** for PDF generation (optional)

### 2. Import Workflow

**Option A: Via n8n UI**
1. Open n8n → Add Workflow → Import from File
2. Select `workflow/workflow.json`

**Option B: Via API**
```bash
curl -X POST "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d @workflow/workflow_import.json
```

### 3. Configure OpenAI Credentials

In n8n UI:
1. Go to **Credentials**
2. Add **HTTP Header Auth** credential:
   - Name: `OpenAI API`
   - Header: `Authorization`
   - Value: `Bearer YOUR_OPENAI_API_KEY`
3. Link credential to all 6 OpenAI nodes in the workflow

### 4. Use the Workflow

**Just 3 steps:**

1. Open the workflow in n8n
2. Click on the **"User Input"** node and edit the JSON:

```json
{
  "job_url": "",
  "jd_text": "Paste the job description here...",
  "resume_path": "/data/input/resume.pdf",
  "language": "en",
  "tone": "professional",
  "pages": 1,
  "scrape_enabled": false,
  "company_override": "",
  "role_override": ""
}
```

3. Click **Execute Workflow**

That's it! Check the **Summary** node for results.

## User Input Fields

| Field | Required | Description |
|-------|----------|-------------|
| `job_url` | If no jd_text | LinkedIn job URL |
| `jd_text` | If no job_url | Paste job description directly (min 50 chars) |
| `resume_path` | Yes | Path to resume PDF file |
| `language` | No | `en`, `ru`, `de`, `fr`, `es`, etc. (default: `en`) |
| `tone` | No | `professional`, `casual`, `creative`, `technical`, `executive` |
| `pages` | No | `1`, `2`, or `3` (default: `1`) |
| `scrape_enabled` | No | `true` to scrape LinkedIn URL (requires browserless) |
| `company_override` | No | Override company name for output folder |
| `role_override` | No | Override role name for output folder |

## Two Ways to Provide Job Description

**Option A: Paste JD Text (Recommended)**
```json
{
  "job_url": "",
  "jd_text": "We are looking for a Senior Software Engineer..."
}
```

**Option B: LinkedIn URL with Scraping**
```json
{
  "job_url": "https://www.linkedin.com/jobs/view/123456789",
  "jd_text": "",
  "scrape_enabled": true
}
```

## Summary Output

The final **Summary** node shows:

```json
{
  "success": true,
  "request_id": "req_1234567890_abc123",
  "company": "Google",
  "role": "Senior_Software_Engineer",
  "fit_score": 78,
  "quality_status": "PASS",
  "need_jd_text": false,
  "output_path": "/data/output/JobApplications/Google/...",
  "files": ["improved_resume.pdf", "cover_letter.md", ...]
}
```

## Project Structure

```
resume-enhancer-n8n/
├── workflow/
│   ├── workflow.json         # Main n8n workflow
│   └── workflow_import.json  # Clean version for import
├── prompts/                  # AI prompt templates (13 files)
├── docs/
│   ├── 00-overview.md
│   ├── 01-quickstart.md
│   ├── 02-workflow.md
│   ├── 03-prompts.md
│   ├── 04-troubleshooting.md
│   └── mcp-n8n.md
├── tests/
│   ├── test_runner.py
│   ├── test_mcp_integration.py
│   └── fixtures/
├── .env.example
└── README.md
```

## Documentation

- [Quick Start](docs/01-quickstart.md) - Getting started guide
- [Workflow](docs/02-workflow.md) - Workflow architecture
- [Prompts](docs/03-prompts.md) - AI prompts reference
- [Troubleshooting](docs/04-troubleshooting.md) - Common issues
- [MCP Integration](docs/mcp-n8n.md) - MCP n8n server usage

## Important Notes

### No Fabrication Policy

This system is designed to **never invent information**:
- Only uses facts from your actual resume
- Never adds skills you don't have
- Never creates fake achievements or metrics
- Quality check flags any potential fabrications

### Single User Input Node

The workflow is designed for simplicity:
- **Only edit the "User Input" node**
- No other nodes require manual editing
- All parameters in one place

### Windows Path Notes

If running on Windows with Docker:
- Use forward slashes in paths: `C:/Users/Name/...`
- Ensure proper volume mounts for OUTPUT_DIR

## License

MIT License
