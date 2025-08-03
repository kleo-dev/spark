title: Ignoring Files and Directories
slug: ignoring-files

# Ignoring Files and Directories

When Spark analyzes your codebase, it's crucial to control which files and directories are included in the context sent to the AI model. This prevents sending irrelevant data (e.g., build artifacts, virtual environments, large datasets, or sensitive files) and focuses the AI on the actual source code. Spark achieves this by integrating with standard ignore file mechanisms.

## How Spark Handles Ignored Files

Spark prioritizes ignore rules in the following order:

1.  **`.sparkignore`:** If a file named `.sparkignore` exists in the root directory where you run the `spark` command, Spark will read and apply the patterns listed in this file. This provides a dedicated way to control what Spark sees, independent of your version control.
2.  **`.gitignore`:** If no `.sparkignore` file is found, Spark will fall back to reading your project's `.gitignore` file. This is a common and convenient scenario, as most projects already have a well-maintained `.gitignore`.

The `main.py` script's logic explicitly checks for these files:

```python
ignore = []

if os.path.exists('.sparkignore'):
    with open('.sparkignore', 'r') as f:
        ignore = f.readlines()

elif os.path.exists('.gitignore'):
    with open('.gitignore', 'r') as f:
        ignore = f.readlines()
```

The contents of the chosen ignore file are loaded into the global `ignore` list. Although the provided code snippet shows `get_local` not directly using the `ignore` list for filtering during traversal, the intent of Spark's design would be for this list to be used to filter files *before* they are sent to the AI. In a more complete implementation, the `get_local` function (or a pre-processing step) would apply these `ignore` patterns. For example, the `os.listdir` loop within `get_local` would typically check if `sub` matches any `ignore` pattern before proceeding.

### Example `.sparkignore` / `.gitignore`

The syntax for `.sparkignore` is the same as `.gitignore`. Each line represents a pattern:

```
# Ignore specific files
.env
keys.py
my_secret_config.json

# Ignore directories
node_modules/
dist/
build/
__pycache__/
venv/
docs_output/ # Prevent Spark from re-processing its own output

# Ignore files by extension
*.log
*.tmp
```

## Best Practices

*   **Start with `.gitignore`:** For most projects, your existing `.gitignore` will be sufficient. This simplifies setup as you don't need a separate configuration.
*   **Use `.sparkignore` for Fine-Grained Control:** If you need to exclude files specifically for documentation generation that you *do* want to keep in version control, create a `.sparkignore`. For instance, you might want to ignore specific large datasets or test fixture files that are part of your repository but not relevant for documentation context.
*   **Exclude `docs_output/`:** It's highly recommended to add `docs_output/` to your `.gitignore` or `.sparkignore` to prevent Spark from trying to document its own output, which could lead to redundant or circular content.
*   **Review Sensitive Information:** Always review the files that will be processed by Spark to ensure no sensitive data (API keys, credentials, PII) is inadvertently included and sent to the LLM. While `keys.py` is ignored by the installer, other sensitive files in your project should also be excluded.
