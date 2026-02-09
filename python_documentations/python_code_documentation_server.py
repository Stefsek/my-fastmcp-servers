"""Python Code Documentation MCP Server.

This module provides a Model Context Protocol (MCP) server that serves
Python documentation guidelines, specifically Google-style docstring
conventions and commenting best practices.

The server exposes tools for retrieving comprehensive Python documentation
standards to help developers write well-documented code according to
Google's Python style guide. It uses the FastMCP framework to implement
the MCP protocol and serves documentation content from local markdown files.

Typical usage example:

  # Run the server with stdio transport
  python python_code_documentation_server.py

  # The server will be available for MCP clients to connect and retrieve
  # Python documentation guidelines through the exposed tools.
"""

from fastmcp import FastMCP
import os
import json
from typing import Dict


# Initialize the FastMCP server instance with a descriptive name
mcp = FastMCP("python-code-documentation")

@mcp.tool(
            name="get_python_code_documentation_google_style",
            description="Google-style Python docstring and commenting guidelines for writing well-documented code"
)
def get_python_code_documentation_google_style() -> str:
    """Retrieves Google-style Python documentation guidelines.

    Reads and returns the comprehensive Google-style Python docstring and
    commenting guidelines from a markdown file. This tool provides developers
    with standards for writing well-documented Python code, including module,
    class, function, and inline comment conventions.

    The function locates the documentation file relative to this server's
    location and reads its contents. It handles common file operation errors
    gracefully by returning structured error messages encoded in JSON format.

    Returns:
        A JSON-encoded string containing a dictionary with the following structure:

        On success, the dictionary contains:
          - status: The string "success"
          - google_style_guideliness: The full markdown documentation content

        On error, the dictionary contains:
          - status: The string "error"
          - error: The exception type name (e.g., "FileNotFoundError", "IOError")
          - message: A detailed error description with the file path and error details

    Raises:
        This function does not raise exceptions. All errors are caught and
        returned as structured error dictionaries in the return value.
    """
    # Determine the directory containing this server file for building relative paths.
    server_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the documentation markdown file.
    full_path = os.path.join(server_dir, "python_guides", "markdown", "google_style_python_guide.md")

    try:
        # Read the documentation content with UTF-8 encoding to support all characters.
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        # Handle case where the documentation file doesn't exist at the expected location.
        return json.dumps({
            "status": "error",
            "error": "FileNotFoundError",
            "message": f"Documentation file not found at path: {full_path}"
        })
    except IOError as e:
        # Handle file read errors such as permission issues or disk failures.
        return json.dumps({
            "status": "error",
            "error": "IOError",
            "message": f"Failed to read documentation file at {full_path}: {str(e)}"
        })

    # Return successful response with the full documentation content.
    return json.dumps({
        "status": "success",
        "google_style_guideliness": content
    })


if __name__ == "__main__":
    # Run the MCP server using stdio transport for communication.
    # This allows the server to be used as a subprocess by MCP clients.
    mcp.run(transport="stdio")
