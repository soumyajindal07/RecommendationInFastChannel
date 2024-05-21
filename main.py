from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommend_by_channelconfig import recommendTitlesByChannelConfig
from recommend_by_holiday import recommendTitlesByHolidaySeason
import helper_functions

app = FastAPI()
origins = ["*"]

#handle CORS issue
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]  
)
@app.post("/CMSAI/MovieRecommendationsInFastChannel")
def recommendMoviesInFastChannel(genre: str,language: str,programme_type: str, channel_title: str = ''): 
    recommendedMoviesIds = []
    try:        
        filteredMovies = helper_functions.filterDataBasedOnChannelParameters(genre, language, programme_type)
       

        programmesidsRecommended = recommendTitlesByChannelConfig(filteredMovies, channel_title) 
        if programmesidsRecommended and len(programmesidsRecommended) > 0:
            recommendedMoviesIds.extend(programmesidsRecommended)
        #print(programmesidsRecommended)

        programmes = recommendTitlesByHolidaySeason(filteredMovies, language)
        if programmes and len(programmes) > 0:
            recommendedMoviesIds.extend(programmes)
        #print(programmes)
    
        #print(recommendedMoviesIds)
        return list(set(recommendedMoviesIds))
    except Exception as e:
        print(e)
        return recommendedMoviesIds
   

#if __name__ == "__main__":
    #recommendMoviesInFastChannel('Comedy','English','Film/Movie','')
