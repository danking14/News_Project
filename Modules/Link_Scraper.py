import os
import requests
import re
from datetime import date
from bs4 import BeautifulSoup

'''
This function scrapes all the links from a url and returns them as a list of strings.
Argument: url - the url of the website to scrape.
Argument: subDirectoryRegexMatch - the regex to match the subdirectory of the links.
Argument: filterString - the string to filter out of the links.  
'''
def get_links(url, subDirectoryRegexMatch=None, filterString=None):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = set()
    for link in soup.find_all("a", href=re.compile(subDirectoryRegexMatch)):
        links.add(link.get("href"))
    filtered_links = [link for link in links if filterString not in link]
    return filtered_links

'''
This function saves a list of links to a text file.
Argument: links - the list of links to save.
Argument: newsSourceName - the name of the news source which defines the name of the folders and files.
Argument: parentURL - the parent url of the links. This is used to add the parent url to the links before saving them.
'''
def save_links(links, newsSourceName, parentURL):
    today = date.today().strftime("%Y_%m_%d")
    folder_path = f"./{today}-{newsSourceName}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = f"./{today}-{newsSourceName}\\{today}-{newsSourceName}-links.txt"
    # convert links to a set to remove duplicates
    links = set(links)
    try:
        with open(file_name, "w", encoding='utf8') as f:
            f.write(",".join([parentURL + link for link in links]))
        print(f"Links saved to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving the links to {file_name}: {e}")

'''
This function scrapes all the links from a list of websites and saves them to a text file.
Normally, this function is called from the Email_Creator.py module.
It is passed a list of dictionaries, each containing the url, subDirectoryRegexMatch, filterString, newsSourceName and parentURL.
'''
def scrape_all_urls(urls):
    for url in urls:
        links = get_links(url=url['url'], subDirectoryRegexMatch=url['subDirectoryRegexMatch'], filterString=url['filterString'])
        save_links(links, newsSourceName=url['newsSourceName'], parentURL=url['parentURL'])
        
        
