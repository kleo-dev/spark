title: Quickstart
slug: quickstart

# Quickstart

Once Spark is installed and your shell environment is set up (after restarting your terminal or sourcing your shell profile), you can immediately start generating documentation. This quickstart guide will show you how to use Spark in its most basic form.

## Running Spark

Navigate to the root directory of your project where your source code resides. For example, if you have a `my_project` directory:

```bash
cd my_project
```

Now, simply execute the `spark` command:

```bash
spark
```

## What Happens Next?

Upon running `spark`, the tool will:

1.  **Scan your current directory:** It recursively reads all files within the current directory, respecting `.gitignore` and `.sparkignore` files (if present).
2.  **Prepare context for the AI:** The content of your source files is formatted into a prompt for the generative AI model.
3.  **Communicate with the AI:** Spark sends the formatted prompt to the Google Gemini model using your configured API key.
4.  **Receive and Parse Response:** The AI generates documentation, which Spark then parses to identify individual Markdown files and their contents.
5.  **Write Documentation Files:** Spark creates a new directory named `docs_output` (overwriting it if it already exists) in your project root. Inside `docs_output`, it organizes the generated Markdown files into logical subdirectories (e.g., `intro/`, `guides/`, `reference/`, etc.) as specified by the AI's output.

## Example Output Structure

After successful execution, you will find a `docs_output` directory in your project root, containing the generated documentation:

```
my_project/
├── .git/
├── my_module.py
├── tests/
└── docs_output/
    ├── intro/
    │   ├── index.md
    │   └── installation.md
    ├── guides/
    │   ├── basic-usage.md
    │   └── ignoring-files.md
    ├── reference/
    │   └── api.md
    └── concepts/
        └── architecture.md
```

Each Markdown file within `docs_output` will contain a `title` and `slug` at the top, followed by the generated documentation content.

Congratulations! You've successfully generated documentation for your project using Spark. Explore the generated files in `docs_output` to see the AI's output.

For more detailed information on how Spark works internally or how to customize its behavior, refer to the following sections:
*   [How Spark Works](concepts/how-spark-works.md)
*   [Ignoring Files and Directories](guides/ignoring-files.md)
*   [Configuration](reference/configuration.md)
