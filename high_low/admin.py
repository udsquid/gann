###
### django libraries
###
from django.contrib import admin


###
### project libraries
###
from high_low.models import Point


###
### admin hook
###
# --- Point ---
def format_date(point):
    return point.time.strftime("%Y-%m-%d")
format_date.short_description = "Time"

class PointAdmin(admin.ModelAdmin):
    list_display = (format_date, 'price')

admin.site.register(Point, PointAdmin)
