import pandas as pd
from datetime import datetime, timedelta
import requests
import json
import config

def configure_url() -> str:
    # Set the time of yesterday and today
    today = datetime.now()
    yesterday =  today - timedelta(days=1)
    # API Token
    api_key = config.api_key
    url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={yesterday}&end_date={today}&api-key={api_key}'
    return url

def extract_data_from_api(url: str) -> dict:
    r = requests.get(url)
    # Start from the third nested dictionary
    articles = r.json()['response']['docs']
    return articles

def convert_to_dataframe(data: dict):
    # Create empty list for the desired columns
    pub_date = []
    headline = []
    source = []
    section = []
    medium = []
    document_type = []
    subject = []
    word_count = []
    url = []
    
    # Extract values from the dictionary into the lists
    for item in data:
        pub_date.append(item['pub_date'])
        headline.append(item['headline']['main'])      
        source.append(item['source'])
        section.append(item['section_name'])
        medium.append(item['type_of_material'])
        document_type.append(item['document_type'])
        # Check if keywords is empty
        if bool(item['keywords']) == False:
            subject.append('None')
        else:
            subject.append(item['keywords'][0]['value'])
        word_count.append(item['word_count'])
        url.append(item['web_url'])

    # Create a dictionary to pass the final columns into the dataframe
    articles_dict = {
        "date" : pub_date,
        "headline" : headline,
        "source" : source,
        "section" : section,
        "medium" : medium,
        "document_type" : document_type,
        "subject" : subject,
        "words" : word_count,
        "url" : url,
    }
    
    # Final columns to be loaded into the database
    col = ['date', 'headline', 'source', 'section', 'medium', 'document_type', 'subject', 'words', 'url']
    # Create dataframe from the appended lists
    df = pd.DataFrame(articles_dict, columns = col)
    # Format date into mm/dd/yyyy
    df['date'] = df.apply(lambda x: x['date'][:-14], axis = 1)
    return df

if __name__ == "__main__":
    data = extract_data_from_api(configure_url())
    df = convert_to_dataframe(data)
    df.to_csv(config.file_path_today, index = False)
