from django.db import models
from django.conf import settings
# Create your models here.



class YoutubeTranscription(models.Model):
    YoutubeId = models.CharField(primary_key=True,max_length=50)
    YoutubeURL = models.CharField(null=True,max_length=50)
    dateRetrived= models.DateTimeField(auto_now=True)
    cached=models.BooleanField()
    Transcript = models.TextField()
    Summary = models.TextField()


class UserWatching(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Title=models.CharField()
    MovieId = models.CharField(null=True,max_length=50,unique=True)
    TvShowId= models.CharField(null=True,max_length=50,unique=True)