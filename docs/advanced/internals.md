title: Spark Internals
slug: internals

# Spark Internals

This document provides a deeper dive into the core components and mechanisms that power Spark. Understanding these internals can be beneficial for debugging, contributing, or simply gaining a better appreciation of how the tool operates.

## `main.py` - The Orchestrator

`main.py` is the heart of Spark, responsible for managing the entire documentation generation pipeline.

### 1. File Inclusion/Exclusion Logic

Before any files are processed, `main.py` attempts to identify which files should be ignored.

```python
# From main.py
ignore = []

if os.path.exists('.sparkignore'):
    with open('.sparkignore', 'r') as f:
        ignore = f.readlines()

elif os.path.exists('.gitignore'):
    with open('.gitignore', 'r') as f:
        ignore = f.readlines()
```

*   **Purpose:** This segment determines the set of file patterns to exclude from being sent to the AI. It prioritizes `.sparkignore` for specific Spark-related exclusions, falling back to `.gitignore` for general version control exclusions.
*   **Usage:** The `ignore` list populated here should ideally be used by `get_local` or a pre-processing step to filter files before their contents are read. The current implementation of `get_local` shown in `main.py` does not explicitly use this `ignore` list during its file traversal, implying that *all* files are read into the prompt regardless of the `ignore` list. For a more robust solution, `get_local` would need to be modified to check each `rel` path against the `ignore` patterns (e.g., using `fnmatch`).

### 2. Source Code Collection (`get_local` and `file_prompt`)

The `get_local` function recursively scans the current directory and its subdirectories to gather file contents.

```python
# From main.py
def file_prompt(path: str, contents: str):
    # Formats a single file's content for the AI prompt
    return f"File: {path}\nContents: ```\n{contents}\n```\n"

def get_local(path: str) -> str:
    prompt = ""
    subs = os.listdir(path) # Lists directory contents

    for sub in subs:
        rel = os.path.join(path, sub)
        if os.path.isdir(rel):
            prompt += get_local(rel) # Recursive call
        else:
            with open(rel, 'r') as f:
                prompt += file_prompt(rel, f.read()) # Read file and format
    return prompt
```

*   **Recursion:** `get_local` effectively creates a flattened representation of the project's source code, with each file clearly delineated.
*   **Concatenation:** All file contents are concatenated into a single string (`prompt`), which forms the dynamic part of the input to the AI.

### 3. AI Output Parsing (`parse_output`)

The AI model's response is a single string that contains multiple Markdown files. The `parse_output` function is crucial for deconstructing this response.

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

*   **Regular Expression:** The `pattern` is specifically designed to match the `File: ... Contents: ```...``` END_FILE` format specified in the prompt. It uses named capture groups (`filePath` and `content`) to easily extract the relevant parts.
*   **Robustness:** `[\s\S]*?` ensures that the `content` group can capture any character, including newlines, and `?` makes it non-greedy, preventing it from consuming text beyond the `END_FILE` delimiter.
*   **Output:** It returns a list of tuples, where each tuple contains the suggested file path and the Markdown content for that file.

### 4. File System Interaction (Output Writing)

The final step in `main.py` is writing the parsed content to the file system.

```python
# From main.py
for file in parse_output(response.text):
    file_path = os.path.join('docs_output', file[0])
    # !!! Critical Note on Potential Bug:
    # shutil.rmtree('docs_output') is called inside the loop.
    # This means for every file processed, it attempts to delete and recreate the entire
    # 'docs_output' directory, leading to inefficiency and potential race conditions
    # or incomplete output if not handled carefully by the OS/Python.
    # It should ideally be called *once* before the loop starts to clear the directory.
    if os.path.exists('docs_output'):
        shutil.rmtree('docs_output')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as f:
        f.write(file[1])
```

