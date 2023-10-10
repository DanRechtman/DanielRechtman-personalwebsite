from django.db import models

# Create your models here.



class YoutubeTranscription(models.Model):
    YoutubeId = models.CharField(primary_key=True,max_length=12)
    YoutubeURL = models.CharField(null=True,max_length=50)
    dateRetrived= models.DateTimeField(auto_now=True)
    cached=models.BooleanField()
    Transcript = models.CharField(max_length=20000)