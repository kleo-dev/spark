# This module takes the source code, either local or a repo and returns a prompt

import os

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

# TODO: Add a repository option, by default only do local