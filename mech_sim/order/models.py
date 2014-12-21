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

    def __unicode__(self):
        return self.name

class Order(models.Model):
    OPEN_TYPE = (
        ('L', 'Long'),
        ('S', 'Short'),
        )
    STATE_CHOICES = (
        ('O', 'Open'),
        ('C', 'Close'),
        )

    @classmethod
    def get_open_type_symbol(cls, display_name):
        for symbol, display in cls.OPEN_TYPE:
            if display == display_name.capitalize():
                return symbol
        return None

    strategy = models.ForeignKey(Strategy)
    open_type = models.CharField(max_length=1,
                                 choices=OPEN_TYPE)
    open_time = models.DateTimeField()
    open_price = models.DecimalField(max_digits=12, decimal_places=2)
    size = models.PositiveIntegerField()
    close_time = models.DateTimeField(null=True)
    close_price = models.DecimalField(max_digits=12, decimal_places=2,
                                      null=True)
    state = models.CharField(max_length=1,
                             choices=STATE_CHOICES)
