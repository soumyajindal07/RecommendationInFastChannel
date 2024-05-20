import pickle
import pandas as pd
import datetime as datetime

#benchmark for classic movies is 10 years old
NUMBER_OF_YEARS_AS_CLASSIC = 10

#Specify the max count of movies to return
MAX_COUNT_OF_MOVIES_TO_RETURN = 10

def recommendTitlesByChannelConfig(movies_df: pd.DataFrame, channel_title: str) -> list[int]:
    
    current_year = datetime.datetime.now()
    movies = pd.DataFrame()

     # Check if title contains 'classic' or any word from title
    if 'classic' in channel_title.lower() or any(word.lower() in channel_title.lower() for word in ['old', 'vintage', 'retro']):
        # Convert 'release_date' to datetime
        movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], format='mixed',dayfirst=True)
        
        # Find movies with release year older than 10 years
        movies = movies_df[(movies_df['release_date'] < pd.Timestamp(current_year.year - NUMBER_OF_YEARS_AS_CLASSIC, 1, 1))]

    if movies.empty:
        movies = movies_df    

    if channel_title and (not movies.empty):
        # Split the channel title into words
        channel_words = channel_title.lower().split()
        # Filter movies where original title contains a complete word from channel title
        movies = movies[movies['original_title'].apply(lambda title: any(word.lower() in title.lower().split() for word in channel_words))]

        #movies = movies[movies['original_title'].str.contains(channel_title, case=False)]
    
    top10movies = movies.head(MAX_COUNT_OF_MOVIES_TO_RETURN)

    if not top10movies.empty:
        return (top10movies.loc[:,["id"]]).values.flatten().tolist()   

#if __name__ == "__main__":
    #recommendTitlesByChannelConfig('[action,adventure]', 'en','series','christmas')
