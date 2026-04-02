from django.contrib import admin

from .models import DownloadEvent, Rating, Resource

admin.site.register(Resource)
admin.site.register(Rating)
admin.site.register(DownloadEvent)

# Register your models here.
