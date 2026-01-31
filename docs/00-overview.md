# Resume Enhancer - Overview

## What is Resume Enhancer?

Resume Enhancer is an n8n workflow that takes a LinkedIn job URL and your resume PDF, then generates a complete job application package tailored to that specific position.

## Key Features

- **ATS Optimization**: Enhances your resume with keywords and formatting that pass Applicant Tracking Systems
- **Quality Assurance**: AI critic checks all output for fabricated information
- **Comprehensive Package**: Generates multiple supporting documents for your application
- **Retry Mechanism**: If LinkedIn scraping fails, provides a manual JD input option

## Generated Files

The workflow creates the following files in `OUTPUT_DIR/JobApplications/{company}/{role}-{date}/{request_id}/`:

| File | Description |
|------|-------------|
| `improved_resume.pdf` | ATS-optimized resume tailored to the job |
| `resume.html` | HTML source of the enhanced resume |
| `cover_letter.md` | Personalized cover letter |
| `interview_prep.md` | Interview questions with suggested answers |
| `ats_keywords.md` | Keyword analysis and optimization guide |
| `gap_analysis.md` | Skills gaps and how to address them |
| `stories_STAR.md` | STAR-format stories for behavioral interviews |
| `questions_to_recruiter.md` | Smart questions to ask interviewers |
| `30-60-90.md` | 30-60-90 day onboarding plan |
| `changes_changelog.md` | All modifications made to the resume |
| `data.json` | Complete structured data (JSON) |
| `warnings.md` | Quality check warnings (if any) |

## Workflow Principles

### No Fabrication
The system is designed to **never invent** information:
- Only uses facts from your actual resume
- Never adds skills you don't have
- Never creates fake metrics or achievements
- Quality check flags any potential fabrications

### Transparency
- All changes are logged in `changes_changelog.md`
- Quality warnings are documented in `warnings.md`
- Original data preserved in `data.json`

## System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Your Resume   │     │ LinkedIn Job URL │     │    n8n Server   │
│     (PDF)       │────▶│                 │────▶│                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                        ┌────────────────────────────────┼────────────────────────────────┐
                        │                                ▼                                │
                        │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
                        │  │ Parse Resume │───▶│ Analyze Job  │───▶│  Fit Analysis│      │
                        │  └──────────────┘    └──────────────┘    └──────────────┘      │
                        │                                                  │              │
                        │                                                  ▼              │
                        │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
                        │  │Quality Check │◀───│Generate Docs │◀───│Enhance Resume│      │
                        │  └──────────────┘    └──────────────┘    └──────────────┘      │
                        │         │                                                       │
                        │         ▼                                                       │
                        │  ┌──────────────┐    ┌──────────────┐                          │
                        │  │  HTML→PDF    │───▶│  Save Files  │                          │
                        │  │ (Gotenberg)  │    │              │                          │
                        │  └──────────────┘    └──────────────┘                          │
                        │                                                                 │
                        └─────────────────────────────────────────────────────────────────┘
                                                         │
                                                         ▼
                                              ┌─────────────────┐
                                              │ Output Directory│
                                              │ /JobApplications│
                                              └─────────────────┘
```

## Requirements

- **n8n** (self-hosted, already running)
- **OpenAI API** access
- **Gotenberg** for HTML to PDF conversion
- **Scraping service** (optional, for LinkedIn)

## Next Steps

1. [Quick Start Guide](01-quickstart.md) - Get up and running
2. [Workflow Details](02-workflow.md) - Understand the workflow
3. [Prompts Reference](03-prompts.md) - All AI prompts used
4. [Troubleshooting](04-troubleshooting.md) - Common issues
5. [MCP Integration](mcp-n8n.md) - Managing via MCP
