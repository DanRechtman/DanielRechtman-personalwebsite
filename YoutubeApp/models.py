from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.



class YoutubeTranscription(models.Model):
    YoutubeId = models.CharField(primary_key=True,max_length=50)
    YoutubeURL = models.CharField(null=True,max_length=100)
    dateRetrived= models.DateTimeField(auto_now=True)
    cached=models.BooleanField()
    Transcript = models.TextField()
    Summary = models.TextField()


class UserWatching(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Title=models.CharField()
    dateRetrived= models.DateTimeField(auto_now=True)
    PosterURL= models.CharField()

    MovieId = models.CharField(null=True,max_length=50,unique=True)
    TvShowId= models.CharField(null=True,max_length=50,unique=True)
    
    
    class State(models.TextChoices):
        Watched = 'W', _('Watched')
        NotStarted = 'NS', _('Not Started')
        InProgress = 'IP',_('In Progress')
        
    state = models.CharField(
        max_length=2,
        choices=State.choices,
        default=State.NotStarted,
    )
    def to_two(self,string):
        return [result for result in self.State.choices if string in result].pop()[0]
    def get_state(self) :
        return ([item for item in self.State.choices if item[0]==self.state].pop())[1]
    
    def get_all_states(self)->State:
        return self.State.labels