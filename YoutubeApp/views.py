from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import loader

from .Jobs.selenium_scraper import youtube_trans,youtube_trans_requests

# Create your views here.


def index(request):
     return render(request,"pages/index.html")
def YoutubePage(request):
    template = loader.get_template("base.html")
    return render(request,"pages/YoutubeTranscript.html")


def Results(request:HttpRequest):
        print(123)
        if (request.method == "POST"):
            url = request.POST["url"]
            sum = youtube_trans_requests(url)
            return render(request,"components/Result.html",{"transcript":sum})
            

