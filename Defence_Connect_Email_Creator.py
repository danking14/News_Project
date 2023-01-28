from Modules.Link_Scraper import scrape_all_urls
from Modules.Extract_Articles import extract_all_articles
from Modules.OpenAI_Summarisation import summarize_all_articles
import time
from datetime import date
import traceback
today = date.today().strftime("%Y_%m_%d")
GlobalConfiguration = {
    "apiKey" : "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"
}

DefenceConnectConfiguration = {
    # "col-md-8", "col-md-12", "col-sm-12", "col-xs-12", "jobsidebar", "footer-cointaner", "b-sidebarevents__title", "b-article__intro"
    "classes_to_exclude": ["row3-container", "b-article__intro"],
    # "photogalleries", "latest-jobs", "majorprojects"
    "ids_to_exclude": ["photogalleries", "latest-jobs", "majorprojects"],
    "strings_to_exclude": ["Get notifications in real-time for staying up to date with content that matters to you.", "Already have an account? Sign in below:", "Subscribe to the Defence Connect daily newsletter. Be the first to hear the latest developments in the defence industry.", "More to follow"],
    "parentURL": "https://www.defenceconnect.com.au"
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
    "apiKey": GlobalConfiguration["apiKey"]
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
    "apiKey": GlobalConfiguration["apiKey"]}

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
    "apiKey": GlobalConfiguration["apiKey"]
}
# file_name, folder_path, classes_to_exclude=None, ids_to_exclude=None, strings_to_exclude=None
dictionary = [DefenceConnectLand, DefenceConnectStrikeAirCombat]

try:
    scrape_all_urls(dictionary)
except Exception as e:
    with open("error.txt", "a", encoding='utf8') as f:
        f.write("Error in running scrape_all_urls :")
        f.write(traceback.format_exc())

# Need to allow some time to scrape links
time.sleep(3)

extract_all_articles(dictionary)

# Need to allow some time to scrape articles
time.sleep(6)

summarize_all_articles(dictionary)
