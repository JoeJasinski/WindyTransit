from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.geos import Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon
from autoslug.settings import slugify
from mobiletrans.mtimport.importer import JSONImportBase
from mobiletrans.mtlocation import models as loc_models
from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import * 

class Landmark(JSONImportBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.Landmark

    def parse_row(self, row):
        
        existing = False
        
        try:
            id = row[0]
        except IndexError, error:
            raise IndexError("id %s" % error)
        
        try:
            uuid = row[1]
        except IndexError, error:
            raise IndexError("id %s: uuid %s" % (id, error))
        
        try:
            landmark = self.get_model_class().objects.get(uuid=uuid)
            existing = True
        except ObjectDoesNotExist:
            landmark = self.get_model_class()(uuid=uuid)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with uuid %s " % uuid)
        
        try:
            name = row[8]
        except IndexError, error:
            raise IndexError("id %s: name %s" % (id, error))
        landmark.name = name
        
        try:
            address = row[9]
        except IndexError, error:
            raise IndexError("id %s: address %s" % (id, error))
        landmark.address = address
        
        try:  
            created_date = row[10]
        except IndexError, error:
            raise IndexError("id %s: created_date %s" % (id, error))
        
        try:
            architect = row[11]
        except IndexError, error:
            raise IndexError("id %s: architect %s" % (id, error)) 
        landmark.architect = architect
        
        try:      
            lattitude = row[13]
        except IndexError, error:
            raise IndexError("id %s: lattitude %s" % (id, error)) 
        
        try:      
            longitude = row[14]
        except IndexError, error:
            raise IndexError("id %s: longitude %s" % (id, error))

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        landmark.point = point
        
        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        
        return landmark