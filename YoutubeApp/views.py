import dataclasses
import json
import os
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import redirect, render
from django.template import loader
from django.core.paginator import Paginator
from YoutubeApp.helper import Helper

from YoutubeApp.models import UserWatching, YoutubeTranscription
from .Jobs.selenium_scraper import summary, youtube_trans_requests,youtube_title_request
from urllib.parse import ParseResult, urlparse
from datetime import datetime
import tmdbsimple as tmdb

from .Jobs.Movies_Database import  Search, SearchTVShow

from django.db.models import Q

from typing import List, Union
# Create your views here.

# Transcript
def index(request):
     return render(request,"pages/index.html")
def YoutubePage(request):
    template = loader.get_template("base.html")
    return render(request,"pages/YoutubeTranscript.html")
def YoutubePageGetAll(request):
    allTranscripts = YoutubeTranscription.objects.all()
    return render(request,"pages/GetAll.html",{"transcripts":allTranscripts})
def Results(request:HttpRequest):
        status = 400
        if (request.method == "POST"):
            url = request.POST["url"]

            if (type(url)==str and url.lower() in ("youtube","youtu.be") ):
                return render(request,"components/Invalid.html")
            
            url_id = ""
            urlparsed:ParseResult = urlparse(url)

            match (urlparsed.hostname):
                case "www.youtube.com":
                        url_id = urlparsed.query.split("=")[1]
                case "youtu.be":
                        url_id = urlparsed.path.strip("/")
            title=youtube_title_request(url)


            
            result:YoutubeTranscription = Helper.get_or_none(YoutubeTranscription,YoutubeId=url_id)
            if result !=None:
                YoutubeTranscription.objects.get
                return render(request,"components/Result.html",{"transcript":result.Summary,"title":title})

            else:
                
                YoutubeTrans = YoutubeTranscription()
                YoutubeTrans.YoutubeId = url_id
                YoutubeTrans.YoutubeURL = url
                YoutubeTrans.cached=True

                
                Transcript = youtube_trans_requests(url)
                YoutubeTrans.Transcript = Transcript
                result = summary(Transcript)['choices'][0]["message"]["content"]
                YoutubeTrans.Summary = result
     
        
                YoutubeTrans.save()
                return render(request,"components/Result.html",{"transcript":result,"title":title})
        


#Currently Watching

def CurrentlyWatching(request:HttpRequest):
    if request.user.is_authenticated:
        return render(request,"pages/CurrentlyWatching.html")
    else:
        return redirect("/")
def Filter(type,search_item)->List[Union[Search,SearchTVShow]]: 
    match type:
        case "T":
            search = tmdb.Search()

            movies = search.tv(query=search_item)
            
            movies_list:list[Search]=[]

            result = movies['results']
            for movie in result:
                Search_Obj = SearchTVShow(**movie)
                movies_list.append(Search_Obj)
            return movies_list
        case "M":
            search = tmdb.Search()

            movies = search.movie(query=search_item)
            
            movies_list:list[Search]=[]

            result = movies['results']
            for movie in result:
                Search_Obj = Search(**movie)
                movies_list.append(Search_Obj)
            return movies_list

def GetResults(request:HttpRequest):
    if (request.method == "POST"):

        type = request.POST["type"]
        movies_list = Filter(type,request.POST["Search"])
      
        final_list = [movie for movie in movies_list if movie.vote_count>0 and movie.original_language=="en"] 
        
        sorted_list = sorted(final_list,key=lambda x:x.popularity,reverse=True)
        if (type == "M"):
            return render(request,"components/movie.html",{"movies":sorted_list})
        else:
            return render(request,"components/tv.html",{"tvs":sorted_list})
            