*   **Output Directory Management:** The code ensures that the target directory for each file exists (`os.makedirs(..., exist_ok=True)`). The placement of `shutil.rmtree('docs_output')` inside the loop is an observed behavior that should be carefully considered for performance and correctness.
*   **Atomic Writes:** Each file is written individually, ensuring that documentation for one module doesn't interfere with another.

## `install.py` - The Setup Script

The `install.py` script manages the entire setup of Spark on a user's system, ensuring it's self-contained and easily accessible.

### 1. Repository Management

```python
# From install.py
home = os.path.expanduser("~")
spark_dir = os.path.join(home, ".spark")

if not os.path.exists(spark_dir):
    subprocess.run(["git", "clone", "https://github.com/kleo-dev/spark.git", ".spark"], check=True)
else:
    subprocess.run(["git", "-C", spark_dir, "pull"], check=True)
```

*   **Location:** Installs Spark into a hidden directory `~/.spark` to keep the user's home directory clean.
*   **Version Control:** Uses `git clone` for initial installation and `git pull` for updates, ensuring users always have the latest version.

### 2. Virtual Environment Setup

```python
# From install.py
bin_dir = os.path.join(spark_dir, "bin")
venv_dir = os.path.join(spark_dir, "venv")
os.makedirs(bin_dir, exist_ok=True)

if not os.path.exists(os.path.join(venv_dir, "bin", "activate")):
    venv.create(venv_dir, with_pip=True)
```

*   **Isolation:** A Python `venv` (virtual environment) is created within `~/.spark/venv`. This is a best practice to isolate Spark's dependencies (like `google-generativeai`) from the system-wide Python installation, preventing dependency conflicts.
*   **Portability:** Ensures Spark runs with its specific Python environment, making it more reliable across different user systems.

### 3. Dependency Installation

```python
# From install.py
subprocess.run([os.path.join(venv_dir, "bin", "pip"), "install", "--upgrade", "pip"], check=True)
subprocess.run([os.path.join(venv_dir, "bin", "pip"), "install", "google-generativeai"], check=True)
```

*   **`pip` within venv:** Ensures that `google-generativeai` is installed directly into the created virtual environment, rather than globally.

### 4. Executable Wrapper and PATH Configuration

```python
# From install.py
spark_script = os.path.join(bin_dir, "spark")
with open(spark_script, 'w') as f:
    f.write(f"""#!/bin/bash
source "{venv_dir}/bin/activate"
python3 "{os.path.join(spark_dir, 'main.py')}" "$@"
""")
os.chmod(spark_script, 0o755)

path_line = 'export PATH="$HOME/.spark/bin:$PATH"\n'
for rc in os.listdir(home):
    if rc.startswith('.') and rc.endswith('rc') and os.path.isfile(os.path.join(home, rc)):
        rc_path = os.path.join(home, rc)
        # ... logic to add path_line to .bashrc, .zshrc etc.
```

*   **Wrapper Script:** A simple bash script is created at `~/.spark/bin/spark`. This script is critical: it first activates the virtual environment and then executes `main.py` using the Python interpreter from that environment. This ensures Spark always runs with its correct dependencies.
*   **Permissions:** `os.chmod(spark_script, 0o755)` makes the script executable.
*   **PATH Export:** The installer attempts to add `~/.spark/bin` to the user's `PATH` environment variable by modifying common shell configuration files (`.bashrc`, `.zshrc`, etc.). This enables the user to simply type `spark` from any directory.

### 5. API Key Storage

```python
# From install.py
gemini_key = getpass.getpass('Enter your Google Gemini API key: ')
with open(os.path.join(spark_dir, 'keys.py'), 'w') as f:
    f.write(f'API_KEY: str = "{gemini_key}"\n')
```

*   **Secure Input:** Uses `getpass` for secure, non-echoing input of the API key.
*   **Dedicated File:** Stores the key in a separate `keys.py` file within the Spark installation directory (`~/.spark/`), which is then imported by `main.py`.

These internal mechanisms collectively ensure Spark is robust, isolated, and easy for users to install and operate, while leveraging powerful AI for documentation generation.
