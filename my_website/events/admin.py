from django.contrib import admin
from .models import Venue
from .models import MyUser
from .models import Event


# admin.site.register(Venue)
admin.site.register(MyUser)
# admin.site.register(Event)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name','address','phone') # columns display 
    ordering = ('name',) # order list by name
    search_fields = ('name','address') # search 

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name','venue'),'event_date','description','manager')
    list_display = ('name','event_date','venue')
    list_filter = ('event_date','venue')
    ordering = ('event_date',)
    