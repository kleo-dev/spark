title: Basic Usage
slug: basic-usage

# Basic Usage

Spark is designed for simplicity. Its primary function is to analyze your current project's codebase and generate documentation without requiring complex command-line arguments. This guide expands on the quickstart, detailing the typical workflow and expected outcomes.

## Running Spark in Your Project

To use Spark, navigate to the root directory of the project you wish to document. This is typically where your main source code files, configuration files, and potentially your `.gitignore` reside.

```bash
cd /path/to/your/project
spark
```

## How Spark Determines Context

Spark's core mechanism for understanding your project is by scanning the local file system. When you run `spark`, it performs a recursive scan starting from your current working directory (`os.getcwd()` in Python terms).

### File Inclusion and Exclusion

*   **Inclusion:** By default, Spark attempts to read all files it encounters in the directory tree.
*   **Exclusion:** To prevent sensitive information or irrelevant files (like build artifacts, virtual environments, or large data files) from being sent to the AI, Spark checks for ignore files:
    1.  **`.sparkignore`:** If a `.sparkignore` file exists in the current directory, Spark will read its contents. Each line in this file is treated as a pattern to exclude files or directories.
    2.  **`.gitignore`:** If `.sparkignore` is not found, Spark falls back to reading `.gitignore`. This provides a convenient way to reuse your existing version control ignore rules for documentation generation.

    The content of these ignore files is loaded into a global `ignore` list within `main.py`. This ensures that `get_local` function, responsible for reading file contents, does not include them in the prompt.

    For more details on managing ignored files, see [Ignoring Files and Directories](guides/ignoring-files.md).

## The Documentation Generation Process

Once executed, Spark orchestrates the following sequence of operations:

1.  **File Collection:** Recursively traverses the current directory, reading the content of included files. Each file's path and content are formatted into a string suitable for the AI prompt.
2.  **Prompt Construction:** The collected file data is appended to a predefined prompt template. This template includes instructions and guidelines for the AI, guiding it on the desired documentation structure and quality.
3.  **AI Interaction:** The complete prompt is sent to the configured Google Generative AI model. Spark waits for the AI's response, which contains the generated Markdown documentation.
4.  **Output Parsing:** The AI's response is a single string containing multiple documentation files, each delimited by a specific pattern (`File: <path>\nContents: ```...```\nEND_FILE`). Spark uses a regular expression to parse this string and extract individual file paths and their corresponding content.
5.  **File System Output:** Spark ensures a clean output environment by first removing any existing `docs_output` directory. It then recreates the directory structure based on the parsed file paths and writes each generated Markdown file to its designated location within `docs_output`.

This streamlined process allows you to get high-quality, structured documentation with a single `spark` command. The generated documentation aims to cover various aspects of your project, organized into categories like `intro/`, `guides/`, `reference/`, `concepts/`, and `advanced/`.
