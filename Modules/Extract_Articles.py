import requests
import os
from datetime import date
from bs4 import BeautifulSoup

def get_todays_date():
    return date.today().strftime("%Y_%m_%d")

def create_linksfile_name(newsSourceName):
    today = get_todays_date()
    file_name = f"./{today}-{newsSourceName}\\{today}-{newsSourceName}-links.txt"
    return file_name

def read_links(file_name):
    with open(file_name, 'r') as file:
        links = file.read().split(',')
    return links

def extract_articles(file_name, folder_path, classes_to_exclude=None, ids_to_exclude=None, strings_to_exclude=None):
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
            if paragraphs:
                for paragraph in paragraphs:
                    if any(string in paragraph.getText() for string in strings_to_exclude or []):
                        continue
                    content += paragraph.getText()
                    content += '\n'
                file_name = f"{folder_path}\\{today}_{link.split('/')[-1]}.txt"
                with open(file_name, "w", encoding='utf-8') as f:
                    f.write(content)
        except Exception as e:
            print(f"An error occurred while processing link {link}: {e}")

def extract_all_articles(linkFiles):
    for linkFile in linkFiles:
        extract_articles(linkFile["file_name"], linkFile["folder_path"], linkFile["classes_to_exclude"], linkFile["ids_to_exclude"], linkFile["strings_to_exclude"])