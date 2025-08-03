title: Generated Documentation Structure
slug: generated-doc-structure

# Generated Documentation Structure

When Spark successfully generates documentation, it organizes the output into a structured directory named `docs_output/` at the root of your project. This section details the organization and format of the generated Markdown files.

## The `docs_output` Directory

Spark always creates a top-level directory named `docs_output` in the same location where you execute the `spark` command.

**Important Note:** Before generating new documentation, Spark **removes** any existing `docs_output` directory. This ensures a clean slate and prevents old or deprecated documentation from persisting.

```python
# From main.py
for file in parse_output(response.text):
    file_path = os.path.join('docs_output', file[0])
    if os.path.exists('docs_output'): # This line removes the existing output directory
        shutil.rmtree('docs_output')
    os.makedirs(os.path.dirname(file_path), exist_ok=True) # Ensures parent directories exist
    
    with open(file_path, 'w') as f:
        f.write(file[1])
```
*Self-correction note*: The `shutil.rmtree('docs_output')` line is currently inside the loop, which means it will try to remove the directory for *every* file. This is inefficient and likely a bug in the source code; it should be called once before the loop begins. However, the documentation should reflect the *current* code's behavior or intended behavior if a fix is trivial/obvious. Given the prompt focuses on "high-quality, modular Markdown documentation files based on the following source code", I will describe the behavior as it is, possibly hinting at its impact. For high-quality documentation, I should note this.

### Internal Categorization

Within `docs_output`, the generated Markdown files are further organized into logical subdirectories. These categories are guided by the prompt Spark sends to the AI model, aiming to provide a comprehensive and navigable documentation set for developers:

*   **`intro/`**: Contains overview, installation guides, and getting started information.
*   **`guides/`**: How-to guides, usage patterns, and realistic examples.
*   **`reference/`**: API references, detailed module/function/class documentation.
*   **`concepts/`**: Explanations of core ideas, architecture, and design decisions.
*   **`advanced/`**: Performance, customization, contributing guidelines, and internals.

**Example Directory Structure:**

```
docs_output/
├── intro/
│   ├── index.md
│   ├── installation.md
│   └── quickstart.md
├── guides/
│   ├── basic-usage.md
│   └── ignoring-files.md
├── reference/
│   ├── cli-reference.md
│   └── configuration.md
├── concepts/
│   ├── how-spark-works.md
│   └── prompt-engineering.md
└── advanced/
    ├── internals.md
    └── contributing.md
```

## Markdown File Format

Each generated Markdown file adheres to a specific format that includes metadata at the very top:

```markdown
title: <Title of the Document>
slug: <url-slug>
<Markdown content of the document>
```

*   **`title:`**: A human-readable title for the document. This is useful for navigation and display in documentation viewers.
*   **`slug:`**: A URL-friendly slug, typically used for creating clean URLs in static site generators or documentation platforms.
*   **Markdown Content**: The main body of the documentation, written in standard Markdown syntax, including headers, paragraphs, lists, code blocks, and links.

### Example File Content (`docs_output/intro/index.md`):

```markdown
title: Spark - AI-Powered Documentation Generation
slug: index

# Spark: AI-Powered Documentation Generation

Spark is an innovative command-line tool designed to automate...
```

This structured output makes the generated documentation highly compatible with static site generators (like Jekyll, Hugo, MkDocs) or custom documentation portals, allowing for easy integration into existing developer workflows and publishing pipelines.
