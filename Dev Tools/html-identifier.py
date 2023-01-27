import requests
from bs4 import BeautifulSoup

def find_html_details(url, search_text):
    # Make a GET request to the provided URL
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Use the find_all method to search for the text
    elements = soup.find_all(text=search_text)
    for element in elements:
        # Get the parent element of the text
        parent = element.parent
        # Get the class of the parent element
        element_class = parent.get('class')
        print(f"The text '{search_text}' was found in element of class {element_class} and its html details are:")
        print(parent)

# Example usage
url = 'https://www.defenceconnect.com.au/land-amphibious/11235-uk-to-provide-ukraine-with-main-battle-tanks-10-downing-street-confirms'
search_text = 'Following earlier speculation, a representative from 10 Downing Street has announced that Prime Minister Rishi Sunak had approved the provision of Challenger 2 main battle tanks for Ukraine.'
find_html_details(url, search_text)