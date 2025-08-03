import re
import os

pattern = r"File: (?P<filePath>.*?)\nContents: ```(?:\n|)(?P<content>[\s\S]*?)```\nEND_FILE"

def parse_output(input: str) -> list[tuple[str, str]]:
    output = []

    for match in re.finditer(pattern, input):
        file_path = match.group("filePath")
        content = match.group("content")
        output.append((file_path, content))

    return output
