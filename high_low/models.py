###
### django libraries
###
from django.db import models


###
### models
###
class Point(models.Model):
    time = models.DateField()
    price = models.IntegerField()


    def __unicode__(self):
        return "%s %d" % (self.time, self.price)
