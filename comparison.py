import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

class comparison_analysis:
    
    def __init__(self):
        print("class initialised")
        
        
#simple comparison takes the top 10 items from each list and compares the mean.

    def simple_comparison(self, shop1_dict, shop2_dict):
        
        short1 = shop1_dict['data'].head(10)
        short2 = shop2_dict['data'].head(10)

        mean1 = round(short1['price'].mean(),2)
        mean2 = round(short2['price'].mean(),2)
        
        print(mean1,mean2)
        print(mean1>mean2)
        print(type(mean1))
        print(type(mean2))
        
        if mean1 < mean2:
            
            self.results = shop1_dict['name'] + " is cheaper with an average of " + str(mean1) + " in comparison to " + shop2_dict['name']  + " with an average of " + str(mean2)
        
        elif mean1 > mean2:
            
            self.results = shop2_dict['name'] + " is cheaper with an average of " + str(mean2) + " in comparison to " + shop1_dict['name']  + " with an average of " + str(mean1)
        
        elif mean1 == mean2:
            
            self.results = "Both are the same price with an average of " + str(mean1) 
        
        else:
            print("comparison cannot be made")


    def complex_comparison(self,shop1_dict, shop2_dict, search_term):
        
        shop1_df = shop1_dict['data']
        shop2_df = shop2_dict['data']
        
        shop1_df["comparison_value"] = shop1_df.apply(lambda row: round(fuzz.partial_ratio(row["title"], search_term),2),axis = 1)
        shop2_df["comparison_value"] = shop2_df.apply(lambda row: round(fuzz.partial_ratio(row["title"], search_term),2),axis = 1)
        
        self.shop1df = shop1_df
        self.shop2df = shop2_df


    def multi_comparison(self,final_df,list):
        
        agg_stats = pd.pivot_table(final_df, index=['shop'], columns=['search_term'], values = 'price', aggfunc = np.mean)
    
        #agg_stats['avg_sum'] = agg_stats.apply(lambda x : round(x[list[0]] + x[list[1]],2), axis = 1)
        agg_stats['avg_sum'] = round(agg_stats[list].sum(axis = 1),2)
        
        print(agg_stats)
        
        mean1 = agg_stats.iloc[0]["avg_sum"]
        mean2 = agg_stats.iloc[1]['avg_sum']
        
        if mean1 < mean2:
            
            self.results = "Sainsburys" + " is cheaper with an average of " + str(mean1) + " in comparison to " + "Waitrose"  + " with an average of " + str(mean2)
        
        elif mean1 > mean2:
            
            self.results = "Waotrose" + "is cheaper with an average of " + str(mean2) + " in comparison to " + "Sainsburys"  + " with an average of " + str(mean1)
        
        elif mean1 == mean2:
            
            self.results = "Both are the same price with an average of " + str(mean1) 
        
        else:
            print("comparison cannot be made")
    
    
    