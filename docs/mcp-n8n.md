# MCP n8n Server Integration

## Overview

The MCP (Model Context Protocol) n8n server allows Claude Code to directly manage n8n workflows, executions, and more. This document explains how to use MCP with this project.

## Required Environment Variables

For MCP to connect to your n8n instance:

```env
# n8n API URL (without /api/v1 suffix)
N8N_API_URL=http://localhost:5678/api/v1

# n8n API Key (get from n8n Settings > API)
N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiN2ZiNDUwMC1jMTA3LTRkYWMtODM3NS1mZmFlZDc3MmQxNTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5MTQ3NjEwLCJleHAiOjE3NzE3MDc2MDB9.LZ4C4Nvs5zZJulJiF242eVTBX9IYBqc2GkX7tNvU2No
```

## Getting the n8n API Key

1. Open your n8n instance: `http://localhost:5678`
2. Go to **Settings** (gear icon)
3. Click **API**
4. Click **Create API Key**
5. Copy the generated key
6. Add to your environment or Claude Desktop config

## MCP Configuration

### For Claude Desktop

Add to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["-y", "n8n-mcp"],
      "env": {
        "N8N_API_URL": "http://localhost:5678/api/v1",
        "N8N_API_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiN2ZiNDUwMC1jMTA3LTRkYWMtODM3NS1mZmFlZDc3MmQxNTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5MTQ3NjEwLCJleHAiOjE3NzE3MDc2MDB9.LZ4C4Nvs5zZJulJiF242eVTBX9IYBqc2GkX7tNvU2No"
      }
    }
  }
}
```

### For Claude Code

MCP servers are automatically available if configured in Claude Desktop or via environment variables.

## Common MCP Operations

### 1. Import Workflow

To import the workflow from this project:

```
# Using Claude Code with MCP
Read the workflow file at workflow/workflow.json and create it in n8n
```

**MCP Tools Used**:
- `n8n_create_workflow` - Creates new workflow

**Example**:
```javascript
// MCP will call:
n8n_create_workflow({
  name: "Resume Enhancer from LinkedIn Job URL",
  nodes: [...],
  connections: {...}
})
```

### 2. Update Workflow

To update an existing workflow:

```
# Using Claude Code with MCP
Update workflow ID "xxx" with the changes from workflow/workflow.json
```

**MCP Tools Used**:
- `n8n_get_workflow` - Get current workflow
- `n8n_update_full_workflow` - Full update
- `n8n_update_partial_workflow` - Partial update (add/remove nodes)

**Example for Partial Update**:
```javascript
// Add a new node
n8n_update_partial_workflow({
  id: "workflow_id",
  operations: [
    {
      type: "addNode",
      node: {
        id: "new-node",
        name: "New Node",
        type: "n8n-nodes-base.code",
        // ...
      }
    }
  ]
})
```

### 3. Run Execution

To trigger the workflow:

```
# Using Claude Code with MCP
Test the resume enhancer workflow with webhook trigger
```

**MCP Tools Used**:
- `n8n_test_workflow` - Trigger webhook execution

**Example**:
```javascript
n8n_test_workflow({
  workflowId: "xxx",
  triggerType: "webhook",
  data: {
    job_url: "https://linkedin.com/jobs/view/123",
    // Note: Binary files need special handling
  }
})
```

### 4. View Execution Logs

To check execution results:

```
# Using Claude Code with MCP
Show me the last execution of the resume enhancer workflow
```

**MCP Tools Used**:
- `n8n_executions` with `action: "list"` - List executions
- `n8n_executions` with `action: "get"` - Get execution details

**Example**:
```javascript
// List recent executions
n8n_executions({
  action: "list",
  workflowId: "xxx",
  limit: 10
})

// Get specific execution details
n8n_executions({
  action: "get",
  id: "execution_id",
  mode: "full"
})

// Get error details
n8n_executions({
  action: "get",
  id: "execution_id",
  mode: "error"
})
```

## Complete Workflow Management Example

### Import and Activate Workflow

```
1. Check n8n connection:
   n8n_health_check({ mode: "diagnostic" })

2. Import workflow:
   n8n_create_workflow({
     name: "Resume Enhancer from LinkedIn Job URL",
     nodes: <from workflow.json>,
     connections: <from workflow.json>
   })

3. Validate workflow:
   n8n_validate_workflow({ id: "new_workflow_id" })

4. Auto-fix issues:
   n8n_autofix_workflow({
     id: "new_workflow_id",
     applyFixes: true
   })

5. Activate workflow:
   n8n_update_partial_workflow({
     id: "new_workflow_id",
     operations: [{ type: "activateWorkflow" }]
   })
```

### Test Workflow

```
1. Trigger with test data:
   n8n_test_workflow({
     workflowId: "xxx",
     triggerType: "webhook",
     webhookPath: "resume-enhancer",
     data: { ... }
   })

2. Check execution:
   n8n_executions({
     action: "get",
     id: "execution_id",
     mode: "summary"
   })
```

### Debug Failed Execution

```
1. List recent failed executions:
   n8n_executions({
     action: "list",
     workflowId: "xxx",
     status: "error"
   })

2. Get error details:
   n8n_executions({
     action: "get",
     id: "failed_execution_id",
     mode: "error",
     includeStackTrace: true
   })
```

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `n8n_health_check` | Check n8n connection and status |
| `n8n_list_workflows` | List all workflows |
| `n8n_get_workflow` | Get workflow details |
| `n8n_create_workflow` | Create new workflow |
| `n8n_update_full_workflow` | Full workflow update |
| `n8n_update_partial_workflow` | Incremental updates |
| `n8n_delete_workflow` | Delete workflow |
| `n8n_validate_workflow` | Validate workflow |
| `n8n_autofix_workflow` | Auto-fix common issues |
| `n8n_test_workflow` | Trigger execution |
| `n8n_executions` | Manage executions |
| `n8n_workflow_versions` | Version history |

## Troubleshooting MCP Connection

### Connection Failed

```
Error: ECONNREFUSED
```

**Solution**:
1. Verify n8n is running: `curl http://localhost:5678/healthz`
2. Check N8N_API_URL in config
3. Ensure no firewall blocking

### Authentication Failed

```
Error: 401 Unauthorized
```

**Solution**:
1. Verify API key is correct
2. Check API key hasn't expired
3. Regenerate API key in n8n Settings

### Workflow Not Found

```
Error: Workflow with ID xxx not found
```

**Solution**:
1. List workflows: `n8n_list_workflows()`
2. Use correct workflow ID
3. Verify workflow wasn't deleted

## Best Practices

1. **Always validate** before activating:
   ```
   n8n_validate_workflow → n8n_autofix_workflow → activate
   ```

2. **Use partial updates** for small changes:
   ```
   n8n_update_partial_workflow for adding/removing nodes
   ```

3. **Check execution logs** after testing:
   ```
   n8n_executions with mode="error" for failures
   ```

4. **Keep workflow versions**:
   ```
   n8n_workflow_versions to track changes
   ```
