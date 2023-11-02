import dataclasses
import json
import os
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.core.paginator import Paginator
from YoutubeApp.helper import Helper

from YoutubeApp.models import UserWatching, YoutubeTranscription
from .Jobs.selenium_scraper import summary, youtube_trans_requests,youtube_title_request
from urllib.parse import ParseResult, urlparse
from datetime import datetime
import tmdbsimple as tmdb

from .Jobs.Movies_Database import Search, SearchTVShow
# Create your views here.


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
        
def CurrentlyWatching(request:HttpRequest):
    if request.user.is_authenticated:
        return render(request,"pages/CurrentlyWatching.html")
    else:
        return redirect("/")


def Movies(request:HttpRequest):

    if (request.method == "POST"):
        search_item = request.POST["Search"]

        search = tmdb.Search()
        
        movies = search.movie(query=search_item)
        
        movies_list:list[Search]=[]

        movies_result= movies['results']

        for movie in movies_result:
             

            Search_Obj = Search(**movie)
            movies_list.append(Search_Obj)
      
        final_list = [movie for movie in movies_list if movie.vote_count>10 and movie.original_language=="en"] 
        
        sorted_list = sorted(final_list,key=lambda x:x.popularity,reverse=True)
        
        return render(request,"components/movies.html",{"movies":sorted_list})
    

def TV_Show(request:HttpRequest):
    if (request.method == "POST"):
        search_item = request.POST["Search"]

        search = tmdb.Search()

        movies = search.tv(query=search_item)
        
        movies_list:list[Search]=[]

        movies_result= movies['results']

        for movie in movies_result:
            Search_Obj = SearchTVShow(**movie)
            movies_list.append(Search_Obj)
      
        final_list = [movie for movie in movies_list if movie.vote_count>10 and movie.original_language=="en"] 
        
        sorted_list = sorted(final_list,key=lambda x:x.popularity,reverse=True)
        
        return render(request,"components/tv.html",{"movies":sorted_list})


def addEntertainment(request:HttpRequest):
    if (request.method == "POST"):
        search_item =""
        title = ""
        for key,value in request.POST.items():
             
            if ("movie" in key):
                search_item = value
            if ("title" or "original_name" in key):
                title = value
                
        try:
            user = UserWatching(User=request.user,MovieId=search_item,Title=title)
            user.save()
        except IntegrityError as e: 
            print(e)
            pass
        response = HttpResponse()
        response["HX-Redirect"] = request.build_absolute_uri('/CurrentlyWatching')

        return response


def GetUserWatching(request:HttpRequest):
    allCurrent = UserWatching.objects.filter(User=request.user)
    return render(request,"components/UserWatching.html",{"allCurrent":allCurrent})
