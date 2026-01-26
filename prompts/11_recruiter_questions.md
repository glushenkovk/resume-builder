# Questions for Recruiter Prompt

You are an expert career advisor. Generate thoughtful questions for the candidate to ask recruiters and interviewers.

## Input
- Job requirements (JSON): {{job_json}}
- Fit analysis (JSON): {{fit_json}}
- Company: {{company}}
- Role: {{role}}
- Language: {{language}}

## Task
Create a curated list of insightful questions that demonstrate genuine interest and strategic thinking.

## Output Structure

```markdown
# Questions to Ask the Recruiter/Interviewer
## {{role}} at {{company}}

### About the Role

#### Understanding the Position
1. **What does a typical day/week look like in this role?**
   - *Why ask:* Shows you want to understand daily realities
   - *Listen for:* Work variety, meeting load, independent vs collaborative work

2. **What are the most important projects or initiatives this person will work on in the first 6 months?**
   - *Why ask:* Shows forward-thinking and eagerness to contribute
   - *Listen for:* Priorities, current challenges, team needs

3. **How is success measured in this role?**
   - *Why ask:* Shows results-orientation
   - *Listen for:* KPIs, review process, growth opportunities

### About the Team

4. **Can you tell me about the team I'd be working with?**
   - *Why ask:* Understanding team dynamics
   - *Listen for:* Team size, experience levels, collaboration style

5. **What's the team's biggest challenge right now?**
   - *Why ask:* Shows problem-solving mindset
   - *Listen for:* Pain points you might help solve

### About Growth & Development

6. **What opportunities for professional development does the company offer?**
   - *Why ask:* Shows long-term interest
   - *Listen for:* Training, conferences, learning budget

7. **What does the career path look like for someone in this role?**
   - *Why ask:* Shows ambition and retention mindset
   - *Listen for:* Promotion timeline, lateral moves, growth stories

### About Company Culture

8. **How would you describe the company culture?**
   - *Why ask:* Cultural fit assessment
   - *Listen for:* Values in action, not just stated values

9. **What do you enjoy most about working here?**
   - *Why ask:* Personal perspective, builds rapport
   - *Listen for:* Genuine enthusiasm (or lack thereof)

### Strategic Questions (Advanced)

10. **Where do you see this department/team in 2-3 years?**
    - *Why ask:* Shows strategic thinking
    - *Listen for:* Vision, growth plans, stability

### Questions About Process

11. **What are the next steps in the interview process?**
    - *Why ask:* Shows organization and interest
    - *Listen for:* Timeline, additional interviews

12. **Is there anything about my background that gives you pause?**
    - *Why ask:* Address concerns directly
    - *Listen for:* Honest feedback to address

---

### Questions NOT to Ask
- Salary/benefits (save for offer stage)
- Vacation time (too early)
- "What does your company do?" (shows no research)
- Negative questions about past employees
```

## CRITICAL RULES
1. Questions should be specific to the role and company
2. Avoid questions easily answered by job posting or website
3. Include follow-up prompts for deeper conversation
4. Mix tactical and strategic questions
