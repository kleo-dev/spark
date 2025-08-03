import keys
import os
import shutil
import google.generativeai as genai
import re

ignore = []

if os.path.exists('.sparkignore'):
    with open('.sparkignore', 'r') as f:
        ignore = f.readlines()

elif os.path.exists('.gitignore'):
    with open('.gitignore', 'r') as f:
        ignore = f.readlines()

def file_prompt(path: str, contents: str):
    return f"File: {path}\nContents: ```\n{contents}\n```\n"

def get_local(path: str) -> str:
    prompt = ""
    subs = os.listdir(path)

    for sub in subs:
        rel = os.path.join(path, sub)
        if os.path.isdir(rel):
            get_local(rel)
        else:
            with open(rel, 'r') as f:
                prompt += file_prompt(rel, f.read())

    return prompt

pattern = r"File: (?P<filePath>.*?)\nContents: ```(?:\n|)(?P<content>[\s\S]*?)```\nEND_FILE"

def parse_output(input: str) -> list[tuple[str, str]]:
    output = []

    for match in re.finditer(pattern, input):
        file_path = match.group("filePath")
        content = match.group("content")
        output.append((file_path, content))

    return output

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

prompt += get_local('.')

genai.configure(api_key=keys.API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content(prompt)
print(response.text)
print('---------------')

for file in parse_output(response.text):
    file_path = os.path.join('docs_output', file[0])
    if os.path.exists('docs_output'):
        shutil.rmtree('docs_output')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as f:
        f.write(file[1])
