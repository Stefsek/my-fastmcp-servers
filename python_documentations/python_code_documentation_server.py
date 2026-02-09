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
