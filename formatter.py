import os
import re
import subprocess


def format_markdown_cpp_files(directory):
    markdown_files = [f for f in os.listdir(directory) if f.endswith(".md")]

    for filename in markdown_files:
        filepath = os.path.join(directory, filename)
        print(f"formatting {filepath}")

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        cpp_blocks = re.findall(r"```cpp(.*?)```", content, re.DOTALL)

        if cpp_blocks:
            formatted_blocks = []
            for block in cpp_blocks:
                formatted_block = subprocess.check_output(
                    ["clang-format"], input=block, text=True
                )
                formatted_blocks.append(formatted_block)

            new_content = content
            for original, formatted in zip(cpp_blocks, formatted_blocks):
                new_content = new_content.replace(
                    f"```cpp{original}```", f"```cpp{formatted}```"
                )

            with open(filepath, "w", encoding="utf-8") as file:
                file.write(new_content)


def list_directories_and_files(path, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = [".git"]

    for root, dirs, _ in os.walk(path):
        dirs[:] = [
            d
            for d in dirs
            if os.path.join(root, d)
            not in (os.path.join(path, d) for d in exclude_dirs)
        ]

        for dir in dirs:
            format_markdown_cpp_files(root + "/" + dir)


current_path = os.getcwd()
exclude_dirs = [
    ".git",
    ".svn",
    ".github",
    "_exts",
    "_static",
    "_templates",
    "__pycache__",
    "_tmp",
]
list_directories_and_files(current_path + "/" + "docs", exclude_dirs)
