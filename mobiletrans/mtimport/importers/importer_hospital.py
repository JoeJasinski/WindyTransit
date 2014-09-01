from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.geos import Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon
from autoslug.settings import slugify
from mobiletrans.mtimport.importer import KMLImportBase
from mobiletrans.mtlocation import models as loc_models
from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import * 

class Hospital(KMLImportBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.Hospital
   
    def parse_row(self, row):
        existing = False

        pk = "name"                 
        try:
            pk_val = row.getElementsByTagName(pk)[0]
        except Exception as error:
            raise IndexError("%s %s" % (pk, error))

        try:
            pk_text = pk_val.childNodes[0].nodeValue
        except Exception as error:
            raise Exception("%s %s: Error Reading 'text' from 'pk': %s" % (pk, pk_val, error)) 

        slug = slugify(pk_text)
        
        try:
            hospital = self.get_model_class().objects.get(slug=slug)
            existing = True
        except ObjectDoesNotExist:
            hospital = self.get_model_class()(slug=slug)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with %s %s " % (pk, pk_val))

        hospital.name = pk_text
        

        try:
            point = row.getElementsByTagName("Point")[0]
        except Exception as error:
            raise IndexError("%s %s: Error Reading 'Point' from 'Placemark': %s" % (pk, pk_val, error)) 
        
        try:       
            coordinates = point.getElementsByTagName("coordinates")[0]
        except Exception as error:        
            raise Exception("%s %s: Error Reading 'coordinates' from 'Point': %s" % (pk, pk_val, error)) 
        
        try:
            coord_text = coordinates.childNodes[0].nodeValue
        except Exception as error:
            raise Exception("%s %s: Error Reading 'text' from 'coordinates': %s" % (pk, pk_val, error)) 
        
        try:
            longitude, lattitude, other =  coord_text.split(',')
        except Exception as error:
            raise Exception("%s %s: Error splitting 'text': %s" % (pk, pk_val, error)) 
        

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        hospital.point = point     

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        print vars(hospital)
        return hospital