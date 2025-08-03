title: How Spark Works
slug: how-spark-works

# How Spark Works: An Architectural Overview

Spark operates as a bridge between your codebase and a generative AI model, streamlining the documentation process. Its core functionality involves preparing your source code for the AI, interacting with the model, and then processing the AI's response into structured Markdown files.

## The Workflow in Detail

The `main.py` script orchestrates the entire documentation generation process. Here's a step-by-step breakdown of its internal workflow:

```mermaid
graph TD
    A[Start Spark] --> B{Check .sparkignore or .gitignore};
    B --> C[Read Ignore Patterns];
    C --> D[Scan Project Directory Recursively];
    D --> E{For Each File:};
    E --> F{Read File Content};
    F --> G[Format File for Prompt];
    G --> H[Append to Main Prompt];
    H --> I[Configure Gemini API];
    I --> J[Send Prompt to Generative AI];
    J --> K[Receive AI Response];
    K --> L[Parse AI Output into File Segments];
    L --> M{For Each File Segment:};
    M --> N[Clear Existing docs_output (first segment only)];
    N --> O[Create Output Directory Structure];
    O --> P[Write Markdown File];
    P --> Q[End Spark];
```

### 1. Source Code Collection (`get_local` function)

The process begins by gathering all relevant source code files from your project.

```python
# From main.py
def file_prompt(path: str, contents: str):
    return f"File: {path}\nContents: ```\n{contents}\n```\n"

def get_local(path: str) -> str:
    prompt = ""
    subs = os.listdir(path)

    for sub in subs:
        rel = os.path.join(path, sub)
        if os.path.isdir(rel):
            prompt += get_local(rel) # Recursively call for subdirectories
        else:
            with open(rel, 'r') as f:
                prompt += file_prompt(rel, f.read())

    return prompt
```

*   **Recursion:** The `get_local` function recursively traverses the file system starting from the current directory. This ensures all files within subdirectories are also considered.
*   **File Formatting:** For each file identified, its full path and content are formatted using the `file_prompt` helper function. This structured format helps the AI clearly distinguish between different files and their content.
*   **Ignoring Files:** Before adding files to the prompt, Spark checks for `.sparkignore` or `.gitignore` files at the project root. While the provided `get_local` doesn't explicitly filter files based on the `ignore` list *during traversal*, the design intent is to use these patterns to prevent irrelevant or sensitive files from being included in the final prompt sent to the AI.

### 2. Prompt Construction

Once all relevant file contents are collected, they are appended to a predefined prompt template. This template serves as the primary instruction set for the generative AI.

```python
# From main.py (simplified)
prompt = """title: <Title of the Document>
slug: <url-slug>
<Markdown content of the document> ``` END_FILE

Guidelines:
    Organize the documentation into logical categories such as:
        intro/ - Overview, installation, getting started
        guides/ - How-to guides, usage patterns, real-world examples
        reference/ - API reference, detailed module/function/class docs
        concepts/ - Explanations of core ideas, architecture, and design decisions
        advanced/ - Performance, customization, contributing, and internals
    Write for a developer audience. Use precise, professional language and explain why things work the way they do—not just how.
    Be helpful, not verbose. Use clear headers, short paragraphs, bullet points, and examples.
    Where relevant, include:
        Code samples and explanations
        Links to related documents
        Realistic usage scenarios

Generate high-quality, modular Markdown documentation files based on the following source code:
"""
prompt += get_local('.') # Appends all collected source code
```

The prompt defines the desired output format (title, slug, Markdown) and provides explicit guidelines for the AI on content organization, tone, and what to include. This "prompt engineering" is critical for guiding the AI to produce high-quality, relevant documentation.

### 3. AI Interaction

Spark then sends this comprehensive prompt to the configured Google Generative AI model.

```python
# From main.py
genai.configure(api_key=keys.API_KEY) # Authenticates with the API key
model = genai.GenerativeModel('gemini-2.5-flash') # Initializes the model
response = model.generate_content(prompt) # Sends the prompt and gets a response
print(response.text)
```

Spark uses the `gemini-2.5-flash` model, chosen likely for its balance of speed and quality. The `generate_content` call is where the AI processes the provided source code and generates the documentation.

### 4. Output Parsing (`parse_output` function)

The AI's response is a single, large string containing multiple generated Markdown files, each delimited by a specific pattern. Spark uses a regular expression to extract these individual files.

```python
# From main.py
pattern = r"File: (?P<filePath>.*?)\nContents: ```(?:\n|)(?P<content>[\s\S]*?)```\nEND_FILE"

def parse_output(input: str) -> list[tuple[str, str]]:
    output = []
    for match in re.finditer(pattern, input):
        file_path = match.group("filePath")
        content = match.group("content")
        output.append((file_path, content))
    return output
```

This `parse_output` function is robust enough to identify each file's path and its corresponding Markdown content, even if there are newlines or varied whitespace within the content.

### 5. Writing Documentation Files

Finally, Spark takes the parsed file paths and content and writes them to the local file system.

```python
# From main.py
for file in parse_output(response.text):
    file_path = os.path.join('docs_output', file[0])
    # Bug: shutil.rmtree('docs_output') is called inside the loop.
    # It should ideally be called once before the loop to clear output cleanly.
    if os.path.exists('docs_output'):
        shutil.rmtree('docs_output')
    os.makedirs(os.path.dirname(file_path), exist_ok=True) # Ensures parent directories exist
    
    with open(file_path, 'w') as f:
        f.write(file[1])
```

*   **`docs_output` Management:** Spark first attempts to remove the `docs_output` directory (though, as noted, the current placement in the loop means it will re-remove it for *every* file, which is inefficient and might have unintended side effects if not carefully managed). Then, it ensures that all necessary parent directories (e.g., `docs_output/intro/`) exist before writing the file.
*   **File Writing:** Each extracted Markdown content block is written to its designated file path within the `docs_output` structure.

This comprehensive workflow ensures that Spark efficiently transforms raw source code into organized, AI-generated documentation.
