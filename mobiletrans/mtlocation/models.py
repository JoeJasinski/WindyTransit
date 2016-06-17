import uuid
from django.contrib.gis.db import models
from django.contrib.gis.measure import D
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.conf import settings
from mobiletrans.mtlocation.fields import SeparatedValuesField
from autoslug import AutoSlugField

TRANSIT_STOP_TYPE_STOP = 0
TRANSIT_STOP_TYPE_STATION = 1
TRANSIT_STOP_TYPES = (
    (TRANSIT_STOP_TYPE_STOP, 'Stop'),
    (TRANSIT_STOP_TYPE_STATION, 'Station'),
)

TRANSIT_ROUTE_TYPE = (
    (0, "Tram, Streetcar, Light rail. Any light rail or street level system within a metropolitan area."),
    (1, "Subway, Metro. Any underground rail system within a metropolitan area."),
    (2, "Rail. Used for intercity or long-distance travel."),
    (3, "Bus. Used for short- and long-distance bus routes."),
    (4, "Ferry. Used for short- and long-distance boat service."),
    (5, "Cable car. Used for street-level cable cars where the cable runs beneath the car."),
    (6, "Gondola, Suspended cable car. Typically used for aerial cable cars where the car is suspended from the cable."),
    (7, "Funicular. Any rail system designed for steep inclines."),
)


class SubclassingQuerySet(models.query.GeoQuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.as_leaf_class()
        else:
            return result

    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()


class LocationSubclassingManager(models.GeoManager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)


class LocationQuerySet(models.query.GeoQuerySet):
    def displayable(self):
        transit_stop = ContentType.objects.get_for_model(TransitStop)
        return super(LocationQuerySet, self).exclude(content_type__in=[transit_stop])

    def get_closest(self, from_point, distance_dict):
        """
        Only select landmarks with a given distance of a point.
        The from_point is a valid Point object
        The distance_dict is of the format
          {distance_unit:str(distance)}
          where distance_unit is one of the geodjango supported units
             https://docs.djangoproject.com/en/dev/ref/contrib/gis/measure/#supported-units
          and distance is a radius around the from_point
        """
        return self.filter(point__distance_lte=(from_point, D(**distance_dict) )).distance(from_point).order_by('distance')

    def get_closest_x(self, from_point, distance_dict, number=2):
        return self.get_closest(from_point, distance_dict)[:number]


class LocationManager(models.GeoManager):
    def get_query_set(self):
        return LocationQuerySet(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)


class RegionManager(models.GeoManager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)


class Location(models.Model):

    class_slug = 'location'

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', max_length=255)
    point = models.PointField(help_text="Represented as (longitude, lattitude)")
    uuid = models.UUIDField(default=uuid.uuid4)

    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    sub_objects = LocationSubclassingManager()
    objects = LocationManager()

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def serialize(self):
        point = {'lattitude': self.point.y, 'longitude': self.point.x}
        return {'created': self.created, 'active': self.active, 'name': self.name,
                'point': point, 'uuid': self.uuid, 'type': self.__class__.__name__}

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Location):
            return self
        return model.objects.get(id=self.id)

    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Location, self).save(*args, **kwargs)

    def placemark_icon(self):
        site = Site.objects.get_current()
        static_url = settings.STATIC_URL
        return_value = "http://%s%simage/location-transit.png" % (site, static_url)
        return return_value


class Landmark(Location):

    class_slug = 'landmark'

    address = models.CharField(max_length=255, blank=True, null=True)
    architect = models.CharField(max_length=255, blank=True, null=True)
    build_date = models.CharField(max_length=64, blank=True, null=True)
    landmark_date = models.DateField(blank=True, null=True)

    objects = LocationManager()

    class Meta:
        verbose_name = "Landmark Location"
        verbose_name_plural = "Landmark Locations"

    def serialize(self):
        serialize_parent = super(self.__class__, self).serialize().copy()
        serialize_parent.update(
            {'address': self.address, 'architect': self.architect,
             'build_date': self.build_date, 'landmark_date': self.landmark_date, })
        return serialize_parent


