# Troubleshooting Guide

## Common Issues

### LinkedIn Scraping Blocked

**Symptoms**:
- Response contains `need_jd_text: true`
- Scrape error: "Could not extract job description"

**Causes**:
- LinkedIn blocks automated requests
- Rate limiting
- CAPTCHA challenges

**Solutions**:

1. **Use the retry endpoint** with manual job description:
```bash
curl -X POST "http://localhost:5678/webhook/resume-enhancer/retry" \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "req_xxx",
    "jd_text": "Copy the job description here..."
  }'
```

2. **Configure a scraping service**:
   - Set up Browserless, ScrapingBee, or similar
   - Update `SCRAPE_PROVIDER` and `SCRAPE_API_KEY` in `.env`

3. **Use a proxy**:
   - Configure `BROWSERLESS_URL` with proxy settings

---

### Windows Path Issues

**Symptoms**:
- Files not saved to OUTPUT_DIR
- Permission denied errors
- Path not found

**Solutions**:

1. **Use forward slashes** in paths:
```env
# Correct
OUTPUT_DIR=C:/Users/Name/JobApplications

# Incorrect
OUTPUT_DIR=C:\Users\Name\JobApplications
```

2. **Ensure Docker volume mount** if n8n runs in Docker:
```yaml
volumes:
  - C:/Users/Name/JobApplications:/data/output
```

3. **Check permissions**:
```bash
# Windows PowerShell
icacls "C:\Users\Name\JobApplications"
```

---

### Gotenberg Connection Failed

**Symptoms**:
- "Connection refused" to Gotenberg URL
- PDF not generated
- Timeout errors

**Solutions**:

1. **Verify Gotenberg is running**:
```bash
docker ps | grep gotenberg
curl http://localhost:3000/health
```

2. **Start Gotenberg if not running**:
```bash
docker run -d -p 3000:3000 gotenberg/gotenberg:8
```

3. **Check network** (if n8n and Gotenberg are in different Docker networks):
```bash
# Create shared network
docker network create shared
docker network connect shared n8n
docker network connect shared gotenberg
```

4. **Update URL** if using Docker:
```env
# If both in same Docker network
GOTENBERG_URL=http://gotenberg:3000

# If Gotenberg on host
GOTENBERG_URL=http://host.docker.internal:3000
```

---

### OpenAI API Errors

**Symptoms**:
- 401 Unauthorized
- 429 Rate limit exceeded
- 500 Internal server error

**Solutions**:

1. **Verify API key**:
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

2. **Check rate limits**:
   - Reduce concurrent requests
   - Add delays between calls
   - Upgrade OpenAI plan

3. **Verify model availability**:
```env
# Use a supported model
OPENAI_MODEL=gpt-4o
# or
OPENAI_MODEL=gpt-4-turbo
# or
OPENAI_MODEL=gpt-3.5-turbo
```

4. **Update credentials in n8n**:
   - Go to Credentials
   - Edit "OpenAI API" credential
   - Verify Authorization header format: `Bearer sk-xxx`

---

### PDF Extraction Failed

**Symptoms**:
- Empty resume text
- `needs_vision_fallback: true`
- Garbled text output

**Solutions**:

1. **Check PDF format**:
   - Ensure PDF is text-based, not scanned image
   - Try re-saving PDF from original source

2. **For image-based PDFs**:
   - Use OpenAI Vision for OCR
   - Convert to text-based PDF first

3. **Test extraction manually**:
```bash
# Using pdftotext
pdftotext resume.pdf -

# Using Python
pip install PyPDF2
python -c "import PyPDF2; print(PyPDF2.PdfReader('resume.pdf').pages[0].extract_text())"
```

---

### Workflow Not Found

**Symptoms**:
- 404 when calling webhook
- "Workflow not active" error

**Solutions**:

1. **Verify workflow is imported**:
```bash
curl "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: your_key"
```

2. **Activate the workflow**:
   - Open n8n UI
   - Find "Resume Enhancer from LinkedIn Job URL"
   - Toggle to Active

3. **Check webhook path**:
   - Should be `/webhook/resume-enhancer`
   - Verify in workflow settings

---

### Files Not Created

**Symptoms**:
- Success response but no files
- Empty output directory

**Solutions**:

1. **Check OUTPUT_DIR exists**:
```bash
ls -la $OUTPUT_DIR
# or on Windows
dir %OUTPUT_DIR%
```

2. **Verify permissions**:
```bash
# n8n must have write access
chmod 755 /data/output
```

3. **Check Docker volume mount**:
```bash
docker inspect n8n | grep Mounts -A 20
```

4. **Look in n8n execution logs**:
   - Open n8n UI
   - Go to Executions
   - Check "Write Files to Disk" node output

---

### Quality Check Failures

**Symptoms**:
- `quality_status: "FAIL"`
- Many issues in warnings.md

**Solutions**:

1. **Review warnings.md** for specific issues

2. **Common issues**:
   - Skills added that aren't in original resume
   - Metrics invented
   - Experience exaggerated

3. **If false positives**:
   - Verify original resume contains the flagged content
   - Adjust quality check prompt sensitivity

---

## Debug Mode

Enable detailed logging:

1. **n8n environment variables**:
```env
N8N_LOG_LEVEL=debug
N8N_LOG_OUTPUT=console,file
```

2. **Check execution history**:
   - n8n UI → Executions
   - Click on failed execution
   - Inspect each node's input/output

3. **Test individual nodes**:
   - Pin test data to nodes
   - Execute workflow manually
   - Check node by node

---

## Getting Help

1. **Check n8n logs**:
```bash
docker logs n8n --tail 100
```

2. **Review this documentation**:
   - [Overview](00-overview.md)
   - [Quick Start](01-quickstart.md)
   - [Workflow Details](02-workflow.md)

3. **Common log patterns**:
```
# Connection issues
ECONNREFUSED - Service not running or wrong URL
ETIMEDOUT - Network issue or firewall

# Authentication issues
401 - Invalid API key
403 - Access denied

# Resource issues
429 - Rate limited
500 - Server error
```
