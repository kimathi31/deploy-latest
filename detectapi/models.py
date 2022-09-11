from django.db import models
from django.utils import timezone
from django.db.models.fields.json import KeyTransform
import os
import json

#class CustomJSONField(models.JSONField):
#    def from_db_value(self, value, expression, connection):
#        if value is None:
#            return value
#        # Some backends (SQLite at least) extract non-string values in their
#        # SQL datatypes.
#        if isinstance(expression, KeyTransform) and not isinstance(value, str):
#            return value
#        try:
#            if type(value)==dict:
#                return json.loads(json.dumps(value), cls=self.decoder)
#            else:
#                return json.loads(value, cls=self.decoder)
#        except json.JSONDecodeError:
#            return value

# Create your models here.

class detection(models.Model):
    Analysis_REF_No = models.AutoField(primary_key=True)
    Crop = models.CharField(max_length=255)
    Disease = models.CharField(max_length=255)
    #Probability = models.CharField(max_length=255)
    Date = models.DateField(auto_now=True)
    Time = models.DateTimeField(default=timezone.now)
    image = models.CharField(max_length=255)
    symptoms = models.CharField(max_length=255)
    measures = models.CharField(max_length=255)
    #def __str__(self):
    #    return self.Disease
  
    class Meta:
        db_table = 'detection'
    


class crop_diseases(models.Model):
    nameid = models.IntegerField(primary_key=True)
    disease = models.CharField(max_length=255)
    symptom = models.CharField(max_length=255)
    measure = models.CharField(max_length=255)

    class Meta:
        db_table = 'crop_diseases'

       