# Tests

## Overview

This directory contains tests for the Resume Enhancer n8n workflow. Tests are designed to work **without** depending on LinkedIn scraping.

## Test Files

| File | Description |
|------|-------------|
| `test_runner.py` | Main test runner for workflow functionality |
| `test_mcp_integration.py` | Tests MCP n8n server integration |
| `fixtures/sample_resume.txt` | Sample resume for testing |
| `fixtures/sample_job_description.txt` | Sample job description for testing |

## Running Tests

### Prerequisites

1. n8n running and accessible
2. N8N_API_KEY set
3. Python 3.8+
4. `requests` library installed

### Install Dependencies

```bash
pip install requests
```

### Run Main Tests

```bash
# Using environment variables
export N8N_HOST=http://localhost:5678
export N8N_API_KEY=your_api_key
export OUTPUT_DIR=/data/output

python test_runner.py
```

Or with command line arguments:

```bash
python test_runner.py \
  --n8n-url http://localhost:5678 \
  --api-key your_api_key \
  --output-dir /data/output
```

### Run MCP Integration Tests

```bash
python test_mcp_integration.py
```

## Test Cases

### test_runner.py

1. **Load fixtures** - Verifies sample files exist
2. **Check n8n connection** - Tests API connectivity
3. **Find/Import workflow** - Locates or imports the workflow
4. **Trigger workflow** - Calls /retry endpoint with test data
5. **Check output files** - Verifies generated files
6. **Check execution logs** - Reviews n8n execution history

### test_mcp_integration.py

1. **Health check** - n8n_health_check simulation
2. **List workflows** - n8n_list_workflows simulation
3. **Find/Import workflow** - n8n_create_workflow simulation
4. **Get workflow details** - n8n_get_workflow simulation
5. **Validate workflow** - n8n_validate_workflow simulation
6. **List executions** - n8n_executions simulation

## Fixtures

### sample_resume.txt

A sample resume with:
- Contact information
- Professional summary
- 3 work experiences
- Education
- Technical and soft skills
- Certifications

### sample_job_description.txt

A sample Senior Software Engineer job posting with:
- Role description
- Responsibilities
- Must-have requirements
- Nice-to-have requirements
- Benefits and salary range

## Test Output

### Successful Run

```
[PASS] Loaded fixtures
[PASS] n8n is accessible
[PASS] Found workflow: abc123
[PASS] Workflow executed successfully
[PASS] Found 11 files
====================================
Test Results Summary
====================================
Total:    6
Passed:   6
Failed:   0
Warnings: 0
====================================
```

### Failed Run

```
[PASS] Loaded fixtures
[FAIL] Cannot connect to n8n

Cannot continue without n8n connection. Exiting.
====================================
Test Results Summary
====================================
Total:    2
Passed:   1
Failed:   1
Warnings: 0
====================================
```

## Customizing Tests

### Adding New Fixtures

1. Add files to `fixtures/` directory
2. Update `load_fixtures()` in test_runner.py

### Testing Different Scenarios

Modify fixtures to test:
- Different resume formats
- Various job types
- Different languages
- Edge cases

## Troubleshooting

### Connection Refused

```
[FAIL] n8n health check failed: Connection refused
```

**Solution**: Ensure n8n is running at the specified URL

### API Key Invalid

```
[FAIL] n8n health check failed: 401 Unauthorized
```

**Solution**: Verify N8N_API_KEY is correct

### Timeout

```
[FAIL] Request timed out
```

**Solution**:
- Increase timeout in test
- Check n8n and OpenAI API status
- Verify network connectivity
