from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.geos import Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon
from autoslug.settings import slugify
from mobiletrans.mtimport.importer import JSONImportBase
from mobiletrans.mtlocation import models as loc_models
from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import * 

class Library(JSONImportBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.Library

    def parse_row(self, row):
        
        existing = False
        
        try:
            id = row[0]
        except IndexError as error:
            raise IndexError("id %s" % error)
        
        try:
            uuid = row[1]
        except IndexError as error:
            raise IndexError("id %s: uuid %s" % (id, error))
        
        try:
            library = self.get_model_class().objects.get(uuid=uuid)
            existing = True
        except ObjectDoesNotExist:
            library = self.get_model_class()(uuid=uuid)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with uuid %s " % uuid)
        
        try:
            name = row[8]
        except IndexError as error:
            raise IndexError("id %s: name %s" % (id, error))
        library.name = name

        try:
            hours = row[9]
        except IndexError as error:
            raise IndexError("id %s: address %s" % (id, error))
        library.hours = hours
                
        try:
            address = row[10]
        except IndexError as error:
            raise IndexError("id %s: address %s" % (id, error))
        library.address = address
 
        try:
            zip = row[13]
        except IndexError as error:
            raise IndexError("id %s: address %s" % (id, error))
        library.zip = zip 
        
        try:
            phone = row[14]
        except IndexError as error:
            raise IndexError("id %s: address %s" % (id, error))
        library.phone = phone 
        
        try:
            website = row[15][0]
        except IndexError as error:
            raise IndexError("id %s: address %s" % (id, error))
        library.website = website 
        
        try:      
            lattitude = row[16][1]
        except IndexError as error:
            raise IndexError("id %s: lattitude %s" % (id, error)) 
        
        try:      
            longitude = row[16][2]
        except IndexError as error:
            raise IndexError("id %s: longitude %s" % (id, error))

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        library.point = point
        
        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        
        return library