title: Managing Your API Key
slug: managing-api-key

# Managing Your API Key

Spark relies on a Google Gemini API key to interact with the generative AI model for documentation generation. This key is crucial for the tool's operation. This guide explains how the API key is handled during installation and how you can manage or update it.

## API Key Storage

During the initial installation process (via `install.py`), Spark prompts you to enter your Google Gemini API key.

```python
# From install.py
gemini_key = getpass.getpass('Enter your Google Gemini API key: ')
with open(os.path.join(spark_dir, 'keys.py'), 'w') as f:
    f.write(f'API_KEY: str = "{gemini_key}"\n')
```

The `install.py` script takes the key you provide and writes it to a file named `keys.py` located within the `~/.spark/` directory (where the Spark repository is cloned).

The `keys.py` file simply contains a single line:

```python
# ~/.spark/keys.py
API_KEY: str = "YOUR_API_KEY_HERE"
```

This approach keeps your API key local to your machine and separate from the main `spark` repository.

## How Spark Uses the Key

The `main.py` script, which is the core logic of Spark, imports this `keys.py` file to access your API key:

```python
# From main.py
import keys
# ...
genai.configure(api_key=keys.API_KEY)
```

By importing `keys`, the `API_KEY` variable becomes available, allowing the `google.generativeai` library to authenticate your requests to the Gemini API.

## Updating or Changing Your API Key

If your API key expires, is revoked, or you simply wish to use a different one, you can update it manually.

1.  **Locate the `keys.py` file:**
    The file is located in your Spark installation directory, typically `~/.spark/keys.py`.

2.  **Edit the file:**
    Open `~/.spark/keys.py` in a text editor and replace the existing API key with your new one:

    ```python
    # ~/.spark/keys.py
    API_KEY: str = "YOUR_NEW_API_KEY_GOES_HERE"
    ```

    Save the file after making the change.

3.  **Run Spark again:**
    The next time you run the `spark` command, it will use the newly updated API key.

## Security Considerations

*   **Keep your API key private:** Never commit `keys.py` (or any file containing sensitive credentials) to a public version control repository. The `install.py` script places `keys.py` inside `~/.spark`, which is outside of your project's typical version control, reducing the risk of accidental exposure.
*   **Revoke compromised keys:** If you suspect your API key has been compromised, revoke it immediately through the [Google AI Studio](https://ai.google.dev/) and generate a new one.
*   **Environment variables (future consideration):** For more robust and widely adopted security practices, especially in CI/CD environments, storing API keys as environment variables (`export API_KEY=...`) is often preferred. While Spark currently relies on `keys.py`, future versions might offer environment variable support.
