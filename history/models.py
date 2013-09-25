###
### django libraries
###
from django.db import models


###
### models
###
class Taiex(models.Model):
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=12, decimal_places=2)


    def __unicode__(self):
        return "[%s] %s" % (self.time, self.price)
