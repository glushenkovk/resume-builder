#!/usr/bin/env python3
"""
Resume Enhancer n8n Workflow Test Runner

This script tests the Resume Enhancer workflow without depending on LinkedIn.
It uses the /retry endpoint with a sample job description.

Usage:
    python test_runner.py [--n8n-url URL] [--api-key KEY] [--output-dir DIR]
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_status(message: str, status: str = "info"):
    """Print colored status message"""
    colors = {
        "pass": Colors.GREEN,
        "fail": Colors.RED,
        "warn": Colors.YELLOW,
        "info": Colors.BLUE
    }
    color = colors.get(status, Colors.RESET)
    symbol = {"pass": "[PASS]", "fail": "[FAIL]", "warn": "[WARN]", "info": "[INFO]"}
    print(f"{color}{symbol.get(status, '[INFO]')}{Colors.RESET} {message}")


def load_fixtures() -> dict:
    """Load test fixtures"""
    fixtures_dir = Path(__file__).parent / "fixtures"

    resume_path = fixtures_dir / "sample_resume.txt"
    jd_path = fixtures_dir / "sample_job_description.txt"

    if not resume_path.exists():
        raise FileNotFoundError(f"Resume fixture not found: {resume_path}")
    if not jd_path.exists():
        raise FileNotFoundError(f"JD fixture not found: {jd_path}")

    return {
        "resume_text": resume_path.read_text(encoding="utf-8"),
        "job_description": jd_path.read_text(encoding="utf-8")
    }


def check_n8n_health(base_url: str, api_key: str) -> bool:
    """Check if n8n is accessible"""
    try:
        response = requests.get(
            f"{base_url}/api/v1/workflows",
            headers={"X-N8N-API-KEY": api_key},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print_status(f"n8n health check failed: {e}", "fail")
        return False


def find_workflow(base_url: str, api_key: str, workflow_name: str) -> str | None:
    """Find workflow ID by name"""
    try:
        response = requests.get(
            f"{base_url}/api/v1/workflows",
            headers={"X-N8N-API-KEY": api_key},
            timeout=30
        )
        if response.status_code == 200:
            workflows = response.json().get("data", [])
            for wf in workflows:
                if workflow_name.lower() in wf.get("name", "").lower():
                    return wf.get("id")
        return None
    except Exception as e:
        print_status(f"Failed to list workflows: {e}", "fail")
        return None


def import_workflow(base_url: str, api_key: str, workflow_path: str) -> str | None:
    """Import workflow from JSON file"""
    try:
        with open(workflow_path, "r", encoding="utf-8") as f:
            workflow_data = json.load(f)

        response = requests.post(
            f"{base_url}/api/v1/workflows",
            headers={
                "X-N8N-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json=workflow_data,
            timeout=30
        )

        if response.status_code in [200, 201]:
            result = response.json()
            return result.get("id")
        else:
            print_status(f"Import failed: {response.status_code} - {response.text}", "fail")
            return None
    except Exception as e:
        print_status(f"Failed to import workflow: {e}", "fail")
        return None


def activate_workflow(base_url: str, api_key: str, workflow_id: str) -> bool:
    """Activate a workflow"""
    try:
        response = requests.patch(
            f"{base_url}/api/v1/workflows/{workflow_id}",
            headers={
                "X-N8N-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json={"active": True},
            timeout=30
        )
        return response.status_code == 200
    except Exception as e:
        print_status(f"Failed to activate workflow: {e}", "fail")
        return False


def trigger_retry_endpoint(base_url: str, fixtures: dict, language: str = "en",
                           tone: str = "professional", pages: int = 1) -> dict:
    """Trigger the /retry endpoint with test data"""

    # Generate unique request ID
    request_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.getpid()}"

    payload = {
        "request_id": request_id,
        "jd_text": fixtures["job_description"],
        "resume_text": fixtures["resume_text"],  # Simulating pre-extracted resume
        "language": language,
        "tone": tone,
        "pages": pages
    }

    try:
        response = requests.post(
            f"{base_url}/webhook/resume-enhancer/retry",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=300  # 5 minutes for full processing
        )

        return {
            "status_code": response.status_code,
            "response": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
            "request_id": request_id
        }
    except requests.exceptions.Timeout:
        return {
            "status_code": 0,
            "response": "Request timed out",
            "request_id": request_id
        }
    except Exception as e:
        return {
            "status_code": 0,
            "response": str(e),
            "request_id": request_id
        }


def check_output_files(output_dir: str, request_id: str) -> dict:
    """Check if expected output files were created"""

    expected_files = [
        "improved_resume.pdf",
        "resume.html",
        "cover_letter.md",
        "interview_prep.md",
        "ats_keywords.md",
        "gap_analysis.md",
        "stories_STAR.md",
        "questions_to_recruiter.md",
        "30-60-90.md",
        "changes_changelog.md",
        "data.json"
    ]

    # Find the output directory (may be nested under company/role)
    output_path = Path(output_dir)
    found_files = []
    missing_files = []

    # Search for request_id in subdirectories
    for path in output_path.rglob(request_id):
        if path.is_dir():
            for expected_file in expected_files:
                file_path = path / expected_file
                if file_path.exists():
                    found_files.append(expected_file)
                else:
                    missing_files.append(expected_file)
            break
    else:
        # If no directory found with request_id, all files are missing
        missing_files = expected_files

    return {
        "found": found_files,
        "missing": missing_files,
        "success": len(missing_files) == 0 or len(found_files) > 0
    }


def get_execution_logs(base_url: str, api_key: str, workflow_id: str,
                       limit: int = 5) -> list:
    """Get recent execution logs for the workflow"""
    try:
        response = requests.get(
            f"{base_url}/api/v1/executions",
            headers={"X-N8N-API-KEY": api_key},
            params={"workflowId": workflow_id, "limit": limit},
            timeout=30
        )

        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except Exception as e:
        print_status(f"Failed to get executions: {e}", "fail")
        return []


def run_tests(args):
    """Main test runner"""

    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}Resume Enhancer n8n Workflow Tests{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")

    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "warnings": 0
    }

    # Test 1: Load fixtures
    print_status("Test 1: Loading test fixtures...", "info")
    results["total"] += 1
    try:
        fixtures = load_fixtures()
        print_status(f"Loaded resume ({len(fixtures['resume_text'])} chars) and JD ({len(fixtures['job_description'])} chars)", "pass")
        results["passed"] += 1
    except Exception as e:
        print_status(f"Failed to load fixtures: {e}", "fail")
        results["failed"] += 1
        print("\nCannot continue without fixtures. Exiting.")
        return results

    # Test 2: Check n8n connection
    print_status("\nTest 2: Checking n8n connection...", "info")
    results["total"] += 1
    if check_n8n_health(args.n8n_url, args.api_key):
        print_status("n8n is accessible", "pass")
        results["passed"] += 1
    else:
        print_status("Cannot connect to n8n", "fail")
        results["failed"] += 1
        print("\nCannot continue without n8n connection. Exiting.")
        return results

    # Test 3: Find or import workflow
    print_status("\nTest 3: Finding Resume Enhancer workflow...", "info")
    results["total"] += 1
    workflow_id = find_workflow(args.n8n_url, args.api_key, "Resume Enhancer")

    if workflow_id:
        print_status(f"Found workflow: {workflow_id}", "pass")
        results["passed"] += 1
    else:
        print_status("Workflow not found, attempting import...", "warn")
        workflow_path = Path(__file__).parent.parent / "workflow" / "workflow.json"

        if workflow_path.exists():
            workflow_id = import_workflow(args.n8n_url, args.api_key, str(workflow_path))
            if workflow_id:
                print_status(f"Imported workflow: {workflow_id}", "pass")
                results["passed"] += 1

                # Activate workflow
                if activate_workflow(args.n8n_url, args.api_key, workflow_id):
                    print_status("Workflow activated", "pass")
                else:
                    print_status("Failed to activate workflow", "warn")
                    results["warnings"] += 1
            else:
                print_status("Failed to import workflow", "fail")
                results["failed"] += 1
                return results
        else:
            print_status(f"Workflow file not found: {workflow_path}", "fail")
            results["failed"] += 1
            return results

    # Test 4: Trigger workflow via retry endpoint
    print_status("\nTest 4: Triggering workflow via /retry endpoint...", "info")
    print_status("This may take a few minutes...", "info")
    results["total"] += 1

    trigger_result = trigger_retry_endpoint(args.n8n_url, fixtures)

    if trigger_result["status_code"] == 200:
        response = trigger_result["response"]
        if isinstance(response, dict) and response.get("success"):
            print_status(f"Workflow executed successfully", "pass")
            print_status(f"Request ID: {trigger_result['request_id']}", "info")
            results["passed"] += 1

            # Print some details
            if response.get("fit_score"):
                print_status(f"Fit Score: {response['fit_score']}", "info")
            if response.get("quality_status"):
                print_status(f"Quality Status: {response['quality_status']}", "info")
        else:
            print_status(f"Workflow returned error: {response}", "fail")
            results["failed"] += 1
    else:
        print_status(f"Request failed: {trigger_result['status_code']} - {trigger_result['response']}", "fail")
        results["failed"] += 1

    # Test 5: Check output files
    print_status("\nTest 5: Checking output files...", "info")
    results["total"] += 1

    if args.output_dir:
        file_check = check_output_files(args.output_dir, trigger_result["request_id"])

        if file_check["success"]:
            print_status(f"Found {len(file_check['found'])} files", "pass")
            for f in file_check["found"]:
                print_status(f"  - {f}", "info")
            results["passed"] += 1

            if file_check["missing"]:
                print_status(f"Missing {len(file_check['missing'])} files:", "warn")
                for f in file_check["missing"]:
                    print_status(f"  - {f}", "warn")
                results["warnings"] += 1
        else:
            print_status("No output files found", "fail")
            results["failed"] += 1
    else:
        print_status("OUTPUT_DIR not specified, skipping file check", "warn")
        results["warnings"] += 1

    # Test 6: Check execution logs
    print_status("\nTest 6: Checking execution logs...", "info")
    results["total"] += 1

    if workflow_id:
        executions = get_execution_logs(args.n8n_url, args.api_key, workflow_id)

        if executions:
            print_status(f"Found {len(executions)} recent executions", "pass")
            results["passed"] += 1

            # Show latest execution status
            latest = executions[0]
            status = latest.get("status", "unknown")
            print_status(f"Latest execution: {status}", "info")
        else:
            print_status("No executions found", "warn")
            results["warnings"] += 1

    # Print summary
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}Test Results Summary{Colors.RESET}")
    print(f"{'='*60}")
    print(f"Total:    {results['total']}")
    print(f"{Colors.GREEN}Passed:   {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}Failed:   {results['failed']}{Colors.RESET}")
    print(f"{Colors.YELLOW}Warnings: {results['warnings']}{Colors.RESET}")
    print(f"{'='*60}\n")

    return results


def main():
    parser = argparse.ArgumentParser(description="Resume Enhancer n8n Workflow Test Runner")
    parser.add_argument(
        "--n8n-url",
        default=os.getenv("N8N_HOST", "http://localhost:5678"),
        help="n8n base URL (default: $N8N_HOST or http://localhost:5678)"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("N8N_API_KEY", ""),
        help="n8n API key (default: $N8N_API_KEY)"
    )
    parser.add_argument(
        "--output-dir",
        default=os.getenv("OUTPUT_DIR", ""),
        help="Output directory to check for files (default: $OUTPUT_DIR)"
    )

    args = parser.parse_args()

    if not args.api_key:
        print(f"{Colors.RED}Error: n8n API key is required{Colors.RESET}")
        print("Set N8N_API_KEY environment variable or use --api-key")
        sys.exit(1)

    results = run_tests(args)

    # Exit with error code if any tests failed
    sys.exit(1 if results["failed"] > 0 else 0)


if __name__ == "__main__":
    main()
