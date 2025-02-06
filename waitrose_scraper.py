import requests #get data from website
from bs4 import BeautifulSoup #webscraping
import pandas as pd 
import re 
import os 
import numpy as np


class Waitrose: #webscraping

    #store url 
    def __init__(self):
        self.url = "https://www.waitrose.com/ecom/shop/search?&searchTerm="
                
    #web scraping
    def webscraping(self, search_term):

        #defining variables
        title = []
        price_temp = []
        link = []

        #initialise soup
        html = requests.get(self.url+search_term, verify=False)
        soup = BeautifulSoup(html.text)

        #accomodate class name change in product title 
        for a in soup.decode().split(' '):
            if 'name___' in a:
                break
        b = a.replace('class="','').replace('"','')

        #accomodate class name change in price, price_per_unit, and unit
        for c in soup.decode().split(' '):
            if 'prices___' in c:
                break
        d = c.replace('class="','').replace('"','').replace('><span','')

        #beautifulsoup scraping
        for items in range(1,50):      
            #scraping: product title 
            for j in soup.findAll("article",{"data-testid":"product-pod"}):
                title.append((j.find("span",{"class": b})).text)
            
            #scraping: price, price_per_unit, and unit
            for i in soup.findAll("article",{"data-testid":"product-pod"}):
                price_temp.append((i.find("div",{"class": d})).text)    
                
            #scraping: link
            for k in soup.findAll("article",{"data-testid":"product-pod"}):
                ahref = k.find("a")['href']
                mystring = 'https://www.waitrose.com'+ahref
                link.append(mystring)
        
        #create temporary df from results (as price_temp still contains: price, price_per_unit, and 
        # unit combined)
        df = pd.DataFrame(
        {'title': title,
        'price_temp': price_temp,
        'link' : link,
        })

        #split price_temp to price, price_per_unit, and unit to different columns
        to_replace = {
        'Item price': '',
        'Price per unit': '/',
        'litre': 'ltr'
        }
        df['price_temp'] = pd.DataFrame(df['price_temp'].replace(to_replace, regex=True))
        df[['price', 'price_per_unit', 'unit']] = df['price_temp'].str.split('/', expand=True)
        df = df.drop(columns=['price_temp'])
        df = df.dropna().drop_duplicates().reset_index().drop(columns=['index'])
        
        #data cleaning price, checking which has £ and p
        list_price = []
        list_price_per_unit = []
        
        for item in range(len(df['price'])):
            if df['price'][item][0] =='£':
                list_price.append(float(df['price'][item][1:]))
            
            elif df['price'][item][-1] =='p':
                list_price.append(float(df['price'][item][:-1])/100)
            else:
                print('unable to pull unit price')
                list_price.append('unknown')
        
        #data cleaning price_per_unit, which has £ and p
        for item in range(len(df['price_per_unit'])):
            if df['price_per_unit'][item][0] =='£':
                list_price_per_unit.append(float(df['price_per_unit'][item][1:]))
            
            elif df['price_per_unit'][item][-1] =='p':
                list_price_per_unit.append(float(df['price_per_unit'][item][:-1])/100)
            else:
                print('unable to pull unit price')
                list_price_per_unit.append('unknown')

        #combining results for price & price_per_unit
        df_price = pd.DataFrame(list_price).round(decimals=2)
        df_price_per_unit  = pd.DataFrame(list_price_per_unit).round(decimals=2)
        df['price'] = df_price
        df['price_per_unit'] = df_price_per_unit

        #data cleaning unit, which has ml
        list_unit = []
        list_price_per_unit = []

        for item in range(len(df['unit'])):
            if df['unit'][item][-2:] =='ml':
                list_price_per_unit.append(float(df['price_per_unit'][item])*10)
                list_unit.append('ltr')
            else:
                list_price_per_unit.append(float(df['price_per_unit'][item]))
                list_unit.append(df['unit'][item])

        #combining results for units & price_per_unit
        df['unit'] = list_unit
        df['price_per_unit'] = list_price_per_unit

        #result :)
        return df
