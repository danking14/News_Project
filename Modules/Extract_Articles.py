import requests
import os
from datetime import date
from bs4 import BeautifulSoup

def get_todays_date():
    return date.today().strftime("%Y_%m_%d")
'''
This function identifies the name of the links file which is standardised to be in the format: {today}-{newsSourceName}-links.txt
'''
def create_linksfile_name(newsSourceName):
    today = get_todays_date()
    file_name = f"./{today}-{newsSourceName}\\{today}-{newsSourceName}-links.txt"
    return file_name
'''
This function reads the links from a text file and returns them as a list of strings separated by commas.
This gets passed to the extract_articles and extract_headline function.
'''
def read_links(file_name):
    with open(file_name, 'r') as file:
        links = file.read().split(',')
    return links
'''
This function extracts the headlines from the links and stores it for the extract_articles function.
Argument: link - the link to extract the headlines from. Passed from the read_links function.
Headline_tag - the tag of the headline to extract from the page. Passed from the extract_articles function.
'''
def extract_headline(link, headline_tag):
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding='utf-8')
        if headline_tag.startswith("."):
            headlines = soup.find_all(class_=headline_tag[1:])
        elif headline_tag.startswith("#"):
            headlines = soup.find_all(id=headline_tag[1:])
        elif headline_tag.startswith("h"):
            headlines = soup.find_all(headline_tag)
        else:
            headlines = soup.find_all(class_=headline_tag)
        if headlines:
            return [headline.get_text() for headline in headlines]
        else:
            raise ValueError(f"No element with the {headline_tag} was found on the page")
    except Exception as e:
        print(f"An error occurred while processing link {link}: {e}")


'''
This function extracts the articles from the links and saves them to a text file.
It takes the following arguments:
Argument: file_name - the name of the links file.
Argument: folder_path - the path of the folder to save the articles to.
Argument: classes_to_exclude - a list of classes to exclude from the articles.
Argument: ids_to_exclude - a list of ids to exclude from the articles.
Argument: strings_to_exclude - a list of strings to exclude from the articles.
Argument: headline_tag - the tag of the headline to extract from the page.
The output is a text file with the name: {today}-{newsSourceName}-articles.txt containing the articles 
Each article is separated by the string "ARTICLE_DELIMITER", which is used by the Summary_To_HTML module to separate the articles.
'''
def extract_articles(file_name, folder_path, classes_to_exclude=None, ids_to_exclude=None, strings_to_exclude=None, headline_tag=None):
    today = date.today().strftime("%Y_%m_%d")
    with open(file_name, 'r', encoding='utf-8') as file:
        links = file.read().split(',')
    for link in links:
        try:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser', from_encoding='utf-8')
            
            for a in soup.find_all('a'):
                a.unwrap()
            
            for exclude_class in classes_to_exclude or []:
                for div in soup.find_all(class_=exclude_class):
                    for p in div.find_all("p"):
                        p.decompose()
                        
            for exclude_id in ids_to_exclude or []:
                for div in soup.find_all(id=exclude_id):
                    for p in div.find_all("p"):
                        p.decompose()

            paragraphs = soup.find_all('p')
            content = ''
            headline = extract_headline(link, headline_tag)
            content += f"HEADLINE: {headline}\n"

            if paragraphs:
                for paragraph in paragraphs:
                    if any(string in paragraph.getText() for string in strings_to_exclude or []):
                        continue
                    content += paragraph.getText()
                    content += '\n'
                content += '\n'
                content += link
                file_name = f"{folder_path}\\{today}_{link.split('/')[-1]}.txt"
                with open(file_name, "w", encoding='utf-8') as f:
                    f.write(content)
        except Exception as e:
            print(f"An error occurred while processing link {link}: {e}")

'''
Normally, this function is called from the Email_Creator.py module.
It is passed a list of dictionaries, each dictionary containing the following keys:
Key: file_name - the name of the links file.
Key: folder_path - the path of the folder to save the articles to.
Key: classes_to_exclude - a list of classes to exclude from the articles.
Key: ids_to_exclude - a list of ids to exclude from the articles.
Key: strings_to_exclude - a list of strings to exclude from the articles.
Key: headline_tag - the tag of the headline to extract from the page.
'''
def extract_all_articles(linkFiles):
    for linkFile in linkFiles:
        extract_articles(linkFile["file_name"], linkFile["folder_path"], linkFile["classes_to_exclude"], linkFile["ids_to_exclude"], linkFile["strings_to_exclude"], linkFile["headline_tag"])