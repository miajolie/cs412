from django.contrib import admin

# Register your models here.

from . models import Viewer, Show, Season, Review, ListEntry, List, Watch
admin.site.register(Viewer)
admin.site.register(Show)
admin.site.register(Season)
admin.site.register(Review)
admin.site.register(ListEntry)
admin.site.register(List)
admin.site.register(Watch)
