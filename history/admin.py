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
def format_date(point):
    return point.time.strftime("%Y-%m-%d %H:%M:%s")
format_date.short_description = "Time"

class TaiexAdmin(admin.ModelAdmin):
    list_display = (format_date, 'price')

admin.site.register(Taiex, TaiexAdmin)
