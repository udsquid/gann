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
