from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("YoutubePage", views.YoutubePage, name="YoutubePage"),
    path("YoutubePage/GetAll", views.YoutubePageGetAll, name="YoutubePage"),

    path("Results",views.Results),


    path("CurrentlyWatching",views.CurrentlyWatching,name="watching"),

    path("getresults",views.GetResults,name="getresults"),


    path("addEntertainment",views.addEntertainment,name="addMovie"),
    path("deleteEntertainment/<url_id>",views.deleteEntertainment,name="GetUserWatching"),

    path("GetEntertainment/<index_id>",views.getEntertainment,name="GetEntertainment"),
    path("updateEntertainment/<index_id>",views.updatetEntertainment,name="updateEntertainment"),

    
    path("GetUserWatching",views.GetUserWatching,name="GetUserWatching"),


]