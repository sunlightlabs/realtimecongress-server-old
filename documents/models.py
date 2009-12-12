from django.db import models

DOCUMENT_TYPES = (
    '','','','','','','','','',
)

class Document(models.Model):
    url = models.URLField(verify_exists=False, blank=True)