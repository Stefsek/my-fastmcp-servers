"""FastMCP server for Python code documentation guidelines.

This module provides access to Python code documentation standards and
best practices, specifically focusing on Google-style docstrings and
commenting conventions. It helps developers write well-documented Python
code that follows industry standards.

Typical usage example:

  # Get Google-style Python documentation guidelines
  guidelines = get_python_code_documentation_google_style()
"""

from fastmcp import FastMCP
import os
import json
from typing import Dict

mcp = FastMCP("python-code-documentation")

@mcp.tool(
            name="get_python_code_documentation_google_style",
            description="Google-style Python docstring and commenting guidelines for writing well-documented code"
)
def get_python_code_documentation_google_style() -> str:
    """Retrieves Google-style Python documentation guidelines.

    Loads and returns comprehensive documentation guidelines for writing
    Python code using Google-style docstrings. The guidelines include
    standards for module, class, function, and method documentation,
    as well as inline commenting conventions.

    Returns:
        A JSON string containing:
        - Success: status and the complete guidelines content.
        - Error: status, error type, and descriptive error message
          if the guidelines file cannot be accessed.

    Raises:
        Does not raise exceptions directly, but returns JSON-encoded
        errors for FileNotFoundError or IOError cases.
    """
    server_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(server_dir, "python_guides", "markdown", "google_style_python_guide.md")

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return json.dumps({
            "status": "error",
            "error": "FileNotFoundError",
            "message": f"Documentation file not found at path: {full_path}"
        })
    except IOError as e:
        return json.dumps({
            "status": "error",
            "error": "IOError",
            "message": f"Failed to read documentation file at {full_path}: {str(e)}"
        })
    return json.dumps({
        "status": "success",
        "google_style_guideliness": content
    })


if __name__ == "__main__":
    mcp.run(transport="stdio")
