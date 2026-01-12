# HopOn Project Structure

This file provides a brief analysis of the core files and directories created by the setup script.

*   ./.venv/
    *   **Purpose**: Virtual environment, sandboxed Python interpreter and packages.

*   ./.env.template
    *   **Purpose**: A template for your secrets file. Rename this to .env and add your GEMINI_API_KEY.

*   ./.gitignore
    *   **Purpose**: Tells Git which files/directories to ignore (e.g., .venv, .env).

*   ./requirements.yaml
    *   **Purpose**: Lists Python packages & versions for reproducible installs.

*   ./LICENSE.md
    *   **Purpose**: Contains GNU GPL v3 license text.

*   ./memory/
    *   **Purpose**: Local folder for short-lived project memory files.

*   ./opinions/
    *   **Purpose**: Folder for AI-generated or curated opinion markdown files (e.g., claude.md, chatgpt.md, gemini.md).

*   ./Gemini.md
    *   **Purpose**: Root-level markdown file for project-specific Gemini notes, experiments, or logs.
