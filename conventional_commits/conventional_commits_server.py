"""FastMCP server for generating and validating conventional commits.

This module provides tools for working with conventional commit messages,
including automatic generation based on staged git changes and validation
using commitlint. It helps maintain consistent commit message formatting
across projects.

Typical usage example:

  # Generate a conventional commit message
  result = generate_conventional_commit()

  # Validate a commit message
  validation = validate_commit_message("feat: add new feature")
"""

from fastmcp import FastMCP
import subprocess
import os
import json
from typing import Dict

mcp = FastMCP("conventional-commits")


@mcp.tool(
    name="generate_conventional_commit",
    description=(
        "Generate a conventional commit message by analyzing staged git changes. "
        "Reads repository status and diff to help create properly formatted commit "
        "messages following conventional commit guidelines."
    )
)
def generate_conventional_commit(repository_path: str = None) -> str:
    """Generates a conventional commit message from staged git changes.

    Analyzes the current git repository's staged changes and provides
    the necessary information to generate a properly formatted conventional
    commit message. The function loads conventional commit guidelines,
    retrieves git status and diff, and returns structured data for
    commit message generation.

    Args:
        repository_path: Optional path to the git repository. If None,
            uses the current working directory.

    Returns:
        A JSON string containing either:
        - Success: repository path, git status, staged diff, guidelines,
          and instructions for generating the commit message.
        - Error: error message with hints for resolution.

    Raises:
        Does not raise exceptions directly, but returns JSON-encoded
        errors for file access issues or git command failures.
    """
    try:
        server_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(
            server_dir, "git_guides", "markdown", "conventional_commit_guidelines.md"
        )

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (FileNotFoundError, IOError, OSError) as e:
        error = {
            "error": f"Failed to load conventional commit guidelines: {str(e)}",
            "file_path": full_path,
            "hint": (
                "Ensure the file 'conventional_commit_guidelines.md' exists at "
                "git_guides/markdown/ relative to the server script."
            )
        }
        return json.dumps(error)

    try:
        work_dir = repository_path if repository_path else os.getcwd()
        git_root = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            text=True,
            stderr=subprocess.STDOUT,
            cwd=work_dir
        ).strip()
        status = subprocess.check_output(
            ['git', 'status'],
            text=True,
            cwd=git_root
        )
        staged_diff = subprocess.check_output(
            ['git', 'diff', '--staged'],
            text=True,
            cwd=git_root
        )
        if not staged_diff.strip():
            response = {
                "error": (
                    "No staged changes found. Please run 'git add .' to stage "
                    "your changes first, then try again."
                ),
                "repository": git_root
            }
            return json.dumps(response)
        response = {
            "repository": git_root,
            "status": status,
            "diff": staged_diff,
            "required_guideliness": content,
            "instructions": """
            Generate a conventional commit message:
            Step 1: Read the required guideliness
            Step 2: Analyze the diff above
                    - Understand what changed in the code
                    - Determine the most appropriate commit type
                    - Identify the scope if applicable
            Step 3: Generate commit message
                    - Follow the EXACT required guideliness
            Step 4: Output the command
                    - Return ONLY: git commit -m "your message"
            """
        }
        return json.dumps(response)

    except subprocess.CalledProcessError as e:
        error = {
            "error": f"Git command failed: {e.output}",
            "hint": "Make sure you're in a git repository"
        }
        return json.dumps(error)

@mcp.tool(
    name="validate_commit_message",
    description=(
        "Validate a commit message using commitlint. Checks if the message "
        "follows conventional commit format and returns validation errors if any. "
        "Use this after generating a commit message if you want to verify it's correct."
    )
)
def validate_commit_message(message: str) -> str:
    """Validates a commit message against conventional commit standards.

    Uses commitlint to verify that a commit message follows the conventional
    commit format. Can handle messages with or without the 'git commit -m'
    prefix. Returns validation results with detailed error information if
    the message is invalid.

    Args:
        message: The commit message to validate. Can be a plain message or
            include 'git commit -m' prefix with quotes.

    Returns:
        A JSON string containing:
        - If valid: validation status, formatted message, and git command.
        - If invalid: validation status, errors, and fix instructions.
        - If commitlint not installed: installation instructions.

    Raises:
        Does not raise exceptions directly, but returns JSON-encoded
        errors for missing commitlint or validation failures.
    """
    try:
        # Extract the actual commit message if wrapped in git command format.
        # Handle both quoted and unquoted message formats.
        if message.startswith('git commit -m'):
            import re
            match = re.search(r'git commit -m ["\'](.+?)["\']', message)
            if match:
                message = match.group(1)
            else:
                message = message.replace('git commit -m', '').strip().strip('"').strip("'")
        result = subprocess.run(
            ['commitlint'],
            input=message,
            text=True,
            capture_output=True
        )
        if result.returncode == 0:
            response = {
                "valid": True,
                "message": message,
                "output": result.stdout,
                "git_command": f'git commit -m "{message}"',
                "note": (
                    "✓ Message is valid and follows "
                    "guide://git-conventional-commits format"
                )
            }
            return json.dumps(response)
        else:
            response = {
                "valid": False,
                "message": message,
                "errors": result.stdout,
                "required_resource": "guide://git-conventional-commits",
                "fix_instructions": (
                    "Your commit message failed validation. "
                    "Re-read guide://git-conventional-commits and fix the message, "
                    "then validate again if needed."
                )
            }
            return json.dumps(response)

    except FileNotFoundError:
        error = {
            "error": "commitlint is not installed",
            "solution": "Install commitlint with: npm install -g @commitlint/cli @commitlint/config-conventional",
            "note": "You also need a .commitlintrc.json file in your project root"
        }
        return json.dumps(error)
    except Exception as e:
        error = {
            "error": f"Validation failed: {str(e)}"
        }
        return json.dumps(error)

if __name__ == "__main__":
    mcp.run(transport="stdio")