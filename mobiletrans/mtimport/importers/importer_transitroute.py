from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.geos import Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon
from autoslug.settings import slugify
from mobiletrans.mtimport.importer import CSVImportBase
from mobiletrans.mtlocation import models as loc_models
from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import * 

class TransitRoute(CSVImportBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.TransitRoute

    def parse_row(self, row):
        row = list(row)
        existing = False
        
        pk = "route_id"          
        try:
            pk_val = row[0]
        except IndexError, error:
            raise IndexError("%s %s" % (pk, error))
        
        try:
            transitroute = self.get_model_class().objects.get(route_id=pk_val)
            existing = True
        except ObjectDoesNotExist:
            transitroute = self.get_model_class()(route_id=pk_val)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with %s %s " % (pk, pk_val))

        attr = (1, 'short_name')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        attr = (2, 'long_name')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        attr = (3, 'type')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        attr = (4, 'url')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        attr = (5, 'color')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        attr = (6, 'text_color')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        print(vars(transitroute))
        return transitroute
