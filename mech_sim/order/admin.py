#
# python libraries
#
from django.contrib import admin


#
# project libraries
from mech_sim.order.models import *
from lib.time_utils import to_local


#
# common utilities
#
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def format_created_time(point):
    from pytz import timezone
    local = point.created_time.astimezone(timezone("Asia/Taipei"))
    return local.strftime("%Y-%m-%d %H:%M:%S")
format_created_time.short_description = "Time"


def format_open_time(point):
    local = to_local(point.open_time)
    return local.strftime(TIME_FORMAT)
format_open_time.short_description = "Open time"

def format_close_time(point):
    if not point.close_time:
        return None
    local = to_local(point.close_time)
    return local.strftime(TIME_FORMAT)
format_close_time.short_description = "Close time"


#
# order admins
#
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', format_created_time)
    date_hierarchy = 'created_time'
    ordering = ('created_time',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('strategy',
                    'open_type',
                    format_open_time,
                    'open_price',
                    'size',
                    format_close_time,
                    'close_price',
                    'state',
                    'per_size_gross_profit',
                    'gross_profit')
    date_hierarchy = 'open_time'
    ordering = ('open_time',)

admin.site.register(Strategy, StrategyAdmin)
admin.site.register(Order, OrderAdmin)
