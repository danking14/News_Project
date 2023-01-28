'''
The purpose of this function is to scrape the links from a list of urls and save them to a text file.
It takes the following arguments:
Argument: folder_path - the path to the folder where the links are saved
Argument: apiKey - the API key for the OpenAI API
'''
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
        total_files = len([name for name in os.listdir(folder_path) if name.endswith(".txt") and '-links' not in name and '-summary' not in name])
        done_files = 0
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if filepath.endswith(".txt") and '-links' not in filename and '-summary' not in filename:
                with open(filepath, "r", encoding='utf8') as file:
                    article = file.read()
                    prompt = f"Can you summarise this news article into five key dot points {article}"
                    summary = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=1000, api_key=apiKey, temperature=0.9, top_p=1, frequency_penalty=0, presence_penalty=0.6, stop=["\n\n"])
                    f.write(f"\n\n{filename}\n\n")
                    f.write(summary.choices[0].text)
                    time.sleep(5)
                    done_files += 1
                    print(f"{done_files} out of {total_files} files have been done.")
    print("Summary file created at: ", summary_file)



def summarize_all_articles(options):
    for option in options:
        summarize_articles(option["folder_path"], option["apiKey"])
