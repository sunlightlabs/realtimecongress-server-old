from django.db import models
import datetime

DOCUMENT_TYPES = (
    ('WN', 'Whip Notice'),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
)

class Document(models.Model):
    source_url = models.URLField(verify_exists=False, blank=True)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    type = models.CharField(max_length=8, choices=DOCUMENT_TYPES)
    
    class Meta:
        ordering = ('timestamp',)
    
    def __unicode__(self):
        return self.description