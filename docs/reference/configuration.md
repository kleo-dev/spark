title: Configuration
slug: configuration

# Configuration

Spark offers a minimalistic yet effective approach to configuration, primarily through convention-over-configuration and dedicated files for specific settings. This section details the key configuration points available.

## 1. API Key (`~/.spark/keys.py`)

**Purpose:** This file stores your Google Gemini API key, which is essential for Spark to authenticate and interact with the generative AI model.

**Location:** `~/.spark/keys.py` (within your home directory).

**Content Example:**

```python
API_KEY: str = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"
```

**Management:**
*   **Initial Setup:** The `install.py` script automatically creates this file and prompts you for your API key during installation.
*   **Updating:** You can manually edit this file to change or update your API key. See [Managing Your API Key](guides/managing-api-key.md) for more details.

**Rationale:** Storing the API key in a dedicated, isolated file outside of your project directory helps prevent accidental exposure in version control systems.

## 2. Ignored Files (`.sparkignore` or `.gitignore`)

**Purpose:** These files control which files and directories Spark will *not* send to the AI model for analysis. This is critical for excluding sensitive data, build artifacts, virtual environments, or any content irrelevant to documentation.

**Location:** In the root of your project directory (where you run the `spark` command).

**Hierarchy:**
*   Spark first checks for `.sparkignore`.
*   If `.sparkignore` is not found, it falls back to `.gitignore`.

**Content Example (for either file):**

```
# Exclude Python virtual environment
venv/

# Exclude compiled Python files
__pycache__/
*.pyc

# Exclude Spark's own output
docs_output/

# Exclude sensitive files
.env
my_secrets.txt
```

**Rationale:**
*   **Contextual Relevance:** Ensures the AI focuses only on the source code and relevant assets, leading to more accurate and concise documentation.
*   **Security:** Prevents sensitive information from being sent to external AI services.
*   **Performance:** Reduces the amount of data processed by both Spark and the AI model, potentially speeding up generation.

**Best Practice:** Always include `docs_output/` in your ignore file to prevent Spark from attempting to document its own output, which could lead to recursive or nonsensical content. See [Ignoring Files and Directories](guides/ignoring-files.md) for more details.

## Summary

Spark's configuration is designed to be minimal and intuitive. The API key is managed automatically during installation, and content exclusion is handled via widely understood `.gitignore`-style patterns. This allows developers to quickly integrate Spark into their workflow without extensive setup.
