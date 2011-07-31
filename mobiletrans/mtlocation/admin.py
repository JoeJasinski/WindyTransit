from django.contrib import admin
from . import models

admin.site.register(models.Location)
admin.site.register(models.Landmark)