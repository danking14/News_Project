from Modules.Link_Scraper import scrape_all_urls
from Modules.Extract_Articles import extract_all_articles
from Modules.OpenAI_Summarisation import summarize_all_articles
from Modules.OpenAI_Summarisation import get_API_key
from Modules.Summary_To_HTML import process_all_files
import time
from datetime import date
import traceback
today = date.today().strftime("%Y_%m_%d")

GlobalConfiguration = {
    "apiKey": get_API_key("OpenAI_APIKey.txt")
}

DefenceConnectConfiguration = {
    "classes_to_exclude": ["row3-container", "b-article__intro"],
    "ids_to_exclude": ["photogalleries", "latest-jobs", "majorprojects"],
    "strings_to_exclude": ["Get notifications in real-time for staying up to date with content that matters to you.", "Already have an account? Sign in below:", "Subscribe to the Defence Connect daily newsletter. Be the first to hear the latest developments in the defence industry.", "More to follow"],
    "parentURL": "https://www.defenceconnect.com.au",
    "headline_tag": ".b-article__title", #append with . if class or # if id. For example, ".b-article__title" or "#b-article__title"
}

GoAutoConfiguration = {
    "classes_to_exclude": None,
    "ids_to_exclude": None,
    "strings_to_exclude": None,
    "parentURL": "https://www.goauto.com.au/",
    "headline_tag": "#article_lead"
}

DefenceConnectLand = {
    "url": "https://www.defenceconnect.com.au/land-amphibious",
    "subDirectoryRegexMatch": "/land-amphibious/\d+",
    "filterString": "#ccomment-content-",
    "newsSourceName": "land-amphibious",
    "classes_to_exclude": DefenceConnectConfiguration["classes_to_exclude"],
    "ids_to_exclude": DefenceConnectConfiguration["ids_to_exclude"],
    "strings_to_exclude": DefenceConnectConfiguration["strings_to_exclude"],
    "folder_path": f"./{today}-land-amphibious",
    "file_name": f"{today}-land-amphibious\\{today}-land-amphibious-links.txt",
    "parentURL": DefenceConnectConfiguration["parentURL"],
    "apiKey": GlobalConfiguration["apiKey"],
    "headline_tag": DefenceConnectConfiguration["headline_tag"],
    "file_path": f"./{today}-land-amphibious\\{today}-summary.txt",
    "output": f"{today}-land-amphibious\\{today}-land-amphibious-output.html"
}
DefenceConnectIntelCyber = {
    "url": "https://www.defenceconnect.com.au/intel-cyber",
    "subDirectoryRegexMatch": "intel-cyber/\d+",
    "filterString": "#ccomment-content-",
    "newsSourceName": "intel-cyber",
    "classes_to_exclude": DefenceConnectConfiguration["classes_to_exclude"],
    "ids_to_exclude": DefenceConnectConfiguration["ids_to_exclude"],
    "strings_to_exclude": DefenceConnectConfiguration["strings_to_exclude"],
    "folder_path": f"./{today}-intel-cyber",
    "file_name": f"{today}-intel-cyber\\{today}-intel-cyber-links.txt",
    "parentURL": DefenceConnectConfiguration["parentURL"],
    "apiKey": GlobalConfiguration["apiKey"],
    "headline_tag": DefenceConnectConfiguration["headline_tag"],
    "file_path": f"./{today}-intel-cyber\\{today}-summary.txt",
    "output": f"{today}-intel-cyber\\{today}-intel-cyber-output.html"
}

DefenceConnectStrikeAirCombat = {
    "url": "https://www.defenceconnect.com.au/strike-air-combat",
    "subDirectoryRegexMatch": "strike-air-combat/\d+",
    "filterString": "#ccomment-content-",
    "newsSourceName": "strike-air-combat",
    "classes_to_exclude": DefenceConnectConfiguration["classes_to_exclude"],
    "ids_to_exclude": DefenceConnectConfiguration["ids_to_exclude"],
    "strings_to_exclude": DefenceConnectConfiguration["strings_to_exclude"],
    "folder_path": f"./{today}-strike-air-combat",
    "file_name": f"{today}-strike-air-combat\\{today}-strike-air-combat-links.txt",
    "parentURL": DefenceConnectConfiguration["parentURL"],
    "apiKey": GlobalConfiguration["apiKey"],
    "headline_tag": DefenceConnectConfiguration["headline_tag"],
    "file_path": f"./{today}-strike-air-combat\\{today}-summary.txt",
    "output": f"{today}-strike-air-combat\\{today}-strike-air-combat-output.html"
}

GoAutoNews = {
    "url": "https://www.goauto.com.au/news",
    "subDirectoryRegexMatch": None,
    "filterString": None,
    "newsSourceName": "go-auto-news",
    "classes_to_exclude": GoAutoConfiguration["classes_to_exclude"],
    "ids_to_exclude": GoAutoConfiguration["ids_to_exclude"],
    "strings_to_exclude": GoAutoConfiguration["strings_to_exclude"],
    "folder_path": f"./{today}-go-auto-news",
    "file_name": f"{today}-go-auto-news\\{today}-go-auto-news-links.txt",
    "parentURL": GoAutoConfiguration["parentURL"],
    "apiKey": GlobalConfiguration["apiKey"]
}


dictionary = [GoAutoNews]

try:
     scrape_all_urls(dictionary)
except Exception as e:
    with open("error.txt", "a", encoding='utf8') as f:
        f.write("Error in running scrape_all_urls :")
        f.write(traceback.format_exc())



extract_all_articles(dictionary)

# summarize_all_articles(dictionary)

# process_all_files(dictionary)