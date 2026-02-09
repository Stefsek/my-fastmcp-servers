"""Conventional Commits MCP Server.

This module provides a Model Context Protocol (MCP) server for generating and
validating conventional commit messages. It includes tools for analyzing git
repository changes and creating properly formatted commit messages according
to conventional commit guidelines.

The server uses the FastMCP framework to expose two main tools:
  - generate_conventional_commit: Analyzes staged changes and provides
    guidelines for creating a conventional commit message
  - validate_commit_message: Validates commit messages using commitlint

Typical usage example:

    # Run the server with stdio transport
    python conventional_commits_server.py
"""

from fastmcp import FastMCP
import subprocess
import os
import json
from typing import Dict

# Initialize the FastMCP server instance with a descriptive name.
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

    Analyzes the git repository's staged changes and provides all necessary
    information to generate a properly formatted conventional commit message.
    Loads conventional commit guidelines from a local markdown file and combines
    them with repository status and diff information.

    Args:
        repository_path: Path to the git repository. If None, uses the current
            working directory. The function will auto-detect the git root using
            git rev-parse.

    Returns:
        A JSON-encoded string containing a dictionary with the following structure:

        On success with staged changes:
          - repository: The path to the git repository root
          - status: The git status output showing current branch and changes
          - diff: The staged changes diff output
          - required_guideliness: The full conventional commit guidelines content
          - instructions: Step-by-step instructions for generating the commit

        On error (no staged changes, missing guidelines, or git command failure):
          - error: A descriptive error message
          - Additional context fields (file_path, hint, repository) depending on
            the error type

    Raises:
        This function does not raise exceptions. All errors are caught and
        returned as structured error dictionaries in the return value.
    """

    try:
        # Load conventional commit guidelines from the local markdown file.
        server_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(
            server_dir, "git_guides", "markdown", "conventional_commit_guidelines.md"
        )

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (FileNotFoundError, IOError, OSError) as e:
        # Handle errors when loading the guidelines file.
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
        # Use the provided repository path or fallback to current directory.
        work_dir = repository_path if repository_path else os.getcwd()

        # Auto-detect the git root directory using git rev-parse.
        git_root = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            text=True,
            stderr=subprocess.STDOUT,
            cwd=work_dir
        ).strip()

        # Get the current repository status.
        status = subprocess.check_output(
            ['git', 'status'],
            text=True,
            cwd=git_root
        )

        # Get the diff of staged changes only.
        staged_diff = subprocess.check_output(
            ['git', 'diff', '--staged'],
            text=True,
            cwd=git_root
        )

        # Check if there are any staged changes to commit.
        if not staged_diff.strip():
            response = {
                "error": (
                    "No staged changes found. Please run 'git add .' to stage "
                    "your changes first, then try again."
                ),
                "repository": git_root
            }
            return json.dumps(response)

        # Build the response with all necessary information for commit generation.
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
        # Handle git command failures such as not being in a git repository.
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
    """Validates a commit message using commitlint.

    Runs the commitlint tool to verify that the provided commit message follows
    the conventional commit format. Automatically strips 'git commit -m' prefix
    if present in the message to extract just the commit message text.

    Args:
        message: The commit message to validate. Can be either the raw message
            text or include the full 'git commit -m "message"' command format.

    Returns:
        A JSON-encoded string containing a dictionary with the following structure:

        On successful validation (message is valid):
          - valid: Boolean set to True
          - message: The validated message text
          - output: The commitlint stdout output
          - git_command: A ready-to-use git commit command with the message
          - note: A confirmation that the message follows the correct format

        On validation failure (message is invalid):
          - valid: Boolean set to False
          - message: The message that failed validation
          - errors: The commitlint error output with details
          - required_resource: Reference to the conventional commits guide
          - fix_instructions: Instructions for fixing the message

        On error (commitlint not installed or other exceptions):
          - error: A descriptive error message
          - solution/note: Additional context or installation instructions

    Raises:
        This function does not raise exceptions. All errors are caught and
        returned as structured error dictionaries in the return value.
    """
    try:
        # Remove 'git commit -m' prefix if present and extract just the message.
        if message.startswith('git commit -m'):
            import re
            # Match the message within quotes using regex.
            match = re.search(r'git commit -m ["\'](.+?)["\']', message)
            if match:
                message = match.group(1)
            else:
                # Fallback: strip the prefix and quotes manually.
                message = message.replace('git commit -m', '').strip().strip('"').strip("'")

        # Run commitlint validation using subprocess.
        result = subprocess.run(
            ['commitlint'],
            input=message,
            text=True,
            capture_output=True
        )

        # Check the validation result and build the appropriate response.
        if result.returncode == 0:
            # Message passed validation successfully.
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
            # Message failed validation.
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
        # Handle case where commitlint is not installed on the system.
        error = {
            "error": "commitlint is not installed",
            "solution": "Install commitlint with: npm install -g @commitlint/cli @commitlint/config-conventional",
            "note": "You also need a .commitlintrc.json file in your project root"
        }
        return json.dumps(error)
    except Exception as e:
        # Handle any other unexpected validation errors.
        error = {
            "error": f"Validation failed: {str(e)}"
        }
        return json.dumps(error)

if __name__ == "__main__":
    # Run the MCP server using stdio transport for communication.
    # This allows the server to be used as a subprocess by MCP clients.
    mcp.run(transport="stdio")