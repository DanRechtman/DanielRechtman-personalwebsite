from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator
from YoutubeApp.helper import Helper

from YoutubeApp.models import YoutubeTranscription
from .Jobs.selenium_scraper import summary, youtube_trans_requests,youtube_title_request
from urllib.parse import ParseResult, urlparse
from datetime import datetime

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
        

