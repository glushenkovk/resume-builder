# Workflow Architecture

## Workflow Diagram

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                        Resume Enhancer Workflow (v2)                               │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                          │
│  │   Manual    │────▶│ User Input  │────▶│  Validate   │                          │
│  │   Trigger   │     │  (EDIT ME)  │     │   Input     │                          │
│  └─────────────┘     └─────────────┘     └──────┬──────┘                          │
│                                                 │                                  │
│                                            ┌────┴────┐                             │
│                                            ▼         ▼                             │
│                                         [Pass]    [Fail]                           │
│                                            │         │                             │
│                                            │    ┌────┴────┐                        │
│                                            │    │ Summary │                        │
│                                            │    │  Error  │                        │
│                                            │    └─────────┘                        │
│                                            ▼                                       │
│                                     ┌─────────────┐                                │
│                                     │ Read Resume │                                │
│                                     │    File     │                                │
│                                     └──────┬──────┘                                │
│                                            │                                       │
│                                            ▼                                       │
│                                     ┌─────────────┐                                │
│                                     │  Extract    │                                │
│                                     │  PDF Text   │                                │
│                                     └──────┬──────┘                                │
│                                            │                                       │
│                                       ┌────┴────┐                                  │
│                                       ▼         ▼                                  │
│                                    [Valid]   [Invalid]                             │
│                                       │         │                                  │
│                                       │    ┌────┴────┐                             │
│                                       │    │ Summary │                             │
│                                       │    │  Error  │                             │
│                                       │    └─────────┘                             │
│                                       ▼                                            │
│                                ┌─────────────┐                                     │
│                                │ Check JD    │                                     │
│                                │   Source    │                                     │
│                                └──────┬──────┘                                     │
│                                       │                                            │
│                           ┌───────────┼───────────┐                                │
│                           ▼           │           ▼                                │
│                    ┌──────────┐       │    ┌──────────┐                            │
│                    │  Manual  │       │    │  Scrape  │                            │
│                    │   JD     │       │    │ Enabled? │                            │
│                    └────┬─────┘       │    └────┬─────┘                            │
│                         │             │         │                                  │
│                         │             │    ┌────┴────┐                             │
│                         │             │    ▼         ▼                             │
│                         │             │ [Yes]     [No]                             │
│                         │             │    │         │                             │
│                         │             │    ▼    ┌────┴────┐                        │
│                         │             │ Scrape  │ Summary │                        │
│                         │             │   JD    │ Need JD │                        │
│                         │             │    │    └─────────┘                        │
│                         │             │    │                                       │
│                         └──────┬──────┴────┘                                       │
│                                │                                                   │
│                                ▼                                                   │
│                         ┌─────────────┐                                            │
│                         │   Merge     │                                            │
│                         │  JD Paths   │                                            │
│                         └──────┬──────┘                                            │
│                                │                                                   │
│  ┌─────────────────────────────┼─────────────────────────┐                         │
│  │       OPENAI ANALYSIS PIPELINE                        │                         │
│  │                             │                         │                         │
│  │                             ▼                         │                         │
│  │                      ┌─────────────┐                  │                         │
│  │                      │Parse Resume │                  │                         │
│  │                      │  (OpenAI)   │                  │                         │
│  │                      └──────┬──────┘                  │                         │
│  │                             │                         │                         │
│  │                             ▼                         │                         │
│  │                      ┌─────────────┐                  │                         │
│  │                      │Analyze Job  │                  │                         │
│  │                      │  (OpenAI)   │                  │                         │
│  │                      └──────┬──────┘                  │                         │
│  │                             │                         │                         │
│  │                             ▼                         │                         │
│  │                      ┌─────────────┐                  │                         │
│  │                      │Fit Analysis │                  │                         │
│  │                      │  (OpenAI)   │                  │                         │
│  │                      └──────┬──────┘                  │                         │
│  │                             │                         │                         │
│  │                             ▼                         │                         │
│  │                      ┌─────────────┐                  │                         │
│  │                      │  Enhance    │                  │                         │
│  │                      │   Resume    │                  │                         │
│  │                      └──────┬──────┘                  │                         │
│  │                             │                         │                         │
│  │                             ▼                         │                         │
│  │                      ┌─────────────┐                  │                         │
│  │                      │  Generate   │                  │                         │
│  │                      │  Artifacts  │                  │                         │
│  │                      └──────┬──────┘                  │                         │
│  │                             │                         │                         │
│  │                             ▼                         │                         │
│  │                      ┌─────────────┐                  │                         │
│  │                      │  Quality    │                  │                         │
│  │                      │   Check     │                  │                         │
│  │                      └─────────────┘                  │                         │
│  │                                                       │                         │
│  └───────────────────────────────────────────────────────┘                         │
│                                │                                                   │
│                                ▼                                                   │
│                         ┌─────────────┐                                            │
│                         │  Generate   │                                            │
│                         │    HTML     │                                            │
│                         └──────┬──────┘                                            │
│                                │                                                   │
│                                ▼                                                   │
│                         ┌─────────────┐                                            │
│                         │  HTML→PDF   │                                            │
│                         │ (Gotenberg) │                                            │
│                         └──────┬──────┘                                            │
│                                │                                                   │
│                                ▼                                                   │
│                         ┌─────────────┐                                            │
│                         │Write Files  │                                            │
│                         └──────┬──────┘                                            │
│                                │                                                   │
│                                ▼                                                   │
│                         ┌─────────────┐                                            │
│                         │  Summary    │  ◀── Final output for user                 │
│                         └─────────────┘                                            │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

