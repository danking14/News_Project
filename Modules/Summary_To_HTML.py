import re
import os

def get_articles_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        articles = text.split("ARTICLE_DELIMITER")
    return articles

def process_file(file_path, output):
    articles = get_articles_from_file(file_path)
    processed_articles = []
    for article in articles:
        lines = article.split("\n")
        processed_lines = []
        for line in lines:
            line = line.replace("ARTICLE DELIMITER", "")
            if line.startswith("HEADLINE"):
                line = line[8:]
                line = line.replace("[", "")
                line = line.replace("]", "")
                line = line.replace("'", "")
                line = line.replace(":", "")
                processed_lines.append("<h1>" + line + "</h1>")
                processed_lines.append("<ol>")
            elif line.startswith("-"):
                processed_lines.append("<li>" + line[2:] + "</li>")
            elif line.startswith("https"):
                processed_lines.append("</ol>")
                processed_lines.append("<a href='" + line + "'>" + line + "</a>")
            else:
                processed_lines.append(line)
        processed_articles.append("\n".join(processed_lines))
    final_text = "<html>\n<body>\n" + "\n".join(processed_articles) + "\n</body>\n</html>"
    if not os.path.exists(output):
        open(output, 'w')
    with open(output, 'w', encoding='utf-8') as out:
        out.write(final_text)


def process_all_files(options):
    for option in options:
        process_file(option["file_path"], option["output"])

