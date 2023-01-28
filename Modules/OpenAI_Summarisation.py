'''
The purpose of this function is to scrape the links from a list of urls and save them to a text file.
It takes the following arguments:
Argument: folder_path - the path to the folder where the links are saved
Argument: apiKey - the API key for the OpenAI API
'''
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
                    last_line = lines[-1] #This is the last line of the file.
                    link = last_line.strip() #The link is the last line of the file. We reuse this link below.
                    noLinkArticle = lines[:-1] #This is everything except the last line of the file.
                    article = ''.join(map(str,noLinkArticle)) #This joins the list of lines into a string. OpenAI seems to prefer a single string.
                    print(article)
                    prompt = f"Can you summarise this news article into five key points. The points should be numbered. Here is the article: {article}"
                    summary = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=1000, api_key=apiKey)
                    f.write(f"\n\n{filename}\n\n")
                    print(summary.choices[0].text)
                    f.write(summary.choices[0].text)
                    f.write(f"\n\n{link}\n\n") #This adds the link to the end of the summary.
                    time.sleep(5)
                    # done_files += 1
                    # print(f"{done_files} out of {total_files} files have been done.")
    print("Summary file created at: ", summary_file)

    

def summarize_all_articles(options):
    for option in options:
        summarize_articles(option["folder_path"], option["apiKey"])

