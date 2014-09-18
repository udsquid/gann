#
# django libraries
#
from django.db import models


#
# models
#
class Taiex(models.Model):
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __unicode__(self):
        return "[%s] %s" % (self.time, self.price)


class Tx(models.Model):
    time = models.DateTimeField()
    open = models.DecimalField(max_digits=12, decimal_places=0)
    high = models.DecimalField(max_digits=12, decimal_places=0)
    low = models.DecimalField(max_digits=12, decimal_places=0)
    close = models.DecimalField(max_digits=12, decimal_places=0)

    def __unicode__(self):
        return "[%s] %s|%s|%s|%s" % (self.time,
                                     self.open,
                                     self.high,
                                     self.low,
                                     self.close)

class ProductInfo(models.Model):
    symbol = models.CharField(max_length=10)
    full_name = models.CharField(max_length=200)
    market = models.CharField(max_length=100)
    tick_value = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     null=True)
