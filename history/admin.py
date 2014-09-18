#
# 3-party libraries
#
from django.contrib import admin


#
# project libraries
#
from history.models import *


#
# admin hook
#

# --- common ---
def format_datetime(point):
    from pytz import timezone
    local = point.time.astimezone(timezone("Asia/Taipei"))
    return local.strftime("%Y-%m-%d %H:%M:%S")
format_datetime.short_description = "Time"

# --- indexes ---
class TaiexAdmin(admin.ModelAdmin):
    list_display = (format_datetime, 'price')
    date_hierarchy = 'time'
    ordering = ('time',)

class TxAdmin(admin.ModelAdmin):
    list_display = (format_datetime, 'open', 'high', 'low', 'close')
    date_hierarchy = 'time'
    ordering = ('time',)

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'full_name', 'market', 'tick_value')
    ordering = ('market', 'symbol',)

admin.site.register(Taiex, TaiexAdmin)
admin.site.register(Tx, TxAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
