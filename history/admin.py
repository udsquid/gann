###
### django libraries
###
from django.contrib import admin


###
### project libraries
###
from history.models import Taiex


###
### admin hook
###
# --- Taiex ---
def format_datetime(point):
    from pytz import timezone
    local = point.time.astimezone(timezone("Asia/Taipei"))
    return local.strftime("%Y-%m-%d %H:%M:%S")
format_datetime.short_description = "Time"

class TaiexAdmin(admin.ModelAdmin):
    list_display = (format_datetime, 'price')
    date_hierarchy = 'time'
    ordering = ('time',)

admin.site.register(Taiex, TaiexAdmin)
