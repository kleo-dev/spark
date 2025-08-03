title: Installation
slug: installation

# Installation

This guide walks you through the steps to install Spark on your system. The installation script handles cloning the repository, setting up a dedicated Python virtual environment, installing dependencies, and configuring your shell's `PATH`.

## Prerequisites

*   **Python 3:** Ensure you have Python 3.8 or higher installed.
*   **Git:** Git must be installed on your system to clone the Spark repository.
*   **`wget` (Linux/macOS):** Used by the one-liner installer to fetch the script.

## Step-by-Step Installation

Spark provides a convenient one-liner script for installation:

1.  **Run the Installation Command:**
    Open your terminal and execute the following command:

    ```bash
    wget -qO- https://raw.githubusercontent.com/kleo-dev/spark/refs/heads/master/install.py | python3
    ```

    **What this command does:**
    *   `wget -qO- ...`: Downloads the `install.py` script from the Spark GitHub repository.
    *   `| python3`: Pipes the downloaded script directly to the Python 3 interpreter, executing it.

2.  **Installation Script Execution:**
    The `install.py` script performs the following actions:

    *   **Clones/Updates Repository:** It clones the Spark repository into `~/.spark`. If the directory already exists, it pulls the latest changes.
    *   **Creates Directories:** Sets up `~/.spark/bin` and `~/.spark/venv`.
    *   **Virtual Environment Setup:** Creates a dedicated Python virtual environment within `~/.spark/venv` to isolate Spark's dependencies from your system's Python packages.
    *   **Dependency Installation:** Installs `google-generativeai` (and upgrades `pip`) into the virtual environment.
    *   **Executable Wrapper:** Creates an executable script named `spark` in `~/.spark/bin`. This script activates the virtual environment and runs the `main.py` script.
    *   **PATH Configuration:** Appends `~/.spark/bin` to your shell's `PATH` environment variable by modifying common shell configuration files (e.g., `~/.bashrc`, `~/.zshrc`). This allows you to run `spark` from any directory.
    *   **API Key Prompt:** Prompts you to enter your Google Gemini API key. This key is saved securely in `~/.spark/keys.py`.

3.  **Enter Your Google Gemini API Key:**
    During the installation, you will be prompted to enter your Google Gemini API key. This key is essential for Spark to interact with the generative AI model.

    ```
    Enter your Google Gemini API key:
    ```
    Paste your API key and press Enter.

    **Note:** If you don't have an API key yet, you can obtain one from the [Google AI Studio](https://ai.google.dev/).

4.  **Final Steps and Shell Restart:**
    The script will output a success message:

    ```
    ✅ Installation complete.
    👉 Restart your shell or run 'source ~/.bashrc' (or equivalent) to update your PATH.
    ```
    It's crucial to restart your terminal or explicitly `source` your shell configuration file (e.g., `source ~/.bashrc` or `source ~/.zshrc`) for the `spark` command to become available in your `PATH`.

## Troubleshooting

*   **`spark: command not found`**: Ensure you have restarted your shell or sourced your `rc` file after installation.
*   **Permission Errors**: If you encounter permission errors during cloning or file creation, verify that your user has write access to your home directory.
*   **Network Issues**: Check your internet connection if the `wget` or `git clone` steps fail.

Once installed, you can proceed to the [Quickstart guide](guides/quickstart.md) to generate your first set of documentation.
