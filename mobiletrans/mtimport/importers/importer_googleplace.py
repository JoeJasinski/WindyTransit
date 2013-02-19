import decimal
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.geos import Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon
from autoslug.settings import slugify
from mobiletrans.mtimport.importer import ImportBase
from mobiletrans.mtlocation import models as loc_models
from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import * 
from django.conf import settings
from googleplaces import GooglePlaces, types, lang, GooglePlacesError

class GoogleIOImportException(IOImportException):
    pass

def search_places_from_lat_long(lag_lng, radius=3200, keyword=None, types=[]):
    google_places = GooglePlaces(settings.GOOGLE_PLACES_API_KEY)
    query_result = google_places.query(
            lat_lng=lag_lng, keyword=keyword,
            radius =radius, types=types)
    return query_result
  
class GPlaceLocation(ImportBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.GPlace

    @classmethod
    def open_data(cls, lat_lng, radius):
        try:
            data = search_places_from_lat_long(lat_lng, radius=radius)
        except GooglePlacesError, error:
            raise GoogleIOImportException("GooglePlaces lookup error: %s" % (error)) 
        except Exception, error:
            raise ImportException("Unknown import error: lat_lng [%s] radius [%s]: %s" % (lat_lng, radius, error, ))
        except: 
            raise ImportException("Unknown import error: lat_lng [%s] radius [%s]" % (lat_lng, radius, ))
        return data

    def get_iteration_root(self):
        if hasattr(self.input_data, 'places'):
            data = self.input_data.places
        else:
            models.InputRecord.objects.make_note(
             input_record=self.input_record,
             note="query data missing 'places' element.",
             type=models.TRANSFER_NOTE_STATUS_ERROR,    
             )
            models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            raise ImportException("query data missing 'places' element.")     
        return data

    def parse_row(self, row):
        
        existing = False

        row.get_details()

        print "------------------------------------------------"
        print "JJJJ", vars(row)
        print "------------------------------------------------"

        try:
            uuid = row.id
        except AttributeError, error:
            raise AttributeError("id %s: uuid %s" % (id, error))
        
        try:
            place = self.get_model_class().objects.get(uuid=uuid) 
            existing = True
        except ObjectDoesNotExist:
            place = self.get_model_class()(uuid=uuid)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with uuid %s " % uuid)
       
        try:
            name = row.name
        except AttributeError, error:
            raise AttributeError("id %s: name %s" % (id, error))
        place.name = name

        try:
            geo = row.geo_location
        except AttributeError, error:
            raise AttributeError("id %s: geo_location %s" % (id, error))
        else:
            if geo.has_key('lng'):
                longitude = geo['lng']
            else:
                raise AttributeError("id %s: geo_location.lng" % (id))

            if geo.has_key('lat'):
                lattitude = geo['lat']
            else:
                raise AttributeError("id %s: geo_location.lat " % (id ))

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        place.point = point
 
        if hasattr(row, 'rating'):
            try:
                d = decimal.Decimal("%s" % row.rating)
            except decimal.InvalidOperation:
                pass
            else:
                place.rating = d

        if hasattr(row, 'vicinity'):
            place.vicinity = row.vicinity

        if hasattr(row, 'types'):
            place.types = row.types

        if hasattr(row, 'reference'):
            place.reference = row.reference

        if hasattr(row, 'international_phone_number'):
            place.international_phone_number = row.international_phone_number

        if hasattr(row, 'local_phone_number'):
            place.local_phone_number = row.local_phone_number
 
        if hasattr(row, 'website'):
            place.website = row.website
 
        if hasattr(row, 'formatted_address'):
            place.address = row.formatted_address

        if hasattr(row, 'url'):
            place.url = row.url
     
        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        
        print "------------------------------"
        print "JJJJAAA", vars(place)
        print "------------------------------"

        return place

    
