import pandas as pd
import pickle

def filterDataBasedOnChannelParameters(genre: str,language: str,programme_type: str) -> pd.DataFrame:
    #Load the artifacts from the artifacts folder (movies)
    movies = pickle.load(open('artifacts/movie_list.pkl','rb')) 
    
    if language and (not movies.empty):
        movies = movies[movies['original_language'] == language.lower()]

    if programme_type and (not movies.empty):
        movies = movies[movies['programme_type'] == programme_type.lower()]

    if genre and (not movies.empty):
        #movies = movies[movies['genres'].apply(lambda x: any(genre.lower() in genres for genre in x))]
        movies = movies[movies['genres'] == genre.lower()]

    return movies
