from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("YoutubePage", views.YoutubePage, name="YoutubePage"),
    path("YoutubePage/GetAll", views.YoutubePageGetAll, name="YoutubePage"),

    path("Results",views.Results),


    path("CurrentlyWatching",views.CurrentlyWatching,name="watching"),

    path("movies",views.Movies,name="movies"),
    path("tvshow",views.TV_Show,name="movies"),

    path("addEntertainment",views.addEntertainment,name="addMovie"),

    path("GetUserWatching",views.GetUserWatching,name="GetUserWatching"),

]