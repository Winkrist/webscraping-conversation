#import packages
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd


class Sainsburys:
    
    #initialise object
    def __init__(self):
        
        self.url = 'https://www.sainsburys.co.uk/gol-ui/SearchResults/'
    '''
    def __str__(self):
        return f"search term = {self.search_term}"
    '''
    #scraper method using chrome driver
    def scrape(self,search_term):
        
        #set up web driver
        wait_time = 20
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.implicitly_wait(wait_time)
        driver.get(self.url+search_term)
        
        #initialise lists
        price_list = []
        title_list = []
        link_list = []
        price_per_unit_list = []
        units_list = []
        
        #find all sections of html with prices
        prices = driver.find_elements(By.CLASS_NAME, "pt__cost__retail-price")
        total_products = len(prices)

        #find all sections of html with titles and links
        titles = driver.find_elements(By.XPATH,'//h2[contains(@class, "pt__info__description")]/a')
        total_titles = len(titles)
        
        #find all sections of html with price per unit
        per_unit = driver.find_elements(By.CLASS_NAME, "pt__cost__unit-price-per-measure")
        total_per_unit = len(per_unit)

        if total_products == total_titles and total_products == total_per_unit:

            #Loop through all webelements to extract price, titles and links in lists
            for a in range(total_products):
                
                price = prices[a].text
                title = titles[a].text
                link = titles[a].get_attribute('href')
                price_per_unit = per_unit[a].text
                
                #convert price to points
                if price[0]=='£':
                    price1 = float(price[1:])
                    
                elif price[-1] == 'p':
                    price1 = float(price[:-1])/100
                
                #convert unit price to pounts per unit
                split = price_per_unit.replace(" ","").split("/")

                if len(split) == 2:
    
                    units = split[1]
    
                    if split[0][0]=='£':
                        price_per_unit_int = float(split[0][1:])
                    
                    elif split[0][-1] == 'p':
                        price_per_unit_int = float(split[0][:-1])/100
                        
                else: 
                    print("unable to pull unit price")
                    price_per_unit_int = "unknown"
                    units = "unknown"
                    
                price_list.append(price1)
                title_list.append(title)
                link_list.append(link)
                price_per_unit_list.append(price_per_unit_int)
                units_list.append(units)
                
            #Create Dataframe
            products_dict = {'title':title_list, 'price':price_list, 'link':link_list, 'price_per_unit':price_per_unit_list, 'unit':units_list}
            products_df = pd.DataFrame(products_dict)
            
            return products_df
        
        else: print("Titles and products do not align")
