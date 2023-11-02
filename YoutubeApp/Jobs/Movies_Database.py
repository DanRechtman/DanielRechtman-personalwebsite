from dataclasses import dataclass
import tmdbsimple as tmdb




@dataclass
class Search:
    adult:bool
    backdrop_path:str
    genre_ids:list[int]
    id:int 
    original_language:str
    original_title:str
    overview:str
    popularity:float
    poster_path:str
    release_date:str
    title:str
    video:bool
    vote_average:float
    vote_count:int
    
@dataclass
class SearchTVShow:
   adult:bool
   backdrop_path:str
   genre_ids:list[int]
   id:int
   origin_country:[str]
   original_language:str
   original_name:str
   overview:str
   popularity:float
   poster_path:str
   first_air_date:str
   name:str
   vote_average:float
   vote_count:int