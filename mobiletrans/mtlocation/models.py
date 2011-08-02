from django.contrib.gis.db import models
from django_extensions.db import fields as ext_fields
import uuid

TRANSIT_STOP_TYPE_STOP=0
TRANSIT_STOP_TYPE_STATION=1
TRANSIT_STOP_TYPES=(
  (TRANSIT_STOP_TYPE_STOP, 'Stop'),
  (TRANSIT_STOP_TYPE_STATION, 'Station'),
)


class Location(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    name = models.CharField(max_length=255)
    point = models.PointField()
    uuid = ext_fields.UUIDField(auto=False)
    
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


class TransitStop(Location):
    
    stop_id = models.IntegerField(unique=True)
    stop_code = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(verify_exists=True, blank=True, null=True)
    location_type = models.IntegerField(choices=TRANSIT_STOP_TYPES)
    
    class Meta:
        verbose_name = "Transit Location"
        verbose_name_plural = "Transit Locations"
        
    def save(self, *args, **kwargs):
        if not self.location_type:
            self.location_type = TRANSIT_STOP_TYPE_STOP
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(TransitStop, self).save(*args, **kwargs)
        