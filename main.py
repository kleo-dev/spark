import keys
import src_code
import output_parser
import os
import shutil
import google.generativeai as genai

prompt = """You are a senior software engineer tasked with documenting a Rust project.
Your output must be structured as follows for each generated documentation file:

File: <path/to/documentation/file.md>
Contents: ```
---
title: <Doc title>
slug: <doc/slug>
---
<Markdown content for the documentation file>
```
END_FILE

Generate the clear and understandable Markdown documentation based on the following source code:
"""

prompt += src_code.get_local('')

genai.configure(api_key=keys.API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content(prompt)
print(response.text)
print('---------------')

for file in output_parser.parse_output(response.text):
    file_path = os.path.join('docs_output', file[0])
    if os.path.exists('docs_output'):
        shutil.rmtree('docs_output')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as f:
        f.write(file[1])