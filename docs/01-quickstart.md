# Quick Start Guide

## Prerequisites

1. **n8n** running locally (Docker or standalone)
2. **OpenAI API key** configured in n8n credentials
3. **Resume PDF** file accessible to n8n (e.g., `/data/input/resume.pdf`)
4. **Gotenberg** (optional) for PDF generation

## Setup Steps

### 1. Configure OpenAI Credentials in n8n

1. Open n8n UI: http://localhost:5678
2. Go to **Settings** → **Credentials** → **Add Credential**
3. Select **HTTP Header Auth**
4. Configure:
   - **Name**: `OpenAI API`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer sk-your-openai-api-key`
5. Save

### 2. Link Credentials to Workflow

1. Open the workflow "Resume Enhancer from LinkedIn Job URL"
2. For each OpenAI node (6 nodes), click on it and select the `OpenAI API` credential
3. Save the workflow

### 3. Place Your Resume

Copy your resume PDF to a location accessible by n8n:
- If using Docker: `/data/input/resume.pdf` (mount this volume)
- If local: Use full path like `C:/Users/YourName/Documents/resume.pdf`

## Usage

### Basic Usage (Recommended)

1. Open the workflow in n8n
2. Click on the **"User Input"** node (the ONLY node you need to edit)
3. Edit the JSON fields:

```json
{
  "job_url": "",
  "jd_text": "Paste the full job description here...",
  "resume_path": "/data/input/resume.pdf",
  "language": "en",
  "tone": "professional",
  "pages": 1,
  "scrape_enabled": false,
  "company_override": "",
  "role_override": ""
}
```

4. Click **Execute Workflow**
5. Check the **Summary** node output for results

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `job_url` | If no jd_text | LinkedIn job URL (e.g., `https://www.linkedin.com/jobs/view/123456789`) |
| `jd_text` | If no job_url | Paste the job description text directly (min 50 chars) |
| `resume_path` | Yes | Path to your resume PDF file |
| `language` | No | Output language: `en`, `ru`, `de`, `fr`, `es`, `pt`, `it`, `zh`, `ja`, `ko` (default: `en`) |
| `tone` | No | Writing style: `professional`, `casual`, `creative`, `technical`, `executive` (default: `professional`) |
| `pages` | No | Target resume length: `1`, `2`, or `3` pages (default: `1`) |
| `scrape_enabled` | No | Set to `true` to scrape job_url (requires browserless) |
| `company_override` | No | Override company name for output folder |
| `role_override` | No | Override role name for output folder |

### Two Ways to Provide Job Description

**Option A: Paste JD Text (Recommended)**
```json
{
  "job_url": "",
  "jd_text": "We are looking for a Senior Software Engineer...",
  ...
}
```

**Option B: Use LinkedIn URL with Scraping**
```json
{
  "job_url": "https://www.linkedin.com/jobs/view/123456789",
  "jd_text": "",
  "scrape_enabled": true,
  ...
}
```

## Output

After successful execution, files are saved to:
```
/data/output/JobApplications/{Company}/{Role}-{Date}/{request_id}/
```

Generated files:
- `improved_resume.pdf` - ATS-optimized resume
- `resume.html` - HTML version
- `cover_letter.md` - Personalized cover letter
- `interview_prep.md` - Interview questions & answers
- `ats_keywords.md` - Keyword optimization guide
- `gap_analysis.md` - Skills gap analysis
- `stories_STAR.md` - STAR format stories
- `questions_to_recruiter.md` - Questions to ask
- `30-60-90.md` - 90-day plan
- `data.json` - Full analysis data
- `changes_changelog.md` - What was changed
- `warnings.md` - Quality issues (if any)

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
  "output_path": "/data/output/JobApplications/Google/Senior_Software_Engineer-2025-01-22/req_1234567890_abc123",
  "files": ["cover_letter.md", "interview_prep.md", "improved_resume.pdf", ...]
}
```

## Troubleshooting

### "job_url is required when jd_text is not provided"
Either provide a valid LinkedIn job URL or paste the job description into `jd_text`.

### "Resume text too short"
The PDF extraction failed. Try a different PDF or use a text-based resume.

### "need_jd_text: true"
Scraping failed. Paste the job description manually into `jd_text`.

### OpenAI errors
Check that:
1. OpenAI credential is configured correctly
2. API key is valid and has credits
3. Credential is linked to all 6 OpenAI nodes

## Next Steps

- [Workflow Details](02-workflow.md) - Understand how it works
- [Troubleshooting](04-troubleshooting.md) - If something goes wrong
- [MCP Integration](mcp-n8n.md) - Manage via MCP
