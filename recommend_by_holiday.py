from datetime import datetime
import requests
import pandas as pd
import json
import pickle
import os
import re

COUNTRY_CODE = "MY"
def get_holidays():    
    key = os.getenv("CALENDARIFIC_API_KEY") 
    print(key)
    current_date = datetime.today()  
    year = current_date.year
    month = 12 #current_date.month

    endpoint_url = f"https://calendarific.com/api/v2/holidays?api_key={key}&country={COUNTRY_CODE}&year={year}&month={month}"
    response = requests.get(endpoint_url)
    if response.status_code == 200:
        holidays = response.json()['response']['holidays']
        return holidays
    else:        
        return []
    
def contains_festive_word(title, festive_tags):
    # Use regular expression to split the title into words
    words = re.findall(r'\b\w+\b', title.lower())
    # Check if any word in the title is in festive_tags
    return any(word in festive_tags for word in words)

# Function to recommend movies for a given festive season using cosine similarity
def recommend_movies_cosine_similarity(movies_df, festive_season,festive_keywords):
   
    # Festive keywords for each festive occasion    
    festive_tags = festive_keywords.get(festive_season, [])   

    festive_tags = {tag.lower() for tag in festive_tags}

   # filtered_movies = movies_df[movies_df['original_title'].apply(lambda title: any(word.lower() in festive_tags for word in title.lower().split()))]
    filtered_movies = movies_df[movies_df['original_title'].apply(lambda title: contains_festive_word(title, festive_tags))]

    top10movies = filtered_movies.head(10)

    if not top10movies.empty:        
        return top10movies['id'].tolist()
    else:
        return []
    
def recommendTitlesByHolidaySeason(movies_df:pd.DataFrame, language: str):  
  with open('festive_list.json', 'r') as f:
        festive_list = json.load(f)
        festive_keywords = festive_list.get(language.lower(), [])
        if len(festive_keywords) == 0:
            return
        holidaysToConsider = festive_keywords.keys()      

        recommendedMovies = []
        holidaysUsed = []

        holidays = get_holidays()    
        if holidays is not None:  
            for holiday in holidays:      
                holiday_name = holiday.get("name") 
                for holidayToConsider in holidaysToConsider:  
                    if (holidayToConsider in holiday_name.lower().split(" ")) and (holidayToConsider not in holidaysUsed): 
                        movies = recommend_movies_cosine_similarity(movies_df,holidayToConsider,festive_keywords) 
                        recommendedMovies.extend(movies)
                        holidaysUsed.append(holidayToConsider)
                        break  
            return recommendedMovies



          
    
