from django.contrib.gis.db import models


class Location(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    point = models.PointField()
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class Landmark(Location):
    
    address = models.CharField(max_length=255, blank=True, null=True)
    architect = models.CharField(max_length=255, blank=True, null=True)
    build_date = models.CharField(max_length=64, blank=True, null=True)
    landmark_date = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Landmark Location"
        verbose_name_plural = "Landmark Locations"
