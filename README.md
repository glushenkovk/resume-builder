# AI-Powered Resume Builder

An n8n workflow system that uses AI to analyze, enhance, and optimize resumes for specific job applications.

## Features

- **Resume Parsing** - Extracts structured data from PDF resumes
- **Job Analysis** - Analyzes job descriptions to identify requirements
- **Fit Analysis** - Scores resume match against job requirements
- **Resume Enhancement** - Optimizes resume content for ATS systems
- **Cover Letter Generation** - Creates tailored cover letters
- **Interview Prep** - Generates interview questions and STAR stories
- **PDF Generation** - Outputs professional PDF resumes via Gotenberg

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Resume PDF │────▶│  Parse &    │────▶│  Enhance &  │
│  + Job Desc │     │  Analyze    │     │  Optimize   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                   │
                           ▼                   ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  Fit Score  │     │  PDF Output │
                    │  & Gaps     │     │  (Gotenberg)│
                    └─────────────┘     └─────────────┘
```

## Workflow Components

| Workflow | Description |
|----------|-------------|
| `minimal_workflow.json` | Core resume enhancement pipeline |
| `job_ingest_linkedin.json` | LinkedIn job ingestion |
| `minimal_workflow_webhook.json` | Webhook-triggered version |

## Prompts Library

The `/prompts` folder contains 13 specialized AI prompts:

| # | Prompt | Purpose |
|---|--------|---------|
| 01 | Resume Parser | Extract structured data from resume |
| 02 | Job Analyzer | Parse job description requirements |
| 03 | Fit Analysis | Score resume against job match |
| 04 | Resume Enhancer | Optimize resume for specific role |
| 05 | Cover Letter | Generate tailored cover letter |
| 06 | Interview Prep | Create interview preparation guide |
| 07 | STAR Stories | Generate behavioral interview answers |
| 08 | Gap Analysis | Identify skill gaps and solutions |
| 09 | ATS Keywords | Optimize for applicant tracking systems |
| 10 | 30-60-90 Plan | Create onboarding plan |
| 11 | Recruiter Questions | Questions to ask recruiters |
| 12 | Quality Critic | Review and critique resume |
| 13 | Resume HTML | Generate HTML resume template |

## Tech Stack

- **n8n** - Workflow automation
- **OpenAI GPT-4** - AI text processing
- **Gotenberg** - PDF generation
- **Docker** - Container orchestration

## Setup

### Prerequisites
- n8n instance (self-hosted or cloud)
- OpenAI API key
- Gotenberg service (optional, for PDF output)

### Installation

1. Import workflows into n8n:
   - Go to n8n > Workflows > Import
   - Select workflow JSON files

2. Configure credentials:
   - Add OpenAI API credentials in n8n
   - Update credential references in workflows

3. (Optional) Start Gotenberg:
   ```bash
   docker run -d -p 3000:3000 gotenberg/gotenberg:8
   ```

## Usage

1. Place your resume PDF in the input folder
2. Paste the job description in the workflow
3. Run the workflow
4. Get your optimized resume as PDF

## Example Output

The workflow produces:
- Enhanced resume tailored to the job
- Fit score with gap analysis
- ATS-optimized keywords
- Cover letter (optional)

## Built With

This project was built using AI-assisted development (Claude, GPT-4) demonstrating modern "vibe coding" workflows where AI accelerates development while humans provide direction and architecture decisions.

## License

MIT

## Author

Konstantin Glushenkov - [GitHub](https://github.com/glushenkovk)
