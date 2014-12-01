#
# python libraries
#
from django.db import models


#
# models
#
class Strategy(models.Model):
    name = models.CharField(max_length=256, unique=True)
    symbol = models.CharField(max_length=8)
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Strategy created time")


class Order(models.Model):
    strategy = models.ForeignKey(Strategy)
    open_time = models.DateTimeField()
    open_price = models.DecimalField(max_digits=12, decimal_places=2)
    size = models.PositiveIntegerField()
    close_time = models.DateTimeField(null=True)
    close_price = models.DecimalField(max_digits=12, decimal_places=2,
                                      null=True)
    state = models.CharField(max_length=8)
