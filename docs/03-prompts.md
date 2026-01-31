# Prompts Reference

## Overview

All prompts are located in the `prompts/` directory. They are used by the OpenAI nodes in the workflow to perform specific tasks.

## Prompt Files

| File | Purpose | Used In |
|------|---------|---------|
| `01_resume_parser.md` | Extract structured data from resume | Parse Resume - OpenAI |
| `02_job_analyzer.md` | Analyze job requirements | Analyze Job - OpenAI |
| `03_fit_analysis.md` | Calculate fit and identify gaps | Fit Analysis - OpenAI |
| `04_resume_enhancer.md` | Optimize resume for the job | Enhance Resume - OpenAI |
| `05_cover_letter.md` | Generate personalized cover letter | Generate All Artifacts |
| `06_interview_prep.md` | Create interview preparation guide | Generate All Artifacts |
| `07_star_stories.md` | Generate STAR-format stories | Generate All Artifacts |
| `08_gap_analysis.md` | Detailed skill gap analysis | Generate All Artifacts |
| `09_ats_keywords.md` | ATS keyword optimization | Generate All Artifacts |
| `10_30_60_90_plan.md` | 30-60-90 day onboarding plan | Generate All Artifacts |
| `11_recruiter_questions.md` | Questions to ask interviewers | Generate All Artifacts |
| `12_quality_critic.md` | Verify accuracy, flag fabrications | Quality Check - OpenAI |
| `13_resume_html.md` | Generate ATS-friendly HTML | Generate Resume HTML |

## Prompt Variables

Each prompt uses template variables that are replaced at runtime:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{resume_text}}` | Raw text extracted from PDF | "John Doe..." |
| `{{resume_json}}` | Parsed resume as JSON | `{personal:...}` |
| `{{job_description}}` | Raw job description text | "We're looking for..." |
| `{{job_json}}` | Analyzed job as JSON | `{requirements:...}` |
| `{{fit_json}}` | Fit analysis as JSON | `{fitScore:...}` |
| `{{language}}` | Output language | "en", "ru" |
| `{{tone}}` | Desired tone | "professional" |
| `{{pages}}` | Max resume pages | 1, 2 |
| `{{company}}` | Target company name | "Google" |
| `{{role}}` | Target job title | "Software Engineer" |

## Critical Rules (All Prompts)

Every prompt includes these critical rules to prevent fabrication:

```markdown
## CRITICAL RULES
1. **NEVER INVENT** achievements, metrics, or experiences
2. Only use facts from the original resume
3. Never add skills the candidate doesn't have
4. Never fabricate experience or qualifications
5. If information isn't available, don't make it up
```

## Prompt Details

### 01_resume_parser.md

**Purpose**: Convert unstructured resume text to structured JSON

**Output Schema**:
```json
{
  "personal": {
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "github": "",
    "portfolio": ""
  },
  "summary": "",
  "experience": [{
    "title": "",
    "company": "",
    "location": "",
    "startDate": "",
    "endDate": "",
    "current": false,
    "description": "",
    "achievements": []
  }],
  "education": [{
    "degree": "",
    "field": "",
    "institution": "",
    "location": "",
    "graduationDate": "",
    "gpa": "",
    "honors": []
  }],
  "skills": {
    "technical": [],
    "soft": [],
    "languages": [],
    "tools": [],
    "certifications": []
  },
  "projects": [],
  "awards": [],
  "publications": [],
  "volunteer": []
}
```

### 02_job_analyzer.md

**Purpose**: Extract requirements from job description

**Output Schema**:
```json
{
  "job": {
    "title": "",
    "company": "",
    "location": "",
    "type": "",
    "level": "",
    "salary": ""
  },
  "requirements": {
    "mustHave": [{
      "skill": "",
      "category": "technical|soft|experience|education",
      "yearsRequired": null,
      "importance": "critical"
    }],
    "niceToHave": [...]
  },
  "keywords": {
    "technical": [],
    "industry": [],
    "action_verbs": [],
    "ats_critical": []
  },
  "responsibilities": [],
  "culture": {...},
  "applicationTips": []
}
```

### 03_fit_analysis.md

**Purpose**: Analyze match between resume and job

**Output Schema**:
```json
{
  "fitScore": {
    "overall": 0-100,
    "technical": 0-100,
    "experience": 0-100,
    "education": 0-100,
    "soft_skills": 0-100
  },
  "coverage": {
    "mustHave": {
      "matched": [],
      "missing": [],
      "partial": []
    },
    "niceToHave": {...}
  },
  "keywords": {
    "present": [],
    "missing_critical": [],
    "recommended_additions": []
  },
  "gaps": [{
    "area": "",
    "severity": "critical|moderate|minor",
    "suggestion": ""
  }],
  "strengths": [...],
  "improvementPlan": {...}
}
```

### 12_quality_critic.md

**Purpose**: Verify no information was fabricated

**Output Schema**:
```json
{
  "overallStatus": "PASS|FAIL|WARNING",
  "issues": [{
    "severity": "critical|warning|info",
    "location": "",
    "issue": "",
    "original": "",
    "generated": "",
    "recommendation": ""
  }],
  "verified": {
    "personal_info": true,
    "experience": true,
    "education": true,
    "skills": true,
    "cover_letter": true,
    "interview_prep": true,
    "star_stories": true
  },
  "summary": "",
  "confidence_score": 0.0-1.0
}
```

## Customizing Prompts

To customize prompts:

1. Edit files in `prompts/` directory
2. Update the corresponding node in the workflow
3. Test with sample data

**Best Practices**:
- Keep the CRITICAL RULES section
- Maintain JSON output format requirements
- Test changes with diverse resume samples
- Monitor quality check results for issues
