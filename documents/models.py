from django.db import models
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
    source_url = models.URLField(verify_exists=False, blank=True)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    type = models.CharField(max_length=8, choices=DOCUMENT_TYPES)
    
    class Meta:
        ordering = ('timestamp',)
    
    def __unicode__(self):
        return self.description