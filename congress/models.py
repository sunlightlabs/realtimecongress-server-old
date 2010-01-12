from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.localflavor.us.models import USStateField

"""
    outstanding:
        Legislation
        * subject terms
        * other resources
"""

BILL_TYPE_CHOICES = (
    ('H.R.', ''),
    ('H.RES.', ''),
    ('S.', ''),
    ('S.R.', ''),
    ('H.CON.RES.', ''),
    ('S.CON.RES.', ''),
    ('H.J.RES.', ''),
    ('S.J.RES.', ''),
    ('H.J.RES.', ''),
    ('S.J.RES.', ''),
)

TITLE_CHOICES = (
    ('Com', 'Commissioner'),
    ('Del', 'Delegate'),
    ('Rep', 'Representative'),
    ('Sen', 'Senator'),
)

PARTY_CHOICES = (
    ('D', 'Democratic'),
    ('I', 'Independent'),
    ('R', 'Republican'),
)

GENDER_CHOICES = (
    ('F', 'Female'),
    ('M', 'Male'),
)

CHAMBER_CHOICES = (
    ('H', 'House of Representatives'),
    ('S', 'Senate'),
)

VOTE_CHOICES = (
    ('Y', 'Yea'),
    ('N', 'Nay'),
    ('A', 'Abstain'),
    ### what else?
)

#
# legislator related models
#

class Legislator(models.Model):
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    suffix = models.CharField(max_length=8, blank=True)
    nickname = models.CharField(max_length=128, blank=True)
    district = models.CharField(max_length=16, blank=True)
    state = USStateField(max_length=2)
    party = models.CharField(max_length=1, choices=PARTY_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    currently_serving = models.BooleanField(default=False)
    govtrack_id = models.CharField(max_length=16, blank=True)
    bioguide_id = models.CharField(max_length=16, blank=True)
    
    class Meta:
        ordering = ('last_name','first_name')
    
    def __unicode__(self):
        return self.display_name()
    
    def display_name(self):
        return u"%s. %s %s" % (self.title, self.first_name, self.last_name)

#
# legislation related models
#

class Legislation(models.Model):
    sponsor = models.ForeignKey(Legislator, related_name="sponsored")
    co_sponsors = models.ManyToManyField(Legislator, related_name="co_sponsored")
    chamber = models.CharField(max_length=1, choices=CHAMBER_CHOICES)
    congress = models.IntegerField()
    type = models.CharField(max_length=16, choices=BILL_TYPE_CHOICES)
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    summary = models.TextField()
    introduced = models.DateTimeField()
    
    class Meta:
        ordering = ('-introduced',)
        verbose_name_plural = 'legislation'
    
    def __unicode__(self):
        return self.title
    
    def current_state(self):
        return self.actions.latest('datestamp')

class Action(models.Model):
    legislation = models.ForeignKey(Legislation, related_name="actions")
    datestamp = models.DateTimeField()
    ### what else?
    
    class Meta:
        ordering = ('-datestamp',)
    
    def __unicode__(self):
        return u"????" #### what here?

#
# roll call related models
#

class RollCall(models.Model):
    legislation = models.ForeignKey(Legislation, related_name="roll_calls")
    datestamp = models.DateTimeField()
    number = models.IntegerField()
    congress = models.IntegerField()
    chamber = models.CharField(max_length=1, choices=CHAMBER_CHOICES)
    question = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('-datestamp',)
    
    def __unicode__(self):
        return self.question

class Vote(models.Model):
    roll_call = models.ForeignKey(RollCall, related_name="votes")
    legislator = models.ForeignKey(Legislator, related_name="votes")
    legislation = models.ForeignKey(Legislation, related_name="votes")
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES)
    
    def __unicode__(self):
        return u"%s voted %s on %s" % (self.legislator.display_name, self.vote, self.legislation.title)
        
class LegislativeSubjectTerm(models.Model):
    term = models.CharField(max_length=255)
    parent = models.ForeignKey("self", null=True)

#
# relations
#

class LegislatorRelation(models.Model):
    legislator = models.ForeignKey(Legislator)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

class LegislationRelation(models.Model):
    legislation = models.ForeignKey(Legislation)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()