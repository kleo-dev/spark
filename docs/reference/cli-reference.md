title: Command Line Interface Reference
slug: cli-reference

# Command Line Interface (CLI) Reference

Spark provides a straightforward command-line interface, designed for simplicity and ease of use. Currently, the `spark` command operates without any explicit arguments or options, relying on its contextual execution.

## The `spark` Command

The core of Spark's CLI is a single command:

```bash
spark
```

### Usage

To use `spark`, simply navigate to the root directory of the project you wish to document and run the command:

```bash
cd /path/to/your/project
spark
```

### Behavior Without Arguments

Despite the lack of explicit arguments, the `spark` command performs a complex sequence of operations based on its implicit context:

*   **Current Directory Context:** Spark always operates on the files within the directory where it is executed. It recursively scans this directory and its subdirectories.
*   **Implicit File Inclusion/Exclusion:** It automatically detects and respects `.sparkignore` or `.gitignore` files to determine which files should be included in the AI prompt.
*   **Output Destination:** It creates (or overwrites) a `docs_output/` directory in the current working directory, populating it with the generated Markdown documentation.

### Example Workflow

1.  **Initialize a new project:**
    ```bash
    mkdir my-awesome-project
    cd my-awesome-project
    echo "def greet(name): return f'Hello, {name}!' " > app.py
    ```

2.  **Run Spark:**
    ```bash
    spark
    ```

3.  **Inspect Output:**
    ```bash
    ls docs_output
    # This will show the generated documentation categories and files, e.g., intro/, guides/, etc.
    ```

### Future Enhancements

While Spark's current design prioritizes simplicity, future versions might introduce command-line options to:

*   Specify an input directory other than the current working directory.
*   Define a custom output directory name.
*   Control the level of detail or categories of documentation to generate.
*   Select specific AI models or configurations.

For now, the `spark` command provides a powerful "set it and forget it" mechanism for generating initial drafts of your project's documentation.
