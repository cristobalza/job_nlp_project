from bs4 import BeautifulSoup
import lxml
import requests
import pandas as pd
import numpy as np

# https://www.indeed.com/cmp/Google/reviews?fcountry=ALL&start=
link = 'https://www.indeed.com/cmp/Google/reviews?fcountry=ALL&start='

base_url = requests.get(link, timeout=5)

def parse(full_url):
    page_content = BeautifulSoup(full_url.content, 'lxml')
    containers = page_content.findAll('div', 
                 {'class':'cmp-Review-container'})
    df = pd.DataFrame(columns = 
    ['rating',
    'rating_title',
    'rating_description',
    'rating_pros',
    'rating_cons'])
    
    for item in containers:        
        try:
            rating = item.find('button', 
                     {'class': 'cmp-ReviewRating-text'}).text.replace('\n', '')
        except:
            rating = None
        try:
            rating_title = item.find('div', 
                           {'class': 'cmp-Review-title'}).text.replace('\n', '')
        except:
            rating_title = None
        try:
            rating_description = item.find('span', 
                                 {'itemprop': 'reviewBody'}).text.replace('\r', '. ')
        except:
            rating_description = None
        try:
            rating_pros = item.find('div', 
                          {'class': 'cmp-ReviewProsCons-prosText'}).text.replace('\n', '')
        except:
            rating_pros = None
        try:
            rating_cons = item.find('div', 
                          {'class': 'cmp-ReviewProsCons-consText'}).text.replace('\n', '')
        except:
            rating_cons = None
        df = df.append({'rating': rating, 
             'rating_title': rating_title, 
             'rating_description': rating_description,
             'rating_pros': rating_pros, 
             'rating_cons': rating_cons}, ignore_index=True)
    return df

# df = parse(base_url)
# print(df[['rating_description']].head())
# print(df.head())
# print(df.columns)
# print(df.shape)

base_url = 'https://www.indeed.com/cmp/Google/reviews?fcountry=ALL&start='
all_reviews_df = pd.DataFrame(columns = ['rating', 'rating_title', 
'rating_description','rating_pros', 'rating_cons'])
num_reviews = 20
# you can adjust this number on how many reviews you which to scrape
while num_reviews < 3000:  
    
    full_url = base_url + str(num_reviews)
    
    get_url = requests.get(full_url, timeout=5)  
        
    partial_reviews_df = parse(get_url)   
    all_reviews_df = all_reviews_df.append(
                     partial_reviews_df, ignore_index=True) 
    
    num_reviews += 20

all_reviews_df.to_csv('outputs/indeed_scrape.csv')