from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import loader

from .Jobs.selenium_scraper import youtube_trans

# Create your views here.
def index(request):
    template = loader.get_template("base.html")
    return render(request,"base.html")


def Results(request:HttpRequest):
        print(123)
        if (request.method == "POST"):
            url = request.POST["url"]
            sum = youtube_trans(url)
            return render(request,"components/Result.html",{"summary":sum})
            

