#
# python libraries
#
from django.contrib import admin


#
# project libraries
from mech_sim.order.models import *


#
# common utilities
#
def format_created_time(point):
    from pytz import timezone
    local = point.created_time.astimezone(timezone("Asia/Taipei"))
    return local.strftime("%Y-%m-%d %H:%M:%S")
format_created_time.short_description = "Time"


#
# order admins
#
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', format_created_time)
    date_hierarchy = 'created_time'
    ordering = ('created_time',)

admin.site.register(Strategy, StrategyAdmin)
