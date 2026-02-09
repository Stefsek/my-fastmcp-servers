# FastMCP Servers

A collection of Model Context Protocol (MCP) servers built with FastMCP for enhancing development workflows.

## Servers

### 1. Conventional Commits Server

**Location:** `conventional_commits/`

**Purpose:** Automates the generation and validation of conventional commit messages according to the Conventional Commits specification.

**Features:**
- `generate_conventional_commit`: Analyzes staged git changes and provides guidelines for creating properly formatted commit messages
- `validate_commit_message`: Validates commit messages using commitlint to ensure they follow the conventional commit format

**Stack:**
- Python 3.13.5+
- FastMCP 2.14.5+
- Git
- Commitlint (for validation)

**How it works:**
1. Reads staged changes from the git repository
2. Loads conventional commit guidelines from local markdown files
3. Analyzes the diff and provides structured commit message recommendations
4. Validates messages against conventional commit standards using commitlint

**Tools Exposed:**
- `generate_conventional_commit(repository_path)` - Generate commit message from staged changes
- `validate_commit_message(message)` - Validate commit message format

---

### 2. Python Code Documentation Server

**Location:** `python_documentations/`

**Purpose:** Provides Google-style Python docstring and commenting guidelines to help developers write well-documented code.

**Features:**
- `get_python_code_documentation_google_style`: Retrieves comprehensive Python documentation standards including module, class, function, and inline comment conventions

**Stack:**
- Python 3.13+
- FastMCP 2.14.5+

**How it works:**
1. Serves pre-loaded Google-style Python documentation guidelines
2. Returns markdown-formatted documentation content
3. Provides structured error handling for file operations

**Tools Exposed:**
- `get_python_code_documentation_google_style()` - Get Google-style docstring guidelines

---

## Technology Stack

Both servers are built using:
- **FastMCP**: A Python framework for building Model Context Protocol servers
- **Python 3.13+**: Modern Python with type hints and enhanced error handling
- **MCP Protocol**: Standard protocol for AI model context integration
- **JSON**: Structured data exchange format

## Running the Servers

Each server can be run independently using stdio transport:

```bash
# Conventional Commits Server
cd conventional_commits
python conventional_commits_server.py

# Python Documentation Server
cd python_documentations
python python_code_documentation_server.py
```

## Project Structure

```
FastMcpServers/
├── conventional_commits/
│   ├── conventional_commits_server.py
│   ├── git_guides/
│   ├── pyproject.toml
│   └── uv.lock
├── python_documentations/
│   ├── python_code_documentation_server.py
│   ├── python_guides/
│   ├── pyproject.toml
│   └── uv.lock
└── README.md
```
