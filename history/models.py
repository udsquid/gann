#
# 3-party libraries
#
from django.db import models
from django.utils import timezone
import pytz


#
# module constants
#
CURRENT_TIMEZONE = timezone.get_current_timezone()
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


#
# models
#
class Taiex(models.Model):
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __unicode__(self):
        local_time = self.time.astimezone(CURRENT_TIMEZONE)
        return "[{:{format}}] {}".format(local_time,
                                         self.price,
                                         format=TIME_FORMAT)


class Tx(models.Model):
    time = models.DateTimeField()
    open = models.DecimalField(max_digits=12, decimal_places=0)
    high = models.DecimalField(max_digits=12, decimal_places=0)
    low = models.DecimalField(max_digits=12, decimal_places=0)
    close = models.DecimalField(max_digits=12, decimal_places=0)

    def __unicode__(self):
        local_time = self.time.astimezone(CURRENT_TIMEZONE)
        return "[{:{format}}] {}|{}|{}|{}".format(local_time,
                                                  self.open,
                                                  self.high,
                                                  self.low,
                                                  self.close,
                                                  format=TIME_FORMAT)

class ProductInfo(models.Model):
    symbol = models.CharField(max_length=10)
    full_name = models.CharField(max_length=200)
    market = models.CharField(max_length=100)
    tick_value = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     null=True)
