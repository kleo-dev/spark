title: Contributing to Spark
slug: contributing

# Contributing to Spark

We welcome contributions to Spark! Whether it's reporting bugs, suggesting features, or submitting code, your input helps make Spark better for everyone. This guide provides an overview of how to get involved and the technical setup for development.

## How to Contribute

1.  **Bug Reports:** If you find a bug, please open an issue on the [GitHub repository](https://github.com/kleo-dev/spark/issues). Provide clear steps to reproduce, expected behavior, and actual behavior.
2.  **Feature Requests:** Have an idea for a new feature or improvement? Open an issue to discuss it.
3.  **Documentation Improvements:** Spotted a typo, an unclear explanation, or something missing in the documentation (even the documentation Spark generates!)? Contributions to clarity and completeness are always appreciated.
4.  **Code Contributions:**
    *   Fork the repository.
    *   Create a new branch for your feature or bug fix.
    *   Write clean, well-commented code.
    *   Ensure your changes align with the project's goals.
    *   Submit a pull request.

## Setting Up Your Development Environment

The `install.py` script provides an excellent foundation for setting up a development environment, as it handles cloning, virtual environment creation, and dependency installation.

1.  **Clone the Repository:**
    Instead of using the one-liner, you can directly clone the repository if you plan to modify the `install.py` script itself or prefer manual setup:

    ```bash
    git clone https://github.com/kleo-dev/spark.git
    cd spark
    ```

2.  **Run `install.py` for Initial Setup:**
    Even for development, running `install.py` is the easiest way to get the virtual environment (`venv`), dependencies, and the `spark` executable wrapper set up correctly.

    ```bash
    python3 install.py
    ```
    This will set up Spark in `~/.spark/`, create the `venv`, install dependencies, and configure your `PATH`.

3.  **Activate the Development Virtual Environment:**
    While `install.py` creates a wrapper script that automatically activates the venv, for active development, it's often more convenient to manually activate the venv:

    ```bash
    source ~/.spark/venv/bin/activate
    ```
    Now your shell's Python environment is configured to use Spark's dependencies.

4.  **Work on the Code:**
    The core logic is in `~/.spark/main.py`. You can make changes to this file directly, or, for a typical development flow, you would clone the repository to a different location (e.g., `~/dev/spark`) and then modify the `spark` wrapper script in `~/.spark/bin/spark` to point to your development copy of `main.py`.

    Alternatively, if your cloned repository is at `~/dev/spark`, you can modify the `~/.spark/bin/spark` wrapper script to point to `~/dev/spark/main.py`:

    ```bash
    # ~/.spark/bin/spark
    #!/bin/bash
    source "$HOME/.spark/venv/bin/activate"
    python3 "$HOME/dev/spark/main.py" "$@" # Point to your dev copy
    ```
    Remember to `chmod +x ~/.spark/bin/spark` if you create it manually.

5.  **Test Your Changes:**
    After making changes, run `spark` from a test project directory to see the impact of your modifications.

    ```bash
    # From your test project directory
    spark
    ```

## Coding Guidelines

*   **Readability:** Write clear, concise, and well-commented code.
*   **Error Handling:** Implement robust error handling where appropriate.
*   **Testing (Future):** While not explicitly present in the provided source, consider how your changes might be tested.
*   **Prompt Engineering:** If modifying the core prompt in `main.py`, understand the impact on AI output quality. Test changes to the prompt thoroughly.
*   **File System Operations:** Be cautious with file system operations (e.g., `shutil.rmtree`, `os.makedirs`), especially the `docs_output` cleanup logic in `main.py` which could be optimized for efficiency.

Thank you for considering contributing to Spark!
