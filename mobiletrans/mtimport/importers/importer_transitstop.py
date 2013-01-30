from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.geos import Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon
from autoslug.settings import slugify
from mobiletrans.mtimport.importer import CSVLocationBase
from mobiletrans.mtlocation import models as loc_models
from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import * 

class TransitStop(CSVLocationBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.TransitStop

    def parse_row(self, row):
        row = list(row)
        existing = False
        
        pk = "stop_id"          
        try:
            pk_val = row[0]
        except IndexError, error:
            raise IndexError("%s %s" % (pk, error))
        
        try:
            transitstop = self.get_model_class().objects.get(stop_id=pk_val)
            existing = True
        except ObjectDoesNotExist:
            transitstop = self.get_model_class()(stop_id=pk_val)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with %s %s " % (pk, pk_val))

        #attr = (1, 'stop_code')
        #try:
        #    value = row[attr[0]]
        #except IndexError, error:
        #    raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        #setattr(transitstop, attr[1], value) 
        
        attr = (2, 'name')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error))  
        setattr(transitstop, attr[1], value)  
            
        attr = (3, 'lattitude')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        lattitude = value
        
        attr = (4, 'longitude')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        longitude = value 
        
        attr = (5, 'location_type')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error))  
        setattr(transitstop, attr[1], value)  

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        transitstop.point = point

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        print vars(transitstop)
        return transitstop