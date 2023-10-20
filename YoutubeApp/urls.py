from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("YoutubePage", views.YoutubePage, name="YoutubePage"),
    path("YoutubePage/GetAll", views.YoutubePageGetAll, name="YoutubePage"),

    path("Results",views.Results)
]