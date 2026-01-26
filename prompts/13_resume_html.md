# Resume HTML Generator Prompt

You are an expert resume designer. Generate ATS-friendly HTML for the enhanced resume.

## Input
- Enhanced resume (JSON): {{resume_json}}
- Language: {{language}}
- Pages: {{pages}}

## Task
Generate clean, ATS-compatible HTML that will convert well to PDF.

## HTML Requirements

### Structure
- Use semantic HTML5 elements
- Single column layout (ATS-friendly)
- No tables for layout
- No images or graphics
- Standard fonts (Arial, Calibri, Times New Roman)

### Styling
- Inline CSS only (for PDF conversion)
- Clear hierarchy with proper headings
- Consistent spacing
- Professional color scheme (minimal color)
- Print-optimized margins

## Output Template

```html
<!DOCTYPE html>
<html lang="{{language}}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{name}} - Resume</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: 'Calibri', 'Arial', sans-serif;
      font-size: 11pt;
      line-height: 1.4;
      color: #333;
      max-width: 8.5in;
      margin: 0 auto;
      padding: 0.5in 0.75in;
    }
    h1 {
      font-size: 18pt;
      color: #1a1a1a;
      margin-bottom: 4pt;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    h2 {
      font-size: 12pt;
      color: #2c5282;
      border-bottom: 1px solid #2c5282;
      padding-bottom: 2pt;
      margin: 12pt 0 6pt 0;
      text-transform: uppercase;
    }
    h3 {
      font-size: 11pt;
      font-weight: bold;
      margin-bottom: 2pt;
    }
    .contact {
      text-align: center;
      font-size: 10pt;
      color: #555;
      margin-bottom: 8pt;
    }
    .contact a {
      color: #2c5282;
      text-decoration: none;
    }
    .summary {
      margin-bottom: 8pt;
    }
    .job, .education-item, .project {
      margin-bottom: 8pt;
    }
    .job-header, .edu-header {
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
    }
    .job-title {
      font-weight: bold;
    }
    .company {
      font-style: italic;
    }
    .date {
      color: #666;
      font-size: 10pt;
    }
    ul {
      margin-left: 16pt;
      margin-top: 4pt;
    }
    li {
      margin-bottom: 2pt;
    }
    .skills {
      margin-top: 4pt;
    }
    .skill-category {
      margin-bottom: 4pt;
    }
    .skill-label {
      font-weight: bold;
    }
    @media print {
      body {
        padding: 0;
      }
    }
  </style>
</head>
<body>
  <header>
    <h1>{{name}}</h1>
    <div class="contact">
      {{email}} | {{phone}} | {{location}}
      {{#if linkedin}}<br><a href="{{linkedin}}">LinkedIn</a>{{/if}}
      {{#if github}} | <a href="{{github}}">GitHub</a>{{/if}}
      {{#if portfolio}} | <a href="{{portfolio}}">Portfolio</a>{{/if}}
    </div>
  </header>

  {{#if summary}}
  <section>
    <h2>Professional Summary</h2>
    <p class="summary">{{summary}}</p>
  </section>
  {{/if}}

  <section>
    <h2>Experience</h2>
    {{#each experience}}
    <div class="job">
      <div class="job-header">
        <span class="job-title">{{title}}</span>
        <span class="date">{{startDate}} - {{endDate}}</span>
      </div>
      <div class="company">{{company}}{{#if location}}, {{location}}{{/if}}</div>
      <ul>
        {{#each achievements}}
        <li>{{this}}</li>
        {{/each}}
      </ul>
    </div>
    {{/each}}
  </section>

  <section>
    <h2>Education</h2>
    {{#each education}}
    <div class="education-item">
      <div class="edu-header">
        <span><strong>{{degree}}</strong> in {{field}}</span>
        <span class="date">{{graduationDate}}</span>
      </div>
      <div class="company">{{institution}}</div>
    </div>
    {{/each}}
  </section>

  <section>
    <h2>Skills</h2>
    <div class="skills">
      {{#if skills.technical}}
      <div class="skill-category">
        <span class="skill-label">Technical:</span> {{join skills.technical ", "}}
      </div>
      {{/if}}
      {{#if skills.tools}}
      <div class="skill-category">
        <span class="skill-label">Tools:</span> {{join skills.tools ", "}}
      </div>
      {{/if}}
    </div>
  </section>
</body>
</html>
```

## CRITICAL RULES
1. Only include information from the enhanced resume JSON
2. Keep formatting simple and ATS-compatible
3. Ensure all text is selectable (for ATS parsing)
4. Test that HTML renders correctly before PDF conversion
