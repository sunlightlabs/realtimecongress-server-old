from django.db import models
from realtimecongress_server.congress.models import Committee, Legislation

class Event(models.Model):
    type = models.CharField(max_length=255)   # 'House Floor'
    timestamp = models.DateTimeField()
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    url = models.URLField(null=True, verify_exists=False)

    class Meta:
        abstract=True
        
class LiveEvent(Event):
    pass
    
class CommitteeMeeting(Event):
    location = models.CharField(max_length=255)
    committee = models.ForeignKey(Committee, related_name='meetings')
    legislation = models.ManyToManField(Legislation, related_name='hearings')