## Key Design Principle

**Single "User Input" Node** - The workflow is designed so users only need to edit ONE node:
- Click on "User Input" node
- Edit the JSON parameters
- Click Execute

No other nodes require manual editing.

## Node Descriptions

### Entry Point

| Node | Type | Purpose |
|------|------|---------|
| Manual Trigger | Manual Trigger | Starts workflow when user clicks Execute |
| User Input | Set | **THE ONLY NODE TO EDIT** - contains all user parameters |

### Validation Layer

| Node | Type | Purpose |
|------|------|---------|
| Validate Manual Input | Code | Validates all user inputs |
| Check Validation | IF | Routes valid/invalid inputs |
| Summary - Validation Error | Code | Returns error summary |

### Resume Processing

| Node | Type | Purpose |
|------|------|---------|
| Read Resume File | Read Binary Files | Reads resume from disk |
| Extract Resume Text | Extract from File | Extracts text from PDF |
| Check Resume Extracted | Code | Validates extraction success |
| Check Resume Valid | IF | Routes based on extraction result |
| Summary - Resume Error | Code | Returns extraction error |

### Job Description Handling

| Node | Type | Purpose |
|------|------|---------|
| Check JD Source | IF | Checks if manual JD provided |
| Use Manual JD | Code | Uses provided jd_text |
| Check Scrape Enabled | IF | Checks if scraping is enabled |
| Scrape Job Description | HTTP Request | Scrapes LinkedIn (optional) |
| Check Scrape Result | Code | Validates scrape success |
| Summary - Need JD | Code | Returns "need jd_text" message |
| Summary - Scrape Failed | Code | Returns scrape failure message |
| Merge JD Paths | Merge | Combines both JD sources |

### AI Analysis Pipeline (6 OpenAI Calls)

| Node | Type | Purpose |
|------|------|---------|
| Parse Resume - OpenAI | HTTP Request | Parses resume to structured JSON |
| Analyze Job - OpenAI | HTTP Request | Analyzes job requirements |
| Combine Analysis Data | Code | Merges resume + job data |
| Fit Analysis - OpenAI | HTTP Request | Calculates fit score and gaps |
| Enhance Resume - OpenAI | HTTP Request | Optimizes resume for job |
| Generate All Artifacts | HTTP Request | Creates all supporting docs |
| Quality Check - OpenAI | HTTP Request | Verifies no fabrications |

### Output Generation

| Node | Type | Purpose |
|------|------|---------|
| Prepare All Files | Code | Prepares all file contents |
| Generate Resume HTML | Code | Creates ATS-friendly HTML |
| Convert HTML to PDF | HTTP Request | Gotenberg HTML→PDF |
| Write Files to Disk | Code | Writes to OUTPUT_DIR |
| Summary | Code | **Final output for user** |

## User Input Fields

```json
{
  "job_url": "https://www.linkedin.com/jobs/view/123456789",
  "jd_text": "",
  "resume_path": "/data/input/resume.pdf",
  "language": "en",
  "tone": "professional",
  "pages": 1,
  "scrape_enabled": false,
  "company_override": "",
  "role_override": ""
}
```

| Field | Required | Description |
|-------|----------|-------------|
| job_url | If no jd_text | LinkedIn job URL |
| jd_text | If no job_url | Paste job description directly (min 50 chars) |
| resume_path | Yes | Path to resume PDF |
| language | No | en/ru/de/fr/es/pt/it/zh/ja/ko |
| tone | No | professional/casual/creative/technical/executive |
| pages | No | 1, 2, or 3 |
| scrape_enabled | No | true to scrape LinkedIn URL |
| company_override | No | Override detected company name |
| role_override | No | Override detected role name |

## Summary Output Structure

```json
{
  "success": true,
  "request_id": "req_1234567890_abc123",
  "company": "Google",
  "role": "Senior_Software_Engineer",
  "fit_score": 78,
  "quality_status": "PASS",
  "need_jd_text": false,
  "output_path": "/data/output/JobApplications/Google/Senior_Software_Engineer-2025-01-22/req_xxx",
  "files": ["improved_resume.pdf", "cover_letter.md", "interview_prep.md", ...],
  "errors": []
}
```

## Error States

| Summary Field | Meaning | Action |
|---------------|---------|--------|
| `success: false, errors: [...]` | Validation failed | Fix User Input and re-run |
| `need_jd_text: true` | JD not available | Paste JD into jd_text |
| `quality_status: "WARNING"` | Quality issues found | Check warnings.md |
| `quality_status: "FAIL"` | Major quality issues | Review generated content carefully |

## Performance

- **Total OpenAI calls**: 6
- **Estimated tokens**: ~10-20k per run
- **Timeouts**: 60-180s per OpenAI call
- **Output files**: ~12-13 files per run
