from django.db import models
from realtimecongress_server.congress.models import Legislation
import datetime

DOCUMENT_TYPES = (
    ('DWD', 'Democratic Daily Whipline'),
    ('DWW', 'Democratic Weekly Whip Pack'),
    ('DPC LB', 'Democratic Policy Committee Legislative Brief'),
    ('OMB SAP', 'Statement of Administration Policy'),
    ('CBO CE', 'CBO Cost Estimate'),
    ('CRS', 'Congressional Research Service'),
    ('GAO', 'GAO Report'),
    ('JCT', 'Joint Committee on Taxation'),
    ('OMB Memo', 'OMB Memo'),
    ('OMB SAP', 'Statement of Administration Policy'),
    ('RCR SRP', 'Statement of Republican Policy'),
    ('RPC LN', 'Republican Policy Committee Legislative Notice'),
    ('RWD', 'Republian Daily Whipping Post'),
    ('RWW', 'Republican Weekly Whip Notice'),
)

class Document(models.Model):
    urn = models.CharField(max_length=128)
    version = models.CharField(max_length=128, blank=True)
    type = models.CharField(max_length=8, choices=DOCUMENT_TYPES)
    pub_date = models.DateTimeField()
    title = models.TextField()
    description = models.CharField(max_length=255)
    source_url = models.URLField(verify_exists=False, blank=True)
    cache_url = models.URLField(verify_exists=False, blank=True)
    full_text = models.TextField()
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    legislation = models.ManyToManyField(Legislation, related_name='documents')
    
    class Meta:
        ordering = ('timestamp',)
        
    def doc_id(self):
        if self.version:
            return u"%s:%s" % (self.urn, self.version)
        else:
            return self.urn
    
    def __unicode__(self):
        return self.description