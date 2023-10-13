from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator
from YoutubeApp.helper import Helper

from YoutubeApp.models import YoutubeTranscription
from .Jobs.selenium_scraper import summary, youtube_trans_requests
from urllib.parse import ParseResult, urlparse
from datetime import datetime
# Create your views here.


def index(request):
     return render(request,"pages/index.html")
def YoutubePage(request):
    template = loader.get_template("base.html")
    return render(request,"pages/YoutubeTranscript.html")


def Results(request:HttpRequest):
        status = 400
        if (request.method == "POST"):
            url = request.POST["url"]

            if (type(url)==str and "youtube" not in url.lower()):
                return render(request,"components/Invalid.html")
            urlparsed:ParseResult = urlparse(url)
            url_id = urlparsed.query.split("=")[1]
            result:YoutubeTranscription = Helper.get_or_none(YoutubeTranscription,YoutubeId=url_id)
            if result !=None:
                
                return render(request,"components/Result.html",{"transcript":result.Summary})

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
                return render(request,"components/Result.html",{"transcript":result})
        

