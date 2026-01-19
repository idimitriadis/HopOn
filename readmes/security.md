# Security Architecture & Decisions

This document outlines the security measures implemented in HopOn to protect against common vulnerabilities, specifically focusing on AI interactions and data handling.

## 1. AI Safety & Prompt Injection
**Risk:** "Prompt Injection" where malicious instructions hidden in the project data (e.g., in a project description from CORDIS) could override the system prompt and manipulate the AI's output.

**Mitigation:**
*   **XML Delimiters:** We use strict XML-style tags (`<project_data>...</project_data>`) to wrap user-provided content. The system prompt is explicitly instructed to *only* process information within these tags.
*   **Sanitization:** The `utils/ai.py` module constructs prompts defensively, ensuring that data is treated as context, not instruction.

## 2. Secrets Management & Logging
**Risk:** Leaking API keys (like `OPENROUTER_API_KEY`) or sensitive PII in application logs or error tracebacks.

**Mitigation:**
*   **Log Sanitization:** We explicitly removed code that logged raw API response bodies (`response.text`) in error handlers, as these can sometimes contain echoed keys or sensitive session data.
*   **Environment Variables:** All secrets are managed via `.env` and `python-dotenv`, never hardcoded.

## 3. Dependency Management
**Risk:** Vulnerabilities in third-party packages (e.g., `nbconvert` in the Jupyter ecosystem) potentially exposing the development environment.

**Strategy:**
*   **Monitoring:** We use `osv-scanner` to audit dependencies.
*   **Scope Awareness:** We differentiate between runtime vulnerabilities (critical) and development/notebook vulnerabilities (managed by keeping dev tools updated).

## 4. Local-Only Security Model
**Decision:** HopOn is architected as a **local, single-user application**.
*   **Authentication:** We intentionally do not implement complex auth (OAuth/Passwords) because the app runs on `localhost`. The "User ID" system is for personalization (watchlists), not security.
*   **Network:** The app binds to localhost. Deployment to a public server is **strongly discouraged** without an external authentication layer (like a VPN or Reverse Proxy with Auth).
