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


print("Enter directory", dirhtml)
collect_html(dirhtml)
match_pages = [
    dirhtml + "/" + "theory/operating-system/callgraph.html",
    dirhtml + "/" + "script/plantuml.html",
]

js_code = """
document.querySelector("div.bd-sidebar-secondary").classList.add("hide");
"""

for html_file in html_list:
    if html_file not in match_pages:
        continue

    with open(html_file, "r", encoding="UTF-8") as f:
        html_content = f.read()

    if '<footer class="bd-footer">' in html_content and "</footer>" in html_content:
        print("Processing: " + html_file)

        start_index = html_content.find('<footer class="bd-footer">')
        end_index = html_content.find("</footer>", start_index) + len("</footer>")

        script_tag = "<script>{}</script>".format(js_code)
        modified_html = (
            html_content[:end_index] + "\n" + script_tag + html_content[end_index:]
        )

        with open(html_file, "w", encoding="UTF-8") as f:
            f.write(modified_html)
