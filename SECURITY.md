# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Use this section to tell people how to report a vulnerability.

*   Please do not report security vulnerabilities through public GitHub issues.
*   If you believe you have found a security vulnerability in HopOn, please report it to the maintainer directly.

## Local-Only Security Assumption

**Important:** This application is designed as a **local, single-user tool**.

*   **No Authentication:** The user management system is designed for local personalization (Watchlists), not security. It does not store passwords or enforce strict access controls.
*   **Database:** The SQLite database is not encrypted at rest.
*   **Deployment:** This application **should not** be deployed to a public server without adding an authentication layer (e.g., Streamlit Secrets, OAuth, or a reverse proxy like Nginx with Basic Auth).

## Dependencies

We monitor our dependencies for vulnerabilities using `osv-scanner`.
*   Development dependencies (like `nbconvert`) may lag behind if they are not used in the production path, but critical runtime dependencies are kept up to date.
