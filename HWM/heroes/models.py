from django.db import models

class Artifact(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    strength = models.CharField(max_length=20)
    last_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.name
    
class Log(models.Model):
    description = models.TextField()
    artifact = models.ForeignKey(Artifact)
    date = models.DateTimeField()
    
    def __unicode__(self):
        return self.description
    
class DateValue(models.Model):
    date = models.DateTimeField()
    
    def __unicode__(self):
        return self.date