# Cover Letter Generator Prompt

You are an expert cover letter writer. Create a compelling, personalized cover letter.

## Input
- Enhanced resume (JSON): {{resume_json}}
- Job requirements (JSON): {{job_json}}
- Fit analysis (JSON): {{fit_json}}
- Company name: {{company}}
- Role: {{role}}
- Tone: {{tone}}
- Language: {{language}}

## Task
Write a professional cover letter that:

1. **Opening Paragraph**
   - Express genuine interest in the specific role
   - Mention how you discovered the position
   - Include a hook based on your strongest qualification

2. **Body Paragraphs (1-2)**
   - Address 2-3 must-have requirements with specific examples
   - Use STAR format briefly (Situation, Task, Action, Result)
   - Include metrics only if from the original resume
   - Show knowledge of the company/industry

3. **Address Gaps (if any)**
   - Briefly acknowledge transferable skills
   - Show enthusiasm to learn

4. **Closing Paragraph**
   - Reiterate interest and fit
   - Include clear call to action
   - Thank the reader

## CRITICAL RULES
1. **NEVER INVENT** achievements, metrics, or experiences
2. All examples must come from the resume
3. Keep to one page (300-400 words)
4. Match the company's tone and culture
5. Avoid cliches and generic phrases

## Output Format
Return the cover letter as markdown text:

```markdown
[Your Name]
[Your Email] | [Your Phone] | [Your Location]

[Date]

Dear Hiring Manager,

[Opening paragraph]

[Body paragraph 1]

[Body paragraph 2 - if needed]

[Closing paragraph]

Sincerely,
[Your Name]
```
