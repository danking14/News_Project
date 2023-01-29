import re
import os

"""
This function splits a text file into a list of articles. This is passed to the process_file function.
The file_path argument is the path of the file to split, which is the summary file created by the OpenAI Summarisation module.
"""
def get_articles_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        articles = text.split("ARTICLE_DELIMITER")
    return articles

"""
The function processes the summary articles and converts them to HTML.
The file_path argument is the path of the file to split, which is the summary file created by the OpenAI Summarisation module.
The output argument is the path of the file to save the HTML to.
"""
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
                processed_lines.append("<h3>" + line + "</h3>")
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
        

"""
This function processes all the files in the options list. This list is passed to the function from the Email_Creator.py module.
A dictionary is passed to the function for each file to process. The dictionary contains the following relevant keys:
Key: file_path - the path of the file to split, which is the summary file created by the OpenAI Summarisation module.
Key: output - the path of the file to save the HTML to.
"""

def process_all_files(options):
    for option in options:
        process_file(option["file_path"], option["output"])

