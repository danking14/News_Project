def get_API_key(APIKey):
    """ Given a OpenAIAPIKey.txt,
        return the contents of that file
    """
    try:
        with open(APIKey, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % APIKey)

def summarize_articles(folder_path, apiKey):
    """
    This function takes a folder path and an API key and uses the OpenAI API to summarise the articles in the folder.
    Argument: folder_path: The path to the folder containing the articles to be summarised.
    Argument: apiKey: The API key for the OpenAI API.
    """
    import os
    import openai
    from datetime import date
    import time

    openai.api_key = apiKey
    today = date.today().strftime("%Y_%m_%d")
    summary_file = f"{folder_path}\\{today}-summary.txt"

    print("Summarising dot points using OpenAI API now...")
    with open(summary_file, "a", encoding='utf8') as f:
        # total_files = len([name for name in os.listdir(folder_path) if name.endswith(".txt") and '-links' not in name and '-summary' not in name])
        # done_files = 0
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if filepath.endswith(".txt") and '-links' not in filename and '-summary' not in filename:
                with open(filepath, 'r', encoding='utf8') as g:
                    lines = g.readlines() #The next few lines are to get the last line of the file which is the link. The rest of the lines are the article.
                    first_line = lines[0] #This is the first line of the file.
                    headline = first_line.strip() #The headline is the first line of the file. We reuse this headline below.
                    last_line = lines[-1] #This is the last line of the file.
                    link = last_line.strip() #The link is the last line of the file. We reuse this link below.
                    noLinkArticle = lines[:-1] #This is everything except the last line of the file.
                    article = ''.join(map(str,noLinkArticle)) #This joins the list of lines into a string. OpenAI seems to prefer a single string.
                    print(article)
                    prompt = f"Can you summarise this news article into five key points. The points should be tagged with a hyphen and space. Like this: - Point 1. Here is the article: {article}"
                    summary = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=1000, api_key=apiKey)
                    print(headline)
                    print(summary.choices[0].text)
                    f.write(f"{headline}")
                    f.write(summary.choices[0].text)
                    f.write(f"\n\n{link}\n\n") #This adds the link to the end of the summary.
                    f.write(f"\n\nARTICLE DELIMITER\n\n")
                    time.sleep(5)
                    # done_files += 1
                    # print(f"{done_files} out of {total_files} files have been done.")
    print("Summary file created at: ", summary_file)

"""
This function summarises all the articles in a folder. It outputs a summary file with the date in the name.
This function is normally called from the Email_Creator.py file.
It gets passed a list of dictionaries. Each dictionary contains the folder path and the API key.
"""
def summarize_all_articles(options):
    for option in options:
        summarize_articles(option["folder_path"], option["apiKey"])

