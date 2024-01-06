import os
import sys

dirhtml = sys.argv[1]
html_list = []


def collect_html(path):
    for item in os.listdir(path):
        new_path = path + "/" + item
        if os.path.isdir(new_path):
            collect_html(new_path)
        else:
            _, ext = os.path.splitext(new_path)
            if ext == ".html":
                html_list.append(new_path)


print("dirhtml: ", dirhtml)
collect_html(dirhtml)
for html_file in html_list:
    html_content = ""
    with open(html_file, "r", encoding="UTF-8") as f:
        html_content_lines = f.readlines()
        for line in html_content_lines:
            html_content += line
    if html_content.find("div.section") != -1:
        print("Processing: " + html_file)
        html_content = html_content.replace("div.section", "div>section")
        with open(html_file, "w", encoding="UTF-8") as f:
            f.write(html_content)
    with open(html_file, "r", encoding="UTF-8") as f:
        print(f.readlines())