class TransitStop(Location):

    class_slug = 'transit_stop'

    route = models.ManyToManyField('mtlocation.TransitRoute', blank=True)
    stop_id = models.IntegerField(unique=True,
        help_text=("Required. The stop_id field contains an ID that uniquely "
                   "identifies a stop or station. Multiple routes may use the "
                   "same stop. The stop_id is dataset unique."))
    stop_code = models.IntegerField(blank=True, null=True,
        help_text=("Optional. The stop_code field contains short text or a "
                   "number that uniquely identifies the stop for passengers. "
                   "Stop codes are often used in phone-based transit information "
                   "systems or printed on stop signage to make it easier for "
                   "riders to get a stop schedule or real-time arrival information "
                   "for a particular stop."))
    description = models.TextField(blank=True, null=True,
        help_text=("Optional. The stop_desc field contains a description of a stop. "
                   "Please provide useful, quality information. Do not simply "
                   "duplicate the name of the stop."))
    url = models.URLField(blank=True, null=True,
        help_text=("Optional. The stop_url field contains the URL of a web page about "
                   "a particular stop. This should be different from the agency_url "
                   "and the route_url fields. "))
    location_type = models.IntegerField(choices=TRANSIT_STOP_TYPES,
        help_text=("Optional. The location_type field identifies whether this stop ID "
                   "represents a stop or station. If no location type is specified, or "
                   "the location_type is blank, stop IDs are treated as stops. Stations "
                   "may have different properties from stops when they are represented "
                   "on a map or used in trip planning."))

    #object = models.GeoManager()
    objects = LocationManager()
    orig_objects = models.GeoManager()

    class Meta:
        verbose_name = "Transit Location"
        verbose_name_plural = "Transit Locations"

    def save(self, *args, **kwargs):
        if not self.location_type:
            self.location_type = TRANSIT_STOP_TYPE_STOP
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(TransitStop, self).save(*args, **kwargs)

    def serialize(self):
        serialize_parent = super(self.__class__, self).serialize().copy()
        serialize_parent.update(
            { #'routes':map(lambda r: r.serialize(), self.route),
            'stop_id': self.stop_id,  'stop_code': self.stop_code,
            'description': self.description, 'url': self.url,
            'location_type_name': self.get_location_type_display(),
            'location_type_id': self.location_type})
        return serialize_parent

    def placemark_icon(self):
        site = Site.objects.get_current()
        static_url = settings.STATIC_URL
        return_value = ""

        if self.location_type == 1:
            try:
                route_id = self.route.all()[0].route_id
            except:
                pass
            else:
                return_value = "http://%s%simage/location-transit-%s.png" % (site, static_url, route_id)
        if not return_value:
            return_value = "http://%s%simage/location-transit.png" % (site, static_url)
        return return_value


class TransitRoute(models.Model):

    class_slug = 'transit_route'

    uuid = models.UUIDField(default=uuid.uuid4)

    route_id = models.CharField(max_length=64,
        help_text=("Required. The route_id field contains an ID that uniquely identifies a "
                   "route. The route_id is dataset unique."))
    short_name = models.CharField(max_length=64,
        help_text=("Required. The route_short_name contains the short name of a route. "
                   "This will often be a short, abstract identifier like \"32\", \"100X\", "
                   "or \"Green\" that riders use to identify a route, but which doesn't give "
                   "any indication of what places the route serves. If the route does not have "
                   "a short name, please specify a route_long_name and use an empty string "
                   "as the value for this field."))
    long_name = models.CharField(max_length=255,
        help_text=("Required. The route_long_name contains the full name of a route. This name "
                   "is generally more descriptive than the route_short_name and will often include "
                   "the route's destination or stop. If the route does not have a long name, "
                   "please specify a route_short_name and use an empty string as the value for this field."))
    description = models.TextField(blank=True, null=True,
        help_text=("Optional. The route_desc field contains a description of a route. Please provide "
                   "useful, quality information. Do not simply duplicate the name of the route. For "
                   "example, \"A trains operate between Inwood-207 St, Manhattan and Far Rockaway-Mott "
                   "Avenue, Queens at all times. Also from about 6AM until about midnight, additional A "
                   "trains operate between Inwood-207 St and Lefferts Boulevard (trains typically alternate "
                   "between Lefferts Blvd and Far Rockaway).\""))
    type = models.IntegerField(choices=TRANSIT_ROUTE_TYPE,
        help_text=("Required. The route_type field describes the type of transportation used on a route."))
    color = models.CharField(max_length=6, blank=True, null=True,
        help_text=("Optional. In systems that have colors assigned to routes, the route_color field defines "
                   "a color that corresponds to a route. The color must be provided as a six-character "
                   "hexadecimal number, for example, 00FFFF. If no color is specified, the default route "
                   "color is white (FFFFFF)."))
    text_color = models.CharField(max_length=6, blank=True, null=True,
        help_text=("Optional. The route_text_color field can be used to specify a legible color to use for "
                   "text drawn against a background of route_color. The color must be provided as a "
                   "six-character hexadecimal number, for example, FFD700. If no color is specified, the "
                   "default text color is black (000000)."))
    url = models.URLField(blank=True, null=True,
        help_text=("Optional. The route_url field contains the URL of a web page about that particular "
                   "route. This should be different from the agency_url."))

    class Meta:
        verbose_name = "Transit Route"
        verbose_name_plural = "Transit Routes"

    def __unicode__(self):
        return "%s: %s" % (self.route_id, self.long_name)

    def serialize(self):
        serialize_parent = {
            'uuid': self.uuid, 'route_id': self.route_id,
            'short_name': self.short_name, 'long_name': self.long_name,
            'description': self.description, 'type_id': self.type,
            'type_name': self.get_type_display(),
            'color': self.color, 'text_color': self.text_color,
            'url': self.url,
        }
        return serialize_parent