def addEntertainment(request:HttpRequest):
    if (request.method == "POST"):
        movie =None
        tv = None
        title = ""
        url = ""
        for key,value in request.POST.items():
             
            if ("movie" in key):
                movie = value

            if ("tv" in key):
                tv = value

            if ("title" or "original_name" in key):
                title = value
            if ("url" in key):
                url = value
        try:
            if (movie is not None ):

                user = UserWatching(User=request.user,MovieId=movie,Title=title,PosterURL=url)
                user.save()
            elif (tv is not None):
                user = UserWatching(User=request.user,TvShowId=tv,Title=title,PosterURL=url)

                user.save()
        except IntegrityError as e: 
            print(e)
            pass
        response = HttpResponse()
        response["HX-Redirect"] = request.build_absolute_uri('/CurrentlyWatching')

        return response

#old 
def GetUserWatching(request:HttpRequest):
    search = tmdb.Search()
    Movies = UserWatching.objects.filter(User=request.user,MovieId__isnull=False)
    TV = UserWatching.objects.filter(User=request.user,TvShowId__isnull=False)
    movie_list = []
    tv_list = []
    for movie in Movies:
        results = search.movie(query=movie.Title)
        final_list = [movie_q for movie_q in results['results'] if str(movie_q["id"]) == movie.MovieId] 
        if len(final_list)>0:

            movie_list.append(Search(**final_list.pop(),state=movie.get_state(),db_id=movie.id))
        
    for tv in TV:
        results = search.tv(query=tv.Title)
        final_list = [tv_q for tv_q in results['results'] if str(tv_q["id"]) == tv.TvShowId] 
        if len(final_list)>0:
            tv_list.append(SearchTVShow(**final_list.pop(),state=tv.get_state(),db_id=tv.id))
       
    
    
    
    return render(request,"components/UserWatching.html",{"movies":movie_list,"tv":tv_list,"states":UserWatching().get_all_states()})

def getEntertainment(request:HttpRequest,index_id):
    search = tmdb.Search()
    Movies = UserWatching.objects.filter(User=request.user,MovieId__isnull=False)
    TV = UserWatching.objects.filter(User=request.user,TvShowId__isnull=False)
    
    Movies_TV = UserWatching.objects.filter(User=request.user,MovieId__isnull=False) | UserWatching.objects.filter(User=request.user,TvShowId__isnull=False)
    combined_query = Movies.union(TV)
    

    # first:UserWatching = UserWatching.objects.filter(id__in=combined_query)[int(index_id)]
    try:
        first = Movies_TV.filter()[int(index_id)-1  ]
    except IndexError:
        return HttpResponse('')
    result = []
    
    
    if (first.TvShowId==None):
        results = search.movie(query=first.Title)
        final_list = [movie_q for movie_q in results['results'] if str(movie_q["id"]) == first.MovieId] 
        if len(final_list)>0:
            final = Search(**final_list.pop(),state=first.get_state(),db_id=first.id)
            return render(request,"components/enterainmentMovie.html",{"index_id":index_id,"next_index":int(index_id)+1,"poster_path":final.poster_path,"original_title":final.original_title,"release_date":final.release_date,"state":final.state,"overview":final.overview,"db_id":final.db_id,"states":UserWatching().get_all_states()})
    else:
        results = search.tv(query=first.Title)
        final_list = [movie_q for movie_q in results['results'] if str(movie_q["id"]) == first.TvShowId] 
        if len(final_list)>0:
            final =  SearchTVShow(**final_list.pop(),state=first.get_state(),db_id=first.id)
            return render(request,"components/enterainmentMovie.html",{"index_id":index_id,"next_index":int(index_id)+1,"poster_path":final.poster_path,"original_title":final.original_name,"release_date":final.first_air_date,"state":final.state,"overview":final.overview,"db_id":final.db_id,"states":UserWatching().get_all_states()})
            
    
    
    
    
def deleteEntertainment(request:HttpRequest,url_id):
    UserWatching.objects.get(id=url_id).delete()
    
    return HttpResponse('')
    

    
def updatetEntertainment(request:HttpRequest,index_id):
    if request.method == 'PATCH':
        data = QueryDict(request.body)
        new_states = data['states']
        value = UserWatching().to_two(new_states)
        UserWatching.objects.filter(id=index_id).update(state=value)
        
        
        return render(request,"components/state.html",{"state":new_states,"states":UserWatching().get_all_states()})

    
    return HttpResponse('')
