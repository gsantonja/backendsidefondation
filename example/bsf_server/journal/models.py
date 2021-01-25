from django.db import models
from django.utils.timezone import now


# Create your models here.
    # class test for testing the skeleton template
    # those fields are needed to test the functionnality
class Intervention_Journal(models.Model):
    ticket =  models.CharField(max_length=100,default='',null=True,blank=True)
    comment =  models.CharField(max_length=200,default='',null=True,blank=True)
    update = models.DateTimeField(default = now,null=False)
    create = models.DateTimeField(default = now,null=False)

    def __str__(self):
        return "{} - {}".format(self.update.strftime("%Y-%m-%d %H:%M:%S"),self.ticket)