class Library(Location):

    class_slug = 'library'

    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    hours = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    objects = LocationManager()

    class Meta:
        verbose_name = "Library Location"
        verbose_name_plural = "Library Locations"

    def serialize(self):
        serialize_parent = super(self.__class__, self).serialize().copy()
        serialize_parent.update(
            {'address': self.address, "zip": self.zip, "hours": self.hours,
             'phone': self.phone, 'website': self.website})
        return serialize_parent


class Hospital(Location):

    class_slug = 'hospital'

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(Hospital, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Hospital Location"
        verbose_name_plural = "Hospital Locations"

    def serialize(self):
        serialize_parent = super(self.__class__, self).serialize().copy()
        return serialize_parent


class PoliceStation(Location):

    class_slug = 'police_station'

    district = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Police Station Location"
        verbose_name_plural = "Police Station Locations"

    def serialize(self):
        serialize_parent = super(self.__class__, self).serialize().copy()
        return serialize_parent

    def placemark_icon(self):
        site = Site.objects.get_current()
        static_url = settings.STATIC_URL
        return_value = "http://%s%simage/location-police.png" % (site, static_url)
        return return_value


class Region(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', max_length=255)
    area = models.PolygonField()
    uuid = models.UUIDField(default=uuid.uuid4)

    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    sub_objects = RegionManager()
    objects = models.GeoManager()

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Region"

    def serialize(self):
        return {'created': self.created, 'active': self.active, 'name': self.name,
                'uuid': self.uuid, 'type': self.__class__.__name__}

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Region):
            return self
        return model.objects.get(id=self.id)

    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
            super(Region, self).save(*args, **kwargs)


class Neighborhood(Region):

    long_name = models.CharField(max_length=128, blank=True, null=True)

    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(Neighborhood, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Neighborhood Region"
        verbose_name_plural = "Neighborhood Regions"

    def serialize(self):
        serialize_parent = super(self.__class__, self).serialize().copy()
        serialize_parent.update(
            {'long_name': self.long_name})
        return serialize_parent


class Zipcode(Region):

    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(Zipcode, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Zipcode Region"
        verbose_name_plural = "Zipcode Regions"

    def serialize(self):
        serialize_parent = super(self.__class__, self).serialize().copy()
        return serialize_parent


class GPlace(Location):

    rating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    vicinity = models.TextField(blank=True, null=True)
    types = SeparatedValuesField(blank=True, null=True)
    reference = models.CharField(max_length=1024, blank=True, null=True)
    international_phone_number = models.CharField(max_length=30, blank=True, null=True)
    local_phone_number = models.CharField(max_length=30, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Google Place"
        verbose_name_plural = "Google Places"

    objects = models.GeoManager()

    def placemark_icon(self):
        site = Site.objects.get_current()
        static_url = settings.STATIC_URL
        return_value = "http://%s%simage/location-places.png" % (site, static_url)
        return return_value


class CTARailLines(models.Model):

    objectid = models.IntegerField()
    segment_id = models.IntegerField()
    asset_id = models.IntegerField()
    transit_lines = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    type = models.IntegerField()
    legend = models.CharField(max_length=5)
    alt_legend = models.CharField(max_length=5)
    branch = models.CharField(max_length=50)
    shape_len = models.FloatField()
    line = models.LineStringField(srid=4326)

    objects = models.GeoManager()

    class Meta:
        verbose_name = "Transit Line"
        verbose_name_plural = "Transit Lines"

# Auto-generated `LayerMapping` dictionary for CTA_RailLines2 model
cta_raillines2_mapping = {
    'objectid': 'OBJECTID',
    'segment_id': 'SEGMENT_ID',
    'asset_id': 'ASSET_ID',
    'transit_lines': 'LINES',
    'description': 'DESCRIPTIO',
    'type': 'TYPE',
    'legend': 'LEGEND',
    'alt_legend': 'ALT_LEGEND',
    'branch': 'BRANCH',
    'shape_len': 'SHAPE_LEN',
    'line': 'LINESTRING',
}


class CityBorder(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=25, blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    shape_len = models.FloatField(blank=True, null=True)
    area = models.MultiPolygonField(srid=4326)

    objects = models.GeoManager()

    class Meta:
        verbose_name = "City Border"
        verbose_name_plural = "City Borders"


# Auto-generated `LayerMapping` dictionary for CityBorder model
cityborder_mapping = {
    'objectid': 'OBJECTID',
    'name': 'NAME',
    'shape_area': 'SHAPE_AREA',
    'shape_len': 'SHAPE_LEN',
    'area': 'MULTIPOLYGON',
}
