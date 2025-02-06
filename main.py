#Import packages
import sainsburys_scrapper
from sainsburys_scrapper import Sainsburys
import waitrose_scraper
from waitrose_scraper import Waitrose
import comparison
from comparison import comparison_analysis
import audio_converter
from audio_converter import audio
import pandas as pd
import numpy as np

audio_class = audio()
text = audio_class.speechtotext()[0]
search_term = audio_class.keyword_extract(text)

#allow the user to input list of search terms if the audio doesn't pick up the correct terms.
confirm = input("Where you searching for:" + str(search_term) + "Y/N:")

if confirm == "N":
    manual_search = input("What were you searching for (seperated by commas):")
    search_term = manual_search.strip().split(",")
    print(search_term)


#initialise the two scraper classes and set up the result table
sainsburys = Sainsburys()
waitrose = Waitrose()
col_names = ["title", "link", "price", "price_per_unit", "unit", "shop", "search_term"]
result_df = pd.DataFrame(columns = col_names)


#only continue if a search_term has been picked up
if len(search_term) > 0:
    
    #Loop through search terms, scraping the top ten results from each search into the results table    
    for i in search_term:
    
        sainsburys_df = sainsburys.scrape(i)
        sainsburys_df['shop'] = 'sainsburys'
        sainsburys_df['search_term'] = i
        
        
        waitrose_df = waitrose.webscraping(i)
        waitrose_df['shop'] = 'waitrose'
        waitrose_df['search_term'] = i
        
        result_df = pd.concat([result_df,sainsburys_df.head(10)])
        result_df = pd.concat([result_df,waitrose_df.head(10)])
        
    aggregate_results = comparison_analysis()
    aggregate_results.multi_comparison(result_df, search_term)    
    
    audio_class.texttospeech(aggregate_results.results)
    
else:
    
    print('No search terms identified try again')
