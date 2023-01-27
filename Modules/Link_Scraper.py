import os
import requests
import re
from datetime import date
from bs4 import BeautifulSoup

'''
This function gets all the links from the Defence Connect website
Parameter: url - the url of the Defence Connect website
    For example, "https://www.defenceconnect.com.au/land-amphibious"
Parameter: subDirectoryRegexMatch - the regex match for the subdirectory. 
    This parameter is to account for the nuances between News Websites url paths
    For example, "/land-amphibious/\d+" will match all the links in the subdirectory "/land-amphibious/" that end with a number 
Parameter: filterString - the link will be rejected if it contains this string in the URL
    This parameter is to filter out links that are not articles
    For example, ""#ccomment-content-" will reject all the links that contain "#ccomment-content-"
    
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
This function saves the links to a text file seperated by commas
Parameter: links - the list of links to save
    This parameter will likely be passed a list of links that were scraped by the get_links function programatically.
Parameter: newsSourceName - the name of the news source.
    This parameter is used to create the folder and file name. It is also used to create the folder name.
    It exists to place different news sources in different folders.
    For example: "Defence_Connect" may name the folder "2022_12_31-Defence_Connect" and the link file "2022_12_31-Defence_Connect-links.txt"
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
This function scrapes all the links from a list of urls and saves them to a text file
The list of urls is a list of tuples. Each tuple should contain the url, subDirectoryRegexMatch, filterString, and newsSourceName
The url is the url of the website to scrape. The subDirectoryRegexMatch is the regex match for the subdirectory. 
The filterString is the string to filter out links that are not articles. The newsSourceName is the name of the news source which defines the name of the folders and files.
'''
def scrape_all_urls(urls):
    for url in urls:
        links = get_links(url=url['url'], subDirectoryRegexMatch=url['subDirectoryRegexMatch'], filterString=url['filterString'])
        save_links(links, newsSourceName=url['newsSourceName'], parentURL=url['parentURL'])
        
        
