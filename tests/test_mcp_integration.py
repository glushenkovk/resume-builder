#!/usr/bin/env python3
"""
MCP Integration Test Script

Tests MCP n8n server integration for the Resume Enhancer workflow.
This script simulates the MCP commands that Claude Code would use.

Usage:
    python test_mcp_integration.py [--n8n-url URL] [--api-key KEY]
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime


class MCPSimulator:
    """Simulates MCP n8n server commands via direct API calls"""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api/v1"
        self.headers = {
            "X-N8N-API-KEY": api_key,
            "Content-Type": "application/json"
        }

    def health_check(self) -> dict:
        """Simulate n8n_health_check MCP command"""
        print("\n[MCP] n8n_health_check(mode='diagnostic')")

        try:
            # Check API connectivity
            response = requests.get(
                f"{self.api_url}/workflows",
                headers=self.headers,
                timeout=10
            )

            return {
                "success": response.status_code == 200,
                "connected": True,
                "api_url": self.api_url,
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "success": False,
                "connected": False,
                "error": str(e)
            }

    def list_workflows(self, limit: int = 100) -> dict:
        """Simulate n8n_list_workflows MCP command"""
        print(f"\n[MCP] n8n_list_workflows(limit={limit})")

        try:
            response = requests.get(
                f"{self.api_url}/workflows",
                headers=self.headers,
                params={"limit": limit},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                workflows = data.get("data", [])
                return {
                    "success": True,
                    "count": len(workflows),
                    "workflows": [
                        {"id": w["id"], "name": w["name"], "active": w.get("active", False)}
                        for w in workflows
                    ]
                }
            return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_workflow(self, workflow_id: str, mode: str = "full") -> dict:
        """Simulate n8n_get_workflow MCP command"""
        print(f"\n[MCP] n8n_get_workflow(id='{workflow_id}', mode='{mode}')")

        try:
            response = requests.get(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                workflow = response.json()
                return {
                    "success": True,
                    "id": workflow.get("id"),
                    "name": workflow.get("name"),
                    "active": workflow.get("active", False),
                    "nodes_count": len(workflow.get("nodes", [])),
                    "connections_count": len(workflow.get("connections", {}))
                }
            return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_workflow(self, workflow_data: dict) -> dict:
        """Simulate n8n_create_workflow MCP command"""
        print(f"\n[MCP] n8n_create_workflow(name='{workflow_data.get('name')}')")

        try:
            response = requests.post(
                f"{self.api_url}/workflows",
                headers=self.headers,
                json=workflow_data,
                timeout=30
            )

            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    "success": True,
                    "id": result.get("id"),
                    "name": result.get("name")
                }
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_partial_workflow(self, workflow_id: str, operations: list) -> dict:
        """Simulate n8n_update_partial_workflow MCP command"""
        print(f"\n[MCP] n8n_update_partial_workflow(id='{workflow_id}', operations={len(operations)})")

        # For activation, we use the PATCH endpoint
        for op in operations:
            if op.get("type") == "activateWorkflow":
                try:
                    response = requests.patch(
                        f"{self.api_url}/workflows/{workflow_id}",
                        headers=self.headers,
                        json={"active": True},
                        timeout=30
                    )

                    return {
                        "success": response.status_code == 200,
                        "operation": "activateWorkflow"
                    }
                except Exception as e:
                    return {"success": False, "error": str(e)}

        return {"success": False, "error": "No supported operations"}

    def validate_workflow(self, workflow_id: str) -> dict:
        """Simulate n8n_validate_workflow MCP command"""
        print(f"\n[MCP] n8n_validate_workflow(id='{workflow_id}')")

        # Get workflow and perform basic validation
        result = self.get_workflow(workflow_id)
        if not result["success"]:
            return result

        # Basic validation checks
        issues = []
        if result["nodes_count"] == 0:
            issues.append({"severity": "error", "message": "Workflow has no nodes"})

        return {
            "success": True,
            "valid": len(issues) == 0,
            "issues": issues,
            "nodes_count": result["nodes_count"]
        }

    def list_executions(self, workflow_id: str = None, limit: int = 10) -> dict:
        """Simulate n8n_executions MCP command with action='list'"""
        print(f"\n[MCP] n8n_executions(action='list', workflowId='{workflow_id}', limit={limit})")

        try:
            params = {"limit": limit}
            if workflow_id:
                params["workflowId"] = workflow_id

            response = requests.get(
                f"{self.api_url}/executions",
                headers=self.headers,
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                executions = data.get("data", [])
                return {
                    "success": True,
                    "count": len(executions),
                    "executions": [
                        {
                            "id": e.get("id"),
                            "status": e.get("status"),
                            "startedAt": e.get("startedAt"),
                            "stoppedAt": e.get("stoppedAt")
                        }
                        for e in executions
                    ]
                }
            return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_execution(self, execution_id: str, mode: str = "summary") -> dict:
        """Simulate n8n_executions MCP command with action='get'"""
        print(f"\n[MCP] n8n_executions(action='get', id='{execution_id}', mode='{mode}')")

        try:
            response = requests.get(
                f"{self.api_url}/executions/{execution_id}",
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                execution = response.json()
                return {
                    "success": True,
                    "id": execution.get("id"),
                    "status": execution.get("status"),
                    "mode": execution.get("mode"),
                    "startedAt": execution.get("startedAt"),
                    "stoppedAt": execution.get("stoppedAt")
                }
            return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


def run_mcp_tests(args):
    """Run MCP integration tests"""

    print("\n" + "="*60)
    print("MCP n8n Server Integration Tests")
    print("="*60)

    mcp = MCPSimulator(args.n8n_url, args.api_key)
    results = {"passed": 0, "failed": 0}

    # Test 1: Health Check
    print("\n--- Test 1: Health Check ---")
    result = mcp.health_check()
    print(f"Result: {json.dumps(result, indent=2)}")
    if result["success"]:
        results["passed"] += 1
        print("[PASS] Health check successful")
    else:
        results["failed"] += 1
        print("[FAIL] Health check failed")
        return results

    # Test 2: List Workflows
    print("\n--- Test 2: List Workflows ---")
    result = mcp.list_workflows()
    print(f"Result: {json.dumps(result, indent=2)}")
    if result["success"]:
        results["passed"] += 1
        print(f"[PASS] Found {result['count']} workflows")
    else:
        results["failed"] += 1
        print("[FAIL] Could not list workflows")

    # Test 3: Find/Import Resume Enhancer Workflow
    print("\n--- Test 3: Find/Import Workflow ---")

    workflow_id = None
    for wf in result.get("workflows", []):
        if "resume" in wf["name"].lower() and "enhancer" in wf["name"].lower():
            workflow_id = wf["id"]
            print(f"Found existing workflow: {workflow_id}")
            break

    if not workflow_id:
        print("Workflow not found, importing...")
        workflow_path = Path(__file__).parent.parent / "workflow" / "workflow.json"

        if workflow_path.exists():
            with open(workflow_path, "r", encoding="utf-8") as f:
                workflow_data = json.load(f)

            result = mcp.create_workflow(workflow_data)
            print(f"Result: {json.dumps(result, indent=2)}")

            if result["success"]:
                workflow_id = result["id"]
                results["passed"] += 1
                print(f"[PASS] Workflow imported: {workflow_id}")
            else:
                results["failed"] += 1
                print("[FAIL] Could not import workflow")
        else:
            results["failed"] += 1
            print(f"[FAIL] Workflow file not found: {workflow_path}")
    else:
        results["passed"] += 1
        print(f"[PASS] Workflow found: {workflow_id}")

    if not workflow_id:
        return results

    # Test 4: Get Workflow Details
    print("\n--- Test 4: Get Workflow Details ---")
    result = mcp.get_workflow(workflow_id)
    print(f"Result: {json.dumps(result, indent=2)}")
    if result["success"]:
        results["passed"] += 1
        print(f"[PASS] Got workflow with {result['nodes_count']} nodes")
    else:
        results["failed"] += 1
        print("[FAIL] Could not get workflow details")

    # Test 5: Validate Workflow
    print("\n--- Test 5: Validate Workflow ---")
    result = mcp.validate_workflow(workflow_id)
    print(f"Result: {json.dumps(result, indent=2)}")
    if result["success"] and result.get("valid"):
        results["passed"] += 1
        print("[PASS] Workflow is valid")
    elif result["success"]:
        results["passed"] += 1
        print(f"[PASS] Validation complete with {len(result.get('issues', []))} issues")
    else:
        results["failed"] += 1
        print("[FAIL] Validation failed")

    # Test 6: List Executions
    print("\n--- Test 6: List Executions ---")
    result = mcp.list_executions(workflow_id, limit=5)
    print(f"Result: {json.dumps(result, indent=2)}")
    if result["success"]:
        results["passed"] += 1
        print(f"[PASS] Found {result['count']} executions")
    else:
        results["failed"] += 1
        print("[FAIL] Could not list executions")

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print("="*60 + "\n")

    return results


def main():
    parser = argparse.ArgumentParser(description="MCP n8n Server Integration Tests")
    parser.add_argument(
        "--n8n-url",
        default=os.getenv("N8N_HOST", "http://localhost:5678"),
        help="n8n base URL"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("N8N_API_KEY", ""),
        help="n8n API key"
    )

    args = parser.parse_args()

    if not args.api_key:
        print("Error: n8n API key is required")
        print("Set N8N_API_KEY environment variable or use --api-key")
        sys.exit(1)

    results = run_mcp_tests(args)
    sys.exit(1 if results["failed"] > 0 else 0)


if __name__ == "__main__":
    main()
